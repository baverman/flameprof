#!/bin/sh
set -e
cd `dirname $0`
export PYTHONPATH=..

tmp=$(mktemp --tmpdir -d flameprof-test-module-XXXX)

python -m flameprof -o $tmp/s-out.svg -m sample -- boo
python -m flameprof -o $tmp/s2-out.svg -m sample2 -- boo

test -f $tmp/s-out.svg
test -f $tmp/s2-out.svg

echo test_module Ok $tmp
