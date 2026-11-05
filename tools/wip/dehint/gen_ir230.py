"""Attempt 17: gen_ir229 with the full attribute (no-if-conversion has a job here) and the ok flag only: which spellings move prephitmp's name below lim's."""
import os, sys, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir229 import *
forms = {}
for lk, ak, ik, ok_ in itertools.product(('loc', 'int', 'pg'), ('c', 'a', 'i', 'ca'), ('le', 'gt'), ('o', 'n', 'u', 'x', 'y')):
    k = '.'.join((lk, ak, ik, ok_))
    forms[k] = body(sane((lk, ak, ik, ok_)), zset='')
if __name__ == '__main__':
    r = sweep(forms, top=25)
