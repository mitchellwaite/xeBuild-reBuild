#!/usr/bin/env python3
"""Attempt 30: which of the landed shapes are load-bearing.  Each row is one edit on
today's src/options.c (the natural source), scored with optlib (0 = every function and
section as the reference; the split part's symbol name is ignored).

python tools/wip/dehint/op30chk.py"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

S = open(optlib.SRC).read()
W = "log_printf(0, \"***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n\", name, bad);\n"
IH = 'int optIniInt(const char *name, int def)\n{\n'
i0 = S.index(IH)
IFN = S[i0:S.index('\n}\n', i0) + 3]
INT = {
    # the warning arm returns first (the pre-attempt-30 function): 21.6%
    'int: warning returns first': IH + '\tchar *bad;\n\n\tbad = iniU32Invalid(name);\n\tif (bad) {\n\t\t' + W + '\t\treturn def;\n\t}\n\treturn getIniU32(name, def);\n}\n',
    # result variable, warning arm first: 21.6% (the log block still goes to the return)
    'int: result variable, bad arm first': IH + '\tchar *bad;\n\tint v;\n\n\tbad = iniU32Invalid(name);\n\tif (bad) {\n\t\t' + W + '\t\tv = def;\n\t} else\n\t\tv = getIniU32(name, def);\n\treturn v;\n}\n',
    'int: result variable, good arm first': IH + '\tchar *bad;\n\tint v;\n\n\tbad = iniU32Invalid(name);\n\tif (!bad)\n\t\tv = getIniU32(name, def);\n\telse {\n\t\t' + W + '\t\tv = def;\n\t}\n\treturn v;\n}\n',
    'int: def reused, good arm first': IH + '\tchar *bad;\n\n\tbad = iniU32Invalid(name);\n\tif (!bad)\n\t\tdef = getIniU32(name, def);\n\telse\n\t\t' + W + '\treturn def;\n}\n',
}
V = {'src': S}
for k, fn in INT.items():
    V[k] = S.replace(IFN, fn)
# optIniBool: the warning arm returns (the pre-attempt-30 optIniBool, at every site)
OB = '\t\t\t' + W + '\t\t\ton = 0;\n'
assert S.count(OB) == 1
V['bool: warning arm returns 0'] = S.replace(OB, OB.replace('on = 0;', 'return 0;'))
# optIniBool with early returns throughout (the Linux build's shape)
b0 = S.index('_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{\n')
BFN = S[b0:S.index('\n}\n', b0) + 3]
ER = ('_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\n'
      '\tif ((xb.bootFlags & set) || (xb.bootFlagsOff & set))\n\t\treturn 0;\n'
      '\tif (perboxExists(name))\n\t\tlog_printf(1, "Using %s option (perbox file)\\n", name);\n\telse {\n'
      '\t\tbad = iniBoolInvalid(name);\n\t\tif (bad) {\n\t\t\t' + W + '\t\t\treturn 0;\n\t\t}\n'
      '\t\tif (!getIniBool(name, def))\n\t\t\treturn 0;\n'
      '\t\tlog_printf(1, "Using %s option (ini file)\\n", name);\n\t}\n'
      '\txb.bootFlags &= ~clear;\n\txb.bootFlags |= set;\n\treturn 1;\n}\n')
V['bool: early returns throughout'] = S.replace(BFN, ER)
# the int options with the field as the default (the Linux build's form)
t = re.sub(r'(xb\.\w+) = optIniInt\(("\w+"), -1\);', r'\1 = optIniInt(\2, \1);', S)
V['int sites: field as default'] = t.replace('xb.cfLdv = optIniInt("cfldv", 0);', 'xb.cfLdv = optIniInt("cfldv", xb.cfLdv);')
# olddvd through OPT (guard on a zero mask)
V['olddvd through OPT'] = S.replace('optIniBool("olddvd", 0, 4, 0);', 'OPT("olddvd", 0, 4);')
# rev as early returns / braces
V['rev: one && test'] = S.replace('\t\ts = getIniValue("rev");\n\t\tif (s)\n', '\t\tif ((s = getIniValue("rev")))\n')


def score(k):
    r = optlib.score_text(V[k])
    if 'total' not in r:
        return k, str(r)[:200]
    per = {n: v for n, v in r['per'].items() if 'parseButton' not in n}
    notes = [n for n in r['notes'] if not n.startswith('new fn _parseButton.part') and n != 'BYTES']
    return k, ('same object' if not per and not notes else '%s %s' % (per, ' '.join(notes)))


with ThreadPoolExecutor(8) as ex:
    for k, s in ex.map(score, list(V)):
        print('%-40s %s' % (k, s), flush=True)
