"""Attempt 4, the task's ideas 1-5 crossed: tails using got, remainder and pointer locals, advance forms, calloc check, exit shapes; plain and side select."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrtpl import *
B = chr(92)
ZERO = '*len = 0;' + chr(10) + chr(9) + chr(9) + 'return (uint8_t *)&netEmpty;'
TAIL = {
    'base': dict(),
    'lengot': dict(store='*len = got;\n\t\treturn buf;'),
    'sizegot': dict(store='size = got;\n\t\t*len = size;\n\t\treturn buf;'),
    'neq_store': dict(eq='got != size || !size', store='goto bad;'),  # placeholder replaced below
}
del TAIL['neq_store']
RCV = {
    'base': dict(),
    'left': dict(rcv='{\n\t\t\tint left = size - got;\n\t\t\tr = recv(netSock, (char *)buf + got, left, 0);\n\t\t}'),
    'leftdecl': dict(decl='int size, got, r, left;', rcv='left = size - got;\n\t\tr = recv(netSock, (char *)buf + got, left, 0);'),
    'p': dict(decl='int size, got, r;\n\tchar *p;', rcv='p = (char *)buf + got;\n\t\tr = recv(netSock, p, size - got, 0);'),
    'pleft': dict(decl='int size, got, r, left;\n\tchar *p;', rcv='p = (char *)buf + got;\n\t\tleft = size - got;\n\t\tr = recv(netSock, p, left, 0);'),
}
ADV = {
    'base': dict(),
    'addr': dict(adv='got = got + r;'),
    'gt0': dict(adv='if (r > 0)\n\t\t\tgot += r;'),
    'ne0': dict(adv='if (r != 0)\n\t\t\tgot += r;'),
    'failneg': dict(fail='r < 0'),
    'faille': dict(fail='r <= 0'),
}
HEAD = {
    'base': dict(),
    'le0': dict(head='size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (!size) {\n\t\t*len = size;\n\t\treturn (uint8_t *)&netEmpty;\n\t}'),
    'nested': dict(head='size = getBeU32(hdr);\n\tif (size == -1 || size == 0) {\n\t\tif (size == -1)\n\t\t\treturn NULL;\n\t\t*len = 0;\n\t\treturn (uint8_t *)&netEmpty;\n\t}'),
    'zerofirst': dict(head='size = getBeU32(hdr);\n\tif (size == 0) {\n\t\t*len = 0;\n\t\treturn (uint8_t *)&netEmpty;\n\t}\n\tif (size == -1)\n\t\treturn NULL;'),
    'callocchk': dict(alloc='buf = calloc(size, 1);\n\tif (buf == NULL)\n\t\treturn NULL;'),
    'bufdefault': dict(head='size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tbuf = (uint8_t *)&netEmpty;\n\tif (size == 0) {\n\t\t*len = 0;\n\t\treturn buf;\n\t}'),
}


def variants():
    for (sk, s), (tk, t), (rk, r), (ak, a), (hk, h) in itertools.product((('side', SIDE), ('plain', PLAIN)), TAIL.items(), RCV.items(), ADV.items(), HEAD.items()):
        d = dict(sel=s)
        d.update(t); d.update(r); d.update(a); d.update(h)
        yield '|'.join((sk, tk, rk, ak, hk)), tpl(**d)
