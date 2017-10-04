Flamegraph generator for python's `cProfile <https://docs.python.org/3/library/profile.html>`_ stats.

`Flamegraphs <http://www.brendangregg.com/flamegraphs.html>`_ allow to
visualize relations between functions in a very compact and understandable
manner.

``Flameprof`` solves main problems of built-in cProfile reporting and can replace
`gprof2dot <https://github.com/jrfonseca/gprof2dot>`_ because later outputs
very huge graphs with a lot of noise.

``Flameprof`` works with profile stat files obtained by
`Profile.dump_stats() <https://docs.python.org/3/library/profile.html#profile.Profile.dump_stats>`_
call or via direct script profiling::

    python -m cProfile -o myscript.prof myscript.py


Install
=======

Via pip::

    pip install flameprof

Or you can invoke ``flameprof.py`` directly::

    python flameprof.py input.prof > output.svg


Native svg (--format=svg)
=========================

Native svg features:

* compact function names with full names in a tooltip
* precise timings (cumulative and total)
* call counts (in a tooltip on hover)
* green bars show stack frames where flameprof starts to guess timing ratios
* inverted flamegraph to show total time of all calls

Graph width, row height, font size and threshold can be set via appropriate cli
options.

::

    flameprof requests.prof > requests.svg

.. image:: https://cdn.rawgit.com/baverman/flameprof/master/img/requests.svg
    :alt: Requests profile
    :width: 100%
    :align: center

Inverted flamegraph:

.. image:: https://cdn.rawgit.com/baverman/flameprof/master/img/httplib.svg
    :alt: Requests profile
    :width: 100%
    :align: center

(Images are clickable)


Svg generated with flamegraph.pl (--format=log)
===============================================

Also ``flameprof`` can output trace log suitable as input for flamegraph.pl.

You can treat "samples" as microseconds by default (see ``--log-mult`` option).

::

    flameprof --format=log requests.prof | flamegraph > requests-flamegraph.svg

.. image:: https://cdn.rawgit.com/baverman/flameprof/master/img/requests-flamegraph.svg
    :alt: Requests profile with flamegraph.pl
    :width: 100%
    :align: center

(Image is clickable)
