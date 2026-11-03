"""netSendFile: the netSendStr test's spelling, with the `||` head (P(pass) .39 gives buf's registers)."""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
INIT = 'char cmd[264] = "SNDF";\n\n\tstrcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n'
STR = {'not': '!netSendStr(cmd)', 'ne1': 'netSendStr(cmd) != 1', 'eq0': 'netSendStr(cmd) == 0', 'le': 'netSendStr(cmd) <= 0', 'lt1': 'netSendStr(cmd) < 1'}
DATA = {'not': '!' + T, 'eq0': T + ' == 0', 'ne1': T + ' != 1', 'le': T + ' <= 0'}
HEAD = {'or': 'if (!name || !buf)\n\t\treturn 0;\n\t', 'seq': 'if (!name)\n\t\treturn 0;\n\tif (!buf)\n\t\treturn 0;\n\t'}
CMDB = ['fn', 'block']
SEND = {'seq': 'if (%s)\n\t\treturn 0;\n\tif (%s)\n\t\treturn 0;\n\t', 'or': 'if (%s || %s)\n\t\treturn 0;\n\t'}
CHECK = {
    'set': 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n',
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n',
}
RS = ['block', 'flat']


def variants():
    for (h, hv), (s, sv), (d, dv), (e, ev), cs, rs, (c, cv) in itertools.product(
            HEAD.items(), STR.items(), DATA.items(), SEND.items(), CMDB, RS, CHECK.items()):
        tl = 'if (ret)\n\t\treturn 1;\n\treturn 0;\n'
        if rs == 'block':
            body = '{\n\tint rlen;\n\n\tr = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + cv + '\tnetFree(r);\n\t}\n\t' + tl
            decl = 'int ret;\n\tuint8_t *r;\n\n\t'
        else:
            body = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + cv + '\tnetFree(r);\n\t' + tl
            decl = 'int rlen, ret;\n\tuint8_t *r;\n\n\t'
        core = INIT + '\t' + (ev % (sv, dv)) + body
        if cs == 'block':
            core = '{\n\t' + core + '\t}\n'
        yield ('|'.join((h, s, d, e, cs, rs, c)),
               'int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t' + decl + hv + core + '}\n')
