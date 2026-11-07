"""Attempt 49: whole-function restructures of loadConsoleBlFiles without the precheck and the
cold `none:` label (attempt 48: 4/8, the not-entered return 20 laid out before case 24's r = 1
block 14).  Helpers per entry, a result variable, case order, the glitch guard hoisted, a shared
case-24 helper.  python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a49_con.py"""
import os, re
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
HEAD = 'int loadConsoleBlFiles(void)\n{'
END = 'none: __attribute__((cold));\n\treturn 0;\n}\n'


def strip(t):
    t = t.replace('\t/* the cold label gives the shrink-wrapped return 0 frequency 0, so\n'
                  '\t   bb-reorder lays it out last */\n\tif ((uint32_t)xb.nFiles <= 1)\n\t\tgoto none;\n', '', 1)
    t = t.replace(END, '}\n', 1)
    return t


def fn(t):
    a = t.index(HEAD)
    b = t.index('\n}\n', a) + 3
    return a, b


def cases(t):
    """the switch text (from 'switch (type) {' to its closing brace) of loadConsoleBlFiles"""
    a, b = fn(t)
    f = t[a:b]
    s = f.index('\t\t\tswitch (type) {')
    e = f.index('\t\t\t}\n\t\t}\n\t\tif (r) {')
    return f, s, e


def c24(t, new):
    old = '''				if (!xb.glitch2mfg)
					break;
				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;
'''
    a, b = fn(t)
    f = t[a:b]
    assert old in f
    return t[:a] + f.replace(old, new, 1) + t[b:]


def helper(t, static=True, ret='var'):
    """the switch in a per-entry helper returning r"""
    t = strip(t)
    f, s, e = cases(t)
    sw = f[s:e + 4]  # through '\t\t\t}\n'
    body = '\n'.join(l[2:] if l.startswith('\t\t') else l for l in sw.split('\n'))
    h = ('%sint loadConsoleBl(struct fileent *e)\n{\n\tuint32_t r = 0;\n\tint type = e->type;\n\n%s\treturn r;\n}\n\n'
         % ('static ' if static else '', body))
    nf = f[:f.index('\t\t\tint type = e->type;\n\n')] + '\t\t\tr = loadConsoleBl(e);\n' + f[e + 4:]
    a, b = fn(t)
    return t[:a] + h + nf + t[b:]


def retvar(t):
    t = strip(t)
    a, b = fn(t)
    f = t[a:b]
    f = f.replace('\tuint32_t r;\n', '\tuint32_t r;\n\tint ret = 0;\n', 1)
    f = f.replace('\t\t\treturn -1;\n\t\t}\n\t}\n\treturn 0;\n}', '\t\t\tret = -1;\n\t\t\tbreak;\n\t\t}\n\t}\n\treturn ret;\n}', 1)
    return t[:a] + f + t[b:]


def rbody(t):
    t = strip(t)
    a, b = fn(t)
    f = t[a:b]
    f = f.replace('\tuint32_t r;\n', '', 1).replace('\t\tr = 0;\n', '\t\tuint32_t r = 0;\n\n', 1)
    return t[:a] + f + t[b:]


def hoist(t):
    t = strip(t)
    a, b = fn(t)
    f = t[a:b]
    f = f.replace('\tuint32_t r;\n', '\tuint32_t r;\n\tint glitch = xb.glitch2mfg;\n', 1)
    f = f.replace('\t\t\t\tif (!xb.glitch2mfg)\n', '\t\t\t\tif (!glitch)\n', 1)
    return t[:a] + f + t[b:]


def move24(t, before):
    """move console's case 24 block before `case <before>:`"""
    t = strip(t)
    a, b = fn(t)
    f = t[a:b]
    i = f.index('\t\t\tcase 24:\n')
    j = f.index('\t\t\tcase 25:\n')
    blk = f[i:j]
    f = f[:i] + f[j:]
    k = f.index('\t\t\t%s\n' % before)
    f = f[:k] + blk + f[k:]
    return t[:a] + f + t[b:]


SH = '''/* case 24's file, or the default 0x60 bytes in its place */
static int loadBl24(struct fileent *e)
{
	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}

'''


def shared(t, both=True, form=0):
    t = strip(t)
    t = t.replace('/* load the input files by their type;', SH + '/* load the input files by their type;', 1)
    if form == 0:
        new = '\t\t\t\tif (xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);\n\t\t\t\tbreak;\n'
    else:
        new = '\t\t\t\tif (!xb.glitch2mfg)\n\t\t\t\t\tbreak;\n\t\t\t\tr = loadBl24(e);\n\t\t\t\tbreak;\n'
    t = c24(t, new)
    if both:
        old1 = '''				if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}'''
        assert old1 in t
        t = t.replace(old1, '\t\t\t\tif (xb.type == BUILD_JTAG || xb.glitch2mfg)\n\t\t\t\t\tr = loadBl24(e);', 1)
    return t


V = {
    'base': strip,
    'h_static': lambda t: helper(t, True),
    'h_global': lambda t: helper(t, False),
    'retvar': retvar,
    'rbody': rbody,
    'hoist': hoist,
    'm24_first': lambda t: move24(t, 'case 5: case 6:'),
    'm24_last': lambda t: move24(t, 'default:'),
    'm24_c2': lambda t: move24(t, 'case 2:'),
    'm24_c3': lambda t: move24(t, 'case 3:'),
    'sh_con0': lambda t: shared(t, False, 0),
    'sh_con1': lambda t: shared(t, False, 1),
    'sh_both0': lambda t: shared(t, True, 0),
    'sh_both1': lambda t: shared(t, True, 1),
}
