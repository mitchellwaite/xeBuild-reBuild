"""Attempt 2: flag-driven loops (extra loop exits at profile_estimate that jump threading removes later), natural
"ok"/"err" variables. Each exit edge counted by PRED_LOOP_EXIT changes a, b, h in the clone's threshold."""
import itertools

HEAD = r'''
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
	int size, got, r%s;

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
'''
SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
SLOG = r'''log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());'''
RLOG = r'''if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %d\n",
				   WSAGetLastError());'''
RECV = 'r = recv(netSock, (char *)buf + got, size - got, 0);'
VERB = r'''if (verbose)
			printf("received 0x%08x of 0x%08x\r", got, size);'''
AFTER = r'''	if (verbose)
		putchar('\n');
'''
SHORT = r'''if (verbose)
		putchar('\n');
	log_printf(0, "received only %x of %x bytes! fail\n", got, size);'''
FREE = '''if (buf != (uint8_t *)&netEmpty)
		free(buf);
	return NULL;'''


def body(kind, sel):
    s = SEL[sel]
    if kind == 'errbreak':  # err set and break, the tail tests it
        return ', err = 0', '''	while (got < size) {
		%s
			%s
			err = 1;
			break;
		}
		%s
		if (r == SOCKET_ERROR) {
			%s
			err = 1;
			break;
		}
		got += r;
		%s
	}
	if (err) {
		%s
	}
%s	if (got == size) {
		*len = size;
		return buf;
	}
	%s
	%s
''' % (s, SLOG, RECV, RLOG, VERB, FREE, AFTER, SHORT, FREE)
    if kind == 'okcond':  # the loop runs while ok
        return ', ok = 1', '''	while (ok && got < size) {
		%s
			%s
			ok = 0;
		} else {
			%s
			if (r == SOCKET_ERROR) {
				%s
				ok = 0;
			} else {
				got += r;
				%s
			}
		}
	}
	if (!ok) {
		%s
	}
%s	if (got == size) {
		*len = size;
		return buf;
	}
	%s
	%s
''' % (s, SLOG, RECV, RLOG, VERB, FREE, AFTER, SHORT, FREE)
    if kind == 'okcond2':  # got < size first
        return ', ok = 1', '''	while (got < size && ok) {
		%s
			%s
			ok = 0;
			continue;
		}
		%s
		if (r == SOCKET_ERROR) {
			%s
			ok = 0;
			continue;
		}
		got += r;
		%s
	}
	if (!ok) {
		%s
	}
%s	if (got == size) {
		*len = size;
		return buf;
	}
	%s
	%s
''' % (s, SLOG, RECV, RLOG, VERB, FREE, AFTER, SHORT, FREE)
    if kind == 'okbreak':  # ok cleared on the way out, the failure paths share the tail through ok
        return ', ok = 1', '''	while (got < size) {
		%s
			%s
			ok = 0;
			break;
		}
		%s
		if (r == SOCKET_ERROR) {
			%s
			ok = 0;
			break;
		}
		got += r;
		%s
	}
	if (ok) {
	%s	if (got == size) {
			*len = size;
			return buf;
		}
		%s
	}
	%s
''' % (s, SLOG, RECV, RLOG, VERB, AFTER, SHORT, FREE)
    if kind == 'retbreak':  # r stays SOCKET_ERROR/0: tested after the loop; ret variable
        return ', fail = 0', '''	for (;;) {
		if (got >= size)
			break;
		%s
			%s
			fail = 1;
			break;
		}
		%s
		if (r == SOCKET_ERROR) {
			%s
			fail = 1;
			break;
		}
		got += r;
		%s
	}
	if (!fail) {
	%s	if (got == size) {
			*len = size;
			return buf;
		}
		%s
	}
	%s
''' % (s, SLOG, RECV, RLOG, VERB, AFTER, SHORT, FREE)
    raise ValueError(kind)


def variants():
    for k, s in itertools.product(('errbreak', 'okcond', 'okcond2', 'okbreak', 'retbreak'), SEL):
        d, b = body(k, s)
        yield k + '|' + s, HEAD % d + b + '}\n'
