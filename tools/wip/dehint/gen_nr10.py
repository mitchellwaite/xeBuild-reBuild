"""uint32_t got, int size (the %x/%08x args and the buffer offset are unsigned): spellings of the casts."""
import itertools

FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
WH = ['(int)got < size', '(int)got - size < 0']
LEN = ['size - got', 'size - (int)got', '(int)(size - got)']
ADDR = ['(char *)buf + got', '(char *)buf + (int)got']
EQ = ['(int)got == size', 'got == (uint32_t)size', 'size == (int)got']
ADD = ['got += r;', 'got = (int)got + r;', 'got += (uint32_t)r;']
ST = ['*len = size;', '*len = got;']
LOG = ['got, size', '(int)got, size']
PR = ['got, size', '(int)got, size']


def src(sel, wh, ln, ad, eq, add, st, lg, pr):
    return r'''
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	int size, r;
	uint32_t got;

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
	while (%s) {
		%s
			log_printf(0, "timeout waiting for data, error %%d\n", WSAGetLastError());
			%s
			return NULL;
		}
		r = recv(netSock, %s, %s, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %%d\n",
				   WSAGetLastError());
			%s
			return NULL;
		}
		%s
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\r", %s);
	}
	if (verbose)
		putchar('\n');
	if (%s) {
		%s
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", %s);
	%s
	return NULL;
}
''' % (wh, SEL[sel], FREE, ad, ln, FREE, add, pr, eq, st, lg, FREE)


def variants():
    for i in itertools.product(SEL, WH, LEN, ADDR, EQ, ADD, ST, LOG, PR):
        yield '|'.join(i), src(*i)
