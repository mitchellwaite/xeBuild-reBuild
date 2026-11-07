"""Attempt 14: applyIniOptions as an int function that falls off its end (or ends in a
bare `return;`): expand_null_return / expand_function_end clobber the return register,
and that clobber is a flow-active insn (not a forwarder) that emits no bytes.

python tools/wip/dehint/op14ret.py [base.c ...]  (default: src/options.c and a13_dzall.c)"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

R = optlib.R
BASES = sys.argv[1:] or [os.path.join(R, 'src', 'options.c'),
                         os.path.join(R, 'build', 'op', 'a13_dzall.c')]


def retype(t, rtype):
    t = t.replace('#include "options.h"',
                  '#define applyIniOptions applyIniOptions_decl\n#include "options.h"\n#undef applyIniOptions', 1)
    t = t.replace('void applyIniOptions(void)\n{', rtype + 'applyIniOptions(void)\n{', 1)
    return t


def variants(t):
    yield 'void', t
    for rt in ('int ', 'uint32_t '):
        yield rt + 'end-return;', retype(t, rt)
        # drop the bare `return;` before the end of the function (dz labels or not)
        t2 = retype(t, rt)
        i = t2.index('applyIniOptions(void)\n{')
        j = t2.index('\nint parseRawPatch', i)
        body = t2[i:j]
        b2 = body.replace('\t}\n\treturn;\n', '\t}\n', 1)
        if b2 != body:
            yield rt + 'falloff', t2[:i] + b2 + t2[j:]
        # every bare return in applyIniOptions as `return 0;` (control: no clobber)
        yield rt + 'return0', t2[:i] + body.replace('return;', 'return 0;') + t2[j:]


for b in BASES:
    t = open(b).read()
    for name, v in variants(t):
        r = optlib.score_text(v)
        print('%-24s %-28s %s' % (os.path.basename(b), name,
                                  'IDENTICAL' if r.get('identical') else r.get('total', r)))
