#!/usr/bin/env python3
"""Attempt 27: op25map.py fixed.  op25map.py prints only matched ids and leaves unmatched
TAG blocks out, so the replays (MAP.get(x, x)) keep their own id, which can collide with
the REFTAG id another TAG block maps to (nodz2a's dz1 260 -> base's sprintf block 260,
xa's asm goto block 193 -> base 193 = xa's 194).  Here:

1. difflib on (freq, signature) as op25map.py;
2. each gap between matched anchors: equal-length gaps are paired in order, otherwise
   blocks with a unique signature in both gaps are paired (freq may differ);
3. what is left of TAG is printed as a drop list (ids the replay must ignore: dummies,
   asm goto blocks with no REFTAG twin), and every map target is checked to be unique.

python tools/wip/dehint/op27map.py REFTAG TAG [-v]
  -> line 1: the map a:b,.. (only ids that differ); line 2: 'drop' ids,..;
     stderr: what was gap-filled, what is dropped, collisions (must be none)"""
import difflib, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..', '..', 'build', 'v', 'aio_p1')


def traces(tag):
    t = subprocess.run([sys.executable, os.path.join(H, 'op13bb.py'), os.path.join(R, tag)],
                       capture_output=True, text=True).stdout
    tr = []
    for line in t.splitlines():
        if re.match(r'T\d+ ', line):
            tr.append([int(x) for x in re.findall(r'(\d+)\[\d+\]', line)])
    return tr


def blocks(tag):
    t = subprocess.run([sys.executable, os.path.join(H, 'op13bb.py'), os.path.join(R, tag)],
                       capture_output=True, text=True).stdout
    d = {}
    for m in re.finditer(r'(\d+)\[(\d+)\](\S*)', t):
        d[int(m.group(1))] = (int(m.group(2)), re.sub(r'^\d+', '', m.group(3)))
    return sorted(d.items())


def build(reftag, tag, log=None):
    ref, tg = blocks(reftag), blocks(tag)
    key = lambda v: '%d %s' % v
    sm = difflib.SequenceMatcher(None, [key(v) for _, v in ref], [key(v) for _, v in tg],
                                 autojunk=False)
    m = {}
    anchors = []
    for a, b, n in sm.get_matching_blocks():
        for i in range(n):
            m[tg[b + i][0]] = ref[a + i][0]
        anchors.append((a, b, n))
    # gaps between anchors
    pa, pb = 0, 0
    for a, b, n in anchors:
        ga, gb = ref[pa:a], tg[pb:b]
        if ga and gb:
            if len(ga) == len(gb):
                for (ri, rv), (ti, tv) in zip(ga, gb):
                    m[ti] = ri
                    if log is not None:
                        log.append('gap pair %d%s -> %d%s' % (ti, tv, ri, rv))
            else:
                sa = {}
                for ri, rv in ga:
                    sa.setdefault(rv[1], []).append(ri)
                sb = {}
                for ti, tv in gb:
                    sb.setdefault(tv[1], []).append(ti)
                for s, tis in sb.items():
                    if s and len(tis) == 1 and len(sa.get(s, [])) == 1:
                        m[tis[0]] = sa[s][0]
                        if log is not None:
                            log.append('gap sig %d -> %d (%s)' % (tis[0], sa[s][0], s))
        pa, pb = a + n, b + n
    # the replays compare trace heads: a TAG head mapped to a REFTAG non-head (dzall's
    # 149 is base's 150, but base's trace 149-150 has head 149) takes its trace's head
    rh = {}
    for t in traces(reftag):
        for x in t:
            rh[x] = t[0]
    used = set(m.values())
    for t in traces(tag):
        h = t[0]
        if h in m and rh.get(m[h], m[h]) != m[h] and rh[m[h]] not in used:
            if log is not None:
                log.append('head %d -> %d (was %d)' % (h, rh[m[h]], m[h]))
            m[h] = rh[m[h]]
            used.add(m[h])
    drop = [k for k, _ in tg if k not in m]
    tgt = {}
    coll = []
    for k, v in m.items():
        if v in tgt:
            coll.append((tgt[v], k, v))
        tgt[v] = k
    # an unmapped TAG id that equals some mapped target collides too if it isn't dropped
    return m, drop, coll


def load(reftag, tag):
    m, drop, coll = build(reftag, tag)
    if coll:
        raise SystemExit('map collisions %s' % coll)
    return m, set(drop)


if __name__ == '__main__':
    log = []
    m, drop, coll = build(sys.argv[1], sys.argv[2], log)
    print(','.join('%d:%d' % (k, v) for k, v in sorted(m.items()) if k != v))
    print('drop ' + ','.join(map(str, drop)))
    for l in log:
        print(l, file=sys.stderr)
    tg = dict(blocks(sys.argv[2]))
    print('dropped', ['%d%s' % (k, tg[k]) for k in drop], file=sys.stderr)
    print('collisions', coll, file=sys.stderr)
