#!/bin/sh
set -e
cd `dirname $0`
export PYTHONPATH=..

tmp=$(mktemp --tmpdir -d flameprof-test-script-XXXX)

python -m flameprof -o $tmp/s-out.svg -r sample.py -- boo
python -m flameprof -o $tmp/s2-out.svg -r sample2.py -- boo

test -f $tmp/s-out.svg
test -f $tmp/s2-out.svg

echo test_script Ok $tmp
