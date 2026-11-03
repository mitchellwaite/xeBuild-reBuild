"""python tools/wip/dehint/iwanneal.py [seconds] [seed] [--from state.json]

Coordinate search over imgAdd/imgAddFile/writeFsTable: `tricks` (each present or removed) and `shapes` (natural
source alternatives).  Objective: diff lines + PEN * tricks kept.  Every variant whose object is IDENTICAL with
fewer tricks than the best so far goes to build/iw/an_best_<ntricks>.c with its state .json.
Log: build/iw/an_<seed>.log.  Reads the base from drafts/image_write.c."""
import json, os, random, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib, iwtricks

BASE = open(os.path.join(iwlib.R, 'tools/wip/dehint/drafts/image_write.c'), newline='').read().replace('\r\n', '\n')
PEN = 6
FLAGS = ['--param', 'builtin-expect-probability=50']

# trick name -> edits to remove it
TRICKS = ['opt', 'pin_t', 'pin_end', 'dead_lenpp', 'dead_add1', 'dead_add2', 'dead_add3', 'dead_add4', 'dead_add5', 'dead_add6']

R = lambda old, *news: (old, list(news))
SHAPES = {
    'start': R('	start = (off - x) >> 14;\n', '	start = off >> 14;\n'),
    'first': R('	first = x ? 0x4000 - x : 0;\n', '	first = 0;\n	if (x)\n		first = 0x4000 - x;\n',
               '	if (x)\n		first = 0x4000 - x;\n	else\n		first = 0;\n'),
    'tail': R('''		if (rem < 0x4000)
			tail = rem;
		else
			tail = rem % 0x4000;
''', '		tail = rem < 0x4000 ? rem : rem % 0x4000;\n', '		tail = rem % 0x4000;\n',
              '		tail = rem;\n		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n'),
    'blocks': R('''		blocks = rem / 0x4000;
		if (tail) {
			blocks++;
		}
		if (x) {
			blocks++;
		}
''', '''		blocks = rem / 0x4000;
		if (x)
			blocks++;
		if (tail)
			blocks++;
''', '''		blocks = rem / 0x4000 + (tail != 0);
		if (x)
			blocks++;
''', '''		blocks = rem / 0x4000;
		if (tail)
			blocks++;
		blocks += x != 0;
'''),
    'range': R('	if (xb.rawSize < off || xb.rawSize < off + len) {\n		return -1;\n	}\n',
               '	if (off > xb.rawSize || off + len > xb.rawSize) {\n		return -1;\n	}\n',
               '	if (xb.rawSize < off + len || xb.rawSize < off) {\n		return -1;\n	}\n',
               '	if (off > xb.rawSize || xb.rawSize < off + len)\n		return -1;\n'),
    'pad': R('	if (pad == 1) if (tail)\n', '	if (pad == 1 && tail)\n', '	if (tail && pad == 1)\n', '	if (tail) if (pad == 1)\n'),
    'memset': R('memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n	for',
                'memset(xb.hdr + off + len, 0, ((off + len + 0x3fff) & ~0x3fff) - off - len);\n	for',
                'memset(xb.hdr + (off + len), 0, ((off + len + 0x3fff) & ~0x3fff) - (off + len));\n	for'),
    't': R("		t = type - '1';\n		partial = type != 0 && type != '0' && len < 0x4000;\n",
           "		partial = type != 0 && type != '0' && len < 0x4000;\n		t = type - '1';\n"),
    'if_p': R('''			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			if (p) p /= 512;
''', '''			p = xb.bigBlock ? off & 0x1ffff : off & 0x3fff;
			p /= 512;
''', '''			if (xb.bigBlock)
				p = off & 0x1ffff;
			else
				p = off & 0x3fff;
			if (p) p /= 512;
''', '''			p = (xb.bigBlock ? off & 0x1ffff : off & 0x3fff) / 512;
'''),
    'pages': R('''			pages = len / 512;
			if (len % 512)
				pages++;
''', '''			pages = len % 512 ? len / 512 + 1 : len / 512;
''', '''			pages = (len % 512) ? (len + 512) / 512 : len / 512;
''', '''			if (len % 512)
				pages = len / 512 + 1;
			else
				pages = len / 512;
'''),
    'left': R('''						left = pages;
						if (left & 3)
							left = (left + 4) & ~3;
''', '''						left = pages & 3 ? (pages + 4) & ~3 : pages;
''', '''						if (pages & 3)
							left = (pages + 4) & ~3;
						else
							left = pages;
'''),
    's9': R('''						s[9] = (((off & 0x1ffff) ? 256 - (off & 0x1ffff) / 512 : 256) - left) >> 2;
''', '''						s[9] = ((off & 0x1ffff ? 256 - (off & 0x1ffff) / 512 : 256) - left) / 4;
''', '''						{ uint32_t room = 256;
						if (off & 0x1ffff)
							room = 256 - (off & 0x1ffff) / 512;
						s[9] = (room - left) >> 2; }
'''),
    'next': R('''			if (next != 0 && next != 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
			}
''', '''			if (next == 0 || next == 0xffff) {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(start - xb.fsStart + i + 1);
			} else {
				fsTable[start - xb.fsStart + i] = SWAP16_IMAGE_WRITE(next);
			}
''', '''			if (next != 0 && next != 0xffff) {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(next);
			} else {
				fsTable[start + i - xb.fsStart] = SWAP16_IMAGE_WRITE(start + i - xb.fsStart + 1);
			}
'''),
    'fsend': R('		if (next == 0xffff) {\n			fsTable[start + blocks - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n		}\n',
               '		if (next == 0xffff) {\n			fsTable[start - xb.fsStart + blocks - 1] = SWAP16_IMAGE_WRITE(0x1fff);\n		}\n',
               '		if (next == 0xffff)\n			fsTable[blocks + start - 1 - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1fff);\n'),
    'nloop': R('	if (next != 0xf1f1) {\n\n		for (i = 0; i < blocks; i++) {\n', '	if (next != 0xf1f1) {\n		i = 0;\n		for (; i < blocks; i++) {\n'),
    'lenle': R('	if (len <= first) {\n		blocks = 1;\n		tail = len;\n	} else {\n',
               '	blocks = 1;\n	tail = len;\n	if (len > first) {\n'),
    'lim': R('''	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
	uint32_t end = off + len;
''', '''	uint32_t end = off + len;
	uint32_t lim = (xb.fsEnd - 1) * 0x4000;
'''),
    'test': R('	if (__builtin_expect(lim >= off + len, 1)) {\n', '	if (__builtin_expect(lim >= end, 1)) {\n', '	if (__builtin_expect(off + len <= lim, 1)) {\n'),
}


