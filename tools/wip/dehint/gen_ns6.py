"""netSendFile: flag head spellings on the matching body (`ret = expr`, scoped rlen), and the body nested as in netMkdir."""

T = 'netSendData(buf, len, log_get_verbose() != 0)'
SEND = 'if (!netSendStr(cmd))\n\t\treturn 0;\n\tif (!' + T + ')\n\t\treturn 0;\n\t'
INIT = 'char cmd[264] = "SNDF";\n\n\tstrcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n\t'
BLOCK = ('{\n\tint rlen;\n\n\tr = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t'
         'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n\tnetFree(r);\n\t}\n\t')
TAIL = 'if (ret)\n\t\treturn 1;\n\treturn 0;\n'
SIG = 'int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t'
BODY = INIT + SEND + BLOCK + TAIL
DECL = 'int ret;\n\tuint8_t *r;\n\t'

SHAPES = {
    'okif': DECL + 'int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (!ok)\n\t\treturn 0;\n\t' + BODY,
    'badif': DECL + 'int bad = 0;\n\n\tif (!name || !buf)\n\t\tbad = 1;\n\tif (bad)\n\t\treturn 0;\n\t' + BODY,
    'ok5': DECL + 'int ok = 1;\n\n\tif (!name || !buf)\n\t\tok = 0;\n\tif (!ok)\n\t\treturn 0;\n\t' + BODY,
    'bad3': DECL + 'int bad = 1;\n\n\tif (name && buf)\n\t\tbad = 0;\n\tif (bad)\n\t\treturn 0;\n\t' + BODY,
    # nested as netMkdir's `if (name) {`
    'oknest': DECL + 'int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (ok) {\n\t' + BODY + '\t}\n\treturn 0;\n',
    'ok5nest': DECL + 'int ok = 1;\n\n\tif (!name || !buf)\n\t\tok = 0;\n\tif (ok) {\n\t' + BODY + '\t}\n\treturn 0;\n',
    'badnest': DECL + 'int bad = 0;\n\n\tif (!name || !buf)\n\t\tbad = 1;\n\tif (!bad) {\n\t' + BODY + '\t}\n\treturn 0;\n',
    # ret as the flag: no second variable
    'retif': 'int ret = 0;\n\tuint8_t *r;\n\n\tif (name && buf)\n\t\tret = 1;\n\tif (!ret)\n\t\treturn 0;\n\t' + BODY,
    'retnest': 'int ret = 0;\n\tuint8_t *r;\n\n\tif (name && buf)\n\t\tret = 1;\n\tif (ret) {\n\t' + BODY + '\t}\n\treturn 0;\n',
    # no flag: ifs that set nothing else
    'plainor': DECL + 'if (!name || !buf)\n\t\treturn 0;\n\t' + BODY,
    'plainand': DECL + 'if (name && buf) {\n\t' + BODY + '\t}\n\treturn 0;\n',
}


def variants():
    for k, v in SHAPES.items():
        yield (k, SIG + v + '}\n')
