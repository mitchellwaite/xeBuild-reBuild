import sys, m, ev, json
src = open(sys.argv[1]).read()
A = 'JUMP(c12, c11, p0, i0, c9, hdd4, hdd5, c2, c1, c10, u2, cdef, c8, c7, c3, s5);'
C4 = 'case 4:\n\t\t\t\tif (cinfo->hwFlags & 0x20)'
C5 = 'case 5:\n\t\t\t\tif (cinfo->hwFlags & 0x20)'
assert A in src and C4 in src and C5 in src, (C4 in src)
src = src.replace(C4, 'case 4:\n\t\t\t\th4t: if (cinfo->hwFlags & 0x20)').replace(C5, 'case 5:\n\t\t\t\th5t: if (cinfo->hwFlags & 0x20)')
def run(tag, rep, fn=True):
    t = src.replace(A, rep)
    r = m.meas(t, tag, fncmp=fn)
    if 'err' in r: print(tag, 'ERR', r['err'][-300:]); return None
    s = ev.score_order(r['order'].split()[1:])[0]
    print(tag, s, r.get('fncmp'), r['order'], flush=True); return s, t
if __name__ == '__main__':
    for a in sys.argv[2:]:
        tag, rep = a.split('=', 1); run(tag, rep)
