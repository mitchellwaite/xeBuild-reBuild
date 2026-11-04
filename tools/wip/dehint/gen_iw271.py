# attempt 20: test spellings for partial that have no opcode heuristic (P 50) but keep `partial`'s cast alive past early opts, as `> 0` does. x partial's type. Base nopt.
# `IWB=build/iw/a20/nopt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw271.py -n 40 -t 2`
import os
BASE = os.environ.get('IWB', 'build/iw/a20/nopt.c')
H = 'if (partial > 0) {'
TE = ['partial', 'partial > 0', 'partial & 1', 'partial == 1', 'partial != 0', '(partial & 1) != 0', '(partial & 1) == 1', 'partial >> 0', 'partial * 1', '!!partial', 'partial >= 1', 'partial ^ 0', 'partial | 0', 'partial == 1 || 0', '0 != partial', 'partial - 0', '!(partial == 0)', '!(partial ^ 1) ', 'partial > 0 && 1', '(partial << 1) != 0', 'partial << 1', 'partial << 8', '(uint8_t)partial', '(_Bool)partial', '(uint16_t)partial', '(uint32_t)partial', '(uint32_t)partial > 0', '(unsigned char)partial > 0', '-partial', '~partial + 1', 'partial * 2', 'partial * 512', 'partial << 14', 'partial << 9']
A = [(('t%d' % i), [(H, 'if (%s) {' % x)]) for i, x in enumerate(TE)]
T = [('int', []), ('u32', [('\tint partial;\n', '\tuint32_t partial;\n')]), ('u8', [('\tint partial;\n', '\tuint8_t partial;\n')]), ('s16', [('\tint partial;\n', '\tint16_t partial;\n')]), ('u16', [('\tint partial;\n', '\tuint16_t partial;\n')]), ('s8', [('\tint partial;\n', '\tchar partial;\n')])]
AXES = [A, T]
