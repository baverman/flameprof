#!/bin/sh
set -e
cd `dirname $0`
export PYTHONPATH=..

tmp=$(mktemp --tmpdir -d flameprof-test-pytest-XXXX)

rm /tmp/pytest-prof.svg || true

py.test -p flameprof sample_test.py
py.test -p flameprof --flameprof-opts="-o $tmp/boo.svg" sample_test.py

test -f $tmp/boo.svg
test -f /tmp/pytest-prof.svg

echo test_pytest Ok $tmp
