"""On the side-effect select (V=0): axes that may lift got over the clone's threshold."""
import itertools

TAIL = {
    'eq': ('got == size', 1),
    'ne': ('got != size', 0),
    'ge': ('got >= size', 1),
    'lt': ('got < size', 0),
    'seq': ('size == got', 1),
    'sne': ('size != got', 0),
    'sle': ('size <= got', 1),
    'sgt': ('size > got', 0),
    'nlt': ('!(got < size)', 1),
}
STORE = ('size', 'got')
INIT = ('after', 'decl', 'before')    # got = 0 after the verbose printf; at the declaration; before calloc
LOOP = ('while', 'for', 'forinc')
RSCOPE = ('func', 'body')
FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'


def src(tail, store, init, loop, rscope):
    cond, pos = TAIL[tail]
    fail = '''if (verbose)
		putchar('\\n');
	log_printf(0, "received only %%x of %%x bytes! fail\\n", got, size);
	%s
	return NULL;''' % FREE
    ok = '*len = %s;\n\treturn buf;' % store
    if pos:
        t = 'if (%s) {\n\t\t%s\n\t}\n\t%s' % (cond, ok, fail)
    else:
        t = 'if (%s) {\n\t\t%s\n\t}\n\t%s' % (cond, fail, ok)
    ginit = ''
    if init == 'after' and loop == 'while':
        ginit = 'got = 0;'
    gbefore = 'got = 0;' if init == 'before' else ''
    decl = 'int size, got = 0%s;' if init == 'decl' else 'int size, got%s;'
    decl = decl % ', r'
    rlocal = '\t\tint r;\n' if rscope == 'body' else ''
    if rscope == 'body':
        # the head tests keep the function-level r under another scope
        pass
    if loop == 'while':
        head = 'while (got < size) {'
        inc1 = 'got += r;'
        inc2 = ''
    elif loop == 'for':
        head = 'for (%s; got < size; ) {' % ('got = 0' if init == 'after' else '')
        inc1 = 'got += r;'
        inc2 = ''
    else:
        head = 'for (%s; got < size; got += r) {' % ('got = 0' if init == 'after' else '')
        inc1 = ''
        inc2 = ''
    pr_got = 'got' if loop != 'forinc' else 'got + r'
    return r'''
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	%s

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
	%s
	buf = calloc(size, 1);
	if (verbose)
		printf("waiting for 0x%%x bytes\n", size);
	%s
	%s
%s		if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {
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
		%s
		if (verbose)
			printf("received 0x%%08x of 0x%%08x\r", %s, size);
	}
	if (verbose)
		putchar('\n');
	%s
}
''' % (decl, gbefore, ginit, head, rlocal, FREE, FREE, inc1, pr_got, t)


def variants():
    for tail, store, init, loop, rscope in itertools.product(TAIL, STORE, INIT, LOOP, RSCOPE):
        yield '|'.join((tail, store, init, loop, rscope)), src(tail, store, init, loop, rscope)
