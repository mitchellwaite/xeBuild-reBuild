"""Attempt 6: gen_ca83's plain for loop (`i = n` then the step's i++). Text 4: only the inlined freeManifest's cmp, an SSA number. Axes: body x head x
item x prepSysex spelling x tail. A prepSysex spelling must also match standalone (checked afterwards)."""
import itertools, os
from importlib import util

here = os.path.dirname(os.path.abspath(__file__))


def load(n):
    s = util.spec_from_file_location(n, os.path.join(here, n + '.py'))
    m = util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


g = load('gen_ca80')
g10 = load('gen_ca10')
BODY = {
    'F1': 'if (!ret) {\n%(f)s\ni = n;\n} else\nn = manifest.count;\n',
    'F2': 'if (ret)\nn = manifest.count;\nelse {\n%(f)s\ni = n;\n}\n',
    'F5': 'if (!ret) {\n%(f)s\ni = n;\ncontinue;\n}\nn = manifest.count;\n',
}
HEADS = {
    'in': 'n = manifest.count;\nfor (i = 0; i < n; i++) {\n',
    'fi': 'for (i = 0, n = manifest.count; i < n; i++) {\n',
}
LOG = g.LOG
ITEMS = {
    'e': ('struct manifestItem *e = &manifest.e[i];\n', 'e->'),
    'x': ('', 'manifest.e[i].'),
}
ARMS3 = r'''if (netSendFile(manifest.path, manifest.data, manifest.size)) {
log_printf(0, "success! Avatar data is successfully sent to the console!\n");
netTimerEnd();
ret = 1;
} else {
ret = 0;
log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
}
'''
ARMS2 = g.ARMS.replace('if (!netSendFile(manifest.path, manifest.data, manifest.size)) {', 'ret = netSendFile(manifest.path, manifest.data, manifest.size);\nif (!ret) {')
TAILS = {
    'a1': g.ARMS,
    'a2': ARMS2,
    'a3': ARMS3,
    'a4': ARMS2.replace('ret = 0;\n', ''),
}


def variants():
    for b, h, it, (ph, pt), t in itertools.product(BODY, HEADS, ITEMS, itertools.product(g10.HEADS, g10.TAIL), TAILS):
        decl, acc = ITEMS[it]
        body = decl + (g.LOG + '\n' + g.SEND + '\n' + BODY[b] % {'f': g.FAIL}).replace('e->', acc)
        prep = 'int prepSysex(void)\n{\n' + g10.HEADS[ph] + g10.TAIL[pt] + '\n}\n\n'
        tail = 'if (ret) {\n' + g.MFS + '\n' + TAILS[t] + '}\n'
        yield '|'.join((b, h, it, ph + pt, t)), prep + g.FRAME.replace('@LOOP@', HEADS[h] + body + '}\n').replace('@TAIL@', tail)
