"""Borderline review, net: netRecvVerbose's select arm with the status flag in place of
`size = got` (both arms set status), and one status test after an if/else of the two arms.

Axes: select arm's stop, the two loop tests' spelling and exit, the loop condition's spelling,
and the if/else form where one `if (status != 1)` follows both failures."""
from nbsweep import BASE

A = BASE.index('\t\tgot = 0;\n\t\twhile (got < size) {')
B0 = '\t\tif (status != 1)\n\t\t\treturn NULL;\n\t\tif (verbose)\n\t\t\tputchar'
B = BASE.index(B0) + len('\t\tif (status != 1)\n\t\t\treturn NULL;\n')

FREE = '\t\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\t\tfree(buf);\n'
SEL = ('\t\t\tr = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == SOCKET_ERROR || r == 0) {\n'
       '\t\t\t\tlog_printf(0, "timeout waiting for data, error %d\\n", WSAGetLastError());\n' + FREE)
RECVCALL = 'recv(netSock, (char *)buf + got, size - got, 0)'
RECVLOG = ('\t\t\t\tif (verbose)\n\t\t\t\t\tputchar(\'\\n\');\n'
           '\t\t\t\tlog_printf(0, "could not receive data on socket, error %d\\n",\n\t\t\t\t\t   WSAGetLastError());\n' + FREE)
RECV = '\t\t\tr = ' + RECVCALL + ';\n\t\t\tif (r == SOCKET_ERROR) {\n' + RECVLOG
TAIL = '\t\t\tgot += r;\n\t\t\tif (verbose)\n\t\t\t\tprintf("received 0x%08x of 0x%08x\\r", got, size);\n\t\t}\n'
POST = '\t\tif (status != 1)\n\t\t\treturn NULL;\n'

SA = {'size': ('size = got;', 'got >= size'), 'st': ('status = 0;', None)}
TESTS = {'ne1': 'status != 1', 'not': '!status'}
EXITS = {'b': 'break;', 'r': 'return NULL;'}
CONDS = {'lt': 'got < size', 'gt': 'size > got'}


def loop(cond, body):
    return '\t\tgot = 0;\n\t\twhile (' + cond + ') {\n' + body + TAIL + POST


def two(sa, t1, x1, t2, x2, cond):
    a, t = SA[sa]
    t = t or TESTS[t1]
    body = (SEL + '\t\t\t\t' + a + '\n\t\t\t}\n\t\t\tif (' + t + ')\n\t\t\t\t' + EXITS[x1] + '\n' +
            RECV + '\t\t\t\tstatus = 0;\n\t\t\t}\n\t\t\tif (' + TESTS[t2] + ')\n\t\t\t\t' + EXITS[x2] + '\n')
    return loop(CONDS[cond], body)


def one(t, x, cond, elif_):
    if elif_:
        mid = ('\t\t\t\tstatus = 0;\n\t\t\t} else if ((r = ' + RECVCALL + ') == SOCKET_ERROR) {\n' + RECVLOG +
               '\t\t\t\tstatus = 0;\n\t\t\t}\n')
    else:
        mid = ('\t\t\t\tstatus = 0;\n\t\t\t} else {\n' + RECV.replace('\n\t\t\t', '\n\t\t\t\t') + '\t\t\t\t\tstatus = 0;\n\t\t\t\t}\n\t\t\t}\n')
    body = SEL + mid + '\t\t\tif (' + TESTS[t] + ')\n\t\t\t\t' + EXITS[x] + '\n'
    return loop(CONDS[cond], body)


def variants():
    for sa in SA:
        for t1 in (TESTS if sa == 'st' else ['-']):
            for x1 in (EXITS if sa == 'st' else ['r']):
                for t2 in TESTS:
                    for x2 in EXITS:
                        for c in CONDS:
                            yield 'two|%s|%s%s|%s%s|%s' % (sa, t1, x1, t2, x2, c), BASE[:A] + two(sa, t1, x1, t2, x2, c) + BASE[B:]
    for t in TESTS:
        for x in EXITS:
            for c in CONDS:
                for e in (0, 1):
                    yield 'one|%s|%s|%s|%s' % ('elif' if e else 'else', t, x, c), BASE[:A] + one(t, x, CONDS[c] and c, e) + BASE[B:]
