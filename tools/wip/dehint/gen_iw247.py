# attempt 17: on build/iw/a17/s4t.c (writeFsTable clean, no dead test; imgAdd's and constprop.1's compare left): spellings of left, rounding, s[9], FS chain, each worth a few names to PRE.
import os
BASE = os.environ.get('IWB', 'build/iw/a17/s4t.c')
LEFT = '						left = bo ? 256 - bo / 512 : 256;\n'
RD = '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n'
S9 = '						s[9] = (left - pages) >> 2;\n'
SA = '				pages = len % 512 ? len / 512 + 1 : len / 512;\n				((struct sps'
FS0 = 'fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);'
A = [[('', []),
  ('b1', [(LEFT, '						left = bo ? 256 - (int)(bo / 512) : 256;\n')]),
  ('b2', [(LEFT, '						left = bo ? 256 - (bo >> 9) : 256;\n')]),
  ('b3', [(LEFT, '						left = 256 - (bo ? bo / 512 : 0);\n')]),
  ('b4', [(LEFT, '						left = bo / 512;\n						if (bo)\n							left = 256 - left;\n						else\n							left = 256;\n')]),
  ('b5', [(LEFT, '						left = 256;\n						if (bo)\n							left -= bo / 512;\n')]),
 ],
 [('', []),
  ('r1', [(RD, '						pages = pages & 3 ? (pages + 4) & ~3 : pages;\n')]),
  ('r2', [(RD, '						if (pages & 3) {\n							pages &= ~3;\n							pages += 4;\n						}\n')]),
  ('r3', [(RD, '						if (pages % 4)\n							pages = (pages + 4) & ~3;\n')]),
 ],
 [('', []),
  ('s1', [(S9, '						left -= pages;\n						s[9] = left >> 2;\n')]),
  ('s2', [(S9, '						s[9] = (left - (int)pages) >> 2;\n')]),
  ('s3', [(S9, '						pages = left - pages;\n						s[9] = pages >> 2;\n')]),
  ('s4', [(S9, '						s[9] = (uint32_t)(left - pages) >> 2;\n')]),
  ('s5', [(S9, '						s[9] = (uint8_t)((left - pages) >> 2);\n')]),
  ('s6', [(S9, '						s[9] = (left - pages) / 4;\n')]),
 ],
 [('', []),
  ('a1', [(SA, '				pages = len / 512;\n				if (len % 512)\n					pages++;\n				((struct sps')]),
  ('a2', [(SA, '				if (len % 512)\n					pages = len / 512 + 1;\n				else\n					pages = len / 512;\n				((struct sps')]),
 ],
]
AXES = A
FLAGS = []
