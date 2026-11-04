# attempt 24: a local array in the nonzero arm whose entries are all real values: the page count (rounded first) with the block offset, or the page total with the offset negated. Scored by iw23sw.py (lines, arm at dce4, sccp names).
# `python tools/wip/dehint/iw23sw.py tools/wip/dehint/gen_iw298.py build/iw/a24/nt.c 4 40`
L0 = '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n'
RO = '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n'
S9 = '						left -= pages;\n						s[9] = left >> 2;\n'
OLD = L0 + RO + S9
I = '						'
M = '(off & 0x1ffff)'
def arm(*l):
    return ''.join(I + '	' + x + '\n' for x in l)
def rep(body, tail=S9, head=RO):
    return [(OLD, head + body + tail)]
J = I + 's[9] = left >> 2;\n'
LOOP = ('int k;', '', 'left = 256;', 'for (k = 0; k < 2; k++)', '	left -= used[k];')
LOOPU = ('int k;', 'uint32_t u = 256;', '', 'for (k = 0; k < 2; k++)', '	u -= used[k];', 'left = u;')
FO = [('', [])]
for ty in ('uint32_t', 'int'):
    tl = ty[0]
    for ol, ent in (('op', '{ ' + M + ' / 512, pages }'), ('po', '{ pages, ' + M + ' / 512 }')):
        for ll, lp in (('l', LOOP), ('u', LOOPU)):
            for el, els in (('e1', 'left = 256 - pages;'), ('e2', 'left = 256;\n' + I + '	left -= pages;')):
                b = I + 'if ' + M + ' {\n' + arm(ty + ' used[2] = ' + ent + ';', *lp) + I + '} else\n' + I + '	' + (els if el == 'e1' else '{ ' + els.replace('\n' + I + '	', ' ') + ' }') + '\n'
                FO.append((tl + ol + ll + el, rep(b, J)))
    # the page total and the offset, negated, added up: every entry is real, but no one would write this (probe of the mechanism)
    b = I + 'if ' + M + ' {\n' + arm('int parts[2] = { 256, -(int)(' + M + ' / 512) };', 'int k;', '', 'left = 0;', 'for (k = 0; k < 2; k++)', '	left += parts[k];') + I + '} else\n' + I + '	left = 256;\n'
    if tl == 'u':
        FO.append(('sum', [(L0, b)]))
AXES = [FO]
