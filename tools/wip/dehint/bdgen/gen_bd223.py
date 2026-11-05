"""Attempt 11: the tail with the kit test first (`if (xb.type > BUILD_DEVGL16) { if (type == 14) set; break; }`), no t5le
label: 4 loose in loadBlFiles (gen_bd222 `gt`), the SE copy and alignment right; left is the sig-failed setFlashBuild copy
reading `xb.files[i].data` through the IV (ebx) where the reference recomputes it.  Axes: forms of the kit arm and the
`*pr` arm, with and without the `*pr` expect."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

SET = 'setFlashBuild(getBeU16(xb.files[i].data + 2));\n'
SETE = 'setFlashBuild(getBeU16(e->data + 2));\n'
TAIL = ('		if (xb.type <= BUILD_DEVGL16) {\n		t5le: __attribute__((hot));\n			if (__builtin_expect(*pr != 0, 0))\n'
        '				goto fail;\n			break;\n		}\n		if (type == 14)\n			' + SET + '		break;\n')

KIT = {
    'brk': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				SET			break;\n		}\n',
    'and': '		if (xb.type > BUILD_DEVGL16 && type == 14) {\n			SET			break;\n		}\n',
}
PR = {
    'exp': '		if (__builtin_expect(*pr != 0, 0))\n			goto fail;\n		break;\n',
    'pl': '		if (*pr)\n			goto fail;\n		break;\n',
    'pl2': '		if (*pr != 0)\n			goto fail;\n		break;\n',
    'none': '		break;\n',
}
ELSE = {'b': None}  # the else spellings are gen_bd224's (this file's 'e' edit never applied: identical scores)


def mk(t, k, p, s, e):
    kit = KIT[k].replace('SET', SET if s == 'i' else SETE)
    if e == 'e':
        kit = kit.replace('			break;\n		}\n', '		} else ')
        pr = PR[p].replace('		if', 'if', 1) if p != 'none' else None
        if pr is None:
            return None
        tail = kit + pr.replace('\n		', '\n			', 1).replace('\n		break', '\n		break', 1)
    else:
        tail = kit + PR[p]
    return bdrun.sub(t, TAIL, tail, 1)


def CASES(base):
    out = []
    for k, p, s, e in itertools.product(KIT, PR, ('i', 'e'), ELSE):
        out.append(('%s %s %s %s' % (k, p, s, e), lambda b, k=k, p=p, s=s, e=e: mk(b, k, p, s, e)))
    return out


FOCUS = ['_loadBlFiles']