SHAPES.update({
    'wf_loop': R('''		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		p += 0x200;
		memcpy(p, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x200;
''', '''		memcpy(p, (uint8_t *)fsTable + i * 0x200, 0x200);
		memcpy(p + 0x200, (uint8_t *)fsFiles + i * 0x200, 0x200);
		p += 0x400;
'''),
    'wf_blk': R('''	blk = off >> 14;
	if (xb.bigBlock && (off & 0x1ffff)) {
		off = (off + 0x20000) & ~0x1ffff;
		blk = off >> 14;
	}
''', '''	if (xb.bigBlock && (off & 0x1ffff))
		off = (off + 0x20000) & ~0x1ffff;
	blk = off >> 14;
''', '''	if (xb.bigBlock) {
		if (off & 0x1ffff)
			off = (off + 0x20000) & ~0x1ffff;
	}
	blk = off >> 14;
'''),
    'wf_big': R('	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n', '	imgAdd(off, buf, 0x400 * i, 0x2c, 0x1ffe, 0);\n'),
    'wf_small': R('	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n', '	imgAdd(off, buf, 0x400 * i, 0x30, 0x1ffd, 0);\n'),
    'big_lba': R('''				((struct spb *)s)->b2lo = BLK >> 8;
				((struct spb *)s)->b0 = 0xff;
				s[1] = BLK;
''', '''				((struct spb *)s)->b2lo = (start + b) >> 8;
				((struct spb *)s)->b0 = 0xff;
				*(s + 1) = BLK;
'''),
    'bigarg': R('''						s[8] = xb.spare8;
						s[7] = xb.spare7;
''', '''						s[8] = xb.spare8, s[7] = xb.spare7;
'''),
    'end': R('		for (end = p + npages; p < end; p++) {\n', '		end = p + npages;\n		for (; p < end; p++) {\n', '		end = npages + p;\n		for (; p < end; p++) {\n'),
    'blkvar': R('			s = xb.spare + (BLK * 32 + p) * 16;\n', '			s = xb.spare + (b * 32 + start * 32 + p) * 16;\n', '			s = (BLK * 32 + p) * 16 + xb.spare;\n',
                '			s = xb.spare + BLK * 512 + p * 16;\n'),
    'type0': R("		partial = type != 0 && type != '0' && len < 0x4000;\n", "		partial = type && type != '0' && len < 0x4000;\n"),
    'imgend': R('	imgEnd = off + len;\n	return 0;\n}\n\nint imgFits', '	imgEnd = len + off;\n	return 0;\n}\n\nint imgFits'),
})


