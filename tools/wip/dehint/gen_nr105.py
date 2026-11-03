"""Attempt 11, family 4c: gen_nr104's nolen|inl|ifnot2 (V=0, C=6, margin +2, log = J = 282, tie goes to log, so the store is placed early). Arm of the `!len` test x where it sits x tail x caller: log has to fall a little, or J win the tie."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import *
from gen_nr104 import SIG, caller

FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n\t\t'
L = 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n\t\t'
L2 = 'log_printf(0, "no length pointer' + BS + 'n");\n\t\t'
ARMS = {
 'dup': NL1 + L + FREE + 'return NULL;',
 'dup0': L + FREE + 'return NULL;',
 'free': FREE + 'return NULL;',
 'netfree': 'netFree(buf);\n\t\treturn NULL;',
 'null': 'return NULL;',
 'buf': 'return buf;',
 'logfree': L2 + FREE + 'return NULL;',
 'lognull': L2 + 'return NULL;',
 'vput': NL1 + 'return NULL;',
 'vputfree': NL1 + FREE + 'return NULL;',
 'set': 'buf = NULL;\n\t\treturn buf;',
}
TEST = {'not': '!len', 'eq0': 'len == NULL'}
TAILS = {
 'eq': 'if (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + NL + LOG + '\treturn NULL;\n}\n\n',
 'ne': 'if (got != size) {\n\t\t' + NL1 + LOG.replace('\n\t', '\n\t\t').replace('\t\tfree', '\t\t\tfree') + '\t\treturn NULL;\n\t}\n\t*len = size;\n\treturn buf;\n}\n\n',
 'var': 'if (got == size)\n\t\t*len = size;\n\telse {\n\t\t' + NL1 + LOG.replace('\n\t', '\n\t\t').replace('\t\tfree', '\t\t\tfree') + '\t\tbuf = NULL;\n\t}\n\treturn buf;\n}\n\n',
}


def mk(an, tn, place, tl, ck):
    t = 'if (' + TEST[tn] + ') {\n\t\t' + ARMS[an] + '\n\t}\n\t'
    if place == 'afternl':
        b = SIG + NL + t + TAILS[tl]
    elif place == 'first':
        b = SIG + t + NL + TAILS[tl]
    return b + PRE + caller(ck)


def variants():
    for an, tn, place, tl, ck in itertools.product(ARMS, TEST, ('afternl', 'first'), TAILS, ('ifnot2', 'ret')):
        yield '|'.join((an, tn, place, tl, ck)), mk(an, tn, place, tl, ck)
