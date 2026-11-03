"""netSendFile: null tests x body scope x netSendStr test x tail; all hint-free."""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
INIT = '''char cmd[264] = "SNDF";

\tstrcpy(cmd + 4, name);
\tstrcat(cmd, "\\n");
'''

HEADS = {
    'seq': ('if (!name)\n\t\treturn 0;\n\tif (!buf)\n\t\treturn 0;\n\t', '', ''),
    'or': ('if (!name || !buf)\n\t\treturn 0;\n\t', '', ''),
    'and': ('if (name && buf) {\n\t', '}\n\treturn 0;\n', ''),
    'nest': ('if (name) {\n\tif (buf) {\n\t', '}\n\t}\n\treturn 0;\n', ''),
    'swap': ('if (!buf)\n\t\treturn 0;\n\tif (!name)\n\t\treturn 0;\n\t', '', ''),
    'orsw': ('if (!buf || !name)\n\t\treturn 0;\n\t', '', ''),
}
STR = {'not': '!netSendStr(cmd)', 'le': 'netSendStr(cmd) <= 0'}
SEND = {
    'seq': 'if (%s)\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;\n',
    'or': 'if (%s || !%s)\n\t\treturn 0;\n',
}
SCOPE = ['block', 'flat']
CHECK = {
    'set': 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n',
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n',
    'nest': 'ret = 0;\n\tif (rlen == 2) {\n\t\tif (getBeU16(r) == OK_REPLY)\n\t\t\tret = 1;\n\t}\n',
}
TAIL = {
    'if': 'if (ret)\n\t\treturn 1;\n\treturn 0;\n',
    'ret': 'return ret;\n',
}


def variants():
    for (h, hv), (s, sv), (d, dv), sc, (c, cv), (t, tv) in itertools.product(
            HEADS.items(), STR.items(), SEND.items(), SCOPE, CHECK.items(), TAIL.items()):
        send = dv % (sv, T)
        body = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + cv + '\tnetFree(r);\n'
        if sc == 'block':
            mid = '{\n\tint rlen;\n\n\t' + body + '\t}\n\t'
            decl = 'int ret;\n\tuint8_t *r;\n\n\t'
        else:
            mid = body + '\t'
            decl = 'int rlen, ret;\n\tuint8_t *r;\n\n\t'
        src = ('int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t' + decl + hv[0]
               + '{\n\t' + INIT + '\t' + send + '\t' + mid + tv + '\t}\n' + hv[1] + '}\n')
        if not hv[1]:
            pass
        yield ('|'.join((h, s, d, sc, c, t)), src)
