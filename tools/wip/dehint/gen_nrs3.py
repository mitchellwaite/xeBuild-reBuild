"""netRecv alone: head select/recv test spellings (raise the head-exit blocks above the store block),
x loop select x loop form x tail x decl type."""
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
       'le': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r <= 0) {\n' + SELFAIL + '\n}',
       }
RECV = 'r = recv(netSock, (char *)buf + got, size - got, 0);\n if (r == SOCKET_ERROR) {\n' + RECVFAIL + '\n}'
LOOP = {
    'while': ('got = 0;\nwhile (got < size) {', 'got += r;\n}'),
    'doguard': ('got = 0;\nif (size > 0) do {', 'got += r;\n} while (got < size);'),
}
LOG = r'log_printf(0, "received only %x of %x bytes! fail\n", got, size);'
TAIL = {
    'eq': 'if (got == size) {\n*len = size;\nreturn buf;\n}\n' + 'LOG\n' + F + '\nreturn NULL;',
    'ne': 'if (got != size) {\nLOG\n' + F + '\nreturn NULL;\n}\n*len = size;\nreturn buf;',
}
DECL = {'sgr': 'int size, got, r;', 'u': 'int size, r;\nuint32_t got;'}
HSEL = {
    'pl': r'''r = select(0, &fds, NULL, NULL, &tv);
	if (r == SOCKET_ERROR || r == 0) {''',
    'side': r'''if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {''',
    'le': r'''r = select(0, &fds, NULL, NULL, &tv);
	if (r <= 0) {''',
    'nz': r'''r = select(0, &fds, NULL, NULL, &tv);
	if (!r || r == SOCKET_ERROR) {''',
}
HRECV = {
    'pl': r'''r = recv(netSock, (char *)hdr, 4, 0);
	if (r == SOCKET_ERROR || r == 0) {''',
    'side': r'''if ((r = recv(netSock, (char *)hdr, 4, 0)) == SOCKET_ERROR || r == 0) {''',
    'le': r'''r = recv(netSock, (char *)hdr, 4, 0);
	if (r <= 0) {''',
    'nz': r'''r = recv(netSock, (char *)hdr, 4, 0);
	if (!r || r == SOCKET_ERROR) {''',
}
HEAD = r'''static uint8_t *netRecv(int *len)
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
	HSEL
		log_printf(0, "timeout waiting for data, %d\n", WSAGetLastError());
		return NULL;
	}
	HRECV
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


def variants():
    for k in itertools.product(HSEL, HRECV, LOOP, SEL, TAIL, DECL):
        hs, hr, lp, sel, tl, dc = k
        a, b = LOOP[lp]
        yield '|'.join(k), HEAD.replace('DECLS', DECL[dc]).replace('HSEL', HSEL[hs]).replace('HRECV', HRECV[hr]) + '\n'.join([a, SEL[sel], RECV, b, TAIL[tl].replace('LOG', LOG)]) + '\n}\n'
