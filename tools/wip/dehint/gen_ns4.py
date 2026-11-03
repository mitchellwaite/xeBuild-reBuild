"""netSendFile: head written with a flag; the flag test is threaded away, the first test keeps its own estimate."""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
INIT = 'char cmd[264] = "SNDF";\n\n\tstrcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n'
HEAD = {
    'okif': 'int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (!ok)\n\t\treturn 0;\n\t',
    'badif': 'int bad = 0;\n\n\tif (!name || !buf)\n\t\tbad = 1;\n\tif (bad)\n\t\treturn 0;\n\t',
    'okexpr': 'int ok = name && buf;\n\n\tif (!ok)\n\t\treturn 0;\n\t',
    'badexpr': 'int bad = !name || !buf;\n\n\tif (bad)\n\t\treturn 0;\n\t',
    'ok2': 'int ok = 1;\n\n\tif (!name)\n\t\tok = 0;\n\tif (!buf)\n\t\tok = 0;\n\tif (!ok)\n\t\treturn 0;\n\t',
    'bad2': 'int bad = 0;\n\n\tif (!name)\n\t\tbad = 1;\n\tif (!buf)\n\t\tbad = 1;\n\tif (bad)\n\t\treturn 0;\n\t',
    'oknest': 'int ok = 0;\n\n\tif (name) {\n\t\tif (buf)\n\t\t\tok = 1;\n\t}\n\tif (!ok)\n\t\treturn 0;\n\t',
    'ok3': 'int ok = name != 0;\n\n\tif (ok)\n\t\tok = buf != 0;\n\tif (!ok)\n\t\treturn 0;\n\t',
    'ok4': 'int ok = 0;\n\n\tif (name)\n\t\tok = buf != 0;\n\tif (!ok)\n\t\treturn 0;\n\t',
    'bad3': 'int bad = 1;\n\n\tif (name && buf)\n\t\tbad = 0;\n\tif (bad)\n\t\treturn 0;\n\t',
    'ok5': 'int ok = 1;\n\n\tif (!name || !buf)\n\t\tok = 0;\n\tif (!ok)\n\t\treturn 0;\n\t',
    'ok6': 'int ok = 1;\n\n\tif (!name || !buf)\n\t\tok = 0;\n\tif (ok) {\n\t',
}
STR = {'not': '!netSendStr(cmd)', 'ne1': 'netSendStr(cmd) != 1', 'le': 'netSendStr(cmd) <= 0'}
RS = ['block', 'flat']


def variants():
    for (h, hv), (s, sv), rs in itertools.product(HEAD.items(), STR.items(), RS):
        tl = 'if (ret)\n\t\treturn 1;\n\treturn 0;\n'
        chk = 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n'
        if rs == 'block':
            body = '{\n\tint rlen;\n\n\tr = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + chk + '\tnetFree(r);\n\t}\n\t' + tl
            decl = 'int ret;\n\tuint8_t *r;\n\t'
        else:
            body = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + chk + '\tnetFree(r);\n\t' + tl
            decl = 'int rlen, ret;\n\tuint8_t *r;\n\t'
        close = '\t}\n\treturn 0;\n' if h == 'ok6' else ''
        yield ('|'.join((h, s, rs)), 'int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t' + decl + hv + INIT + '\tif (' + sv + ')\n\t\treturn 0;\n\tif (!' + T + ')\n\t\treturn 0;\n\t' + body + close + '}\n')
