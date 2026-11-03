"""netSendFile: structure sweep.  Function-level cmd declaration or block, returns or single exit, nesting."""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
INIT = 'strcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n'
CMD = 'char cmd[264] = "SNDF";\n\n\t'


def tail_block(check, tail, ret0='return 0;'):
    return '{\n\tint rlen;\n\n\tr = netRecv(&rlen);\n\tif (!r)\n\t\t%s\n\t%s\tnetFree(r);\n\t}\n\t%s' % (ret0, check, tail)


CHECK = {
    'set': 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n',
    'nest': 'ret = 0;\n\tif (rlen == 2) {\n\t\tif (getBeU16(r) == OK_REPLY)\n\t\t\tret = 1;\n\t}\n',
}
TAIL = {'if': 'if (ret)\n\t\treturn 1;\n\treturn 0;\n', 'ret': 'return ret;\n'}
HEADS = {
    # (before cmd, after whole body)
    'seq': ('if (!name)\n\t\treturn 0;\n\tif (!buf)\n\t\treturn 0;\n\t', ''),
    'or': ('if (!name || !buf)\n\t\treturn 0;\n\t', ''),
    'and': ('if (name && buf) {\n\t', '}\n\treturn 0;\n'),
    'nest': ('if (name) {\n\tif (buf) {\n\t', '}\n\t}\n\treturn 0;\n'),
    'nest2': ('if (!name)\n\t\treturn 0;\n\tif (buf) {\n\t', '}\n\treturn 0;\n'),
    'nest3': ('if (name) {\n\tif (!buf)\n\t\treturn 0;\n\t{\n\t', '}\n\t}\n\treturn 0;\n'),
}
SENDS = {
    'seq': ('if (!netSendStr(cmd))\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;\n\t' % T, ''),
    'or': ('if (!netSendStr(cmd) || !%s)\n\t\treturn 0;\n\t' % T, ''),
    'and': ('if (netSendStr(cmd) && %s) {\n\t' % T, '}\n\treturn 0;\n'),
    'nest': ('if (netSendStr(cmd)) {\n\tif (%s) {\n\t' % T, '}\n\t}\n\treturn 0;\n'),
    'nest2': ('if (netSendStr(cmd)) {\n\tif (!%s)\n\t\treturn 0;\n\t{\n\t' % T, '}\n\t}\n\treturn 0;\n'),
}
DECL = {'top': True, 'mid': False}
CMDSCOPE = ['fn', 'block']
RSCOPE = ['block', 'flat']


def variants():
    for (h, hv), (s, sv), (c, cv), (t, tv), cs, rs in itertools.product(
            HEADS.items(), SENDS.items(), CHECK.items(), TAIL.items(), CMDSCOPE, RSCOPE):
        if rs == 'block':
            body = tail_block(cv, tv)
            decl = 'int ret;\n\tuint8_t *r;\n\n\t'
        else:
            body = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + cv + '\tnetFree(r);\n\t' + tv
            decl = 'int rlen, ret;\n\tuint8_t *r;\n\n\t'
        core = CMD + INIT + '\t' + sv[0] + body + sv[1]
        if cs == 'block' and not hv[1]:
            core = '{\n\t' + core + '\t}\n'
        if not hv[1] and cs == 'block':
            pass
        src = ('int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t' + decl + hv[0]
               + core + hv[1] + '}\n')
        yield ('|'.join((h, s, c, t, cs, rs)), src)
