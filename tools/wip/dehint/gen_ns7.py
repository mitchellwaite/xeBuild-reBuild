"""netSendFile: where rlen's block starts (netEraseBlock has it around netSendStr), with the flag heads and tests.

The target is a=1: the shared return-0 block aligned, branch freq > 4 * fallthrough freq.
"""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
INIT = 'char cmd[264] = "SNDF";\n\n\tstrcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n\t'
RECV = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t'
CHECK = 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n\tnetFree(r);\n\t'
TAIL = 'if (ret)\n\t\treturn 1;\n\treturn 0;\n'
SIG = 'int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t'
DECL = 'int ret;\n\tuint8_t *r;\n\t'
OPEN = '{\n\tint rlen;\n\n\t'
HEAD = {
    'okif': ('int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (!ok)\n\t\treturn 0;\n\t', ''),
    'badif': ('int bad = 0;\n\n\tif (!name || !buf)\n\t\tbad = 1;\n\tif (bad)\n\t\treturn 0;\n\t', ''),
    'oknest': ('int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (ok) {\n\t', '\t}\n\treturn 0;\n'),
}
STR = {'not': 'if (!netSendStr(cmd))\n\t\treturn 0;\n\t', 'le': 'if (netSendStr(cmd) <= 0)\n\t\treturn 0;\n\t'}
DATA = 'if (!' + T + ')\n\t\treturn 0;\n\t'
WHERE = {
    'recv': lambda s: INIT + s + DATA + OPEN + RECV + CHECK + '}\n\t' + TAIL,
    'data': lambda s: INIT + s + OPEN + DATA + RECV + CHECK + '}\n\t' + TAIL,
    'str': lambda s: INIT + OPEN + s + DATA + RECV + CHECK + '}\n\t' + TAIL,
    'init': lambda s: OPEN + INIT + s + DATA + RECV + CHECK + '}\n\t' + TAIL,
    'cmdin': lambda s: '{\n\t' + INIT + s + OPEN + DATA + RECV + CHECK + '}\n\t}\n\t' + TAIL,
    'cmdin2': lambda s: '{\n\t' + INIT + s + DATA + OPEN + RECV + CHECK + '}\n\t}\n\t' + TAIL,
    'cmdin3': lambda s: '{\n\t' + INIT + OPEN + s + DATA + RECV + CHECK + '}\n\t}\n\t' + TAIL,
}


def variants():
    for (h, hv), (s, sv), (w, wv) in itertools.product(HEAD.items(), STR.items(), WHERE.items()):
        yield ('|'.join((h, s, w)), SIG + DECL + hv[0] + wv(sv) + hv[1] + '}\n')