def render(st):
    t = BASE
    gone = sorted([n for n in TRICKS if st.get(n)], key=lambda n: 0)
    t = iwtricks.apply(t, gone)
    for k, (old, news) in SHAPES.items():
        v = st.get(k, 0)
        if v:
            if old in t:
                t = t.replace(old, news[v - 1])
    return t


def nkept(st):
    return sum(1 for n in TRICKS if not st.get(n))


def score(st):
    r = iwlib.score_text(render(st), FLAGS)
    if 'compile' in r:
        return 10 ** 7, r
    return r['total'] + PEN * nkept(st), r


def neighbours(st, rnd, k):
    out = []
    keys = TRICKS + list(SHAPES)
    for _ in range(k):
        s = dict(st)
        for key in rnd.sample(keys, rnd.choice((1, 1, 1, 2, 2, 3))):
            if key in TRICKS:
                s[key] = not s.get(key)
            else:
                n = len(SHAPES[key][1]) + 1
                s[key] = (s.get(key, 0) + rnd.randrange(1, n)) % n
        out.append(s)
    return out


def main():
    a = sys.argv[1:]
    secs = int(a[0]) if a else 300
    seed = int(a[1]) if len(a) > 1 else 1
    rnd = random.Random(seed)
    st = {}
    if '--from' in a:
        st = json.load(open(a[a.index('--from') + 1]))
    best, r = score(st)
    log = open(os.path.join(iwlib.BUILD, 'an_%d.log' % seed), 'a', newline='\n')
    print('start', best, iwlib.fmt(r), file=log, flush=True)
    best_zero = 99
    t0 = time.time()
    seen = 0
    temp = 12.0
    cur, curv = st, best
    gbest, gval = st, best
    with ThreadPoolExecutor(4) as ex:
        while time.time() - t0 < secs:
            cands = neighbours(cur, rnd, 8)
            res = list(ex.map(lambda s: (s, score(s)), cands))
            seen += len(cands)
            for s, (v, r) in res:
                if r.get('identical'):
                    n = nkept(s)
                    if n < best_zero:
                        best_zero = n
                        open(os.path.join(iwlib.BUILD, 'an_best_%d.c' % n), 'w', newline='\n').write(render(s))
                        json.dump(s, open(os.path.join(iwlib.BUILD, 'an_best_%d.json' % n), 'w'))
                        print('IDENTICAL kept', n, json.dumps(s), file=log, flush=True)
            s, (v, r) = min(res, key=lambda x: x[1][0])
            if v < gval:
                gbest, gval = s, v
                print(seen, 'best', v, 'kept', nkept(s), json.dumps({k: x for k, x in s.items() if x}),
                      iwlib.fmt(r)[:200], file=log, flush=True)
                json.dump(s, open(os.path.join(iwlib.BUILD, 'an_state_%d.json' % seed), 'w'))
            if v <= curv or rnd.random() < 2.718 ** (-(v - curv) / temp):
                cur, curv = s, v
            if rnd.random() < 0.01:
                cur, curv = gbest, gval
    print('end', seen, gval, file=log, flush=True)


if __name__ == "__main__":
    main()
