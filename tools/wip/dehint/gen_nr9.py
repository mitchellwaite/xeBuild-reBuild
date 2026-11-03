"""Sign casts at got's and size's uses only (locals stay int): natural for %x, sizes, offsets. Does a cast leave a copy at IRA?"""
import itertools

FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
LOG = ['got, size', '(uint32_t)got, size', 'got, (uint32_t)size', '(uint32_t)got, (uint32_t)size', '(unsigned int)got, (unsigned int)size']
ADDR = ['(char *)buf + got', '(char *)(buf + got)', '(char *)&buf[got]', '(char *)buf + (uint32_t)got', '(char *)(buf + (size_t)got)']
LEN = ['size - got', '(int)((uint32_t)size - got)', '(int)(size - (uint32_t)got)']
EQ = ['got == size', '(uint32_t)got == (uint32_t)size']
ADD = ['got += r;', 'got += (uint32_t)r;', 'got = (uint32_t)got + r;']


def src(lg, ad, ln, eq, add):
    return r'''
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
	while (got < size) {
		if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {
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
			printf("received 0x%%08x of 0x%%08x\r", got, size);
	}
	if (verbose)
		putchar('\n');
	if (%s) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", %s);
	%s
	return NULL;
}
''' % (FREE, ad, ln, FREE, add, eq, lg, FREE)


def variants():
    for i in itertools.product(LOG, ADDR, LEN, EQ, ADD):
        yield '|'.join(i), src(*i)
