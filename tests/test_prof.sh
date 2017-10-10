#!/bin/sh
set -e
cd `dirname $0`
export PYTHONPATH=..
pyver=$(python -c 'import sys; print(sys.version_info.major)')

tmp=$(mktemp --tmpdir -d flameprof-test-prof-XXXX)

python -m flameprof sample.prof$pyver > $tmp/stdout.svg

python -m flameprof -o $tmp/s-out.svg sample.prof$pyver
python -m flameprof -o $tmp/s2-out.svg sample2.prof$pyver

test -f $tmp/stdout.svg
test -f $tmp/s-out.svg
test -f $tmp/s2-out.svg

echo test_prof Ok $tmp
