"""calcBlAreaSize without the size pin: the reference keeps file sizes in ebx (`mov ebx,[size]; add eax,ebx`), so a temporary per step, shared or not."""
import itertools
OLD = '''		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);
		/* the sum so far in ebx (esi up to the 13 lookup), as in the
		   original: IRA otherwise keeps it in esi */
		__asm__("" : "+b"(size));
		size += xb.files[x].size;
		setPatchSlot(size);
		size += 2 * imgCfSize();
'''
S = {
 'a': lambda n: '		size += xb.files[x].size;\n',
 'b': lambda n: '		xs = xb.files[x].size;\n		size += xs;\n',
 'c': lambda n: '		size = xb.files[x].size + size;\n',
 'd': lambda n: '		xs = xb.files[x].size;\n		size = xs + size;\n',
}
E = {
 'a': '		setPatchSlot(size);\n		size += 2 * imgCfSize();\n',
 'b': '		xs = imgCfSize();\n		setPatchSlot(size);\n		size += 2 * xs;\n',
 'c': '		setPatchSlot(size);\n		xs = imgCfSize();\n		size += 2 * xs;\n',
 'd': '		setPatchSlot(size);\n		xs = 2 * imgCfSize();\n		size += xs;\n',
 'e': '		setPatchSlot(size);\n		size = 2 * imgCfSize() + size;\n',
}
F = {
 'a': '		size = findFileOffset(11) + xb.files[x].size;\n',
 'b': '		xs = xb.files[x].size;\n		size = findFileOffset(11) + xs;\n',
 'c': '		size = xb.files[x].size;\n		size += findFileOffset(11);\n',
 'd': '		size = findFileOffset(11);\n		size += xb.files[x].size;\n',
}
def CASES(base):
    out = []
    for f, s1, s2, s3, e in itertools.product(F, S, S, S, E):
        new = '		x = findFile(11);\n' + F[f] + '		x = findFile(12);\n' + S[s1](1) + '		x = findFile(13);\n' + S[s2](2) + '		x = findFile(14);\n' + S[s3](3) + E[e]
        out.append(('%s %s%s%s %s' % (f, s1, s2, s3, e), base.replace(OLD, new)))
    return out
