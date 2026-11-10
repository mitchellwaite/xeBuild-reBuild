#!/usr/bin/env python3
"""mode_client attempt 17, second part: getArgs in the arms in place of the static helpers.

Spellings of getArgs that keep its own code (the standalone function must stay identical),
then each of those with the arms calling it, compared arm by arm (mc17arm) with the
inliner's growth for the two-argument calls (mc17gs; gcc inlines under 40).

python tools/wip/dehint/mc17ga.py [-arms bp,wb,eb,ip,r,w] [-all] [-only SUBSTR] [-o NAME FILE]
  -arms  which arms call getArgs (the rest as landed in commit 96c65024: static helpers)
  -all   also list the spellings whose standalone code differs
  -only  spellings whose name contains SUBSTR
  -o     write the file for spelling NAME (with -arms) and stop

A spelling's name is decl-a-count-t1-rest-check:
  decl   fi `first = *pi + 1; i = first` usage argv[first - 1], return argv[first]
         f0 `first = *pi; i = first + 1` usage argv[first], return argv[first + 1]
         ps as fi with usage argv[*pi]
         op `opt = *pi; first = opt + 1; i = first` usage argv[opt], return argv[first]
  a      d `char *a = argv[i];` / s assigned after the declarations / x no temporary in the
         first test (`!argv[i] || i == argc || *argv[i] == '-'`)
  count  the first test's count operand: i, e `*pi + 1`, f `first` (f0: `first + 1`), o `opt + 1`
  t1     c count first / n pointer first
  rest   the optional arguments' tests: fn / fc folded (`i++; a = argv[i]; if (!a || i == argc`
         or count first), un `if (!(a = argv[++i]) || i == argc`, uc `a = argv[++i]; if (i ==
         argc || ..` with `i + 0`-free non-simple spelling is not natural so not here, xn no
         temp `i++; if (!argv[i] || i == argc`
  check  a `if (mode && check)` / n `if (mode) if (check)` / c `if (check && mode)`"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
import mc17
import mc17arm
import mc17gs
import mc17lib as L

BASE = 'conn=six,six=usage1,test=pos,bps=inpcbr,ipa=onearg,r=onec,w=onec,o2=jcr'
ARM = {'eb': 'eb=getargs', 'ip': 'ipa=getargs', 'r': 'r=getargs', 'w': 'w=getargs', 'e': 'e=getargs', 'c': 'c=getargs',
       'bp': 'bp=getargs', 'wb': 'wb=getargs'}

DECL = {
    'fi': ('	int first = *pi + 1;\n	int i = first;\n', 'argv[first - 1]', 'argv[first]'),
    'f0': ('	int first = *pi;\n	int i = first + 1;\n', 'argv[first]', 'argv[first + 1]'),
    'ps': ('	int first = *pi + 1;\n	int i = first;\n', 'argv[*pi]', 'argv[first]'),
    'op': ('	int opt = *pi;\n	int first = opt + 1;\n	int i = first;\n', 'argv[opt]', 'argv[first]'),
}
T = {'c': "{i} == argc || !{a}", 'n': "!{a} || {i} == argc"}


def count_operand(decl, k):
    if k == 'i':
        return 'i'
    if k == 'e':
        return '*pi + 1'
    if k == 'f':
        return 'first + 1' if decl == 'f0' else 'first'
    if k == 'o':
        return 'opt + 1' if decl == 'op' else None


def getargs(decl, a1, i1, t1, rest, chk):
    d, use, r = DECL[decl]
    i1e = count_operand(decl, i1)
    if i1e is None:
        return None
    t = 'char *getArgs(int argc, char **argv, int *pi, int mode, int check, char **arg2, char **arg3)\n{\n' + d
    if a1 == 'x':
        # no temporary: the load is in the first test
        if rest[0] in 'fuv':
            t += '	char *a;\n'
        t += "\n	if (%s || *argv[i] == '-')\n		client_usage(3, %s);\n" % (T[t1].format(i=i1e, a='argv[i]'), use)
    else:
        if a1 == 'd':
            t += '	char *a = argv[i];\n\n'
        else:
            t += '	char *a;\n\n	a = argv[i];\n'
        t += "	if (%s || *a == '-')\n		client_usage(3, %s);\n" % (T[t1].format(i=i1e, a='a'), use)
    for k in (2, 3):
        t += '	if (arg%d) {\n' % k
        if rest[0] == 'f':
            t += "		i++;\n		a = argv[i];\n		if (%s || *a == '-')\n" % T[rest[1]].format(i='i', a='a')
            st = 'a'
        elif rest == 'un':
            t += "		if (!(a = argv[++i]) || i == argc || *a == '-')\n"
            st = 'a'
        elif rest == 'vn':
            t += "		i++;\n		if (!(a = argv[i]) || i == argc || *a == '-')\n"
            st = 'a'
        else:
            t += "		i++;\n		if (!argv[i] || i == argc || *argv[i] == '-')\n"
            st = 'argv[i]'
        t += '			client_usage(4, %s);\n		*arg%d = %s;\n	}\n' % (use, k, st)
    if chk == 'a':
        t += '	if (mode && check)\n		client_usage(5, %s);\n' % use
    elif chk == 'n':
        t += '	if (mode) {\n		if (check)\n			client_usage(5, %s);\n	}\n' % use
    else:
        t += '	if (check && mode)\n		client_usage(5, %s);\n' % use
    t += '	*pi = i;\n	return %s;\n}\n\n' % r
    return t


def variants():
    for decl, a1, i1, t1, rest, chk in itertools.product(DECL, 'dsx', 'iefo', 'cn', ('fn', 'fc', 'un', 'vn', 'xn'), 'anc'):
        t = getargs(decl, a1, i1, t1, rest, chk)
        if t:
            yield '%s-%s-%s-%s-%s-%s' % (decl, a1, i1, t1, rest, chk), t


def with_getargs(text, g):
    a = text.index('char *getArgs(int argc')
    b = text.index('\n}\n', a) + 3
    return text[:a] + g.rstrip('\n') + '\n' + text[b:]


def standalone(g):
    """getArgs' own code against the reference's, in the landed file"""
    t = with_getargs(mc17.text_of(BASE), g)
    ok, o, d = L.compile_src(t)
    try:
        if not ok:
            return 'COMPILE ' + o.strip().split('\n')[-1][:100]
        fns, _ = bdlib.disasm(o)
        return bdlib.fdiff(L._ref['fns']['_getArgs'], fns.get('_getArgs', []))
    finally:
        L.cleanup(d)


def file_for(g, arms):
    return with_getargs(mc17.text_of(BASE + ''.join(',' + ARM[x] for x in arms)), g)


def arms_with(g, arms):
    t = file_for(g, arms)
    r, err = mc17arm.compare(t)
    if err:
        return 'COMPILE'
    s = L.score_text(t, lay=True)
    gr, clone, ev = mc17gs.growths(t)
    a, use, diff = r
    two = sorted(set(x[1] for x in gr if x[0] in (3.35, 0.83)))
    return 'grow2=%s %s| %s  usage %d | %s' % ('/'.join(map(str, two)), 'clone ' if clone else '',
                                              ' '.join('%s:%d' % kv for kv in diff.items()) or 'arms equal', len(use),
                                              L.fmt(s)[:70])


if __name__ == '__main__':
    args = sys.argv[1:]
    arms = ['bp', 'wb', 'eb', 'ip', 'r', 'w']
    if '-arms' in args:
        arms = [x for x in args[args.index('-arms') + 1].split(',') if x]
    if '-o' in args:
        k = args.index('-o')
        open(args[k + 2], 'w', newline='\n').write(file_for(dict(variants())[args[k + 1]], arms))
        sys.exit()
    only = args[args.index('-only') + 1] if '-only' in args else ''
    vs = [x for x in variants() if only in x[0]]
    print(len(vs), 'spellings', flush=True)
    with ThreadPoolExecutor(6) as ex:
        st = list(ex.map(lambda x: standalone(x[1]), vs))
    same = [(n, g) for (n, g), s in zip(vs, st) if s == 0]
    print(len(same), 'keep getArgs\' own code', flush=True)
    if '-all' in args:
        for (n, g), s in zip(vs, st):
            if s != 0:
                print('   ', n, s)
    with ThreadPoolExecutor(6) as ex:
        for (n, g), r in zip(same, ex.map(lambda x: arms_with(x[1], arms), same)):
            print('%-20s %s' % (n, r), flush=True)
