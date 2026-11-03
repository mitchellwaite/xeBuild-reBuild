# attempt 3: on a near file (one compare off in writeFsTable's big copy): forms of writeFsTable's length argument and locals, which change how many
# names are released before ivopts (the compare flips when `end` and the iv come from different runs of the free list).
import os
BASE = os.environ.get('IWB', 'build/iw/a3/v2.c')
FOCUS = ['_writeFsTable']
_t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', BASE), newline='').read().replace('\r\n', '\n')
_big = '	imgAdd(off, buf, 0x400 * i, 0x2c, 0x1ffe, 0);\n' if '0x400 * i, 0x2c' in _t else '	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n'
_sm = '	imgAdd(off, buf, 0x400 * i, 0x30, 0x1ffd, 0);\n' if '0x400 * i, 0x30' in _t else '	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n'
BIG = lambda l: '	imgAdd(off, buf, %s, 0x2c, 0x1ffe, 0);\n' % l
SM = lambda l: '	imgAdd(off, buf, %s, 0x30, 0x1ffd, 0);\n' % l
LENS = ['i * 0x400', '0x400 * i', '0x4000', 'p - buf', '(uint32_t)(p - buf)', 'i << 10', '16 * 0x400', '0x200 * 32', 'i * 0x200 * 2', 'i * 2 * 0x200', 'n', 'sizeof(fsFiles) * 2']
V = '	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n'
LOG = '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n'
AXES = [
 [('b' + str(k), [(_big, BIG(l))]) for k, l in enumerate(LENS)],
 [('s' + str(k), [(_sm, SM(l))]) for k, l in enumerate(LENS)],
 [('n0', [(V, V + '	uint32_t n;\n'), (LOG, '	n = i * 0x400;\n' + LOG)]),
  ('n1', [(V, V + '	uint32_t n;\n'), (LOG, LOG + '	n = i * 0x400;\n')]),
  ('n2', [(V, V + '	uint32_t n;\n'), (LOG, '	n = p - buf;\n' + LOG)]),
  ('n3', [(V, V + '	uint32_t n;\n'), (LOG, LOG + '	n = 0x4000;\n')]),
 ],
]
