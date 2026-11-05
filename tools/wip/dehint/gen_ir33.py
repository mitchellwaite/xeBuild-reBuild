"""parseDump, HEAD's unsigned n: n and blk are two names of one value, so `n` as an argument may do what the b2
pin does (a second pseudo for the inner loop).  Which call takes n where, with the pins gone."""
FOCUS = ['_parseDump']
S1 = '''			b2 = blk;
			__asm__("" : "+r"(b2));
			if (!addRemapP(b2, blk, 0, dst, blocks))
'''
S2 = 'if (!addRemapP(blk, blk, blk, -1, blocks))'
S3 = 'if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))'
CB = '''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
'''
AX1 = [
    ('p:bb', [(S1, '			if (!addRemapP(blk, blk, 0, dst, blocks))\n')]),
    ('p:nb', [(S1, '			if (!addRemapP(n, blk, 0, dst, blocks))\n')]),
    ('p:bn', [(S1, '			if (!addRemapP(blk, n, 0, dst, blocks))\n')]),
    ('p:nn', [(S1, '			if (!addRemapP(n, n, 0, dst, blocks))\n')]),
    ('p:k', []),
]
AX2 = [
    ('q:k', []),
    ('q:nbb', [(S2, 'if (!addRemapP(n, blk, blk, -1, blocks))')]),
    ('q:bnb', [(S2, 'if (!addRemapP(blk, n, blk, -1, blocks))')]),
    ('q:nnb', [(S2, 'if (!addRemapP(n, n, blk, -1, blocks))')]),
    ('q:bbn', [(S2, 'if (!addRemapP(blk, blk, n, -1, blocks))')]),
]
AX3 = [('c:k', []), ('c', [(CB, '')])]
AX4 = [('t:k', []), ('t:u', [('static int addRemapP(int block, int ablock, int cb,', 'static int addRemapP(uint32_t block, uint32_t ablock, int cb,')]),
       ('t:u1', [('static int addRemapP(int block, int ablock, int cb,', 'static int addRemapP(uint32_t block, int ablock, int cb,')])]
AXES = [AX1, AX2, AX3, AX4]
