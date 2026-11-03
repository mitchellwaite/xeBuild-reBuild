"""mkcur.py: write cur.c = current best (base.c plus accepted natural replacements).  Kept as code so each step stays visible."""
import os

import gen1base as g

HERE = os.path.dirname(os.path.abspath(__file__))
L = g.LOG
IP_NEW = """			i++;
			if (!argv[i] || i == argc || *argv[i] == '-') {
				%s			}
			ip = argv[i];
""" % L


def cur():
    t = g.BASE
    assert g.IP_OLD_FULL in t
    t = t.replace(g.IP_OLD_FULL, IP_NEW)
    return t


if __name__ == '__main__':
    with open(os.path.join(HERE, 'cur.c'), 'w', newline='\n') as f:
        f.write(cur())
