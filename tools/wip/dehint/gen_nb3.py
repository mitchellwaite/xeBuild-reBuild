"""Borderline review, net: netSendFile's head without the `ok` flag (nested ifs first, as the
author seems to have favoured them), with `<= 0` or `!` on its netSendStr test."""
from nbsweep import BASE, sub

S = BASE.index('int netSendFile(')
E = BASE.index('int netFormatSysex(')
FN = BASE[S:E]
HEAD = '''	int ret, ok = 0;
	uint8_t *r;

	if (name && buf)
		ok = 1;
	if (ok) {
'''
assert FN.count(HEAD) == 1
b0 = FN.index(HEAD) + len(HEAD)
b1 = FN.rindex('\t}\n\treturn 0;\n}')
BODY = FN[b0:b1]          # the `if (ok) {` block's statements, one tab deep
SIG = FN[:FN.index(HEAD)]
DECL = '\tint ret;\n\tuint8_t *r;\n\n'


def indent(s, n=1):
    return ''.join(('\t' * n + l if l.strip() else l) for l in s.splitlines(True))


HEADS = {
    'flag': HEAD + BODY + '\t}\n\treturn 0;\n}',
    'and': DECL + '\tif (name && buf) {\n' + BODY + '\t}\n\treturn 0;\n}',
    'ne': DECL + '\tif (name != NULL && buf != NULL) {\n' + BODY + '\t}\n\treturn 0;\n}',
    'nest': DECL + '\tif (name) {\n\t\tif (buf) {\n' + indent(BODY) + '\t\t}\n\t}\n\treturn 0;\n}',
    'nestbuf': DECL + '\tif (buf) {\n\t\tif (name) {\n' + indent(BODY) + '\t\t}\n\t}\n\treturn 0;\n}',
    'nestseq': DECL + '\tif (name) {\n\t\tif (!buf)\n\t\t\treturn 0;\n' + BODY + '\t}\n\treturn 0;\n}',
    'seqnest': DECL + '\tif (!name)\n\t\treturn 0;\n\tif (buf) {\n' + BODY + '\t}\n\treturn 0;\n}',
    'nestelse': DECL + '\tif (name) {\n\t\tif (buf) {\n' + indent(BODY) + '\t\t} else\n\t\t\treturn 0;\n\t}\n\treturn 0;\n}',
    'flag2': '\tint ret, ok;\n\tuint8_t *r;\n\n\tok = name && buf;\n\tif (ok) {\n' + BODY + '\t}\n\treturn 0;\n}',
    'ret0': '\tint ret = 0;\n\tuint8_t *r;\n\n\tif (name) {\n\t\tif (buf) {\n' + indent(BODY) + '\t\t}\n\t}\n\treturn ret;\n}',
}


def variants():
    for hn, h in HEADS.items():
        fn = SIG + h + '\n\n'
        for neg in (0, 1):
            f = fn
            if neg:
                f = f.replace('netSendStr(cmd) <= 0', '!netSendStr(cmd)')
            yield '%s|%s' % (hn, '!' if neg else '<'), BASE[:S] + f + BASE[E:]
