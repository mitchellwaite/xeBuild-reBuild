# attempt 12: tidier spellings of imgWriteHdr's block number than near11's `p >> 5` / `p / 32 >> 8`, which only stops writeInitialHeader's inline by raising the caller's time. Hi and lo byte spelled independently; also pointer forms of the loop.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near11.c')
OLD = '''				s->b2lo = p / 32 >> 8;
				s->b0 = 0xff;
				*((uint8_t *)s + 1) = p >> 5;
			} else {
				s->b1lo = p / 32 >> 8;
				s->b5 = 0xff;
				*(uint8_t *)s = p >> 5;
'''
def body(hi, lo, hi2=None, lo2=None):
    return [(OLD, OLD.replace('s->b2lo = p / 32 >> 8', 's->b2lo = ' + hi).replace('s->b1lo = p / 32 >> 8', 's->b1lo = ' + (hi2 or hi)).replace('+ 1) = p >> 5', '+ 1) = ' + lo).replace('*(uint8_t *)s = p >> 5', '*(uint8_t *)s = ' + (lo2 or lo)))]
HI = ['p / 32 >> 8', '(start + b) >> 8', 'p >> 13', 'p / 8192', '(p >> 5) >> 8', '(p / 32) / 256']
LO = ['p >> 5', 'p / 32', 'start + b', '(uint8_t)(p / 32)', '(p / 32) & 0xff', '(p >> 5) & 0xff']
A = []
for i, h in enumerate(HI):
    for j, l in enumerate(LO):
        A.append(('h%dl%d' % (i, j), body(h, l)))
AXES = [A]
FLAGS = []
