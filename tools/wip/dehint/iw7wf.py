"""python tools/wip/dehint/iw7wf.py <seconds> <seed> <base.c,base2.c,...> [--workers N] [--dead MAX] [--noopt P]

Attempt 7: random search over writeFsTable's own forms only (imgAdd and its clones stay as they are, so only writeFsTable can
change), with up to MAX dead tests inside writeFsTable.  Plain -O3.  Bases must already match everywhere else.
Log build/iw/a7/wf_<seed>.log; each IDENTICAL state is written to build/iw/a7/wfhit_<seed>_<n>.c with its label."""
import os, random, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib


def opt(args, name, d):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return d


A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
HEAD = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
STORE = '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n'
BUF = '	buf = malloc(0x4000);\n	p = buf;\n'
LOOPA = '		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n'
LOG = '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n'
TAIL = '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n'
CALLS = '	if (!xb.bigBlock)\n		goto small;\n	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	goto done;\nsmall:\n	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\ndone:\n'
LOOPH = '	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable'
LENS = ['i * 0x400', '0x400 * i', '0x4000', 'p - buf', 'i << 10', '16 * 0x400', '0x200 * 32', 'i * 2 * 0x200']


def calls(form, b, s):
    B = '	imgAdd(off, buf, %s, 0x2c, 0x1ffe, 0);\n' % b
    S = '	imgAdd(off, buf, %s, 0x30, 0x1ffd, 0);\n' % s
    return ['	if (!xb.bigBlock)\n		goto small;\n' + B + '	goto done;\nsmall:\n' + S + 'done:\n',
            '	if (xb.bigBlock)\n	' + B + '	else\n	' + S,
            '	if (!xb.bigBlock)\n	' + S + '	else\n	' + B,
            '	if (xb.bigBlock)\n		goto big;\n' + S + '	goto done;\nbig:\n' + B + 'done:\n'][form]


AXES = {
 'head': [None,
  '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n',
  '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	} else\n		blk = off >> 14;\n',
  '	blk = off >> 14;\n	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n			blk = off >> 14;\n		}\n	}\n',
  '	blk = off >> 14;\n	if (xb.bigBlock && off % 0x20000) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n',
  '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		blk = (off + 0x20000) >> 17 << 3;\n		off = blk << 14;\n	}\n',
 ],
 'store': [None, '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n',
           '	*(fsTable + blk - xb.fsStart) = SWAP16_IMAGE_WRITE(0x1ffd);\n'],
 'buf': [None, '	p = buf = malloc(0x4000);\n', '	buf = malloc(16 * 0x400);\n	p = buf;\n'],
 'loop': [None,
  '		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x400;\n',
  '		memcpy(p, &((uint8_t *)fsTable)[i * 0x200], 0x200);\n		p += 0x200;\n		memcpy(p, &((uint8_t *)fsFiles)[i * 0x200], 0x200);\n		p += 0x200;\n',
  '		uint32_t o = i * 0x200;\n		memcpy(p, (uint8_t *)fsTable + o, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + o, 0x200);\n		p += 0x200;\n',
  '		memcpy(buf + i * 0x400, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(buf + i * 0x400 + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n',
  '		memcpy(p, fsTable + i * 0x100, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n',
 ],
 'log': [None, '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, 0x4000 + off);\n'],
 'tail': [None, '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n'],
}
POS = ['	buf = malloc(0x4000);\n', LOOPH, LOG, CALLS, TAIL, STORE]
CONDS = ['(off & 0x3fff) > 0x3fff', '(blk & 0xff) > 0xff', '(off >> 14) > 0x3ffff', 'i > 16', 'off > 0xffffffff - 0', '(blk >> 18) > 0x3fff']
BODIES = ['blk++;', 'off++;', 'i++;', 'off += 0x4000;', 'blk += 2;']


def main():
    args = sys.argv[1:]
    W = int(opt(args, '--workers', 3))
    DEAD = int(opt(args, '--dead', 0))
    NOOPT = float(opt(args, '--noopt', 0.3))
    secs, seed = int(args[0]), int(args[1])
    bases = [open(b, newline='').read().replace('\r\n', '\n') for b in args[2].split(',')]
    rnd = random.Random(seed)
    logf = open(os.path.join(iwlib.BUILD, 'a7', 'wf_%d.log' % seed), 'a', newline='\n')

    def sample():
        bi = rnd.randrange(len(bases))
        st = {'base': bi}
        for k, v in AXES.items():
            st[k] = rnd.randrange(len(v)) if rnd.random() < 0.5 else 0
        st['cf'] = rnd.randrange(4) if rnd.random() < 0.3 else 0
        st['lb'] = rnd.randrange(len(LENS)) if rnd.random() < 0.3 else 0
        st['ls'] = rnd.randrange(len(LENS)) if rnd.random() < 0.3 else st['lb']
        st['noopt'] = rnd.random() < NOOPT
        d = rnd.randint(0, DEAD)
        st['dead'] = [(rnd.randrange(len(POS)), rnd.randrange(len(CONDS)), rnd.randrange(len(BODIES))) for _ in range(d)]
        return st

    def render(st):
        t = bases[st['base']]
        if st['noopt']:
            t = t.replace(A, 'void writeFsTable')
        for pos, c, b in st['dead']:
            if pos == 3:
                t = t.replace(CALLS, '	if (%s)\n		%s\n' % (CONDS[c], BODIES[b]) + CALLS)
            else:
                ps = POS[pos]
                t = t.replace(ps, '	if (%s)\n		%s\n' % (CONDS[c], BODIES[b]) + ps)
        for k, (old, v) in {'head': (HEAD, AXES['head']), 'store': (STORE, AXES['store']), 'buf': (BUF, AXES['buf']),
                            'loop': (LOOPA, AXES['loop']), 'log': (LOG, AXES['log']), 'tail': (TAIL, AXES['tail'])}.items():
            if st[k]:
                t = t.replace(old, v[st[k]])
        t = t.replace(CALLS, calls(st['cf'], LENS[st['lb']], LENS[st['ls']]))
        return t

    best = 10 ** 9
    t0 = time.time()
    seen = hits = 0
    with ThreadPoolExecutor(W) as ex:
        while time.time() - t0 < secs:
            sts = [sample() for _ in range(W * 2)]
            res = list(ex.map(lambda s: (s, iwlib.score_text(render(s), [])), sts))
            seen += len(sts)
            for s, r in res:
                if r.get('identical'):
                    hits += 1
                    p = os.path.join(iwlib.BUILD, 'a7', 'wfhit_%d_%d.c' % (seed, hits))
                    open(p, 'w', newline='\n').write(render(s))
                    print('IDENTICAL', p, s, file=logf, flush=True)
                elif 'total' in r and r['total'] < best:
                    best = r['total']
                    print(seen, 'best', best, s, r['per'], file=logf, flush=True)
    print('end', seen, 'hits', hits, 'best', best, file=logf, flush=True)


main()
