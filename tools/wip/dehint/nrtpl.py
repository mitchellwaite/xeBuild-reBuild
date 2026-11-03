"""Attempt 4's template for netRecvVerbose: tpl(**axes) returns a source; every axis is one piece of C text."""
FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'
PLAIN = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
SIDE = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'
DEF = dict(
    decl='int size, got, r;', sel=SIDE,
    head='size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size == 0) {\n\t\t*len = 0;\n\t\treturn (uint8_t *)&netEmpty;\n\t}',
    alloc='buf = calloc(size, 1);', init='got = 0;', top='',
    rcv='r = recv(netSock, (char *)buf + got, size - got, 0);',
    fail='r == SOCKET_ERROR',
    adv='got += r;', printgot='got', cond='got < size', tail1='', eq='got == size',
    store='*len = size;\n\t\treturn buf;', loggot='got', logsize='size', pre='', free3=FREE,
)


def tpl(**kw):
    d = dict(DEF)
    d.update(kw)
    return r'''
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	%(decl)s

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
	%(head)s
	%(alloc)s
	if (verbose)
		printf("waiting for 0x%%x bytes\n", size);
	%(init)s
	while (%(cond)s) {
		%(top)s
		%(sel)s
			log_printf(0, "timeout waiting for data, error %%d\n", WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		%(rcv)s
		if (%(fail)s) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %%d\n",
				   WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		%(adv)s
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\r", %(printgot)s, size);
		%(tail1)s
	}
	if (verbose)
		putchar('\n');
	if (%(eq)s) {
		%(store)s
	}
	%(pre)s
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", %(loggot)s, %(logsize)s);
	%(free3)s
	return NULL;
}
''' % d
