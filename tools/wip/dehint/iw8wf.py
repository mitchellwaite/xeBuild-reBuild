"""python tools/wip/dehint/iw8wf.py <seconds> <seed> <base.c> [--workers N] [--mode dead|opt|both|any] [--render json out.c]

Attempt 8: random search over STRUCTURAL forms of writeFsTable (static helpers that inline, other loop shapes, named locals),
which attempt 7's iw7wf.py didn't try.  Only writeFsTable's body and new static helpers change, so imgAdd and the clones stay.
--mode: which trick(s) to remove:
  dead  dead test gone, attribute kept       (target 5 tricks)
  opt   attribute gone, dead test kept       (target 5 tricks)
  both  both gone                            (target 4 tricks)
Log build/iw/a8/wf8_<seed>.log; IDENTICAL states are written to build/iw/a8/wf8hit_<seed>_<n>.c."""
import json, os, random, re, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib

A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
PROTO = 'void writeFsTable(uint32_t off)'

HEADS = [
 '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n',
 '	blk = off >> 14;\n	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n			blk = off >> 14;\n		}\n	}\n',
 '	blk = off >> 14;\n	if (xb.bigBlock && off % 0x20000) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n',
 '	blk = off >> 14;\n	if (xb.bigBlock) {\n		uint32_t a = (off + 0x20000) & ~0x1ffff;\n		if (off & 0x1ffff) {\n			off = a;\n			blk = a >> 14;\n		}\n	}\n',
 '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff))\n		blk = (off = (off + 0x20000) & ~0x1ffff) >> 14;\n',
 '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off += 0x20000;\n		off &= ~0x1ffff;\n		blk = off >> 14;\n	}\n',
 '	blk = off >> 14;\n	if (xb.bigBlock && (blk & 7)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n',
 '	HELPER_ALIGN',
]
STORES = [
 '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n',
 '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n',
 '	*(fsTable + blk - xb.fsStart) = SWAP16_IMAGE_WRITE(0x1ffd);\n',
 '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n',
 '	{\n		uint32_t first = blk - xb.fsStart;\n\n		fsTable[first] = SWAP16_IMAGE_WRITE(0x1ffd);\n	}\n',
]
LOOPS = [
 # (needs i after?, text)
 '	buf = malloc(0x4000);\n	p = buf;\n	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n	}\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x400;\n	}\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	for (i = 0; i < 16; i++, p += 0x400) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n	}\n',
 '	buf = malloc(0x4000);\n	for (i = 0; i < 16; i++) {\n		memcpy(buf + i * 0x400, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(buf + i * 0x400 + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n	}\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	for (i = 0; i < 16; i++) {\n		uint32_t o = i * 0x200;\n\n		memcpy(p, (uint8_t *)fsTable + o, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + o, 0x200);\n		p += 0x200;\n	}\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	{\n		uint8_t *t = (uint8_t *)fsTable, *f = (uint8_t *)fsFiles;\n\n		for (i = 0; i < 16; i++) {\n			memcpy(p, t, 0x200);\n			p += 0x200;\n			t += 0x200;\n			memcpy(p, f, 0x200);\n			p += 0x200;\n			f += 0x200;\n		}\n	}\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	i = 0;\n	while (i < 16) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n		i++;\n	}\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	i = 0;\n	do {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n	} while (++i < 16);\n',
 '	buf = malloc(0x4000);\n	p = buf;\n	for (i = 0; i < 0x2000; i += 0x200) {\n		memcpy(p, (uint8_t *)fsTable + i, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i, 0x200);\n		p += 0x200;\n	}\n	i = 16;\n',
 '	HELPER_COPY',
 '	HELPER_BUF',
]
LOGS = [
 '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n',
 '	log_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, 0x4000 + off);\n',
]
LENS = ['i * 0x400', '0x400 * i', '0x4000', 'p - buf', 'i << 10', '16 * 0x400', 'i * 2 * 0x200', 'len']
TAILS = [
 '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n',
 '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n	setBeU16(0, (uint8_t *)&xb.fsReserved);\n	free(buf);\n',
]


def calls(form, b, s, helper):
    B = '	imgAdd(off, buf, %s, 0x2c, 0x1ffe, 0);\n' % b
    S = '	imgAdd(off, buf, %s, 0x30, 0x1ffd, 0);\n' % s
    if helper:
        return '	addFsTable(off, buf);\n'
    return ['	if (!xb.bigBlock)\n		goto small;\n' + B + '	goto done;\nsmall:\n' + S + 'done:\n',
            '	if (xb.bigBlock)\n	' + B + '	else\n	' + S,
            '	if (!xb.bigBlock)\n	' + S + '	else\n	' + B,
            '	if (xb.bigBlock)\n		goto big;\n' + S + '	goto done;\nbig:\n' + B + 'done:\n',
            '	if (xb.bigBlock) {\n	' + B + '		goto done;\n	}\n' + S + 'done:\n'][form]


DEAD = '	if ((off & 0x3fff) > 0x3fff)\n		off += 0x4000;\n'


