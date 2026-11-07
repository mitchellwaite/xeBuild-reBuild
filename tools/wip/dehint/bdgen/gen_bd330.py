"""Attempt 22, exp_upd, diagnostics only (expects moved, not shapes): attempt 22's -p sweep put the window for the first
pair at P23 <= 28% (p 72 matches, 70 doesn't), which fits P23 / (1 - P23) < p_bit, p_bit being the probability of
the block that receives reassoc's merged mask (the `(16|9)` pair, 39%).  If that's the rule, raising p_bit instead of
lowering P23 should match too.  Each case moves the expect to another pair or test, with its probability as given
(param 98).  Runs on src as of c941f014."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

OLD = 'return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
F = {
    'none': 'return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
    'p2_1': 'return type == 23 || type == 15 || __builtin_expect(type == 16 || type == 9, 1) || type == 10 || type == 24 || type == 25;',
    'p3_1': 'return type == 23 || type == 15 || type == 16 || type == 9 || __builtin_expect(type == 10 || type == 24, 1) || type == 25;',
    'p4_1': 'return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || __builtin_expect(type == 25, 1);',
    'p23_1': 'return type == 23 || type == 15 || __builtin_expect(type == 16 || type == 9 || type == 10 || type == 24, 1) || type == 25;',
}
FOCUS = ['_addUpdateBls', '_isUpdateBl']


def CASES(base):
    return [(k, lambda b, v=v: bdrun.sub(b, OLD, v, 1)) for k, v in F.items()]
