"""base.py : build g7b and jT (c9>[hdd4,hdd5]) slots in build/v/mc37 (tags g7b, jT)."""
import m, ev
T = open('best_g7b_dup.c').read()
O = 'AT(c9) clientWriteBlocks(arg, start);'
J = T.replace(O, '{ AT(c9) clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }', 1)
open('jT.c', 'w', newline='\n').write(J)
for tag, t in (('g7b', T), ('jT', J)):
    r = m.meas(t, tag, True)
    inv, miss, o = ev.score_order(r['order'].split()[1:])
    print(tag, 'inv', inv + 5 * len(miss), 'fncmp', r['fncmp']); print(' ', ' '.join(map(str, o)))
