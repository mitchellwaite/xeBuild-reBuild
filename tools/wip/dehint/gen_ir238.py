"""Attempt 18: the header's two fields copied into a local struct or array (aggregate copy, memcpy, field by field), read through it; memcpy of one
field; x E none/pin/t_addr x a3/a0.  Also a size flag table: does a struct copy move anything?"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_ir235 import *

HD = {
 'agg': HS + 'struct { uint32_t size, addr; } c = *(struct { uint32_t size, addr; } *)&h->smcBootSize;\n int addr = SWAP32(c.addr);\n int size = SWAP32(c.size);\n',
 'agg2': HS + 'struct smcField { uint32_t size, addr; } c; c = *(struct smcField *)&h->smcBootSize;\n int size = SWAP32(c.size);\n int addr = SWAP32(c.addr);\n',
 'mc': HS + 'struct { uint32_t size, addr; } c; memcpy(&c, &h->smcBootSize, sizeof(c));\n int addr = SWAP32(c.addr);\n int size = SWAP32(c.size);\n',
 'arr': HS + 'uint32_t c[2]; memcpy(c, &h->smcBootSize, sizeof(c));\n int addr = SWAP32(c[1]);\n int size = SWAP32(c[0]);\n',
 'mc1': HS + 'uint32_t ra, rs; memcpy(&ra, &h->smcBootAddr, 4); memcpy(&rs, &h->smcBootSize, 4);\n int addr = SWAP32(ra);\n int size = SWAP32(rs);\n',
 'ptr': HS + 'uint32_t *f = (uint32_t *)&h->smcBootSize;\n int addr = SWAP32(f[1]);\n int size = SWAP32(f[0]);\n',
 'raw': HS + 'uint32_t ra = h->smcBootAddr, rs = h->smcBootSize;\n int addr = SWAP32(ra);\n int size = SWAP32(rs);\n',
}
forms = {}
for hk, hd in HD.items():
    for ak, at in (('a3', ATTR), ('a0', '')):
        forms[f'{hk}.none.{ak}'] = body(at, ';', hd=hd)
        forms[f'{hk}.pin.{ak}'] = body(at, PIN, hd=hd)
        forms[f'{hk}.ta.{ak}'] = body(at, 't = addr;', hd=hd, cmpa='t', sets=lambda v: f'size = {v}; t = addr;')
if __name__ == '__main__':
    res = []
    for k, f in forms.items():
        s = score(text(f))
        if s[0] == 'E':
            print(k, 'ERR', s[1][:300])
            continue
        res.append((s[1], s[0], k, s[3]))
    for r in sorted(res, key=lambda x: (x[0], x[1])):
        print(r)
