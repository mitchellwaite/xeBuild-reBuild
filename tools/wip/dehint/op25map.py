#!/usr/bin/env python3
"""Attempt 25: block id map TAG -> REFTAG for the replays, by aligning the bbro traces
(op13bb.py's names and frequencies; each block once, in id order).

python tools/wip/dehint/op25map.py REFTAG TAG  -> prints a:b,.. (only ids that differ)"""
import difflib, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def blocks(tag):
    t = subprocess.run([sys.executable, os.path.join(H, 'op13bb.py'), os.path.join(R, tag)],
                       capture_output=True, text=True).stdout
    d = {}
    for m in re.finditer(r'(\d+)\[(\d+)\](\S*)', t):
        d[int(m.group(1))] = '%s %s' % (m.group(2), re.sub(r'^\d+', '', m.group(3)))
    return sorted(d.items())


if __name__ == '__main__':
    # Attempt 27: this map is unsafe.  Unmatched TAG ids keep their own id in the replays
    # (MAP.get(x, x)) and can collide with another block's target (nodz2a's dz1 260 ->
    # base's sprintf 260, xa's 193), and a TAG head mapped to a REFTAG non-head (dzall's
    # 149 -> 150) never compares equal: such maps fail every replay (0 hits for nothing).
    # Use op27map.py (gap pairs, head fix, drop list, collision check) and op27ctl.py's
    # positive control instead.
    print('op25map.py: superseded by op27map.py (see its docstring)', file=sys.stderr)
    ref, tag = blocks(sys.argv[1]), blocks(sys.argv[2])
    sm = difflib.SequenceMatcher(None, [v for _, v in ref], [v for _, v in tag], autojunk=False)
    m = {}
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            m[tag[b + i][0]] = ref[a + i][0]
    un = [k for k, _ in tag if k not in m]
    if un:
        print('unmatched', un, file=sys.stderr)
    print(','.join('%d:%d' % (k, v) for k, v in sorted(m.items()) if k != v))
