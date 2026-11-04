# attempt 14: real values in imgAdd's big/small arms (FsPageCount, FsSize, pages, left) x writeFsTable's natural spellings, on near13, total lines.
import os
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_near13.c')
PG = '''						pages = len / 512;
						if (len % 512)
							pages++;
						left = pages;
						if (left & 3)
							left = (left + 4) & ~3;
						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;
						s[5] = 1;
						s[8] = len >> 8;
						s[7] = len;
'''
def v(pg, cnt, tail):
    return pg + cnt + tail
TAIL = '						s[5] = 1;\n						s[8] = len >> 8;\n						s[7] = len;\n'
PGS = {
 '': '						pages = len / 512;\n						if (len % 512)\n							pages++;\n',
 'p1': '						pages = len % 512 ? len / 512 + 1 : len / 512;\n',
 'p2': '						pages = len >> 9;\n						if (len & 511)\n							pages++;\n',
 'p3': '						if (len % 512)\n							pages = len / 512 + 1;\n						else\n							pages = len / 512;\n',
 'p4': '						pages = (len + 511) / 512;\n',
}
CNT = {
 '': '						left = pages;\n						if (left & 3)\n							left = (left + 4) & ~3;\n						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;\n',
 # free pages in the 128K block, minus what this file takes
 'c1': '						left = pages;\n						if (left & 3)\n							left = (left + 4) & ~3;\n						left = ((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left;\n						s[9] = left >> 2;\n',
 'c2': '						if (pages & 3)\n							pages = (pages + 4) & ~3;\n						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - pages) >> 2;\n',
 'c3': '						left = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n						if (pages & 3)\n							pages = (pages + 4) & ~3;\n						s[9] = (left - pages) >> 2;\n',
 'c4': '						if (off & 0x1ffff)\n							left = 256 - (off & 0x1ffff) / 512;\n						else\n							left = 256;\n						if (pages & 3)\n							pages = (pages + 4) & ~3;\n						s[9] = (left - pages) >> 2;\n',
 'c5': '						left = pages;\n						if (left & 3)\n							left = (left + 4) & ~3;\n						pages = (off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256;\n						s[9] = (pages - left) >> 2;\n',
 'c6': '						left = pages;\n						if (left & 3)\n							left = (left + 4) & ~3;\n						if (off & 0x1ffff)\n							s[9] = (256 - (off & 0x1ffff) / 512 - left) >> 2;\n						else\n							s[9] = (256 - left) >> 2;\n',
 'c7': '						left = 256 - p0;\n						if (pages & 3)\n							pages = (pages + 4) & ~3;\n						s[9] = (left - pages) >> 2;\n',
}
TAILS = {
 '': TAIL,
 't1': '						s[5] = 1;\n						s[7] = len;\n						s[8] = len >> 8;\n',
 't2': '						s[8] = len >> 8;\n						s[7] = len;\n						s[5] = 1;\n',
 't3': '						s[7] = len;\n						s[8] = len >> 8;\n						s[5] = 1;\n',
}
def combo():
    out = []
    for a, pa in PGS.items():
        for b, cb in CNT.items():
            if b == 'c7':
                continue
            for c, tc in TAILS.items():
                out.append(('+'.join(x for x in (a, b, c) if x), [(PG, pa + cb + tc)]))
    return out
ST = '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
TL = '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n'
AXES = [combo(),
 [('', []), ('st0', [(ST, '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n')])],
 [('', []), ('t0', [(TL, '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n')])],
]
FLAGS = []
