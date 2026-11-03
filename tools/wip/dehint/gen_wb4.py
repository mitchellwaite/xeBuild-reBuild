"""netWriteBlocks with `!netSendStr(cmd)`: reply check in a static helper, so the free test's edge
to the helper's return block takes the early-return predictor (.783 instead of .698, free block 1069)."""
import itertools

HELP = {
    'set': 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n',
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n',
}
CALL = {
    'ifret': 'if (netReplyOk(r, rlen))\n\t\t\treturn 1;\n\t\treturn 0;\n',
    'ret': 'return netReplyOk(r, rlen);\n',
    'var': 'ret = netReplyOk(r, rlen);\n\t}\n\tif (ret)\n\t\treturn 1;\n\treturn 0;\n',
}
SCOPE = ['block', 'outer']


def make(h, c, s):
    helper = ('static int netReplyOk(uint8_t *r, int rlen)\n{\n\tint ret;\n\n\t' + HELP[h]
              + '\tnetFree(r);\n\treturn ret;\n}\n\n')
    decl = '\tuint8_t *r;\n\tchar cmd[32];\n'
    if c == 'var':
        decl = '\tint ret;\n' + decl
    if s == 'outer':
        decl = '\tint rlen;\n' + decl
    core = ''
    if s == 'block':
        core += '\t{\n\t\tint rlen;\n\n'
    else:
        core += '\t{\n'
    core += '\t\tr = netRecv(&rlen);\n\t\tif (!r)\n\t\t\treturn 0;\n\t\t' + CALL[c]
    if c != 'var':
        core += '\t}\n'
    return (helper + 'int netWriteBlocks(const uint8_t *buf, uint32_t len, uint32_t start, uint32_t count)\n{\n' + decl
            + '\n\tsprintf(cmd, "WBLK%04x%04x\\n", (uint16_t)start, (uint16_t)count);\n'
            + '\tif (!netSendStr(cmd))\n\t\treturn 0;\n'
            + '\tif (!netSendData(buf, len, log_get_verbose() != 0))\n\t\treturn 0;\n'
            + core + '}\n')


def variants():
    for h, c, s in itertools.product(HELP, CALL, SCOPE):
        yield '%s|%s|%s' % (h, c, s), make(h, c, s)
