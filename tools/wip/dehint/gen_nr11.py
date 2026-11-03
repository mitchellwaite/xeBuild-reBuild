"""Loop structure axis: overshoot checks at the loop bottom (a live 4th exit), continue forms, goto-fail for the frees."""
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
SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
RFAIL = '''if (verbose)
				putchar('\\n');
			log_printf(0, "could not receive data on socket, error %%d\\n",
				   WSAGetLastError());
			%s
			return NULL;''' % FREE
PRINT = 'if (verbose)\n\t\t\tprintf("received 0x%08x of 0x%08x\\r", got, size);\n'
SHORT = '''if (verbose)
		putchar('\\n');
	log_printf(0, "received only %%x of %%x bytes! fail\\n", got, size);
	%s
	return NULL;''' % FREE
TAIL = '''	if (verbose)
		putchar('\\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	%s
}
''' % SHORT
TAILLBL = '''	if (verbose)
		putchar('\\n');
	if (got == size) {
		*len = size;
		return buf;
	}
short_read:
	%s
}
''' % SHORT
# name: (loop head, after-recv code, loop end, tail)
R = 'if (r == SOCKET_ERROR) {\n\t\t\t' + RFAIL + '\n\t\t}\n'
FORMS = {
    'base': ('while (got < size) {', R + '\t\tgot += r;\n\t\t' + PRINT, '\t}\n', TAIL),
    'over-break': ('while (got < size) {', R + '\t\tgot += r;\n\t\t' + PRINT + '\t\tif (got > size)\n\t\t\tbreak;\n', '\t}\n', TAIL),
    'over-break2': ('while (got < size) {', R + '\t\tgot += r;\n\t\tif (got > size)\n\t\t\tbreak;\n\t\t' + PRINT, '\t}\n', TAIL),
    'over-goto': ('while (got < size) {', R + '\t\tgot += r;\n\t\t' + PRINT + '\t\tif (got > size)\n\t\t\tgoto short_read;\n', '\t}\n', TAILLBL),
    'cont-r': ('while (got < size) {', 'if (r != SOCKET_ERROR) {\n\t\t\tgot += r;\n\t\t\t' + PRINT + '\t\t\tcontinue;\n\t\t}\n\t\t' + RFAIL + '\n', '\t}\n', TAIL),
    'else-r': ('while (got < size) {', 'if (r != SOCKET_ERROR) {\n\t\t\tgot += r;\n\t\t\t' + PRINT + '\t\t} else {\n\t\t\t' + RFAIL + '\n\t\t}\n', '\t}\n', TAIL),
    'break-r': ('while (got < size) {', 'if (r == SOCKET_ERROR)\n\t\t\tbreak;\n\t\tgot += r;\n\t\t' + PRINT, '\t}\n', None),
}
BRTAIL = '''	if (got < size) {
		if (verbose)
			putchar('\\n');
		log_printf(0, "could not receive data on socket, error %%d\\n",
			   WSAGetLastError());
		%s
		return NULL;
	}
''' % FREE


def variants():
    for s, f in itertools.product(SEL, FORMS):
        h, a, e, t = FORMS[f]
        if t is None:
            t = BRTAIL + TAIL
        yield s + '|' + f, HEAD + '\t' + h + '\n\t\t' + SEL[s] + r'''
			log_printf(0, "timeout waiting for data, error %%d\n", WSAGetLastError());
			%s
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		''' % FREE + a + e + t
