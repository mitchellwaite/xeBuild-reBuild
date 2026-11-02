import re, sys
NL = chr(10)
L = open(sys.argv[1]).read().split(NL)
lo, hi = 737, 797  # 0-based line range of the switch region
V = {}
pat = re.compile(r'(JMP\(|__asm__ goto \("" :::: )([\w, ]+)\)')
n = 0
for i in range(lo, hi):
    for m in pat.finditer(L[i]):
        labs = [x.strip() for x in m.group(2).split(',')]
        n += 1
        def put(name, newlabs):
            L2 = list(L)
            if newlabs:
                rep = m.group(1) + ', '.join(newlabs) + ')'
            else:
                rep = ''
            L2[i] = L[i][:m.start()] + rep + L[i][m.end():]
            V['%s_%d' % (name, n)] = NL.join(L2)
        if len(labs) > 1:
            put('rev', labs[::-1])
            for j in range(len(labs)):
                put('rm%d' % j, labs[:j] + labs[j + 1:])
        elif m.group(1) == 'JMP(':
            put('del', [])
for k, t in V.items():
    open(sys.argv[2]+'/%s.c' % k, 'w', newline=NL).write(t)
print(len(V))
