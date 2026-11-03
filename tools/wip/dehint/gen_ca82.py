"""Attempt 6: gen_ca81 S2 is text 4: only the inlined freeManifest's cmp order, `i_71 < prephitmp_99` where a5while had `prephitmp_28 > i_73`
(PRE's temporary takes a name off the free list; it must be lower than i's). Sweep plain spellings that change what's released before PRE.
Axes: body x head x tail x start of the function."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))
s = util.spec_from_file_location('gen_ca80', os.path.join(here, 'gen_ca80.py'))
g = util.module_from_spec(s)
s.loader.exec_module(g)

BODY = {
    'S2': 'if (ret) {\ni++;\nn = manifest.count;\n} else {\n%(f)s\ni = n + 1;\n}\n',
    'S2b': 'if (ret) {\nn = manifest.count;\ni++;\n} else {\n%(f)s\ni = n + 1;\n}\n',
    'S3': 'if (!ret) {\n%(f)s\ni = n + 1;\n} else {\ni++;\nn = manifest.count;\n}\n',
    'S1': 'i += ret != 0;\nif (!ret) {\n%(f)s\ni = n + 1;\n} else\nn = manifest.count;\n',
    'S10': 'if (!ret) {\n%(f)s\ni = n + 1;\ncontinue;\n}\ni++;\nn = manifest.count;\n',
    'P1': 'i++;\nif (ret)\nn = manifest.count;\nelse {\n%(f)s\ni = n + 1;\n}\n',
    'P2': 'i++;\nif (!ret) {\n%(f)s\ni = n + 1;\n} else\nn = manifest.count;\n',
    'P3': 'if (!ret) {\n%(f)s\ni = n + 1;\n} else\nn = manifest.count;\ni += ret != 0;\n',
}
HEADS = {
    'in': 'i = 0;\nn = manifest.count;\nwhile (i < n) {\n',
    'ni': 'n = manifest.count;\ni = 0;\nwhile (i < n) {\n',
    'for': 'n = manifest.count;\nfor (i = 0; i < n;) {\n',
    'for2': 'for (i = 0, n = manifest.count; i < n;) {\n',
}
ARMS2 = g.ARMS.replace('if (!netSendFile(manifest.path, manifest.data, manifest.size)) {', 'ret = netSendFile(manifest.path, manifest.data, manifest.size);\nif (!ret) {')
ARMS3 = r'''if (netSendFile(manifest.path, manifest.data, manifest.size)) {
log_printf(0, "success! Avatar data is successfully sent to the console!\n");
netTimerEnd();
ret = 1;
} else {
ret = 0;
log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
}
'''
ARMS4 = ARMS2.replace('ret = 0;\n', '')
ARMS5 = g.ARMS.replace('netTimerEnd();\nret = 1;\n', 'ret = 1;\nnetTimerEnd();\n')
TAILS = {
    'a1': 'if (ret) {\n' + g.MFS + '\n' + g.ARMS + '}\n',
    'a2': 'if (ret) {\n' + g.MFS + '\n' + ARMS2 + '}\n',
    'a3': 'if (ret) {\n' + g.MFS + '\n' + ARMS3 + '}\n',
    'a4': 'if (ret) {\n' + g.MFS + '\n' + ARMS4 + '}\n',
    'a5': 'if (ret) {\n' + g.MFS + '\n' + ARMS5 + '}\n',
}
ITEMS = {
    'e': ('struct manifestItem *e = &manifest.e[(size_t)i];\n', None),
    'e0': ('e = &manifest.e[(size_t)i];\n', '\tstruct manifestItem *e;\n'),
    'k': ('uint32_t k = i;\nstruct manifestItem *e = &manifest.e[k];\n', None),
}
OLD = '\tint i;\n\tlong ret;\n\tint n;\n'
RET1 = {
    'r0': [],
    'r1': [('ret = 1;\n\t\tif (prepSysex()) {', 'if (!prepSysex())\n\t\t\tret = 1;\n\t\telse {')],
}


def variants():
    for b, h, t, it, r in itertools.product(BODY, HEADS, TAILS, ITEMS, RET1):
        code, decl = ITEMS[it]
        body = code + g.LOG + '\n' + g.SEND + '\n' + BODY[b] % {'f': g.FAIL}
        src = g.PREP + g.FRAME.replace('@LOOP@', HEADS[h] + body + '}\n').replace('@TAIL@', TAILS[t])
        if decl:
            src = src.replace(OLD, OLD + decl)
        for o, n in RET1[r]:
            src = src.replace(o, n)
        yield '|'.join((b, h, t, it, r)), src
