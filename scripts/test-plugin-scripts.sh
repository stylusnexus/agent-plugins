#!/usr/bin/env sh
# Discover and run every plugin script's own test suite.
#
# The two tool plugins (work-plan, defect-scan) live in their own repos, but
# a skill pack can still ship executable helper scripts (see
# plugins/release-ops/skills/npm-publish/scripts/) with their own tests. A
# test file that no discovery step ever reaches never runs -- locally or in
# CI -- and looks exactly like a passing test. This finds every such
# directory instead of assuming a fixed list.
#
# Looked for, in these directories:
#   plugins/*/scripts/tests
#   plugins/*/skills/*/scripts/tests
#
#   - Python: any file, run via `python3 -m unittest discover`.
#   - Shell: files matching test_*.sh or *_test.sh, run directly with sh.
#     This is this repo's own shell-test naming convention (see
#     scripts/check-*.sh for the non-test counterpart); no third-party shell
#     test framework (bats, shunit2, ...) is assumed or required.
#
# Exits non-zero if any discovered suite fails. Prints a clear "no tests
# found" and exits 0 if none exist yet -- an empty suite is not a failure,
# but a suite that exists and doesn't run would be.
set -eu

fail=0
found=0
shell_found=0

for dir in plugins/*/scripts/tests plugins/*/skills/*/scripts/tests; do
  [ -d "$dir" ] || continue
  found=1
  echo "== $dir (python) =="
  if ! python3 -B -m unittest discover -s "$dir"; then
    fail=1
  fi

  for shtest in "$dir"/test_*.sh "$dir"/*_test.sh; do
    [ -f "$shtest" ] || continue
    shell_found=1
    echo "== $shtest (shell) =="
    if ! sh "$shtest"; then
      fail=1
    fi
  done
done

if [ "$found" = 0 ]; then
  echo "no plugin script tests found"
  exit 0
fi

if [ "$shell_found" = 0 ]; then
  echo "no shell test scripts found (test_*.sh / *_test.sh) -- only Python unittest suites were run"
fi

exit "$fail"
