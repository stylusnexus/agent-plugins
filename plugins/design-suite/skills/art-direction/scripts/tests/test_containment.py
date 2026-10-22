"""The preview servers in inspect.mjs and scenes.mjs must not serve files outside the project, and
scenes.mjs must not build a file path from a page-supplied scene id.  Run: python3 -m unittest discover -s scripts/tests

These tests run the real request handler from each script against a temporary project. They need
Node and are skipped without it. They do not start Chrome.
"""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")

HARNESS = r"""
import { readFileSync, realpathSync, statSync, createReadStream } from 'node:fs';
import { resolve, join, extname, sep } from 'node:path';
import { createServer, request } from 'node:http';
const [,, script, rootArg, ...paths] = process.argv;
const src = readFileSync(script, 'utf8');
const m = src.match(/server = createServer\(([\s\S]*?\n  \})\);\n/);
if (!m) throw new Error('request handler not found in ' + script);
const MIME = {};
const root = realpathSync(rootArg);
const handler = eval('(' + m[1] + ')');
const server = createServer(handler);
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
const get = (path, host) => new Promise((done) => {
  const req = request({ host: '127.0.0.1', port, path, agent: false, headers: { host: host || `127.0.0.1:${port}`, connection: 'close' } }, (res) => {
    let body = '';
    res.on('data', (c) => { body += c; });
    res.on('end', () => done([res.statusCode, body.trim().slice(0, 12)]));
  });
  req.end();
});
for (const spec of paths) {
  const [p, host] = spec.split('|');
  const [status, body] = await get(p, host);
  console.log(spec, status, body);
}
server.close();
"""


def serve(script, root, paths):
    with tempfile.TemporaryDirectory() as d:
        harness = Path(d, "harness.mjs")
        harness.write_text(HARNESS)
        out = subprocess.run([NODE, str(harness), str(SCRIPTS / script), str(root), *paths],
                             capture_output=True, text=True, check=True).stdout
    return {line.split(" ")[0]: int(line.split(" ")[1]) for line in out.splitlines()}


@unittest.skipUnless(NODE, "node is not installed")
class ServerContainment(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        (base / "outside").mkdir()
        (base / "outside" / "secret.txt").write_text("SECRET")
        proj = base / "proj"
        (proj / "sub").mkdir(parents=True)
        (proj / "ok.txt").write_text("OK")
        (proj / "sub" / "index.html").write_text("IDX")
        (proj / "inlink.txt").symlink_to("ok.txt")
        (proj / ".env").write_text("TOKEN=1")
        (proj / ".well-known").mkdir()
        (proj / ".well-known" / "ok.txt").write_text("WK")
        (proj / "leak.txt").symlink_to("../outside/secret.txt")
        (proj / "leakdir").symlink_to("../outside")
        (base / "projlink").symlink_to(proj)
        self.base, self.proj = base, proj
        self.paths = ["/ok.txt", "/inlink.txt", "/leak.txt", "/leakdir/secret.txt", "/sub/", "/../outside/secret.txt", "/nope",
                      "/.env", "/.well-known/ok.txt", "/ok.txt|evil.example", "/ok.txt|localhost:4000", "/ok.txt|127.0.0.1"]

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, script, root):
        got = serve(script, root, self.paths)
        self.assertEqual(got["/ok.txt"], 200)
        self.assertEqual(got["/inlink.txt"], 200, "a link that stays inside the project still works")
        self.assertEqual(got["/sub/"], 200, "directory index still works")
        self.assertEqual(got["/leak.txt"], 403, "a file link that leaves the project is refused")
        self.assertEqual(got["/leakdir/secret.txt"], 403, "a directory link that leaves the project is refused")
        self.assertIn(got["/../outside/secret.txt"], (403, 404))
        self.assertEqual(got["/nope"], 404)
        self.assertEqual(got["/.env"], 403, "dotfiles are never served")
        self.assertEqual(got["/.well-known/ok.txt"], 200, ".well-known is the one allowed dot folder")
        self.assertEqual(got["/ok.txt|evil.example"], 403, "a foreign Host header is refused (DNS rebinding)")
        self.assertEqual(got["/ok.txt|localhost:4000"], 200)
        self.assertEqual(got["/ok.txt|127.0.0.1"], 200)

    def test_inspect_server(self):
        self.check("inspect.mjs", self.proj)

    def test_scenes_server(self):
        self.check("scenes.mjs", self.proj)

    def test_a_symlinked_project_root_still_works(self):
        self.check("inspect.mjs", self.base / "projlink")
        self.check("scenes.mjs", self.base / "projlink")


class SceneFileNames(unittest.TestCase):
    def test_contact_sheets_do_not_use_the_page_supplied_scene_id(self):
        src = (SCRIPTS / "scenes.mjs").read_text()
        self.assertIn("scene-${si + 1}-${label}.jpg", src)
        self.assertIsNone(re.search(r"join\(outDir,\s*`\$\{sc\.id\}", src))

    def test_scene_ids_are_escaped_in_the_caption_html(self):
        src = (SCRIPTS / "scenes.mjs").read_text()
        self.assertIn("${esc(a.labels[i])}", src)
        self.assertNotIn("${a.labels[i]}", src)


if __name__ == "__main__":
    unittest.main()
