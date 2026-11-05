"""Attempt 17, measurement only (code nobody would write): the arm's addr test hidden from vrp1 and dom2 by arithmetic only reassoc1 cancels,
so S (the size test's join) reaches PRE unsplit and dom3 threads it.  Does the reference's asymmetry come out with no pin and no attribute?"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir225 import *

def v(u):
    return f'unsigned z = {u}; z += (unsigned)size; z += 77u * (unsigned)size; z -= 78u * (unsigned)size;'

HID = {
    'plain': 'unsigned z = addr;',
    'r1': 'unsigned z = (unsigned)addr + (unsigned)size; z += w; z -= (unsigned)size; z -= w;',
    'r2': 'unsigned z = w + (unsigned)addr; z += (unsigned)size; z -= w; z -= (unsigned)size;',
}
forms = {}
for zk, z in ZERO.items():
    for sk, s in SANE.items():
        if sk == 'ok' and zk != 'okf':
            continue
        for hk, h in HID.items():
            for tst in ('z == 0x800', 'z != 0x800'):
                if tst == 'z == 0x800':
                    arm = f'{{ unsigned w = h->smcBootAddr; {h} if ({tst}) {{ {L38} }} else {{ {L30} }} }}'
                else:
                    arm = f'{{ unsigned w = h->smcBootAddr; {h} int o = {tst}; if (o <= 0) {{ {L38} }} else {{ {L30} }} }}'
                forms['.'.join((zk, sk, hk, tst[2:4]))] = form(s, arm, TT['t6'], z)
if __name__ == '__main__':
    sweep(forms, [('', ()), ('.at', ('',))][:1])
