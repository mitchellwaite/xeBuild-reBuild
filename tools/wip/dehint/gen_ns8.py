"""netSendFile: flag heads x rlen's block start x check x tail x netSendStr test: looking for a=1 (exact .s) without `<= 0`."""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
INIT = 'char cmd[264] = "SNDF";\n\n\tstrcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n\t'
RECV = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t'
CHECK = {
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n\tnetFree(r);\n\t',
    'else': 'if (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n\telse\n\t\tret = 0;\n\tnetFree(r);\n\t',
}
TAIL = {
    'if': 'if (ret)\n\t\treturn 1;\n\treturn 0;\n',
    'ifz': 'if (!ret)\n\t\treturn 0;\n\treturn 1;\n',
    'ifelse': 'if (ret)\n\t\treturn 1;\n\telse\n\t\treturn 0;\n',
}
SIG = 'int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t'
DECL = 'int ret;\n\tuint8_t *r;\n\t'
OPEN = '{\n\tint rlen;\n\n\t'
HEAD = {
    'okif': ('int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (!ok)\n\t\treturn 0;\n\t', ''),
    'badif': ('int bad = 0;\n\n\tif (!name || !buf)\n\t\tbad = 1;\n\tif (bad)\n\t\treturn 0;\n\t', ''),
    'oknest': ('int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (ok) {\n\t', '\t}\n\treturn 0;\n'),
    'badnest': ('int bad = 0;\n\n\tif (!name || !buf)\n\t\tbad = 1;\n\tif (!bad) {\n\t', '\t}\n\treturn 0;\n'),
}
STR = {'not': 'if (!netSendStr(cmd))\n\t\treturn 0;\n\t', 'le': 'if (netSendStr(cmd) <= 0)\n\t\treturn 0;\n\t',
       'eq0': 'if (netSendStr(cmd) == 0)\n\t\treturn 0;\n\t'}
DATA = 'if (!' + T + ')\n\t\treturn 0;\n\t'
NESTD = ('if (%s) {\n\t' % T, '}\n\treturn 0;\n\t')


def w_recv(s, c, t): return INIT + s + DATA + OPEN + RECV + c + '}\n\t' + t
def w_str(s, c, t): return INIT + OPEN + s + DATA + RECV + c + '}\n\t' + t
def w_init(s, c, t): return OPEN + INIT + s + DATA + RECV + c + '}\n\t' + t
def w_cmdin(s, c, t): return '{\n\t' + INIT + s + OPEN + DATA + RECV + c + '}\n\t}\n\t' + t
def w_cmdin2(s, c, t): return '{\n\t' + INIT + s + DATA + OPEN + RECV + c + '}\n\t}\n\t' + t
def w_cmdin3(s, c, t): return '{\n\t' + INIT + OPEN + s + DATA + RECV + c + '}\n\t}\n\t' + t
def w_all(s, c, t): return '{\n\t' + INIT + s + DATA + OPEN + RECV + c + t + '}\n\t}\n'
def w_tailin(s, c, t): return INIT + s + DATA + '{\n\t' + 'int rlen;\n\n\t' + RECV + c + '}\n\t{\n\t' + t + '}\n'


WHERE = {'recv': w_recv, 'str': w_str, 'init': w_init, 'cmdin': w_cmdin, 'cmdin2': w_cmdin2, 'cmdin3': w_cmdin3}


def variants():
    for (h, hv), (s, sv), (c, cv), (t, tv), (w, wv) in itertools.product(HEAD.items(), STR.items(), CHECK.items(), TAIL.items(), WHERE.items()):
        yield ('|'.join((h, s, c, t, w)), SIG + DECL + hv[0] + wv(sv, cv, tv) + hv[1] + '}\n')
