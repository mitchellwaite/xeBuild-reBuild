# imgAdd: the table with both entries real, one iteration (attempt 23's first match)
A = ('\t\t\t\t\t\tif (off & 0x1ffff) {\n'
     '\t\t\t\t\t\t\tint used[2] = { (off & 0x1ffff) / 512, 0 };\n'
     '\t\t\t\t\t\t\tint k;\n'
     '\n'
     '\t\t\t\t\t\t\tleft = 256;\n'
     '\t\t\t\t\t\t\tfor (k = 0; k < 2; k++)\n'
     '\t\t\t\t\t\t\t\tleft -= used[k];\n')
I7 = '\t\t\t\t\t\t\t'


def f(ty, kty, cond):
    return [(A, '\t\t\t\t\t\tif (off & 0x1ffff) {\n' + I7 + '%s n[2] = { 256, (off & 0x1ffff) / 512 };\n' % ty
             + I7 + '%s k;\n\n' % kty + I7 + 'left = n[0];\n' + I7 + 'for (k = 1; %s; k++)\n' % cond + I7 + '\tleft -= n[k];\n')]


V = []
for ty in ('int', 'uint32_t'):
    for kty in ('int', 'uint32_t'):
        for cond in ('k < 2', 'k != 2'):
            V.append(('%s_%s_%s' % (ty[0], kty[0], cond[2:].replace(' ', '')), f(ty, kty, cond)))
