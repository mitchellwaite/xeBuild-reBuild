"""python tools/wip/dehint/iw3anneal.py <seconds> <seed> <fixed tricks, comma separated or -> [--workers N] [--free a,b,c] [--pen N]

Attempt 3's search on src/image_write.c (IW3BASE= other base): iwanneal's shapes (natural source alternatives) plus the
dead tests' own forms below.  `fixed` tricks (names in iw3.T) stay removed; --free names may flip on and off.
Objective: diff lines + PEN * tricks kept among fixed+free.  Each IDENTICAL variant with the fewest tricks so far goes to
build/iw/a3/an3_<kept>_<seed>.c, log build/iw/a3/an3_<seed>.log."""
import json, os, random, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
sys.argv = ['x']
import iwanneal as A, iwlib, iw3


def opt(name, d):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return d


WORKERS = int(opt('--workers', 4))
FREE = [x for x in opt('--free', '').split(',') if x]
PEN = int(opt('--pen', 8))
secs, seed, fixed = int(args[0]), int(args[1]), [x for x in args[2].split(',') if x and x != '-']
R = lambda old, *news: (old, list(news))
SH = dict(A.SHAPES)
SH.update({
    'a1body': R('	if (x > first + 0x4000)\n		blocks += 2;\n', '	if (x > first + 0x4000)\n		blocks++;\n', '	if (first + 0x4000 < x)\n		blocks += 2;\n'),
    'a5body': R('			if (x > first + 0x4000)\n				blocks++;\n', '			if (x > first + 0x4000)\n				blocks += 2;\n', '			if (first + 0x4000 < x)\n				blocks++;\n'),
    'a6body': R('		if (x + 0x4000 < first)\n			start++;\n', '		if (first > x + 0x4000)\n			start++;\n', '		if (x + 0x4000 < first)\n			blocks++;\n'),
    'a2body': R('		if (x > first + 0x4000)\n			__asm__("");\n', '		if (first + 0x4000 < x)\n			__asm__("");\n',
                 '		if (x > first + 0x4000)\n			blocks++;\n', '		if (x > first + 0x4000)\n			blocks += 2;\n',
                 '		if (x + 0x4000 < first)\n			__asm__("");\n', '		if (x + 0x4000 < first)\n			blocks++;\n',
                 '		if (first + 0x4000 < x)\n			blocks++;\n', '		if (x > first + 0x4000)\n			start++;\n'),
    'npg': R('''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
''', '''		npages = len / 512;
		if (len % 512)
			npages = (len + 512) / 512;
''', '''		npages = len % 512 ? (len + 512) / 512 : len / 512;
'''),
    'pdecl': R('	int partial;\n', '	uint8_t partial;\n', '	uint32_t partial;\n'),
    'nx': R('		if (next == 0xffff) {\n			fsTable[start + blocks', '		if (next == 0xffff) {\n			fsTable[blocks + start'),
    'mset2': R('	if (pad == 1) if (tail)\n', '	if (pad == 1 && tail != 0)\n', '	if (pad == 1) if (tail != 0)\n'),
    'off': R('	uint32_t off = imgSizeAligned();\n	uint32_t start, b, p, pages, npages, first, rem, tail, blocks;\n',
             '	uint32_t start, b, p, pages, npages, first, rem, tail, blocks;\n	uint32_t off = imgSizeAligned();\n'),
    'fend': R('	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n', '	uint32_t lim = (xb.fsEnd - 1) * 0x4000;\n	uint32_t end = off + len;\n'),
    'lentest': R('	if ((len & 0x3fff) > 0x3fff)\n		len++;\n', '	if (end < off && (len & 0x3fff) > 0x3fff)\n		len++;\n', '	if ((end & 0x3fff) > 0x3fff)\n		len++;\n'),
    'abtest': R('		if ((len & 0x3fff) > 0x3fff)\n			abort();\n', '		if ((end & 0x3fff) > 0x3fff)\n			abort();\n', '		if ((off & 0x3fff) > 0x3fff)\n			abort();\n'),
    'enda': R('			for (end = p + npages; p < end; p++) {\n', '			end = p + npages;\n			for (; p < end; p++) {\n'),
})
_HEAD = '	blk = off >> 14;\n	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	}\n'
SH.update({  # writeFsTable forms (each compare in its copies moves with how many names go through the free list)
    'wh': R(_HEAD, '	if (xb.bigBlock && (off & 0x1ffff))\n		off = (off + 0x20000) & ~0x1ffff;\n	blk = off >> 14;\n',
            '	if (xb.bigBlock && (off & 0x1ffff)) {\n		off = (off + 0x20000) & ~0x1ffff;\n		blk = off >> 14;\n	} else\n		blk = off >> 14;\n',
            '	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n		}\n	}\n	blk = off >> 14;\n',
            '	blk = off >> 14;\n	if (xb.bigBlock) {\n		if (off & 0x1ffff) {\n			off = (off + 0x20000) & ~0x1ffff;\n			blk = off >> 14;\n		}\n	}\n'),
    'wst': R('	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'),
    'wst0': R('	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	fsTable[-xb.fsStart + blk] = SWAP16_IMAGE_WRITE(0x1ffd);\n'),
    'wbuf': R('	buf = malloc(0x4000);\n	p = buf;\n', '	p = buf = malloc(0x4000);\n'),
    'wl': R('		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x200;\n',
            '		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);\n		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);\n		p += 0x400;\n',
            '		memcpy(p, &((uint8_t *)fsTable)[i * 0x200], 0x200);\n		p += 0x200;\n		memcpy(p, &((uint8_t *)fsFiles)[i * 0x200], 0x200);\n		p += 0x200;\n',
            '		uint32_t o = i * 0x200;\n		memcpy(p, (uint8_t *)fsTable + o, 0x200);\n		p += 0x200;\n		memcpy(p, (uint8_t *)fsFiles + o, 0x200);\n		p += 0x200;\n'),
    'wlog': R('(end 0x%x)...", off, off + 0x4000);\n', '(end 0x%x)...", off, 0x4000 + off);\n'),
    'wt': R('	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n'),
    'wt0': R('	setBeU16(blk, (uint8_t *)&xb.fsBlock);\n', '	setBeU16(off >> 14, (uint8_t *)&xb.fsBlock);\n'),
    'wlen': R('	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n', '	imgAdd(off, buf, 0x4000, 0x30, 0x1ffd, 0);\n', '	imgAdd(off, buf, p - buf, 0x30, 0x1ffd, 0);\n'),
    'wlen2': R('	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n', '	imgAdd(off, buf, 0x4000, 0x2c, 0x1ffe, 0);\n', '	imgAdd(off, buf, p - buf, 0x2c, 0x1ffe, 0);\n'),
})
SH = {k: v for k, v in SH.items()}
BASE = iw3.base()
SH = {k: v for k, v in SH.items() if k in ('enda',) or v[0] in BASE or k in ('test',)}
TRICKS = list(dict.fromkeys(fixed + FREE))


