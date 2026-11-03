"""netSendFile: flag head; where the scopes of rlen, cmd, r, ret end relative to netFree and the tail, and how the tail reads."""
import itertools

T = 'netSendData(buf, len, log_get_verbose() != 0)'
SEND = 'if (!netSendStr(cmd))\n\t\treturn 0;\n\tif (!' + T + ')\n\t\treturn 0;\n\t'
INIT = 'char cmd[264] = "SNDF";\n\n\tstrcpy(cmd + 4, name);\n\tstrcat(cmd, "\\n");\n\t'
RECV = 'r = netRecv(&rlen);\n\tif (!r)\n\t\treturn 0;\n\t'
CHECK = {
    'set': 'ret = 0;\n\tif (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n\t',
    'expr': 'ret = rlen == 2 && getBeU16(r) == OK_REPLY;\n\t',
    'nest': 'ret = 0;\n\tif (rlen == 2) {\n\t\tif (getBeU16(r) == OK_REPLY)\n\t\t\tret = 1;\n\t}\n\t',
    'else': 'if (rlen == 2 && getBeU16(r) == OK_REPLY)\n\t\tret = 1;\n\telse\n\t\tret = 0;\n\t',
}
TAIL = {
    'if': 'if (ret)\n\t\treturn 1;\n\treturn 0;\n',
    'ifelse': 'if (ret)\n\t\treturn 1;\n\telse\n\t\treturn 0;\n',
    'ifz': 'if (!ret)\n\t\treturn 0;\n\treturn 1;\n',
    'ret': 'return ret;\n',
    'cond': 'return ret ? 1 : 0;\n',
}
FREE = 'netFree(r);\n\t'
# (head decl, body) from the check, scope arrangement
SCOPES = {
    # rlen ends after free (current)
    'r_afterfree': lambda c, t: ('int ret;\n\tuint8_t *r;\n\t', INIT + SEND + '{\n\tint rlen;\n\n\t' + RECV + c + FREE + '}\n\t' + t),
    # rlen ends before free
    'r_beforefree': lambda c, t: ('int ret;\n\tuint8_t *r;\n\t', INIT + SEND + '{\n\tint rlen;\n\n\t' + RECV + c + '}\n\t' + FREE + t),
    # rlen ends after the check's first part: r only in block
    'r_recvonly': lambda c, t: ('int ret;\n\tuint8_t *r;\n\tint rlen;\n\t', INIT + SEND + RECV + c + FREE + t),
    # cmd + everything to free in a block
    'cmd_afterfree': lambda c, t: ('int ret;\n\tuint8_t *r;\n\tint rlen;\n\t', '{\n\t' + INIT + SEND + RECV + c + FREE + '}\n\t' + t),
    'cmd_rlen_block': lambda c, t: ('int ret;\n\tuint8_t *r;\n\t', '{\n\t' + INIT + SEND + '{\n\tint rlen;\n\n\t' + RECV + c + FREE + '}\n\t}\n\t' + t),
    'cmd_beforefree': lambda c, t: ('int ret;\n\tuint8_t *r;\n\tint rlen;\n\t', '{\n\t' + INIT + SEND + RECV + c + '}\n\t' + FREE + t),
    # the send/recv in their own block with r inside
    'r_inner': lambda c, t: ('int ret;\n\t', INIT + SEND + '{\n\tint rlen;\n\tuint8_t *r;\n\n\t' + RECV + c + FREE + '}\n\t' + t),
    # rlen in a block that ends before the check: needs its value
    'r_len': lambda c, t: ('int ret, n;\n\tuint8_t *r;\n\t', INIT + SEND + '{\n\tint rlen;\n\n\t' + RECV + 'n = rlen;\n\t}\n\t' + c.replace('rlen', 'n') + FREE + t),
    'ifelseblock': lambda c, t: ('int ret;\n\tuint8_t *r;\n\t', INIT + SEND + '{\n\tint rlen;\n\n\t' + RECV + c + FREE + t + '}\n'),
}
HEAD = {
    'okif': 'int ok = 0;\n\n\tif (name && buf)\n\t\tok = 1;\n\tif (!ok)\n\t\treturn 0;\n\t',
}


def variants():
    for (h, hv), (c, cv), (t, tv), (s, sv) in itertools.product(HEAD.items(), CHECK.items(), TAIL.items(), SCOPES.items()):
        decl, body = sv(cv, tv)
        yield ('|'.join((h, c, t, s)), 'int netSendFile(const char *name, const void *buf, uint32_t len)\n{\n\t' + decl + hv + body + '}\n')
