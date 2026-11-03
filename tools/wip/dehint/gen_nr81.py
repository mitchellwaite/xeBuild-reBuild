"""Attempt 9: attempt 8's do + tail helper x scoping of hdr, fds, tv. Removing the null-return prediction from the head (inner PHI at a clobber block) raises the head failures, which relaxes `store <= head failure` and could open the g .73 window (P >= .52)."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_nr72 import helper, BODY, BS

FT = 'fd_set fds;\nstruct timeval tv;\n'
HDR = 'uint8_t hdr[4];\n'
INIT = 'tv.tv_sec = 15;\ntv.tv_usec = 0;\nFD_ZERO(&fds);\nFD_SET(netSock, &fds);\n*len = 0;\n'
SEL = 'r = select(0, &fds, NULL, NULL, &tv);\n'
RCV = 'r = recv(netSock, (char *)hdr, 4, 0);\n'
TEST = 'if (r == SOCKET_ERROR || r == 0) {\n'
L1 = 'log_printf(0, "timeout waiting for data, %d' + BS + 'n", WSAGetLastError());\n'
L2 = 'log_printf(0, "unable to fetch first 4 bytes, %d' + BS + 'n", WSAGetLastError());\n'
Z = '*len = 0;\nreturn (uint8_t *)&netEmpty;\n'
GS = 'size = getBeU32(hdr);\n'
TOP = 'uint8_t *netRecvVerbose(int *len, uint32_t verbose)\n{\n'
LOC = 'uint8_t *buf;\nint size, got, r;\n'
CALL = 'netRecvDone(buf, got, size, len, verbose)'


def core(ck, sel):
    body = BODY
    if sel == 'side':
        a = 'r = select(0, &fds, NULL, NULL, &tv);\n\t\t\tif (r == SOCKET_ERROR || r == 0) {'
        assert a in body
        body = body.replace(a, 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {')
    d = 'buf = calloc(size, 1);\nif (verbose)\n\tprintf("waiting for 0x%x bytes' + BS + 'n", size);\ngot = 0;\nif (size > 0)\ndo {\n' + body + '} while (got < size);\n'
    if ck == 'ret':
        return d + 'return ' + CALL + ';\n'
    if ck == 'var':
        return d + 'buf = ' + CALL + ';\nreturn buf;\n'
    if ck == 'ifnot':
        return d + 'if (' + CALL + ')\nreturn buf;\nreturn NULL;\n'
    if ck == 'fall':
        return d + 'if (' + CALL + ')\nreturn buf;\n'


def shape(sh, T):
    """T: the transfer, inside if (size). May fall out only for shapes with a final return NULL."""
    neg1 = SEL + TEST + L1 + 'return NULL;\n}\n'
    neg2 = RCV + TEST + L2 + 'return NULL;\n}\n' + GS
    flip = 'if (size == -1)\nreturn NULL;\nif (size) {\n' + T + '}\n'
    if sh == 'base':
        return TOP + FT + HDR + LOC + INIT + neg1 + neg2 + flip + Z + '}\n\n'
    if sh == 'hb':  # hdr in a block round its recv
        return TOP + FT + LOC + INIT + neg1 + '{\n' + HDR + neg2 + '}\n' + flip + Z + '}\n\n'
    if sh == 'fb':  # fds, tv round head and transfer; the zero arm falls out
        return TOP + HDR + LOC + '{\n' + FT + INIT + neg1 + neg2 + flip + '}\n' + Z + '}\n\n'
    if sh == 'fhb':
        return TOP + LOC + '{\n' + FT + INIT + neg1 + '{\n' + HDR + neg2 + '}\n' + flip + '}\n' + Z + '}\n\n'
    if sh == 'allb':  # fds, tv, hdr together round head and transfer
        return TOP + LOC + '{\n' + FT + HDR + INIT + neg1 + neg2 + flip + '}\n' + Z + '}\n\n'
    pos = SEL + TEST + L1 + '} else {\n@H' + RCV + TEST + L2 + '} else {\n' + GS + 'if (size != -1) {\nif (size) {\n' + T + '} else {\n' + Z + '}\n}\n}\n}\n'
    if sh == 'posfn':  # nested; head failures fall out to the final return, locals at function level
        return TOP + FT + HDR + LOC + INIT + pos.replace('@H', '') + 'return NULL;\n}\n\n'
    if sh == 'posfb':  # the fall-out is past fds' clobber
        return TOP + HDR + LOC + '{\n' + FT + INIT + pos.replace('@H', '') + '}\nreturn NULL;\n}\n\n'
    if sh == 'poshb':  # hdr in the select's else
        return TOP + FT + LOC + INIT + pos.replace('@H', HDR) + 'return NULL;\n}\n\n'
    if sh == 'posfhb':
        return TOP + LOC + '{\n' + FT + INIT + pos.replace('@H', HDR) + '}\nreturn NULL;\n}\n\n'
    if sh == 'pos2hb':  # negative select, hdr's block is the rest, recv failure falls out
        return TOP + FT + LOC + INIT + neg1 + '{\n' + HDR + RCV + TEST + L2 + '} else {\n' + GS + 'if (size != -1) {\nif (size) {\n' + T + '} else {\n' + Z + '}\n}\n}\n}\nreturn NULL;\n}\n\n'
    raise ValueError(sh)


def variants():
    sels = ('plain', 'side') if os.environ.get('NR81_SIDE') else ('plain',)
    for hk, ck, sh, sel in itertools.product(('eq', 'ne', 'eqs', 'nes', 'nesv', 'var', 'vars'), ('ret', 'var', 'ifnot'), ('base', 'hb', 'fb', 'fhb', 'allb', 'posfn', 'posfb', 'poshb', 'posfhb', 'pos2hb'), sels):
        yield '|'.join((hk, ck, sh, sel)), helper(hk, True) + shape(sh, core(ck, sel))
