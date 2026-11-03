"""Attempt 2: loop forms x guard spellings x tail shapes x shared fail label (predictors on the paths, GOTO and
early return change the log block's and the guard's frequencies)."""
import itertools

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
SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
# (before body, after body, label before the tail or '')
FORMS = {
    'while': ('while (got < size) {\n', '\t}\n', ''),
    'do>0': ('if (size > 0) do {\n', '\t} while (got < size);\n', ''),
    'do-goto': ('if (size <= 0)\n\t\tgoto done;\n\tdo {\n', '\t} while (got < size);\ndone:\n', ''),
    'do-goto<0': ('if (size < 0)\n\t\tgoto done;\n\tdo {\n', '\t} while (got < size);\ndone:\n', ''),
    'wh-goto': ('if (size <= 0)\n\t\tgoto done;\n\twhile (got < size) {\n', '\t}\ndone:\n', ''),
    'for': ('for (; got < size; got += r) {\n', '\t}\n', 'for'),
}
FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t\treturn NULL;'
GFAIL = 'goto fail;'
TAILS = {
    'early': r'''	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	%s
''',
    'ne': r'''	if (got != size) {
		if (verbose)
			putchar('\n');
		log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
		%s
	}
	*len = size;
	return buf;
''',
    'negoto': r'''	if (got != size)
		goto bad;
	*len = size;
	return buf;
bad:
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	%s
''',
    'eqgoto': r'''	if (got == size)
		goto ok;
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %%x of %%x bytes! fail\n", got, size);
	%s
ok:
	*len = size;
	return buf;
''',
}


def src(sel, form, tail, shared):
    a, b, kind = FORMS[form]
    fr = GFAIL if shared else FREE
    add = '' if kind == 'for' else '\t\tgot += r;\n'
    verb = r'''		if (verbose)
			printf("received 0x%08x of 0x%08x\r", got, size);
'''
    if kind == 'for':
        # verbose print must follow the add: keep it in the body through the increment expression
        a = 'while (got < size) {\n'
        b = '\t}\n'
        add = '\t\tgot += r;\n'
    body = '\t\t' + SEL[sel] + r'''
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			''' + fr + r'''
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %d\n",
				   WSAGetLastError());
			''' + fr + r'''
		}
''' + add + verb
    t = TAILS[tail] % fr.replace('%', '%%')
    t = t.replace('%%', '%')
    after = r'''	if (verbose)
		putchar('\n');
'''
    end = ''
    if shared:
        end = 'fail:\n\tif (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;\n'
    return HEAD + '\t' + a + body + b + after + t + end + '}\n'


def variants():
    for s, f, t, sh in itertools.product(SEL, FORMS, TAILS, (0, 1)):
        if f == 'for':
            continue
        yield '|'.join((s, f, t, 'shared' if sh else 'each')), src(s, f, t, sh)
