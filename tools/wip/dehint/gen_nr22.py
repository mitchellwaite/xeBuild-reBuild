"""Attempt 4: the verbose newline as a small helper. The hope: not early-inlined, so a plain call at profile_estimate (guard's else block holds a call, the call heuristic applies: p=.869), and IPA inlines it later."""
import itertools

PLAIN = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {'
SIDE = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {'
NL = "if (verbose)" + chr(10) + chr(9) + chr(9) + "putchar('" + chr(92) + "n');"
CALL = 'endLine(verbose);'
FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);'
_H = r"""void endLine(uint32_t verbose)
{
	if (verbose)
		putchar('BSn');
}

""".replace('BS', chr(92))
HELP = {'static': 'static ' + _H, 'inline': 'static inline ' + _H}


def body(sel, s1, s2, s3):
    return r'''
		%s
			log_printf(0, "timeout waiting for data, error %%%%d\n", WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			%s
			log_printf(0, "could not receive data on socket, error %%%%d\n",
				   WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		got += r;
		if (verbose)
			printf("received 0x%%%%08x of 0x%%%%08x\r", got, size);
''' % (sel, s1)


def src(helper, form, sel, s1, s2, s3):
    b = body(sel, s1, s2, s3)
    if form == 'while':
        loop = 'while (got < size) {' + b + '\t}'
    elif form == 'do':
        loop = 'if (size > 0) do {' + b + '\t} while (got < size);'
    elif form == 'do2':
        loop = 'if (size > 0) {\n\t\tdo {' + b + '\t\t} while (got < size);\n\t}'
    return (helper + r'''uint8_t *netRecvVerbose(int *len, uint32_t verbose)
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
	%s
	%s
	if (got == size) {
		*len = size;
		return buf;
	}
	%s
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	%s
	return NULL;
}
''') % (loop, s2, s3, FREE)


def variants():
    for hk, form, (sk, sel), s1, s2, s3 in itertools.product(('static', 'inline'), ('while', 'do', 'do2'), (('plain', PLAIN), ('side', SIDE)), (NL, CALL), (NL, CALL), (NL, CALL)):
        if NL == s1 == s2 == s3:
            continue
        tag = '%s|%s|%s|%d%d%d' % (hk, form, sk, s1 == CALL, s2 == CALL, s3 == CALL)
        yield tag, src(HELP[hk], form, sel, s1, s2, s3).replace('%%', '%')
