"""Tests for exposure-scan's scan.sh.

A stub `bumblebee` replays made-up NDJSON records, so no real scan runs and
nothing touches the network or the real home directory.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCAN = Path(__file__).resolve().parents[2] / "scan.sh"

STUB = """#!/bin/sh
[ -f "$STUB_OUTPUT" ] && cat "$STUB_OUTPUT"
exit "${STUB_RC:-0}"
"""

SUMMARY = {"record_type": "scan_summary", "files_considered": 1234,
           "counts": {"package": 0}, "duration_ms": 5}
FINDING = {"record_type": "finding", "severity": "critical", "ecosystem": "npm",
           "package_name": "example-pkg", "version": "1.2.3",
           "catalog_id": "example-advisory", "evidence": "lockfile entry",
           "source_file": "/example/package-lock.json"}


@unittest.skipUnless(shutil.which("bash"), "bash required")
class ScanShTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.stub_dir = self.tmp / "stubbin"
        self.stub_dir.mkdir()
        self._write_stub(self.stub_dir)
        self.catalogs = self.tmp / "catalogs"
        self.catalogs.mkdir()
        (self.catalogs / "example.json").write_text(
            json.dumps({"schema_version": "0.2.0", "entries": []}))
        self.scratch = self.tmp / "scratch"
        self.scratch.mkdir()
        self.output = self.tmp / "records.ndjson"

    def _write_stub(self, directory):
        stub = directory / "bumblebee"
        stub.write_text(STUB)
        stub.chmod(0o755)

    def _env(self, **extra):
        env = {
            "PATH": f"{self.stub_dir}{os.pathsep}{os.environ.get('PATH', '')}",
            "HOME": str(self.home),
            "TMPDIR": str(self.scratch),
            "GOENV": "off",
            "GOBIN": str(self.stub_dir),
            "BUMBLEBEE_CATALOG_DIR": str(self.catalogs),
            "STUB_OUTPUT": str(self.output),
        }
        env.update(extra)
        return env

    def _records(self, *records):
        self.output.write_text("".join(json.dumps(r) + "\n" for r in records))

    def _run(self, *args, **env):
        return subprocess.run(["bash", str(SCAN), *args], env=self._env(**env),
                              capture_output=True, text=True, timeout=60)

    def _mktemp_dir(self):
        # GNU `mktemp -t` honours TMPDIR; macOS ignores it and uses the per-user
        # temp dir. Ask mktemp itself where it puts files.
        probe = subprocess.run(["mktemp", "-t", "exposure-probe.XXXXXX"], env=self._env(),
                               capture_output=True, text=True, check=True).stdout.strip()
        os.remove(probe)
        return Path(probe).parent

    def test_clean_run_exits_zero_and_removes_temp_file(self):
        self._records(SUMMARY)
        tmpdir = self._mktemp_dir()
        before = set(tmpdir.glob("exposure-findings*"))
        r = self._run("quick")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("CLEAN", r.stdout)
        self.assertEqual(set(tmpdir.glob("exposure-findings*")) - before, set())

    def test_failed_scan_with_no_summary_is_an_error_not_clean(self):
        self.output.write_text("")
        r = self._run("quick", STUB_RC="1")
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("CLEAN", r.stdout)
        self.assertIn("no scan_summary", r.stderr)

    def test_findings_exit_two(self):
        self._records(FINDING, SUMMARY)
        r = self._run("quick")
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("npm:example-pkg@1.2.3", r.stdout)

    def test_summary_without_files_considered_does_not_crash(self):
        summary = {k: v for k, v in SUMMARY.items() if k != "files_considered"}
        self._records(summary)
        r = self._run("quick")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("scanned: 0 files", r.stdout)

    def test_help_prints_only_the_header_comment(self):
        r = self._run("help")
        self.assertEqual(r.returncode, 0, r.stderr)
        lines = r.stdout.splitlines()
        self.assertTrue(lines)
        for line in lines:
            self.assertTrue(line.startswith("#"), line)

    def test_mixed_catalog_schemas_exit_three(self):
        (self.catalogs / "other.json").write_text(
            json.dumps({"schema_version": "0.1.0", "entries": []}))
        r = self._run("catalogs")
        self.assertEqual(r.returncode, 3, r.stderr)

    @unittest.skipUnless(shutil.which("go"), "go required to resolve GOPATH")
    def test_multi_entry_gopath_uses_first_entry_bin(self):
        first, second = self.tmp / "gopath1", self.tmp / "gopath2"
        (first / "bin").mkdir(parents=True)
        second.mkdir()
        self._write_stub(first / "bin")
        self._records(SUMMARY)
        # Only the tools the script needs, so the stub in the first entry is the
        # one bumblebee the script can find.
        tool_dirs = {os.path.dirname(shutil.which(t)) for t in ("go", "python3", "bash")}
        path = os.pathsep.join(sorted(tool_dirs) + ["/usr/bin", "/bin"])
        env = self._env(GOBIN="", GOPATH=f"{first}{os.pathsep}{second}", PATH=path)
        if shutil.which("bumblebee", path=env["PATH"]):
            self.skipTest("a real bumblebee is already on PATH")
        r = subprocess.run(["bash", str(SCAN), "quick"], env=env,
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("CLEAN", r.stdout)


if __name__ == "__main__":
    unittest.main()
