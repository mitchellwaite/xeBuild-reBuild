#!/usr/bin/env python3
"""mode_client attempt 17, second part: getArgs in the arms, and the order of each arm's
merged tests.

With getArgs' tests spelled `!argv[i] || i == argc || ..` (or with `*pi + 1 == argc`) the
two simple tests of each inlined copy are merged by ifcombine, and which comes first
follows the SSA versions it is handed from the free list: one bit per arm that the source
text does not fix.  This samples behaviour-neutral spellings of mode_client (and getArgs
spellings that keep its own code) and prints, per variant, the arms whose code differs.

python tools/wip/dehint/mc17gl.py [-arms eb,ip,r,w] [-n COUNT] [-seed N] [-ga NAME,..] [-fix axis=v,..]
  -arms  the arms that call getArgs (bp for -bp too; wb is never inlined)
  -n     how many random variants (default 200); results are cached in build/mc/w17/gl.json
  -ga    getArgs spellings to draw from (mc17ga names; default the count-first ones)
  -fix   hold axes at a value"""
import hashlib, json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc17
import mc17arm
import mc17ga
import mc17lib as L

CACHE = os.path.join(L.BUILD, 'gl.json')
GA = dict(mc17ga.variants())
GA_DEFAULT = ['f0-d-f-c-fn-a', 'f0-d-e-c-fn-a', 'f0-s-f-c-fn-a', 'f0-s-e-c-fn-a',
              'f0-x-i-n-xn-a', 'f0-x-i-n-un-a', 'f0-x-i-n-vn-a', 'f0-d-f-n-xn-a', 'f0-d-e-n-un-a']

# behaviour-neutral axes of mode_client (mc17.py's) and of the calls
AX = {
    'help': ['or', 'split'],
    'e': ['plain', 'g', 'gn', 'a', 'an', 'ai', 'ain', 'plainc'],
    'c': ['plain', 'g', 'gn', 'a', 'an', 'ai', 'ain', 'plainc'],
    'six': ['usage1', 'ifelse', 'elseif'],
    'test': ['pos', 'inv'],
    'bps': ['inpcbr', 'injcbr'],
    'wbs': ['icpnbr', 'icjnbr'],
    'ho': ['bwo', 'wbo'],
    'ipm': ['mode', '0'],          # -ip's mode argument (check is 0 either way)
    'nul': ['NULL', '0'],          # how the unused arguments are written
    'keys': ['ma', 'am'],          # -keys: mode = 3; arg = dummy / the reverse
    'ip2': ['plain', 'neg'],       # -i / -p: if (missing) arg = dummy else {..} / the reverse
}
IP_PLAIN = '''			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[i + 1];
				i++;
				log_printf(0, "%s\\n", arg);
			}
'''
IP_NEG = '''			if (argv[i + 1] && i + 1 != argc && *argv[i + 1] != '-') {
				arg = argv[i + 1];
				i++;
				log_printf(0, "%s\\n", arg);
			} else
				arg = dummy;
'''


def text(o, arms):
    v = 'conn=six,ipa=onearg,r=onec,w=onec,o2=jcr'
    for k in ('help', 'e', 'c', 'six', 'test', 'bps', 'wbs', 'ho'):
        v += ',%s=%s' % (k, o[k])
    v += ''.join(',' + mc17ga.ARM[x] for x in arms)
    t = mc17ga.with_getargs(mc17.text_of(v), GA[o['ga']])
    if o['ipm'] == '0':
        a = 'ip = getArgs(argc, argv, &i, mode, 0, NULL, NULL);'
        if a in t:
            t = t.replace(a, 'ip = getArgs(argc, argv, &i, 0, 0, NULL, NULL);')
    if o['nul'] == '0':
        t = t.replace(', NULL, NULL);', ', 0, 0);').replace(', &start, NULL);', ', &start, 0);')
    if o['keys'] == 'am':
        a = '			mode = 3;\n			arg = dummy;\n'
        assert a in t
        t = t.replace(a, '			arg = dummy;\n			mode = 3;\n')
    if o['ip2'] == 'neg':
        for msg in ('info dump path set to %s', 'patch file set to %s'):
            a = IP_PLAIN % msg
            assert a in t, msg
            t = t.replace(a, IP_NEG % msg)
    return t


def measure(t):
    r, err = mc17arm.compare(t)
    if err:
        return {'err': err.strip().split('\n')[-1][:100]}
    a, use, diff = r
    s = L.score_text(t, lay=True)
    return {'arms': diff, 'use': len(use), 'idn': s.get('identical', False), 'lines': s.get('total'),
            'fns': sorted(s.get('per', {})), 'moved': s.get('moved')}


def fmt(r):
    if 'err' in r:
        return 'ERR ' + r['err']
    if r['idn']:
        return 'IDENTICAL'
    return '%4d moved=%-2d %s%s' % (r['lines'], r['moved'], ' '.join('%s:%d' % kv for kv in r['arms'].items()),
                                   '' if r['fns'] == ['_mode_client'] else '  ' + ' '.join(r['fns']))


if __name__ == '__main__':
    a = sys.argv[1:]
    arms = a[a.index('-arms') + 1].split(',') if '-arms' in a else ['eb', 'ip', 'r', 'w']
    n = int(a[a.index('-n') + 1]) if '-n' in a else 200
    rnd = random.Random(int(a[a.index('-seed') + 1]) if '-seed' in a else 1)
    gas = a[a.index('-ga') + 1].split(',') if '-ga' in a else GA_DEFAULT
    fix = dict(x.split('=') for x in a[a.index('-fix') + 1].split(',')) if '-fix' in a else {}
    try:
        cache = json.load(open(CACHE))
    except (OSError, ValueError):
        cache = {}
    todo = {}
    names = {}
    for _ in range(n):
        o = {k: rnd.choice(v) for k, v in AX.items()}
        o['ga'] = rnd.choice(gas)
        o.update(fix)
        t = text(o, arms)
        h = hashlib.sha1(t.encode()).hexdigest()
        names[h] = ','.join('%s=%s' % kv for kv in sorted(o.items()))
        if h not in cache:
            todo[h] = t
    print(len(names), 'variants,', len(todo), 'to compile', flush=True)
    with ThreadPoolExecutor(6) as ex:
        for h, r in zip(todo, ex.map(measure, todo.values())):
            cache[h] = r
    json.dump(cache, open(CACHE, 'w'))
    rows = sorted(((cache[h], v) for h, v in names.items()),
                  key=lambda x: (not x[0].get('idn', False), x[0].get('lines') or 99999))
    hist = {}
    for r, v in rows:
        k = fmt(r)
        hist.setdefault(k, []).append(v)
    for k, vs in list(hist.items())[:25]:
        print('%4d x  %s\n          e.g. %s' % (len(vs), k, vs[0]))
