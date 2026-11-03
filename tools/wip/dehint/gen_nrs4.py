"""Two thin wrappers over one `static inline` helper: netRecv (verbose 0) and netRecvVerbose. IPA inline, not IPA-CP.
Axes: linkage of netRecv, select spelling, helper's verbose type."""
import itertools

F = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
BODY = r'''NAME
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	int size, got, r;

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
	if (verbose)
		printf("waiting for 0x%x bytes\n", size);
	got = 0;
	while (got < size) {
		SEL {
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			FREE
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %d\n",
				   WSAGetLastError());
			FREE
			return NULL;
		}
		got += r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\r", got, size);
	}
	if (verbose)
		putchar('\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %x of %x bytes! fail\n", got, size);
	FREE
	return NULL;
}
'''.replace('FREE', F)
SEL = {'pl': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0)',
       'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0)'}
TYPE = ['uint32_t', 'int']
LINK = ['static inline', 'inline', 'static __inline__']
WRAP = ['static ', '']


def variants():
    for s, t, l, w in itertools.product(SEL, TYPE, LINK, WRAP):
        name = '%s uint8_t *recvReply(int *len, %s verbose)' % (l, t)
        body = BODY.replace('NAME', name).replace('SEL', SEL[s])
        n = body + '\n%suint8_t *netRecv(int *len)\n{\n\treturn recvReply(len, 0);\n}\n' % w
        v = 'uint8_t *netRecvVerbose(int *len, uint32_t verbose)\n{\n\treturn recvReply(len, verbose);\n}\n'
        yield '|'.join((s, t, l, w)), n, v
