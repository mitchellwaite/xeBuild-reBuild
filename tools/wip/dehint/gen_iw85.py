# attempt 5: c13: the three remaining dead tests' conditions
import os
BASE = os.environ.get('IWB', 'build/iw/a5/c13.c')
C4 = '		if ((len & 0x3fff) > 0x3fff)\n			blocks++;\n'
A2 = '		if (x > first + 0x4000)\n			blocks += 2;\n'
A5 = '			if (x > first + 0x4000)\n				blocks++;\n'
CND = ['first + 0x4000 < x', 'x > 0x4000 + first', 'x + 0x4000 < first', 'first > x + 0x4000', 'x > first + 0x8000', 'x > first + 0x3fff', 'x >= first + 0x4000']
AXES = [
 [('', [])] + [('a%d' % i, [(A2, '		if (%s)\n			blocks += 2;\n' % c)]) for i, c in enumerate(CND)],
 [('', [])] + [('f%d' % i, [(A5, '			if (%s)\n				blocks++;\n' % c)]) for i, c in enumerate(CND)],
 [('', []),
  ('c1', [(C4, '		if (0x3fff < (len & 0x3fff))\n			blocks++;\n')]),
  ('c2', [(C4, '		if ((len & 0x3fff) >= 0x4000)\n			blocks++;\n')]),
  ('c3', [(C4, '		if ((len % 0x4000) > 0x3fff)\n			blocks++;\n')]),
  ('c4', [(C4, '		if ((len & 0x3fff) > 0x4000)\n			blocks++;\n')]),
  ('c5', [(C4, '		if (tail > 0x4000)\n			blocks++;\n')]),
  ('c6', [(C4, '		if (x > 0x3fff)\n			blocks++;\n')]),
  ('c7', [(C4, '		if (first > 0x4000)\n			blocks++;\n')]),
 ],
]
FLAGS = []
