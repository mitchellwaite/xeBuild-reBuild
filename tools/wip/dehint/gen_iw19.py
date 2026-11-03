# attempt 2, on drafts/image_write.c: merge imgAdd's dead tests into fewer ifs (each merge is one trick fewer)
BASE = 'tools/wip/dehint/drafts/image_write.c'
A2 = '		if (x > first + 0x4000)\n			__asm__("");\n'
A3 = '		if (x + 0x4000 < first)\n			blocks++;\n'
A4 = '		if ((len & 0x3fff) > 0x3fff)\n			__asm__("");\n'
ALL = A2 + A3 + A4
c2 = 'x > first + 0x4000'
c3 = 'x + 0x4000 < first'
c4 = '(len & 0x3fff) > 0x3fff'
def one(cs, op, body):
    return '		if (' + (' %s ' % op).join(cs) + ')\n			' + body + ';\n'
V = [('', [])]
for op, on in (('||', 'o'), ('&&', 'a')):
    for body, bn in (('blocks++', 'b'), ('__asm__("")', 'e')):
        V.append(('m23' + on + bn, [(ALL, one([c2, c3], op, body) + A4)]))
        V.append(('m32' + on + bn, [(ALL, one([c3, c2], op, body) + A4)]))
        V.append(('m34' + on + bn, [(ALL, A2 + one([c3, c4], op, body))]))
        V.append(('m43' + on + bn, [(ALL, A2 + one([c4, c3], op, body))]))
        V.append(('m24' + on + bn, [(ALL, A3 + one([c2, c4], op, body))]))
        V.append(('m42' + on + bn, [(ALL, one([c4, c2], op, body) + A3)]))
        V.append(('m234' + on + bn, [(ALL, one([c2, c3, c4], op, body))]))
        V.append(('m423' + on + bn, [(ALL, one([c4, c2, c3], op, body))]))
AXES = [V]
