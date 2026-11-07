"""Attempt 63: attempt 47's sig-failed-arm `<= 5` exit (tail without an r test) re-run on the current src
(useBuiltIn / end-form base), for target B (exp_pr and the param together).
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a63_sf.py -p 0 -o "-"
python tools/wip/dehint/bdgen/a62_semeas.py tools/wip/dehint/bdgen/a63_sf.py -x -p 90"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a47_sigfail import TAIL, SF, T_BRK, T_AND, T_KIT, S1, S2, S3
COM = '''				/* the expect leaves vrp1's signature-failed copy of this test a
				   >5 edge (else its setFlashBuild copy has frequency 0 and final
				   aligns the type-11 block after it) */
'''
V = {'src': []}
for sk, s in {'s1': S1, 's2': S2, 's3': S3}.items():
    for tk, t in {'brk': T_BRK, 'and': T_AND, 'kit': T_KIT}.items():
        V[sk + tk] = [(SF, s), (COM, ''), (TAIL, t)]
