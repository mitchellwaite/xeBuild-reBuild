"""Attempt 5: same-root locals survive TER (named var, conversion, then an update of the same var): real copies at expand."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
ADDS = {
 'base': ADD,
 'n=got;n+=r;got=n': 'uint32_t n = got; n += r; got = n;',
 'n=got;n+=(u)r;got=n': 'uint32_t n = got; n += (uint32_t)r; got = n;',
 'n=r;n+=got;got=n': 'uint32_t n = r; n += got; got = n;',
}
LENS = {
 'base': (LEN, ''),
 'want=size;want-=got': ('want', 'uint32_t want = size; want -= got;\n'),
 'want=size;want-=(u)got': ('want', 'uint32_t want = size; want -= (uint32_t)got;\n'),
 'decl': ('want', 'int want = size; want -= got;\n'),
}
def variants():
    for an, a in ADDS.items():
        for ln, (l, pre) in LENS.items():
            s = rep(FLIP, (ADD, a))
            if pre:
                s = rep(s, ('r = recv(netSock, (char *)buf + got, size - got, 0);', '{' + pre + 'r = recv(netSock, (char *)buf + got, want, 0);}'))
            yield an + '|' + ln, s
