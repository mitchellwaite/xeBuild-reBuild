# gen.py: variants from the forwarder/insertion-order analysis
import os
B = {'b18': 'b18.c', 'mc9': '../s122/v/m_c9.c', 'ms5c': '../s122/v/m_s5c.c', 'rm18': '../s121/v2/rm1_8.c'}
R0 = """if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc || !a || *a == '-')"""
AG = lambda l: '({__asm__ goto("" :::: %s); 0;})' % l
A = {
 'r1': R0.replace('r5x, r3x', 'r3x, r5x'),
 'r2': R0.replace('r5x, r3x', 'r3x'),
 'r3': "if (i + 1 == argc || %s || !a || *a == '-')" % AG('r5x, r3x'),
 'r4': "if (i + 1 == argc || !a || %s || *a == '-')" % AG('r5x, r3x'),
 'r5': "if (i + 1 == argc || !a || *a == '-' || %s)" % AG('r5x, r3x'),
 'r7': """__asm__ goto("" :::: r5x, r3x); if (i + 1 == argc || !a || *a == '-')""",
 'r8': "if (i + 1 == argc || %s || !a || *a == '-')" % AG('r3x, r5x'),
 'r9': "if (i + 1 == argc || %s || !a || *a == '-')" % AG('r3x'),
 'r10': R0.replace('r5x, r3x', 'r3x') + '@MODE',
 'r11': "if (%s || i + 1 == argc || !a || *a == '-')" % AG('r3x, r5x, r3x'.replace(', r3x', '', 1)),
}
MODE0 = "if (mode) { r5x: client_usage(5, argv[i]); }"
os.makedirs('v', exist_ok=True)
n = 0
for bn, bf in B.items():
    s = open(bf).read(); assert R0 in s and MODE0 in s
    for an, a in A.items():
        t = s
        if a.endswith('@MODE'):
            a = a[:-5]; t = t.replace(MODE0, "if (mode || %s) { r5x: client_usage(5, argv[i]); }" % AG('r5x'), 1)
        t = t.replace(R0, a, 1)
        open('v/%s_%s.c' % (bn, an), 'w', newline='\n').write(t); n += 1
print(n)
