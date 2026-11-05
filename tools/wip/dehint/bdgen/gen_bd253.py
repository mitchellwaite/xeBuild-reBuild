"""Attempt 14: lab_t5le alone costs only the last no-key log's .p2align, which compute_alignments gives when that
block's frequency is over 10x its layout predecessor's.  That block's frequency is what the __builtin_constant_p dead
entry sets (its weight comes from the form of the test), so try the entry's weights with t5le off.  If one matches, the
label's job moves onto a hint that is already counted (report it as such).  Runs on src/build.c as of eb75581."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

CP_SRC = '(char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1'
I = {
    'pi': '(char *)__builtin_constant_p(i) == (char *)1',
    'ii': '__builtin_constant_p(i) == 1',
    'bi': '__builtin_constant_p(i)',
    'ni': '!__builtin_constant_p(i) == 0',
    'x': None,
}
T = {
    'pt': '(char *)__builtin_constant_p(type) == (char *)1',
    'it': '__builtin_constant_p(type) == 1',
    'bt': '__builtin_constant_p(type)',
    'x': None,
}


def mk(t, a, b, lab, pr, op):
    parts = [p for p in (I[a], T[b]) if p]
    if not parts:
        return None
    cond = (' %s ' % op).join(parts)
    t = bdrun.sub(t, CP_SRC, cond, 1)
    if lab == 'nl':
        t = bdhints.off(t, 'lab_t5le')
    if pr == 'np':
        t = bdhints.off(t, 'exp_pr')
    return t


def CASES(base):
    out = []
    for a, b, lab, pr, op in itertools.product(I, T, ('l', 'nl'), ('p', 'np'), ('&&', '||')):
        if (I[a] is None or T[b] is None) and op == '||':
            continue
        if mk(base, a, b, lab, pr, op) is None:
            continue
        out.append(('%s %s %s %s %s' % (a, b, op, lab, pr), lambda x, a=a, b=b, l=lab, p=pr, o=op: mk(x, a, b, l, p, o)))
    return out


FOCUS = ['_loadBlFiles']
