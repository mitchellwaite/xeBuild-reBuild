"""netWritePatches: head form x netSendStr test x reply check x tail x scope."""
import itertools

STR = 'netSendStr("WBPT\\n")'
DATA = 'netSendData(buf, len, 0)'
HEADS = {
    'or': 'if (!%s || !%s || !(r = netRecv(&rlen)))\n\t\t\treturn 0;' % (STR, DATA),
    'orle': 'if (%s <= 0 || !%s || !(r = netRecv(&rlen)))\n\t\t\treturn 0;' % (STR, DATA),
    'seq': 'if (!%s)\n\t\t\treturn 0;\n\t\tif (!%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'seqle': 'if (%s <= 0)\n\t\t\treturn 0;\n\t\tif (!%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'seqlt': 'if (%s < 1)\n\t\t\treturn 0;\n\t\tif (!%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'seqorle': 'if (%s <= 0 || !%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'seqor': 'if (!%s || !%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'seqne': 'if (%s != 1)\n\t\t\treturn 0;\n\t\tif (!%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'seqeq0': 'if (%s == 0)\n\t\t\treturn 0;\n\t\tif (!%s)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
    'datale': 'if (!%s)\n\t\t\treturn 0;\n\t\tif (%s <= 0)\n\t\t\treturn 0;\n\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;' % (STR, DATA),
}
CHECK = {
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n\t\tnetFree(r);',
    'set': 'ret = 0;\n\t\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\t\tret = 1;\n\t\tnetFree(r);',
    'nest': 'ret = 0;\n\t\tif (rlen == 2) {\n\t\t\tif (getBeU16(r) == OK_REPLY)\n\t\t\t\tret = 1;\n\t\t}\n\t\tnetFree(r);',
    'else': 'if (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\t\tret = 1;\n\t\telse\n\t\t\tret = 0;\n\t\tnetFree(r);',
}
TAIL = {
    'if': 'if (ret)\n\t\treturn 1;\n\treturn 0;',
    'ifelse': 'if (ret)\n\t\treturn 1;\n\telse\n\t\treturn 0;',
    'neg': 'if (!ret)\n\t\treturn 0;\n\treturn 1;',
    'ret': 'return ret;',
    'tern': 'return ret ? 1 : 0;',
}


def variants():
    for (h, hs), (c, cs), (t, ts), sc in itertools.product(HEADS.items(), CHECK.items(), TAIL.items(), (1, 0)):
        if sc:
            body = '\tint ret;\n\tuint8_t *r;\n\n\t{\n\t\tint rlen;\n\n\t\t%s\n\t\t%s\n\t}\n\t%s\n' % (hs, cs, ts)
        else:
            body = '\tint ret, rlen;\n\tuint8_t *r;\n\n\t\t%s\n\t\t%s\n\t%s\n' % (hs, cs, ts)
        yield '%s|%s|%s|%s' % (h, c, t, 'block' if sc else 'flat'), \
            'int netWritePatches(const uint8_t *buf, uint32_t len)\n{\n' + body + '}\n'
