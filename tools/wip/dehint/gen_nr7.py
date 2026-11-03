"""A fourth loop exit placed after recv or at the loop test (not before recv): p = 9%/4 without lowering f2/f3 relative to f1."""
import itertools

FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
HEAD = r'''
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
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
'''
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
SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
RFAIL = r'''log_printf(0, "could not receive data on socket, error %%d\n",
				   WSAGetLastError());
			%s
			return NULL;''' % FREE
R1 = '''if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\\n');
			%s
		}''' % RFAIL
R2 = '''if (r == SOCKET_ERROR && verbose) {
			putchar('\\n');
			%s
		}
		if (r == SOCKET_ERROR) {
			%s
		}''' % (RFAIL, RFAIL)
R3 = '''if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\\n');
		}
		if (r == SOCKET_ERROR) {
			%s
		}''' % RFAIL
FORMS = {
    'w': ('while (got < size) {', '', R1),
    'sz&&': ('while (size > 0 && got < size) {', '', R1),
    '&&sz': ('while (got < size && size > 0) {', '', R1),
    'brk>=': ('while (got < size) {', '\t\tif (got >= size)\n\t\t\tbreak;\n', R1),
    'brk==': ('while (got < size) {', '\t\tif (got == size)\n\t\t\tbreak;\n', R1),
    'R2': ('while (got < size) {', '', R2),
    'R3': ('while (got < size) {', '', R3),
}


def variants():
    for s, f in itertools.product(SEL, FORMS):
        h, e, r = FORMS[f]
        yield s + '|' + f, HEAD + '\t' + h + r'''
		%s
			log_printf(0, "timeout waiting for data, error %%d\n", WSAGetLastError());
			%s
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		%s
		got += r;
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\r", got, size);
%s	}
''' % (SEL[s], FREE, r, e) + TAIL
