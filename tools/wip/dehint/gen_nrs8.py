"""netRecv alone: single-return styles (ret variable, goto out, nested ifs): no early-return predictor, other shares for head exits and store."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('g3', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_nrs3.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
F = 'if (buf != (uint8_t *)&netEmpty)\n\tfree(buf);'
SELMSG = r'log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());'
RECVMSG = r'log_printf(0, "could not receive data on socket, error %d\n", WSAGetLastError());'
TOP = r'''static uint8_t *netRecv(int *len)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf, *ret = NULL;
	int size, got, r;

	tv.tv_sec = 15;
	tv.tv_usec = 0;
	FD_ZERO(&fds);
	FD_SET(netSock, &fds);
	*len = 0;
'''
HEADOUT = r'''	r = select(0, &fds, NULL, NULL, &tv);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "timeout waiting for data, %d\n", WSAGetLastError());
		goto out;
	}
	r = recv(netSock, (char *)hdr, 4, 0);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "unable to fetch first 4 bytes, %d\n", WSAGetLastError());
		goto out;
	}
	size = getBeU32(hdr);
	if (size == -1)
		goto out;
	if (size == 0) {
		*len = 0;
		ret = (uint8_t *)&netEmpty;
		goto out;
	}
	buf = calloc(size, 1);
'''
HEADRET = HEADOUT.replace('goto out;\n\t}\n\tr = recv', 'return NULL;\n\t}\n\tr = recv').replace(
    'goto out;\n\t}\n\tsize =', 'return NULL;\n\t}\n\tsize =').replace('if (size == -1)\n\t\tgoto out;', 'if (size == -1)\n\t\treturn NULL;').replace(
    'ret = (uint8_t *)&netEmpty;\n\t\tgoto out;', 'return (uint8_t *)&netEmpty;')
BODYOUT = 'r = select(0, &fds, NULL, NULL, &tv);\nif (r == SOCKET_ERROR || r == 0) {\n' + SELMSG + '\n' + F + '\ngoto out;\n}\nr = recv(netSock, (char *)buf + got, size - got, 0);\nif (r == SOCKET_ERROR) {\n' + RECVMSG + '\n' + F + '\ngoto out;\n}\ngot += r;\n'
BODYRET = BODYOUT.replace('goto out;', 'return NULL;')
LOG = g.LOG + '\n' + F
TAILS = {
    'eq': 'if (got == size) {\n*len = size;\nret = buf;\n} else {\n' + LOG + '\n}\n',
    'ne': 'if (got != size) {\n' + LOG + '\n} else {\n*len = size;\nret = buf;\n}\n',
    'eqgoto': 'if (got == size) {\n*len = size;\nret = buf;\ngoto out;\n}\n' + LOG + '\n',
    'negoto': 'if (got != size) {\n' + LOG + '\ngoto out;\n}\n*len = size;\nret = buf;\n',
}
LOOPS = {
    'while': lambda b, t: 'got = 0;\nwhile (got < size) {\n' + b + '}\n' + t,
    'do': lambda b, t: 'got = 0;\nif (size > 0) do {\n' + b + '} while (got < size);\n' + t,
    'nest': lambda b, t: 'got = 0;\nif (size > 0) {\ndo {\n' + b + '} while (got < size);\n' + t + '} else {\n' + LOG + '\n}\n',
}


def variants():
    for (hn, h), (bn, b), (tn, t), (ln, l) in itertools.product({'out': HEADOUT, 'ret': HEADRET}.items(), {'out': BODYOUT, 'ret': BODYRET}.items(), TAILS.items(), LOOPS.items()):
        yield '|'.join((hn, bn, tn, ln)), TOP + h + l(b, t) + 'out:\nreturn ret;\n}\n'
