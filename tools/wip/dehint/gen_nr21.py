"""Attempt 4: a second variable carrying got out of the loop (other type), so the PHI at the log block isn't coalesced with got and leaves a copy at IRA."""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrtpl import *


def variants():
    for sel, st in (('side', SIDE), ('plain', PLAIN)):
        for ty in ('uint32_t', 'long', 'DWORD', 'unsigned', 'size_t'):
            for init in ('total = 0;\n\tgot = 0;',):
                for where, kw in (
                    ('adv', dict(adv='got += r;\n\t\ttotal = got;')),
                    ('tail', dict(tail1='total = got;')),
                    ('addtotal', dict(adv='got += r;\n\t\ttotal += r;')),
                ):
                    for lg in ('total',):
                        for eq in ('got == size', 'total == size'):
                            yield '|'.join((sel, ty, where, eq)), tpl(sel=st, decl='int size, got, r;\n\t%s total;' % ty, init=init, loggot=lg, eq=eq, **kw)
