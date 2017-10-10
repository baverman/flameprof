#!/bin/sh
set -e
tdir=$(dirname $0)
$tdir/test_prof.sh
$tdir/test_module.sh
$tdir/test_script.sh
$tdir/test_pytest.sh
$tdir/test_wsgi.sh
