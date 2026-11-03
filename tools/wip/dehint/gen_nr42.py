"""Attempt 6: reuse for the other locals: size through r, buf through a pointer local or a return variable, r on the verbose paths."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
BS = chr(92)
SZ = {
 'plain': [],
 'r-size': [('size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {', 'r = getBeU32(hdr);\n\tif (r == -1)\n\t\treturn NULL;\n\tsize = r;\n\tif (size) {')],
 'r-both': [('size = getBeU32(hdr);\n\tif (size == -1)\n\t\treturn NULL;\n\tif (size) {', 'r = getBeU32(hdr);\n\tif (r == -1)\n\t\treturn NULL;\n\tif (r) {\n\t\tsize = r;')],
 'size-r': [('size = getBeU32(hdr);', 'size = r = getBeU32(hdr);')],
 'got-size': [('got = 0;\n', ''), ('size = getBeU32(hdr);', 'size = getBeU32(hdr);\n\tgot = 0;')],
}
BUF = {
 'plain': [],
 'ret': [('uint8_t *buf;', 'uint8_t *buf, *ret;'), ('\t\t\t*len = size;\n\t\t\treturn buf;', '\t\t\t*len = size;\n\t\t\tret = buf;\n\t\t\treturn ret;')],
 'ret0': [('uint8_t *buf;', 'uint8_t *buf, *ret = NULL;'), ('\t\t\t*len = size;\n\t\t\treturn buf;', '\t\t\t*len = size;\n\t\t\tret = buf;\n\t\t\treturn ret;')],
 'alloc': [('uint8_t *buf;', 'uint8_t *buf;\n\tvoid *p;'), ('buf = calloc(size, 1);', 'p = calloc(size, 1);\n\t\tbuf = p;')],
 'ptr': [('uint8_t *buf;', 'uint8_t *buf, *p;'), ('r = recv(netSock, (char *)buf + got, size - got, 0);', 'p = buf + got;\n\t\t\tr = recv(netSock, (char *)p, size - got, 0);')],
}
VERB = {
 'plain': [],
 'r-got': [('got += r;\n\t\t\tif (verbose)\n\t\t\t\tprintf("received 0x%08x of 0x%08x' + BS + 'r", got, size);', 'got += r;\n\t\t\tif (verbose) {\n\t\t\t\tr = got;\n\t\t\t\tprintf("received 0x%08x of 0x%08x' + BS + 'r", r, size);\n\t\t\t}')],
 'r-sum': [('got += r;\n\t\t\tif (verbose)', 'r += got;\n\t\t\tgot = r;\n\t\t\tif (verbose)')],
 'r-log': [('log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);', 'r = got;\n\t\tlog_printf(0, "received only %x of %x bytes! fail' + BS + 'n", r, size);')],
}


def variants():
    for (a, x), (b, y), (c, z) in itertools.product(SZ.items(), BUF.items(), VERB.items()):
        yield '|'.join((a, b, c)), rep(FLIP, *(x + y + z))
