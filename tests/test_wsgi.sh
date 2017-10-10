#!/bin/sh
set -e

cd `dirname $0`
export PYTHONPATH=..

tmp=$(mktemp --tmpdir -d flameprof-test-wsgi-XXXX)

FLAMEPROF="--wsgi-out-dir=$tmp app" uwsgi -w flameprof:wsgi --need-app --http=127.0.0.1:9999 &
pid=$!
sleep 1

curl http://127.0.0.1:9999/
curl http://127.0.0.1:9999/boo

test -f $tmp/GET.boo.svg
test -f $tmp/GET.root.svg

kill $pid

echo test_wsgi Ok $tmp
