# attempt 24: the block offset passed through its own PHI (`used`, 0 when the test fails) rather than a table: PRE then rebuilds the chain in the arm from that PHI, and anything left of the arm's cast is dead at lim2 and cheap enough to stay (cost counts only the same loop's deps, from memory).
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw296.py build/iw/a24/nt.c 4 60`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
I = '						'
M = '(off & 0x1ffff)'
def blk(*l):
    return [(L0, I + '{\n' + ''.join(I + '	' + x + '\n' for x in l) + I + '}\n')]
LL = [('', [])]
for tl, ty in (('i', 'int'), ('u', 'uint32_t'), ('h', 'uint16_t'), ('s', 'short')):
    ifs = 'if ' + M
    for ul, use in (('a', 'left = 256 - u / 512;'), ('b', 'left = 256 - (uint32_t)u / 512;'), ('c', 'left = 256 - (u >> 9);'), ('d', 'left = 256 - ((uint32_t)u >> 9);')):
        LL.append(('p' + tl + ul, blk(ty + ' u = 0;', ifs, '	u = ' + M + ';', use)))
        LL.append(('q' + tl + ul, blk(ty + ' u;', ifs, '	u = ' + M + ';', 'else', '	u = 0;', use)))
        LL.append(('r' + tl + ul, blk(ty + ' u = ' + M + ' ? ' + M + ' : 0;', use)))
        LL.append(('s' + tl + ul, blk(ty + ' u = 0;', ifs, '	u = ' + M + ' / 512;', 'left = 256 - u;')))
        LL.append(('t' + tl + ul, blk(ty + ' u = 0;', 'uint32_t o = ' + M + ';', 'if (o)', '	u = o;', use)))
        LL.append(('v' + tl + ul, blk('uint32_t o = ' + M + ';', ty + ' u = o;', 'if (!o)', '	u = 0;', use)))
AXES = [LL]
