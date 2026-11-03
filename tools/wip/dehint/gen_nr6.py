"""Loop forms: do-while with a guard (guard prediction raises the short-count block's frequency; loop is normalized),
crossed with plain/side select, while/do, extra guards."""
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
BODY = r'''		%s
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
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\r", got, size);
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
FORMS = {
    'while': ('while (got < size) {\n', '\t}\n'),
    'do>0': ('if (size > 0) do {\n', '\t} while (got < size);\n'),
    'do<got': ('if (got < size) do {\n', '\t} while (got < size);\n'),
    'do>=1': ('if (size >= 1) do {\n', '\t} while (got < size);\n'),
    'wh>0': ('if (size > 0) while (got < size) {\n', '\t}\n'),
    'wh<': ('if (got < size) while (got < size) {\n', '\t}\n'),
    'do-ne': ('if (size > 0) do {\n', '\t} while (got != size && got < size);\n'),
    'for;;': ('if (size > 0) for (;;) {\n', '\t\tif (got >= size)\n\t\t\tbreak;\n\t}\n'),
    'for;;nog': ('for (;;) {\n\t\tif (got >= size)\n\t\t\tbreak;\n', '\t}\n'),
}


def variants():
    for s, f in itertools.product(SEL, FORMS):
        a, b = FORMS[f]
        yield s + '|' + f, HEAD + '\t' + a + BODY % (SEL[s], FREE, FREE) + b + TAIL
