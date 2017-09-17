#!/bin/env python
from __future__ import division, print_function

import sys
import pstats
import argparse
import pprint

from struct import Struct
from hashlib import sha1
from functools import partial
from collections import Counter
from xml.sax.saxutils import escape

eprint = partial(print, file=sys.stderr)
epprint = partial(pprint.pprint, stream=sys.stderr)

PY2 = sys.version_info[0] == 2
if PY2:
    bstr = lambda r: r
else:
    def bstr(data):
        if type(data) is str:
            data = data.encode('utf-8')
        return data


def gen_colors(s, e, size):
    for i in range(size):
        yield (s[0] + (e[0] - s[0]) * i // size,
               s[1] + (e[1] - s[1]) * i // size,
               s[2] + (e[2] - s[2]) * i // size)


COLORS = list(gen_colors((255, 240, 141), (255, 65, 34), 7))
CCOLORS = list(gen_colors((44, 255, 210), (113, 194, 0), 5))


int_struct = Struct('!L')
def name_hash(name):
    v, = int_struct.unpack(sha1(bstr(name)).digest()[:4])
    return v / (0xffffffff + 1.0)


def calc_callers(stats):
    roots = []
    funcs = {}
    calls = {}
    for func, (cc, nc, tt, ct, clist) in stats.items():
        funcs[func] = {'calls': [], 'stat': (cc, nc, tt, ct)}
        if not clist:
            roots.append(func)
            calls[('root', func)] = funcs[func]['stat']

    for func, (cc, nc, tt, ct, clist) in stats.items():
        for cfunc, t in clist.items():
            assert (cfunc, func) not in calls
            funcs[cfunc]['calls'].append(func)
            calls[(cfunc, func)] = t

    funcs['root'] = {'calls': roots,
                     'total': sum(funcs[r]['stat'][3] for r in roots)}

    return funcs, calls


def prepare(funcs, calls, threshold=0.0001, h=24, fsize=12, width=1200):
    blocks = []
    block_counts = Counter()

    def _counts(parent, visited, level=0):
        for child in funcs[parent]['calls']:
            k = parent, child
            block_counts[k] += 1
            if block_counts[k] < 2:
                if k not in visited:
                    _counts(child, visited | {k}, level+1)

    def _calc(parent, timings, level, origin, visited, trace=(), pccnt=1):
        childs = funcs[parent]['calls']
        _, _, ptt, ptc = timings
        fchilds = sorted(((f, funcs[f], calls[(parent, f)], max(block_counts[(parent, f)], pccnt))
                          for f in childs),
                         key=lambda r: r[0])

        gchilds = [r for r in fchilds if r[3] == 1]

        bchilds = [r for r in fchilds if r[3] > 1]
        if bchilds:
            gctc = sum(r[2][3] for r in gchilds)
            bctc = sum(r[2][3] for r in bchilds)
            rest = ptc-ptt-gctc
            if bctc > 0:
                factor = rest / bctc
            else:
                factor = 1
            bchilds = [(f, ff, (round(cc*factor), round(nc*factor), tt*factor, tc*factor), ccnt)
                       for f, ff, (cc, nc, tt, tc), ccnt in bchilds]

        for child, _, (cc, nc, tt, tc), ccnt in gchilds + bchilds:
            if tc/maxw > threshold:
                ckey = parent, child
                ctrace = trace + (child,)
                blocks.append({
                    'trace': ctrace,
                    'ccnt': (pccnt==1 and ccnt > 1),
                    'level': level,
                    'name': child[2],
                    'hash_name': '{0[0]}:{0[1]}:{0[2]}'.format(child),
                    'full_name': '{0[0]}:{0[1]}:{0[2]} {5:.2%} ({1} {2} {3} {4})'.format(child, cc, nc, tt, tc, tc/maxw),
                    'w': tc,
                    'ww': tt,
                    'x': origin
                })
                if ckey not in visited:
                    _calc(child, (cc, nc, tt, tc), level + 1, origin, visited | {ckey}, ctrace, ccnt)
            origin += tc

    maxw = funcs['root']['total'] * 1.0
    _counts('root', set())
    _calc('root', (1, 1, maxw, maxw), 0, 0, set())
    return blocks, maxw


def render_svg(blocks, maxw, threshold=0.0001, h=24, fsize=12, width=1200):
    maxlevel = max(r['level'] for r in blocks)
    height = (maxlevel + 1) * h
    content = []
    for b in blocks:
        x = b['x'] * width / maxw
        tx = h / 6
        y = height - b['level']*h - h
        ty = h / 2
        w = max(1, b['w'] * width / maxw - 1)
        if b['ccnt']:
            fill = CCOLORS[int(len(CCOLORS) * name_hash(b['hash_name']))]
        else:
            fill = COLORS[int(len(COLORS) * name_hash(b['hash_name']))]
        content.append(ELEM.format(w=w, x=x, y=y, tx=tx, ty=ty,
                                   name=escape(b['name']),
                                   full_name=escape(b['full_name']),
                                   fsize=fsize, h=h-1, fill=fill))

    return SVG.format('\n'.join(content), width=width, height=height)


def render_fg(blocks, multiplier):
    for b in blocks:
        trace = []
        for t in b['trace']:
            trace.append('{}:{}:{}'.format(*t))

        print(';'.join(trace), int(b['ww'] * multiplier))


SVG = '''\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" width="{width}" height="{height}"
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<style type="text/css">
    .func_g:hover {{ stroke:black; stroke-width:0.5; cursor:pointer; }}
</style>
{}
</svg>'''

ELEM = '''\
<svg class="func_g" x="{x}" y="{y}" width="{w}" height="{h}"><g>
    <title>{full_name}</title>
    <rect height="100%" width="100%" fill="rgb{fill}" rx="2" ry="2" />
    <text alignment-baseline="central" x="{tx}" y="{ty}" font-size="{fsize}px" fill="rgb(0,0,0)">{name}</text>
</g></svg>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make flamegraph from cProfile stats.')
    parser.add_argument('stats', help='file with cProfile stats')
    parser.add_argument('--width', type=int, help='image width, default is %(default)s', default=1200)
    parser.add_argument('--row-height', type=int, help='row height, default is %(default)s', default=24)
    parser.add_argument('--font-size', type=int, help='font size, default is %(default)s', default=12)
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='limit functions relative cumulative time in percents, default is %(default)s%%')
    parser.add_argument('--format', choices=['svg', 'log'], default='svg',
                        help='output format, default is %(default)s. `log` is suitable as input for flamegraph.pl')
    parser.add_argument('--log-mult', type=int, default=1000000,
                        help='multiply score value for log format, default is %(default)s')

    args = parser.parse_args()

    s = pstats.Stats(args.stats)
    funcs, calls = calc_callers(s.stats)
    blocks, maxw = prepare(funcs, calls, threshold=args.threshold / 100)

    if args.format == 'svg':
        print(render_svg(blocks, maxw, h=args.row_height,
                         fsize=args.font_size, width=args.width))

    if args.format == 'log':
        render_fg(blocks, args.log_mult)
