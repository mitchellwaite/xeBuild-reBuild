"""Attempt 46: one hint on n1 (build/bd/a46/n1.c) at every `if` of loadBlFiles and defaultBl60:
__builtin_expect(cond, 0 / 1), and a hot / cold label at the head of each braced then-block.
Run with a46run.py: python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a46_hint1.py -p 95,99"""
import os, re

N1 = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'build', 'bd', 'a46', 'n1.c')
t = open(N1, newline='').read()
s = t.index('\nstatic int defaultBl60')
e = t.index('\nint loadConsoleBlFiles')


def conds(t):
    for m in re.finditer(r'\bif \(', t[s:e]):
        i = s + m.end()
        d = 1
        j = i
        while d:
            if t[j] == '(':
                d += 1
            elif t[j] == ')':
                d -= 1
            j += 1
        yield m.start() + s, i, j - 1   # if-start, cond start, cond end (the ')')


V = {}
for k, (a, i, j) in enumerate(conds(t)):
    c = t[i:j]
    if '__builtin' in c or c == '0':
        continue
    line = t.count('\n', 0, a) + 1
    for v in (0, 1):
        V['L%d_e%d' % (line, v)] = (lambda i=i, j=j, c=c, v=v: lambda x: x[:i] + '__builtin_expect(%s, %d)' % (c, v) + x[j:])()
    if t[j:j + 3] == ') {':
        ind = re.match(r'\t*', t[t.rindex('\n', 0, a) + 1:]).group(0)
        for h in ('hot', 'cold'):
            V['L%d_%s' % (line, h)] = (lambda j=j, ind=ind, h=h, line=line: lambda x: x[:j + 3] + '\n%s\th%d: __attribute__((%s));' % (ind, line, h) + x[j + 3:])()
