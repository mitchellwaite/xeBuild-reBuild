"""python tools/wip/dehint/iw6anneal.py <seconds> <seed> <base.c> [--workers N] [--state '<json>'] [--render '<json>' out.c]

Attempt 6's search: iwanneal's shapes plus forms of the code after this attempt's changes (pg, partial, FS loop, locals), walking neutral plateaus.
Plain -O3.  An IDENTICAL state goes to build/iw/a6/an6_<seed>.c; log build/iw/a6/an6_<seed>.log (each new best with its state)."""
import json, os, random, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
sys.argv = ['x']
import iwanneal as A, iwlib


def opt(name, d):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return d


WORKERS = int(opt('--workers', 4))
STATE = json.loads(opt('--state', '{}'))
R = lambda old, *news: (old, list(news))
SH = dict(A.SHAPES)
_E = 'start + i - xb.fsStart'
SH.update({
    'pgf': R('			pg = start * 32;\n			s = xb.spare + (pg + p + b * 32) * 16;\n',
             '			pg = start * 32;\n			s = xb.spare + (pg + b * 32 + p) * 16;\n',
             '			pg = 32 * start;\n			s = xb.spare + (b * 32 + pg + p) * 16;\n',
             '			pg = start * 32;\n			pg += p + b * 32;\n			s = xb.spare + pg * 16;\n',
             '			pg = start * 32;\n			pg += b * 32;\n			s = xb.spare + (pg + p) * 16;\n',
             '			pg = start * 32 + p;\n			s = xb.spare + (pg + b * 32) * 16;\n',
             '			pg = p + b * 32;\n			pg += start * 32;\n			s = xb.spare + pg * 16;\n'),
    'part': R("		partial = (len < 0x4000) & (type != 0) & (type != '0');\n",
              "		partial = (type != 0) & (type != '0') & (len < 0x4000);\n",
              "		partial = (type != 0) & (len < 0x4000) & (type != '0');\n",
              "		partial = (len < 0x4000) & ((type != 0) & (type != '0'));\n"),
    'pdecl': R('	int partial;\n', '	uint8_t partial;\n', '	uint32_t partial;\n', '	_Bool partial;\n'),
    'tl': R("		t = type - '1';\n", "		t = (uint8_t)(type - '1');\n", "		t = type - 0x31;\n", "		t = type + 0xcf;\n"),
    'fs0': R('	if (next != 0xf1f1) {\n\n		for (i = 0; i < blocks; i++) {\n',
             '	if (next != 0xf1f1) {\n		i = 0;\n		while (i < blocks) {\n'),
    'blkl': R('				((struct spb *)s)->b2lo = BLK >> 8;\n', '				((struct spb *)s)->b2lo = (start + b) >> 8;\n'),
    'lba': R('				s[1] = BLK;\n', '				*(s + 1) = BLK;\n', '				s[1] = (uint8_t)BLK;\n'),
    'lbs': R('				s[0] = BLK;\n', '				*s = BLK;\n', '				s[0] = (uint8_t)BLK;\n'),
    'tb': R('				if (type > 1) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a',
            '				if (type >= 2) {\n					s[12] = (s[12] & 0xc0) | (type & 0x3f);\n					if (type != 0x2a',
            '				if (type > 1) {\n					s[12] = (s[12] & 0xc0) + (type & 0x3f);\n					if (type != 0x2a'),
    'ty2': R("					if (type != 0x2a && type != 0x2c) {\n", "					if (type != 0x2c && type != 0x2a) {\n", "					if ((type & ~2) != 0x2a) {\n"),
    'pgs': R('			pages = len % 512 ? len / 512 + 1 : len / 512;\n',
             '			pages = len / 512;\n			if (len % 512)\n				pages++;\n',
             '			pages = len / 512 + (len % 512 ? 1 : 0);\n',
             '			pages = len / 512 + (len % 512 != 0);\n'),
    'fsn': R('			if (next != 0 && next != 0xffff) {\n', '			if (next && next != 0xffff) {\n', '			if (next != 0xffff && next != 0) {\n'),
    'wall': R('	fsTable[blk - xb.fsStart] = SWAP16_IMAGE_WRITE(0x1ffd);\n', '	i = blk - xb.fsStart;\n	fsTable[i] = SWAP16_IMAGE_WRITE(0x1ffd);\n'),
    'wc': R('	if (!xb.bigBlock)\n		goto small;\n	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	goto done;\nsmall:\n	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\ndone:\n',
            '	if (xb.bigBlock)\n		imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n	else\n		imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n',
            '	if (!xb.bigBlock)\n		imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);\n	else\n		imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);\n'),
    'tailr': R('		tail = rem;\n		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n',
               '		tail = rem % 0x4000;\n		if (rem < 0x4000)\n			tail = rem;\n',
               '		if (rem >= 0x4000)\n			tail = rem % 0x4000;\n		else\n			tail = rem;\n'),
})
base = open(args[2], newline='').read().replace('\r\n', '\n')
SH = {k: v for k, v in SH.items() if v[0] in base}
seed = int(args[1])
secs = int(args[0])


def render(st):
    t = base
    for k, (old, news) in SH.items():
        v = st.get(k, 0)
        if v and old in t:
            t = t.replace(old, news[v - 1])
    return t


def score(st):
    r = iwlib.score_text(render(st), [])
    return (10 ** 7 if 'compile' in r else r['total']), r


if '--render' in args:
    i = args.index('--render')
    st = json.loads(args[i + 1])
    open(args[i + 2], 'w', newline='\n').write(render(st))
    print(iwlib.fmt(score(st)[1]))
    sys.exit(0)


def main():
    rnd = random.Random(seed)
    log = open(os.path.join(iwlib.BUILD, 'a6', 'an6_%d.log' % seed), 'a', newline='\n')
    print('shapes', len(SH), sorted(SH), file=log, flush=True)
    cur = dict(STATE)
    curv, r = score(cur)
    print('start', curv, iwlib.fmt(r)[:200], file=log, flush=True)
    gbest, gval = cur, curv
    keys = list(SH)
    t0 = time.time()
    seen = 0
    with ThreadPoolExecutor(WORKERS) as ex:
        while time.time() - t0 < secs:
            cands = []
            for _ in range(WORKERS * 2):
                s = dict(cur)
                for key in rnd.sample(keys, rnd.choice((1, 1, 2, 2, 3))):
                    n = len(SH[key][1]) + 1
                    s[key] = (s.get(key, 0) + rnd.randrange(1, n)) % n
                cands.append(s)
            res = list(ex.map(lambda s: (s, score(s)), cands))
            seen += len(cands)
            for s, (v, r) in res:
                if r.get('identical'):
                    open(os.path.join(iwlib.BUILD, 'a6', 'an6_%d.c' % seed), 'w', newline='\n').write(render(s))
                    print('IDENTICAL', json.dumps({k: x for k, x in s.items() if x}), file=log, flush=True)
                    return
            s, (v, r) = min(res, key=lambda x: x[1][0])
            if v < gval:
                gbest, gval = s, v
                print(seen, 'best', v, json.dumps({k: x for k, x in s.items() if x}), iwlib.fmt(r)[:200], file=log, flush=True)
            if v <= curv or rnd.random() < 2.718 ** (-(v - curv) / 4.0):
                cur, curv = s, v
            if rnd.random() < 0.02:
                cur, curv = gbest, gval
    print('end', seen, gval, file=log, flush=True)


main()
