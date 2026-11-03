"""netRecv alone: loop form x select x recv test x tail x types x decl order."""
import itertools

F = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
SELFAIL = r'''log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			FREE
			return NULL;'''.replace('FREE', F)
RECVFAIL = r'''log_printf(0, "could not receive data on socket, error %d\n", WSAGetLastError());
			FREE
			return NULL;'''.replace('FREE', F)
SEL = {'pl': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {\n' + SELFAIL + '\n}',
       'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {\n' + SELFAIL + '\n}',
       'sep': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR) {\n' + SELFAIL + '\n}\n if (r == 0) {\n' + SELFAIL + '\n}',
       }
RECV = {'eq': 'r = recv(netSock, (char *)buf + got, size - got, 0);\n if (r == SOCKET_ERROR) {\n' + RECVFAIL + '\n}',
        'side': 'if ((r = recv(netSock, (char *)buf + got, size - got, 0)) == SOCKET_ERROR) {\n' + RECVFAIL + '\n}',
        }
LOOP = {
    'while': ('got = 0;\nwhile (got < size) {', 'got += r;\n}'),
    'init_while': ('while (got < size) {', 'got += r;\n}'),
    'for': ('for (got = 0; got < size; got += r) {', '}'),
    'doguard': ('got = 0;\nif (size > 0) do {', 'got += r;\n} while (got < size);'),
    'do': ('got = 0;\ndo {', 'got += r;\n} while (got < size);'),
    'forbreak': ('got = 0;\nfor (;;) {\nif (got >= size) break;', 'got += r;\n}'),
    'whilene': ('got = 0;\nwhile (size > got) {', 'got += r;\n}'),
}
LOG = r'log_printf(0, "received only %x of %x bytes! fail\n", got, size);'
TAIL = {
    'eq': 'if (got == size) {\n*len = size;\nreturn buf;\n}\n' + 'LOG\n' + F + '\nreturn NULL;',
    'ne': 'if (got != size) {\nLOG\n' + F + '\nreturn NULL;\n}\n*len = size;\nreturn buf;',
    'lt': 'if (got < size) {\nLOG\n' + F + '\nreturn NULL;\n}\n*len = size;\nreturn buf;',
    'ret': 'if (got != size) {\nLOG\n' + F + '\nbuf = NULL;\n} else\n*len = size;\nreturn buf;',
}
DECL = {'sgr': 'int size, got, r;', 'gsr': 'int got, size, r;', 'rgs': 'int r, got, size;',
        'u': 'int size, r;\nuint32_t got;', 'us': 'uint32_t size, got;\nint r;'}
HEAD = r'''uint8_t *netRecv(int *len)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	DECLS

	tv.tv_sec = 15;
	tv.tv_usec = 0;
	FD_ZERO(&fds);
	FD_SET(netSock, &fds);
	*len = 0;
	r = select(0, &fds, NULL, NULL, &tv);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "timeout waiting for data, %d\n", WSAGetLastError());
		return NULL;
	}
	r = recv(netSock, (char *)hdr, 4, 0);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "unable to fetch first 4 bytes, %d\n", WSAGetLastError());
		return NULL;
	}
	size = getBeU32(hdr);
	if (size == -1)
		return NULL;
	if (size == 0) {
		*len = 0;
		return (uint8_t *)&netEmpty;
	}
	buf = calloc(size, 1);
'''


def src(lp, sel, rc, tl, dc, link):
    a, b = LOOP[lp]
    d = DECL[dc]
    if lp == 'init_while':
        if dc not in ('sgr',):
            return None
        d = 'int size, r;\nint got = 0;'
    return link + HEAD.replace('DECLS', d) + '\n'.join([a, SEL[sel], RECV[rc], b, TAIL[tl].replace('LOG', LOG)]) + '\n}\n'


def variants():
    for k in itertools.product(LOOP, SEL, RECV, TAIL, DECL, ['static ']):
        s = src(*k)
        if s:
            yield '|'.join(k), s
