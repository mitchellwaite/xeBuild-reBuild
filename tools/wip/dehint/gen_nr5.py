"""Sign axes on got/size/r: non-useless casts become pseudo copies at expand (more refs at IRA, coalesced later).
On plain and side-effect select."""
import itertools

FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);'


def src(gt, st, rt, sel, cond, eq):
    decl = ''
    types = {}
    for n, t in (('size', st), ('got', gt), ('r', rt)):
        types.setdefault(t, []).append(n)
    for t, ns in types.items():
        decl += '\t%s %s;\n' % (t, ', '.join(ns))
    if sel == 'side':
        s = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'
    else:
        s = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
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
	if (size == %s)
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
	}
	if (verbose)
		putchar('\n');
	if (%s) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	%s
	return NULL;
}
''' % (decl, '-1' if st == 'int' else '0xffffffff', cond, s, FREE, FREE, eq, FREE)


CONDS = {
    ('int', 'int'): ['got < size'],
    ('uint32_t', 'int'): ['(int)got < size'],
    ('int', 'uint32_t'): ['got < (int)size'],
    ('uint32_t', 'uint32_t'): ['(int)got < (int)size', '(int)(size - got) > 0'],
}


def variants():
    for gt, st, rt, sel in itertools.product(('int', 'uint32_t'), ('int', 'uint32_t'), ('int', 'uint32_t'), ('plain', 'side')):
        for cond in CONDS[(gt, st)]:
            for eq in ('got == size',):
                yield '|'.join((gt, st, rt, sel, cond)), src(gt, st, rt, sel, cond, eq)
