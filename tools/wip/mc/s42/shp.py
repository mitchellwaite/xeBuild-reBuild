"""shp.py: (c) sinking shapes of the option-loop usage(3) calls; ev + insertion sig + cm."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ev, lev, cm
B = open('H5b.c').read().split('\n')
U3 = {'eb': 644, 'ip': 664, 'r': 673, 'w': 682, 'e': 690, 'c': 698}
U5 = {'eb': 646, 'r': 675, 'w': 684, 'e': 692, 'c': 700}
for k, v in list(U3.items()) + list(U5.items()): assert 'client_usage(' in B[v - 1], (k, v, B[v-1])
def mk(sel3, sel5, where):
    L = list(B)
    for k in sel3: L[U3[k] - 1] = L[U3[k] - 1].replace('client_usage(3, argv[i]);', 'goto zu3;')
    for k in sel5: L[U5[k] - 1] = L[U5[k] - 1].replace('client_usage(5, argv[i]);', 'goto zu5;')
    tail = []
    if sel3: tail.append('zu3: client_usage(3, argv[i]);')
    if sel5: tail.append('zu5: client_usage(5, argv[i]);')
    blk = 'if (0) { ' + ' '.join(tail) + ' }'
    if where == 'end': L[723 - 1] = L[723 - 1] + ' continue; ' + ' '.join(tail)
    elif where == 'top': L.insert(594, blk)
    elif where == 'mid': L.insert(669, blk)   # before the -r chain line 670
    return '\n'.join(L)
V = []
for s3 in (['eb', 'ip'], ['r', 'w', 'e', 'c'], list(U3)):
    for s5 in ([], ['r', 'w', 'e', 'c'], list(U5)):
        for w in ('end', 'top', 'mid'):
            V.append((s3, s5, w))
for s3, s5, w in V:
    nm = 'shp_%s_%s_%s' % (''.join(s3), ''.join(s5), w)
    t = mk(s3, s5, w); p = os.path.join(lev.D, nm + '.c'); open(p, 'w', newline='\n').write(t)
    r = ev.ev(t, nm, fncmp=False)
    if r is None: print(nm, 'ERR'); continue
    print(nm, r['tinv'], r['tmiss'], lev.sig(nm), cm.cm(p), flush=True)
