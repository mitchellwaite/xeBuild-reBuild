"""got's update through another variable: the back-edge copy is one more ref of got at IRA, and the allocator coalesces it."""
import itertools

FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
HEAD = r'''
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	int size, got, r%s;

	tv.tv_sec = 15;
	tv.tv_usec = 0;
	FD_ZERO(&fds);
	FD_SET(netSock, &fds);
	*len = 0;
	r = select(0, &fds, NULL, NULL, &tv);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "timeout waiting for data, %%d\n", WSAGetLastError());
		return NULL;
	}
	r = recv(netSock, (char *)hdr, 4, 0);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "unable to fetch first 4 bytes, %%d\n", WSAGetLastError());
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
		printf("waiting for 0x%%x bytes\n", size);
	got = 0;
'''
SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
# (extra decl at function scope, loop-body decl, update code)
UPD = {
    'got+=': ('', '', '''got += r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", got, size);
'''),
    'n': (', n', '', '''n = got + r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", n, size);
		got = n;
'''),
    'nbody': ('', '\t\tint n;\n', '''n = got + r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", n, size);
		got = n;
'''),
    'r+=': ('', '', '''r += got;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", r, size);
		got = r;
'''),
    'n2': (', n', '', '''n = got + r;
		got = n;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", got, size);
'''),
    'r2': ('', '', '''r += got;
		got = r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", got, size);
'''),
    'gotr': ('', '', '''got = r += got;
		if (verbose)
			printf("received 0x%08x of 0x%08x\\r", got, size);
'''),
}
TAIL = r'''	if (verbose)
		putchar('\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	%s
	return NULL;
}
''' % FREE


def variants():
    for s, u in itertools.product(SEL, UPD):
        d, b, code = UPD[u]
        yield s + '|' + u, HEAD % d + '\twhile (got < size) {\n' + b + '\t\t' + SEL[s] + r'''
			log_printf(0, "timeout waiting for data, error %%d\n", WSAGetLastError());
			%s
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %%d\n",
				   WSAGetLastError());
			%s
			return NULL;
		}
		''' % (FREE, FREE) + code + '\t}\n' + TAIL
