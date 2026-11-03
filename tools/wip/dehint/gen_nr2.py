"""Exit-count lever: `if ((r = select(..)) == SOCKET_ERROR || r == 0)` stays two tests (two loop exits) at
profile_estimate; the plain `r == SOCKET_ERROR || r == 0` folds to one range test at GENERIC."""
import itertools

SEL = 'select(0, &fds, NULL, NULL, &tv)'
HDR = 'recv(netSock, (char *)hdr, 4, 0)'


def test(call, form):
    if form == 'plain':
        return 'r = %s;\n\tif (r == SOCKET_ERROR || r == 0)' % call
    if form == 'side':
        return 'if ((r = %s) == SOCKET_ERROR || r == 0)' % call
    if form == 'side0':
        return 'if ((r = %s) == 0 || r == SOCKET_ERROR)' % call
    if form == 'plain0':
        return 'r = %s;\n\tif (r == 0 || r == SOCKET_ERROR)' % call
    raise ValueError(form)


def src(t1, t2, t3, recvform, ft):
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
	%s {
		log_printf(0, "timeout waiting for data, %%d\n", WSAGetLastError());
		return NULL;
	}
	%s {
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
		%s {
			log_printf(0, "timeout waiting for data, error %%d\n", WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		%s {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %%d\n",
				   WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		got += r;
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\r", got, size);
	}
	if (verbose)
		putchar('\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	if (buf != (uint8_t *)&netEmpty)
		free(buf);
	return NULL;
}
''' % (test(SEL, t1), test(HDR, t2), test(SEL, t3), recvform)


RECV = {
    'plain': 'r = recv(netSock, (char *)buf + got, size - got, 0);\n\t\tif (r == SOCKET_ERROR)',
    'side': 'if ((r = recv(netSock, (char *)buf + got, size - got, 0)) == SOCKET_ERROR)',
}


def variants():
    forms = ('plain', 'side', 'side0', 'plain0')
    for t1, t2, t3 in itertools.product(forms, forms, forms):
        for k, v in RECV.items():
            yield '%s|%s|%s|%s' % (t1, t2, t3, k), src(t1, t2, t3, v, 0)
