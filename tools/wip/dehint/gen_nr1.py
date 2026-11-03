"""First sweep: plain source, one flag per hint removed; free helper/macro forms; tail shapes."""
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
'''

FREE = {
    'inl': 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);',
    'nf': 'netFree(buf);',
}


def body(hint, asm, free, tail):
    f = FREE[free]
    start = 'if (__builtin_expect(verbose, 0))' if hint else 'if (verbose)'
    a = '__asm__ ("" : : "g"(got));' if asm else ''
    if tail == 'A':
        t = '''	if (verbose)
		putchar('\\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\\n');
	%s
	log_printf(0, "received only %%x of %%x bytes! fail\\n", got, size);
	%s
	return NULL;
''' % (a, f)
    elif tail == 'B':
        t = '''	if (verbose)
		putchar('\\n');
	if (got != size) {
		if (verbose)
			putchar('\\n');
		%s
		log_printf(0, "received only %%x of %%x bytes! fail\\n", got, size);
		%s
		return NULL;
	}
	*len = size;
	return buf;
''' % (a, f)
    return '''
	%s
		printf("waiting for 0x%%x bytes\\n", size);
	got = 0;
	while (got < size) {
		r = select(0, &fds, NULL, NULL, &tv);
		if (r == SOCKET_ERROR || r == 0) {
			log_printf(0, "timeout waiting for data, error %%d\\n", WSAGetLastError());
			%s
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\\n');
			log_printf(0, "could not receive data on socket, error %%d\\n",
				   WSAGetLastError());
			%s
			return NULL;
		}
		got += r;
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\\r", got, size);
	}
%s}
''' % (start, f, f, t)


def variants():
    for hint in (1, 0):
        for asm in (1, 0):
            for free in FREE:
                for tail in 'AB':
                    yield 'h%d|a%d|%s|%s' % (hint, asm, free, tail), HEAD + body(hint, asm, free, tail)
