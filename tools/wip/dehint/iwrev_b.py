# imgAdd: `int used[2] = { x / 512, 0 }`, one entry longer than needed
A = ('\t\t\t\t\t\tif (off & 0x1ffff) {\n'
     '\t\t\t\t\t\t\tint used[2] = { (off & 0x1ffff) / 512, 0 };\n'
     '\t\t\t\t\t\t\tint k;\n'
     '\n'
     '\t\t\t\t\t\t\tleft = 256;\n'
     '\t\t\t\t\t\t\tfor (k = 0; k < 2; k++)\n'
     '\t\t\t\t\t\t\t\tleft -= used[k];\n'
     '\t\t\t\t\t\t} else\n'
     '\t\t\t\t\t\t\tleft = 256;\n')


def arm(body, els='\t\t\t\t\t\t} else\n\t\t\t\t\t\t\tleft = 256;\n'):
    return [(A, '\t\t\t\t\t\tif (off & 0x1ffff) {\n' + body + els)]


I7 = '\t\t\t\t\t\t\t'
V = [
    ('base', []),
    ('plain', [(A, '\t\t\t\t\t\tif (off & 0x1ffff)\n\t\t\t\t\t\t\tleft = 256 - (off & 0x1ffff) / 512;\n\t\t\t\t\t\telse\n\t\t\t\t\t\t\tleft = 256;\n')]),
    # one iteration, both entries real
    ('n1', arm(I7 + 'int n[2] = { 256, (off & 0x1ffff) / 512 };\n' + I7 + 'int k;\n\n' + I7 + 'left = n[0];\n' + I7 + 'for (k = 1; k < 2; k++)\n' + I7 + '\tleft -= n[k];\n')),
    # counting loops: the used pages, one at a time
    ('c1', arm(I7 + 'int k;\n\n' + I7 + 'left = 256;\n' + I7 + 'for (k = 0; k < (off & 0x1ffff) / 512; k++)\n' + I7 + '\tleft--;\n')),
    ('c2', arm(I7 + 'uint32_t k;\n\n' + I7 + 'left = 256;\n' + I7 + 'for (k = 0; k < (off & 0x1ffff) / 512; k++)\n' + I7 + '\tleft--;\n')),
    ('c3', arm(I7 + 'uint32_t k;\n\n' + I7 + 'left = 256;\n' + I7 + 'for (k = 512; k <= (off & 0x1ffff); k += 512)\n' + I7 + '\tleft--;\n')),
    ('c4', arm(I7 + 'uint32_t k;\n\n' + I7 + 'left = 256;\n' + I7 + 'for (k = off & 0x1ffff; k >= 512; k -= 512)\n' + I7 + '\tleft--;\n')),
    ('c5', arm(I7 + 'int k;\n\n' + I7 + 'left = 256;\n' + I7 + 'for (k = (off & 0x1ffff) / 512; k > 0; k--)\n' + I7 + '\tleft--;\n')),
    # a struct in the arm
    ('s1', arm(I7 + 'struct { int used, total; } u = { (off & 0x1ffff) / 512, 256 };\n\n' + I7 + 'left = u.total - u.used;\n')),
    # the array with its loop over sizeof
    ('z1', arm(I7 + 'int used[2] = { (off & 0x1ffff) / 512, 0 };\n' + I7 + 'unsigned k;\n\n' + I7 + 'left = 256;\n' + I7 + 'for (k = 0; k < sizeof(used) / sizeof(used[0]); k++)\n' + I7 + '\tleft -= used[k];\n')),
    # a page map of the block, counted
    ('m1', arm(I7 + 'uint32_t used = (off & 0x1ffff) / 512, k;\n\n' + I7 + 'left = 0;\n' + I7 + 'for (k = 0; k < 256; k++)\n' + I7 + '\tif (k >= used)\n' + I7 + '\t\tleft++;\n')),
]
