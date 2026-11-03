# attempt 4: on c4a6 (a2 and a5 the only dead tests in imgAdd): a2's condition, body and place, to fix imgAdd's `_1 != ivtmp` compare with one test instead of gen_iw57's two
import os
BASE = os.environ.get('IWB', 'build/iw/a4/c4a6.c')
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
T = "		t = type - '1';\n"
NP = '		if (len % 512)\n			npages = (len + 512) / 512;\n'
P0 = '		p = 0;\n'
FORP = '		for (end = p + npages; p < end; p++) {\n'
LB = '#undef BLK\n'
C = {'g': 'x > first + 0x4000', 'G': 'first + 0x4000 < x', 'd': 'x > 0x4000 + first', 's': 'x - first > 0x4000', 'h': 'x + 0x4000 > first + 0x8000', 'e': 'x > 0x3fff && first > 0x3fff'}
B = {'b2': 'blocks += 2;', 'b1': 'blocks++;', 'b3': 'blocks += 3;', 'bb': '{ blocks++; blocks++; }', 'bx': 'blocks += x;', 'bf': 'blocks += first;', 'bm': 'blocks--;', 'bl': 'blocks = len;', 'st': 'start++;', 'sb': '{ start++; blocks++; }', 'b0': 'blocks = 0;'}
ax = []
for cn, c in C.items():
    for bn, b in B.items():
        s = f'		if ({c})\n			{b}\n'
        ax.append((cn + bn, [(A2, s)]))
        ax.append((cn + bn + '@t', [(A2, ''), (T, s + T)]))
        ax.append((cn + bn + '@n', [(A2, ''), (NP, s + NP)]))
        ax.append((cn + bn + '@p', [(A2, ''), (P0, s + P0)]))
        ax.append((cn + bn + '@f', [(A2, ''), (FORP, s + FORP)]))
AXES = [ax]
