"""Attempt 7: netWait with status returns that phiopt can't fold, so the fail share comes from the helper and recv's merged block takes the helper's ok freq (lowers f2)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr50 import *
VALS = {'m1,0': ('-1', '0', '%s < 0'), 'm1,0ne': ('-1', '0', '%s'), 'm1,1': ('-1', '1', '%s < 0'), '2,0': ('2', '0', '%s'), '3,0': ('3', '0', '%s'), '2,1': ('2', '1', '%s == 2'), '0,2': ('0', '2', '!%s'), '1,2': ('1', '2', '%s == 1'),
        'r,0': ('r', '0', '%s'), '0,r': ('0', 'r', '!%s'), 'm1,r': ('-1', 'r', '%s < 0'), 'r,r': ('r', 'r', '%s <= 0')}
SIGB = 'static int netWait(fd_set *fds, struct timeval *tv%s)\n{\n\tint r = select(0, fds, NULL, NULL, tv);\n\n\tif (r == SOCKET_ERROR || r == 0) {\n%s\t\treturn %s;\n\t}\n\treturn %s;\n}\n\n'
LOGM = '\t\tlog_printf(0, msg, WSAGetLastError());\n'


def variants():
    for (a, (f, o, t)), log, where, rk in itertools.product(VALS.items(), ('hlog', 'clog'), ('loop', 'both'), ('none', 'logeq')):
        hl = log == 'hlog'
        hdr = SIGB % (', const char *msg' if hl else '', LOGM if hl else '', f, o)
        def call(msg):
            c = 'netWait(&fds, &tv, %s)' % msg if hl else 'netWait(&fds, &tv)'
            return 'if (' + t % c + ') {\n' + ('' if hl else '\t\t\tlog_printf(0, %s, WSAGetLastError());\n' % msg)
        s = FLIP
        if where == 'both':
            s = rep(s, (HSEL, call(HMSG) + '\t\treturn NULL;\n\t}\n'))
        s = rep(s, (LSEL, call(LMSG) + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
        rh, rc = recv_helper(rk)
        s = rep(s, (RECV0, rc))
        yield '|'.join((a, log, where, rk)), hdr + rh + s
