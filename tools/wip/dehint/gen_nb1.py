"""Borderline review, net: netSendStr's own shape x `!` or `<= 0` at the three upload sites.

netSendStr is inlined at IPA, so its body's estimate is what its copies in the callers carry.
If one of its shapes gives the callers' layout with `!`, the three `<= 0` can go."""
from nbsweep import BASE, sub

CUR = '''	int len = strlen(s);

	if (send(netSock, s, len, 0) != len)
		return 0;
	return 1;
}'''

HELPERS = {
    'cur': CUR,
    'reteq': '''	int len = strlen(s);

	return send(netSock, s, len, 0) == len;
}''',
    'ifeq': '''	int len = strlen(s);

	if (send(netSock, s, len, 0) == len)
		return 1;
	return 0;
}''',
    'rvar': '''	int len = strlen(s);
	int r = send(netSock, s, len, 0);

	if (r != len)
		return 0;
	return 1;
}''',
    'ok0': '''	int len = strlen(s);
	int ok = 0;

	if (send(netSock, s, len, 0) == len)
		ok = 1;
	return ok;
}''',
    'ok1': '''	int len = strlen(s);
	int ok = 1;

	if (send(netSock, s, len, 0) != len)
		ok = 0;
	return ok;
}''',
    'tern': '''	int len = strlen(s);

	return send(netSock, s, len, 0) != len ? 0 : 1;
}''',
    'sent': '''	int len = strlen(s);
	int sent = send(netSock, s, len, 0);

	return sent == len;
}''',
    'nolen': '''	if (send(netSock, s, strlen(s), 0) != (int)strlen(s))
		return 0;
	return 1;
}''',
    'ifelse': '''	int len = strlen(s);

	if (send(netSock, s, len, 0) == len)
		return 1;
	else
		return 0;
}''',
}

SITES = [
    ('\tif (netSendStr(cmd) <= 0)\n\t\treturn 0;\n\tif (!netSendData', '\tif (!netSendStr(cmd))\n\t\treturn 0;\n\tif (!netSendData'),
    ('\t\tif (netSendStr(cmd) <= 0)\n', '\t\tif (!netSendStr(cmd))\n'),
    ('if (netSendStr("WBPT\\n") <= 0 ||', 'if (!netSendStr("WBPT\\n") ||'),
]


def variants():
    for rt in ('int', 'uint32_t'):
        for hn, h in HELPERS.items():
            t0 = sub(BASE, CUR, h)
            if rt != 'int':
                t0 = sub(t0, 'int netSendStr(const char *s)', rt + ' netSendStr(const char *s)')
            for m in range(8):
                t = t0
                for i, (old, new) in enumerate(SITES):
                    if m & (1 << i):
                        t = sub(t, old, new)
                tag = '%s|%s|%s' % (rt[0], hn, ''.join('!' if m & (1 << i) else '<' for i in range(3)))
                yield tag, t
