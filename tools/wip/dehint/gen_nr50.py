"""Attempt 7: static helpers for the socket work: netWait (select + tests), netRecvSome (recv + test), a fail helper. Axes: where the log is, what is returned."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
HSEL = 'r = select(0, &fds, NULL, NULL, &tv);\n\tif (r == SOCKET_ERROR || r == 0) {\n\t\tlog_printf(0, "timeout waiting for data, %d' + BS + 'n", WSAGetLastError());\n\t\treturn NULL;\n\t}\n'
LSEL = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == SOCKET_ERROR || r == 0) {\n\t\t\t\tlog_printf(0, "timeout waiting for data, error %d' + BS + 'n", WSAGetLastError());\n\t\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;\n\t\t\t}\n'
HMSG = '"timeout waiting for data, %d' + BS + 'n"'
LMSG = '"timeout waiting for data, error %d' + BS + 'n"'
FREE3 = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n\t\t\t\treturn NULL;'
RECV0 = ('r = recv(netSock, (char *)buf + got, size - got, 0);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\tif (verbose)\n\t\t\t\t\tputchar(\'' + BS + 'n\');\n\t\t\t\tlog_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t\t\t   WSAGetLastError());\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n')


def wait_helper(kind):
    # returns helper text and the test spelled at the call
    d = 'static int netWait(fd_set *fds, struct timeval *tv%s)\n{\n\tint r = select(0, fds, NULL, NULL, tv);\n\n\tif (r == SOCKET_ERROR || r == 0) {\n%s\t\treturn %s;\n\t}\n\treturn %s;\n}\n\n'
    logm = '\t\tlog_printf(0, msg, WSAGetLastError());\n'
    if kind == 'bool':	# no log: small
        return d % ('', '', '0', '1'), lambda msg: 'if (!netWait(&fds, &tv)) {\n log_printf(0, %s, WSAGetLastError());\n' % msg
    if kind == 'neg':
        return d % ('', '', '-1', '0'), lambda msg: 'if (netWait(&fds, &tv) < 0) {\n log_printf(0, %s, WSAGetLastError());\n' % msg
    if kind == 'logbool':
        return d % (', const char *msg', logm, '0', '1'), lambda msg: 'if (!netWait(&fds, &tv, %s)) {\n' % msg
    if kind == 'logneg':
        return d % (', const char *msg', logm, '-1', '0'), lambda msg: 'if (netWait(&fds, &tv, %s) < 0) {\n' % msg
    if kind == 'logneg1':
        return d % (', const char *msg', logm, '-1', '1'), lambda msg: 'if (netWait(&fds, &tv, %s) < 0) {\n' % msg
    if kind == 'logerr':
        return d % (', const char *msg', logm, '1', '0'), lambda msg: 'if (netWait(&fds, &tv, %s)) {\n' % msg
    if kind == 'logr':
        h = 'static int netWait(fd_set *fds, struct timeval *tv, const char *msg)\n{\n\tint r = select(0, fds, NULL, NULL, tv);\n\n\tif (r == SOCKET_ERROR || r == 0) {\n\t\tlog_printf(0, msg, WSAGetLastError());\n\t\treturn 0;\n\t}\n\treturn r;\n}\n\n'
        return h, lambda msg: 'if (!netWait(&fds, &tv, %s)) {\n' % msg
    raise ValueError(kind)


def recv_helper(kind):
    logv = '\t\tif (verbose)\n\t\t\tputchar(\'' + BS + 'n\');\n\t\tlog_printf(0, "could not receive data on socket, error %d' + BS + 'n",\n\t\t\t   WSAGetLastError());\n'
    if kind == 'none':
        return '', RECV0
    tailr = {'r': 'return r;', 'neg': 'return -1;'}
    if kind in ('logr', 'logneg'):
        h = 'static int netRecvSome(char *p, int n, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n\tif (r == SOCKET_ERROR) {\n' + logv + '\t\t' + tailr[kind[3:]] + '\n\t}\n\treturn r;\n}\n\n'
        return h, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (r < 0) {\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
    if kind == 'logeq':
        h = 'static int netRecvSome(char *p, int n, uint32_t verbose)\n{\n\tint r = recv(netSock, p, n, 0);\n\n\tif (r == SOCKET_ERROR) {\n' + logv + '\t\treturn SOCKET_ERROR;\n\t}\n\treturn r;\n}\n\n'
        return h, 'r = netRecvSome((char *)buf + got, size - got, verbose);\n\t\t\tif (r == SOCKET_ERROR) {\n\t\t\t\t' + FREE3 + '\n\t\t\t}\n'
    raise ValueError(kind)


def variants():
    for wk, where, rk in itertools.product(['none', 'bool', 'neg', 'logbool', 'logneg', 'logneg1', 'logerr', 'logr'], ['both', 'loop', 'head'], ['none', 'logr', 'logneg', 'logeq']):
        if wk == 'none' and where != 'both':
            continue
        s = FLIP
        hdr = ''
        if wk != 'none':
            h, call = wait_helper(wk)
            hdr += h
            if where in ('both', 'head'):
                s = rep(s, (HSEL, call(HMSG) + ('' if 'log' in wk else '') + '\t\treturn NULL;\n\t}\n'))
            if where in ('both', 'loop'):
                s = rep(s, (LSEL, call(LMSG) + '\t\t\t\t' + FREE3 + '\n\t\t\t}\n'))
        rh, rc = recv_helper(rk)
        hdr += rh
        s = rep(s, (RECV0, rc))
        yield '|'.join((wk, where, rk)), hdr + s
