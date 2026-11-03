"""Attempt 2: do-while + guard with tails that lower P(short count): flags, gotos, a return variable.
Target (traces of do>0): log = P(fail)*(J+else) must be under R = 291; J = 282; else = 323."""
import itertools
from gen_nr13 import HEAD

SEL = {
    'plain': 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r == SOCKET_ERROR || r == 0) {',
    'side': 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {',
}
FORMS = {
    'do>0': ('if (size > 0) do {\n', '\t} while (got < size);\n'),
    'do>0b': ('if (size > 0) {\n\t\tdo {\n', '\t\t} while (got < size);\n\t}\n'),
    'while': ('while (got < size) {\n', '\t}\n'),
}
FREE1 = 'if (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t\treturn NULL;'
FREE = 'if (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\n\treturn NULL;'
SHORT = r'''if (verbose)
		putchar('\n');
	log_printf(0, "received only %x of %x bytes! fail\n", got, size);
	'''
AFTER = "if (verbose)\n\t\tputchar('\\n');\n"
AFTER = AFTER.replace('\\\\', '\\')
TAILS = {
    'base': AFTER + '\tif (got == size) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SHORT + FREE + '\n',
    'okif': 'ok = got == size;\n\t' + AFTER + '\tif (ok) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SHORT + FREE + '\n',
    'okgoto': 'ok = got == size;\n\t' + AFTER + '\tif (!ok)\n\t\tgoto bad;\n\t*len = size;\n\treturn buf;\nbad:\n\t' + SHORT + FREE + '\n',
    'badflag': 'ok = 1;\n\tif (got != size)\n\t\tok = 0;\n\t' + AFTER + '\tif (ok) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SHORT + FREE + '\n',
    'flag2': 'ok = 0;\n\tif (got == size)\n\t\tok = 1;\n\t' + AFTER + '\tif (ok) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SHORT + FREE + '\n',
    'flagafter': AFTER + '\tok = 0;\n\tif (got == size)\n\t\tok = 1;\n\tif (ok) {\n\t\t*len = size;\n\t\treturn buf;\n\t}\n\t' + SHORT + FREE + '\n',
    'badgoto': AFTER + '\tif (got != size)\n\t\tgoto bad;\n\t*len = size;\n\treturn buf;\nbad:\n\t' + SHORT + FREE + '\n',
    'retvar': AFTER + '\tif (got == size) {\n\t\t*len = size;\n\t\tret = buf;\n\t} else {\n\t\t' + SHORT.replace('\n\t', '\n\t\t') + 'if (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n\t\tret = NULL;\n\t}\n\treturn ret;\n',
    'retvar2': AFTER + '\tret = buf;\n\tif (got != size) {\n\t\t' + SHORT.replace('\n\t', '\n\t\t') + 'if (buf != (uint8_t *)&netEmpty)\n\t\t\tfree(buf);\n\t\tret = NULL;\n\t} else\n\t\t*len = size;\n\treturn ret;\n',
    'retvar3': AFTER + '\tret = NULL;\n\tif (got == size) {\n\t\t*len = size;\n\t\tret = buf;\n\t\tgoto done;\n\t}\n\t' + SHORT + 'if (buf != (uint8_t *)&netEmpty)\n\t\tfree(buf);\ndone:\n\treturn ret;\n',
}


def src(sel, form, tail):
    a, b = FORMS[form]
    head = HEAD.replace('int size, got, r;', 'int size, got, r, ok;\n\tuint8_t *ret;')
    body = '\t\t' + SEL[sel] + r'''
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			''' + FREE1 + r'''
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %d\n",
				   WSAGetLastError());
			''' + FREE1 + r'''
		}
		got += r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\r", got, size);
'''
    return head + '\t' + a + body + b + '\t' + TAILS[tail] + '}\n'


def variants():
    for s, f, t in itertools.product(SEL, FORMS, TAILS):
        yield '|'.join((s, f, t)), src(s, f, t)