def render_fn(st, needdead):
    helpers = ''
    decl = '	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n'
    h = HEADS[st['head']]
    if 'HELPER_ALIGN' in h:
        helpers += ['static uint32_t alignFsTable(uint32_t off)\n{\n	if (xb.bigBlock && (off & 0x1ffff))\n		return (off + 0x20000) & ~0x1ffff;\n	return off;\n}\n\n',
                    'static uint32_t alignFsTable(uint32_t off)\n{\n	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	return off;\n}\n\n'][st['ha']]
        h = '	off = alignFsTable(off);\n	blk = off >> 14;\n'
    l = LOOPS[st['loop']]
    lb, ls = LENS[st['lb']], LENS[st['ls']]
    if 'HELPER_COPY' in l:
        helpers += ['static void copyFsTable(uint8_t *p)\n{\n	int i;\n\n	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n	}\n}\n\n',
                    'static int copyFsTable(uint8_t *p)\n{\n	int i;\n\n	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n	}\n	return i * 0x400;\n}\n\n'][st['hc']]
        if st['hc'] == 0:
            l = '	buf = malloc(0x4000);\n	copyFsTable(buf);\n'
            if lb not in ('0x4000', '16 * 0x400'):
                lb = '0x4000'
            if ls not in ('0x4000', '16 * 0x400'):
                ls = '0x4000'
        else:
            l = '	buf = malloc(0x4000);\n	i = copyFsTable(buf);\n'
            lb = ls = 'i'
    elif 'HELPER_BUF' in l:
        helpers += 'static uint8_t *fsTableBuffer(void)\n{\n	uint8_t *buf = malloc(0x4000), *p = buf;\n	int i;\n\n	for (i = 0; i < 16; i++) {\n		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n	}\n	return buf;\n}\n\n'
        l = '	buf = fsTableBuffer();\n'
        lb = ls = '0x4000'
    pre = ''
    if lb == 'len' or ls == 'len':
        decl += '	uint32_t len;\n'
        pre = '	len = %s;\n' % ('i * 0x400' if 'HELPER' not in LOOPS[st['loop']] else '0x4000')
    c = calls(st['cf'], lb, ls, st['hadd'])
    if st['hadd']:
        L = lb if lb not in ('len', 'i', 'p - buf') and 'i' not in lb else '0x4000'
        helpers += calls(st['hcf'] if st['hcf'] < 5 else 0, L, L, False).join(['static void addFsTable(uint32_t off, uint8_t *buf)\n{\n', '}\n\n'])
    log = LOGS[st['log']]
    tail = TAILS[st['tail']]
    if st['ptail']:
        tail = '	setBeU16(0, (uint8_t *)&xb.fsReserved);\n' if False else tail
    d = DEAD if needdead else ''
    s = STORES[st['store']]
    body = {0: h + s + l + log + d + pre + c + tail,
            1: h + s + l + pre + log + d + c + tail,
            2: h + l + s + log + d + pre + c + tail}[st['order']]
    if st['scope']:
        decl = decl.replace('	uint8_t *buf, *p;\n', '	uint8_t *p, *buf;\n') if st['scope'] == 1 else decl.replace('	uint32_t blk;\n	int i;\n', '	int i;\n	uint32_t blk;\n')
    return helpers, decl + '\n' + body


def main():
    args = sys.argv[1:]

    def opt(name, d):
        if name in args:
            i = args.index(name)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return d
    W = int(opt('--workers', 3))
    MODE = opt('--mode', 'dead')
    rend = None
    if '--render' in args:
        i = args.index('--render')
        rend = (json.loads(args[i + 1]), args[i + 2])
        del args[i:i + 3]
    secs, seed = int(args[0]), int(args[1])
    base = open(args[2], newline='').read().replace('\r\n', '\n')
    m = re.search(r'(__attribute__\(\(optimize\("no-tree-scev-cprop"\)\)\) )?void writeFsTable\(uint32_t off\)\n\{\n.*?\n\}\n', base, re.S)
    pre, post = base[:m.start()], base[m.end():]

    def render(st):
        helpers, body = render_fn(st, st['dead'])
        return pre + helpers + (A + '(uint32_t off)' if st['attr'] else PROTO) + '\n{\n' + body + '}\n' + post

    if rend:
        open(rend[1], 'w', newline='\n').write(render(rend[0]))
        print(iwlib.fmt(iwlib.score_text(render(rend[0]), [])))
        return
    rnd = random.Random(seed)
    AX = {'head': len(HEADS), 'ha': 2, 'hc': 2, 'store': len(STORES), 'loop': len(LOOPS), 'log': len(LOGS), 'tail': len(TAILS),
          'cf': 5, 'hcf': 5, 'lb': len(LENS), 'ls': len(LENS), 'order': 3, 'scope': 3}

    def sample():
        st = {}
        for k, n in AX.items():
            st[k] = rnd.randrange(n) if rnd.random() < 0.4 else 0
        st['ls'] = st['lb'] if rnd.random() < 0.7 else st['ls']
        st['hadd'] = rnd.random() < 0.2
        st['ptail'] = 0
        mode = MODE if MODE != 'any' else rnd.choice(['dead', 'opt', 'both'])
        st['dead'] = mode == 'opt'
        st['attr'] = mode == 'dead'
        st['mode'] = mode
        return st
    os.makedirs(os.path.join(iwlib.BUILD, 'a8'), exist_ok=True)
    logf = open(os.path.join(iwlib.BUILD, 'a8', 'wf8_%d.log' % seed), 'a', newline='\n')
    best = {}
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
                    p = os.path.join(iwlib.BUILD, 'a8', 'wf8hit_%d_%d.c' % (seed, hits))
                    open(p, 'w', newline='\n').write(render(s))
                    print('IDENTICAL', p, json.dumps(s), file=logf, flush=True)
                elif 'total' in r and r['total'] < best.get(s['mode'], 10 ** 9):
                    best[s['mode']] = r['total']
                    print(seen, 'best', s['mode'], r['total'], json.dumps(s), r['per'], file=logf, flush=True)
    print('end', seen, 'hits', hits, 'best', best, file=logf, flush=True)


main()
