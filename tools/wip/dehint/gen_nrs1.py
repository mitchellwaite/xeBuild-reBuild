"""netRecv as its own function: the verbose-free text of netRecvVerbose. static/public, plain/side select."""
import itertools


def src(link, sel):
    return link + r'''uint8_t *netRecv(int *len)
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
	got = 0;
	while (got < size) {
		''' + sel + r''' {
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			log_printf(0, "could not receive data on socket, error %d\n",
				   WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		got += r;
	}
	if (got == size) {
		*len = size;
		return buf;
	}
	log_printf(0, "received only %x of %x bytes! fail\n", got, size);
	if (buf != (uint8_t *)&netEmpty)
		free(buf);
	return NULL;
}
'''


SEL = ['r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0)',
       'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0)']


def variants():
    for l, s in itertools.product(['static ', ''], SEL):
        yield l + '|' + str(SEL.index(s)), src(l, s)