def render(st):
    if st.get('lentest') or st.get('abtest'):
        st = dict(st, fend=1)
    t = iw3.apply(BASE, [n for n in TRICKS if st.get(n)])
    for k, (old, news) in SH.items():
        v = st.get(k, 0)
        if v and old in t:
            t = t.replace(old, news[v - 1])
    return t


def kept(st):
    return sum(1 for n in TRICKS if not st.get(n))


def score(st):
    names = [n for n in TRICKS if st.get(n)]
    r = iwlib.score_text(render(st), iw3.flags_for(names))
    if 'compile' in r:
        return 10 ** 7, r
    return r['total'] + PEN * kept(st), r


def main():
    rnd = random.Random(seed)
    outd = os.path.join(iwlib.BUILD, 'a3')
    log = open(os.path.join(outd, 'an3_%d.log' % seed), 'a', newline='\n')
    print('shapes', len(SH), sorted(SH), file=log, flush=True)
    st = {k: True for k in fixed}
    cur, (curv, r) = st, score(st)
    print('start', curv, iwlib.fmt(r)[:200], file=log, flush=True)
    gbest, gval = cur, curv
    keys = FREE + list(SH)
    best_kept = 99
    t0 = time.time()
    seen = 0
    with ThreadPoolExecutor(WORKERS) as ex:
        while time.time() - t0 < secs:
            cands = []
            for _ in range(WORKERS * 2):
                s = dict(cur)
                for key in rnd.sample(keys, rnd.choice((1, 1, 2, 2, 3))):
                    if key in FREE:
                        s[key] = not s.get(key)
                    else:
                        n = len(SH[key][1]) + 1
                        s[key] = (s.get(key, 0) + rnd.randrange(1, n)) % n
                cands.append(s)
            res = list(ex.map(lambda s: (s, score(s)), cands))
            seen += len(cands)
            for s, (v, r) in res:
                if r.get('identical') and kept(s) < best_kept:
                    best_kept = kept(s)
                    open(os.path.join(outd, 'an3_%d_%d.c' % (best_kept, seed)), 'w', newline='\n').write(render(s))
                    print('IDENTICAL kept', best_kept, json.dumps({k: x for k, x in s.items() if x}), file=log, flush=True)
            s, (v, r) = min(res, key=lambda x: x[1][0])
            if v < gval:
                gbest, gval = s, v
                print(seen, 'best', v, 'kept', kept(s), json.dumps({k: x for k, x in s.items() if x}), iwlib.fmt(r)[:200], file=log, flush=True)
            if v <= curv or rnd.random() < 2.718 ** (-(v - curv) / 6.0):
                cur, curv = s, v
            if rnd.random() < 0.02:
                cur, curv = gbest, gval
    print('end', seen, gval, file=log, flush=True)


