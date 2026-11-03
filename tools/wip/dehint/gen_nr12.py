"""Attempt 2 base generator: PRED_CONTINUE (56%) partner for the verbose tests, select side/plain, log cast."""
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
'''
SEL = {'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
       'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'}
BOT = {'if': r'''if (verbose)
			printf("received 0x%08x of 0x%08x\r", got, size);''',
       'cont': r'''if (!verbose)
			continue;
		printf("received 0x%08x of 0x%08x\r", got, size);'''}
LOG = {'p': 'got, size', 'c': '(uint32_t)got, size'}


def src(sel, bot, lg):
    return HEAD + r'''	got = 0;
	while (got < size) {
		%s
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
		got += r;
		%s
	}
	if (verbose)
		putchar('\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", %s);
	%s
	return NULL;
}
''' % (SEL[sel], FREE, FREE, BOT[bot], LOG[lg], FREE)


def variants():
    for s, b, l in itertools.product(SEL, BOT, LOG):
        yield '|'.join((s, b, l)), src(s, b, l)
