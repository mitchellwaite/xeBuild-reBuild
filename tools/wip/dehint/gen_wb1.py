"""netWriteBlocks: head flow x null test x OK check x tail x rlen/r scope."""
import itertools

HEAD = {
    'seq': ('if (!netSendStr(cmd))\n\t\treturn 0;\n\tif (!netSendData(buf, len, log_get_verbose() != 0))\n\t\treturn 0;\n', ''),
    'or': ('if (!netSendStr(cmd) || !netSendData(buf, len, log_get_verbose() != 0))\n\t\treturn 0;\n', ''),
    'and': ('if (netSendStr(cmd) && netSendData(buf, len, log_get_verbose() != 0)) {\n', '}\n\treturn 0;\n'),
    'nest': ('if (netSendStr(cmd)) {\n\tif (netSendData(buf, len, log_get_verbose() != 0)) {\n', '}\n\t}\n\treturn 0;\n'),
}
CHECK = {
    'set': 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n',
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n',
    'else': 'if (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n\telse\n\t\tret = 0;\n',
    'nest': 'ret = 0;\n\tif (rlen == 2) {\n\t\tif (getBeU16(r) == OK_REPLY)\n\t\t\tret = 1;\n\t}\n',
    'neg': 'ret = 1;\n\tif (rlen != 2 || getBeU16(r) != OK_REPLY)\n\t\tret = 0;\n',
}
TAIL = {
    'if': 'if (ret)\n\t\treturn 1;\n\treturn 0;\n',
    'ifn': 'if (!ret)\n\t\treturn 0;\n\treturn 1;\n',
    'ret': 'return ret;\n',
    'cond': 'return ret ? 1 : 0;\n',
}
NULL = ['ret0', 'nest', 'init']
SCOPE = ['outer', 'block', 'blockr', 'blockall']


def make(h, n, c, t, s):
    open_h, close_h = HEAD[h]
    decl_out = ['char cmd[32];']
    in_block = []
    if s == 'outer':
        decl_out += ['int rlen, ret;', 'uint8_t *r;']
    elif s == 'block':
        decl_out += ['int ret;', 'uint8_t *r;']
        in_block = ['int rlen;']
    elif s == 'blockr':
        decl_out += ['int ret;']
        in_block = ['int rlen;', 'uint8_t *r;']
    else:
        in_block = ['int rlen, ret;', 'uint8_t *r;']
    body = ''
    tail_in = s in ('blockr', 'blockall')
    tailtxt = TAIL[t]
    chk = CHECK[c] + '\tnetFree(r);\n'
    if n == 'ret0':
        core = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t' + chk
    elif n == 'nest':
        core = 'r = netRecv(&rlen);\n\tif (r) {\n\t' + chk + '\t' + tailtxt + '\t}\n\treturn 0;\n'
        tailtxt = ''
    else:
        core = None
    if core is None:
        return None
    if in_block:
        core = '{\n\t' + '\n\t'.join(in_block) + '\n\n\t' + core + ('\t' + tailtxt if tail_in and tailtxt else '') + '\t}\n'
        if tail_in:
            tailtxt = '' if t else ''
        if tail_in and n == 'ret0':
            pass
    body = '\t' + open_h + '\t' + core + ('\t' + tailtxt if (tailtxt and not tail_in) else '') + ('\t' + close_h if close_h else '')
    src = ('int netWriteBlocks(const uint8_t *buf, uint32_t len, uint32_t start, uint32_t count)\n{\n\t'
           + '\n\t'.join(decl_out) + '\n\n'
           + '\tsprintf(cmd, "WBLK%04x%04x\\n", (uint16_t)start, (uint16_t)count);\n'
           + body + '}\n')
    return src


def variants():
    for h, n, c, t, s in itertools.product(HEAD, NULL, CHECK, TAIL, SCOPE):
        v = make(h, n, c, t, s)
        if v:
            yield '%s|%s|%s|%s|%s' % (h, n, c, t, s), v