# `iw3anneal.py 0 0 <tricks in the state> --render '<state json from the log>' out.c` writes that state's source
if len(args) > 3 and args[3] == '--render':
    open(args[5], 'w', newline='\n').write(render(json.loads(args[4])))
    print(iwlib.fmt(score(json.loads(args[4]))[1]))
elif len(args) > 3 and args[3] == '--probe':
    # `iw3anneal.py 0 0 <tricks> --probe '<state json>'`: every single shape change from that state: lines and writeFsTable's final iv compares (SSA versions)
    import re, subprocess, tempfile
    from concurrent.futures import ThreadPoolExecutor as TP
    st0 = json.loads(args[4])

    def cmps(text):
        d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='p')
        src = os.path.join(d, 'a.c')
        open(src, 'w', newline='\n').write(text)
        subprocess.run([iwlib.GCC, '-c', '-O3', '--param', 'builtin-expect-probability=50', '-I' + os.path.join(iwlib.R, 'src'), '-fdump-tree-optimized', 'a.c', '-o', 'a.o'], cwd=d, capture_output=True)
        f = ([x for x in os.listdir(d) if 'optimized' in x] or [None])[0]
        if not f:
            iwlib.cleanup(d)
            return 'nocompile'
        t = open(os.path.join(d, f), errors='replace').read()
        iwlib.cleanup(d)
        m = re.search(r'^;; Function writeFsTable .*?(?=^;; Function |\Z)', t, re.S | re.M)
        return ' '.join(re.sub(r'\s+', '', x) for x in re.findall(r'if \(([^)]*ivtmp[^)]*)\)', m.group(0))[0:4])

    def one(kv):
        k, v = kv
        s = dict(st0)
        s[k] = v
        r = score(s)[1]
        return k, v, r.get('total'), cmps(render(s))
    items = [(k, v) for k in list(SH) for v in range(len(SH[k][1]) + 1) if v != st0.get(k, 0)]
    with TP(WORKERS) as ex:
        for k, v, n, c in ex.map(one, items):
            print(k, v, n, c, flush=True)
else:
    main()
