"""Attempt 4: split got over types that don't coalesce (int vs long): got = n stays as a PHI arg of the other type, so the copy lands on the back edge, after the exit test."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrtpl import *


def variants():
    for sel, st in (('side', SIDE), ('plain', PLAIN)):
        # long got, int n computed then stored
        for tag, decl, adv, pg, cond, eq, lg in [
            ('longgot_n', 'long got; int size, r, n;', 'n = got + r;\n\t\tgot = n;', 'got', 'got < size', 'got == size', 'got'),
            ('intgot_longn', 'long n; int size, got, r;', 'n = got + r;\n\t\tgot = n;', 'got', 'got < size', 'got == size', 'got'),
            ('longgot', 'long got; int size, r;', 'got += r;', 'got', 'got < size', 'got == size', 'got'),
            ('longsize', 'long size; int got, r;', 'got += r;', 'got', 'got < size', 'got == size', 'got'),
            ('longr', 'long r; int size, got;', 'got += r;', 'got', 'got < size', 'got == size', 'got'),
            ('allong', 'long size, got, r;', 'got += r;', 'got', 'got < size', 'got == size', 'got'),
            ('longgot_nlog', 'long got; int size, r, n;', 'n = got + r;\n\t\tgot = n;', 'n', 'got < size', 'n == size', 'n'),
            ('longgot_n_inner', 'long got; int size, r;', '{ int n = got + r; got = n; }', 'got', 'got < size', 'got == size', 'got'),
        ]:
            init = 'got = 0;'
            yield sel + '|' + tag, tpl(sel=st, decl=decl, adv=adv, printgot=pg, cond=cond, eq=eq, loggot=lg, init=init)
