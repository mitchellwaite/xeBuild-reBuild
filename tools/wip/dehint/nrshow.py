"""python tools/wip/dehint/nrshow.py <dumpdir> what [fn]: what = est (profile_estimate predictions, netRecvVerbose),
opt (optimized CFG of the clone or fn), got (IRA lines of the clone's got/size)."""
import os, re, sys
d, what = sys.argv[1], sys.argv[2]
fnn = sys.argv[3] if len(sys.argv) > 3 else None


def cut(suffix, name):
    f = next(x for x in os.listdir(d) if x.endswith(suffix))
    t = open(os.path.join(d, f)).read()
    i = t.index(';; Function %s' % name)
    s = t[i:]
    j = s.find('\n;; Function ', 10)
    return s[:j] if j > 0 else s


if what == 'est':
    s = cut('profile_estimate', fnn or 'netRecvVerbose (netRecvVerbose')
    s = re.sub(r'\n\s*# (VUSE|\.MEM)[^\n]*', '', s)
    print(s)
elif what == 'opt':
    s = cut('t.optimized', fnn or 'netRecvVerbose.constprop')
    s = re.sub(r'\n\s*# (PRED|VUSE|\.MEM)[^\n]*', '', s)
    print(s[s.find('basic block 2,') - 5:])
elif what == 'got':
    s = cut('r.ira', fnn or 'netRecvVerbose.constprop')
    regs = sys.argv[4:] if len(sys.argv) > 4 else None
    names = {}
    for m in re.finditer(r'\(reg(?:/\w+)*:\w+ (\d+)(?: \[ ([^\]]*) \])?', s):
        if m.group(2):
            names.setdefault(m.group(1), m.group(2).strip())
    want = {r for r, n in names.items() if n in ('got', 'size', 'buf', '<retval>')}
    print({r: names[r] for r in want})
    for l in s.split('\n'):
        m = re.search(r'\(r(\d+),l0\)|\br(\d+)\b', l)
        if m and (m.group(1) or m.group(2)) in want and re.search(r'costs:|conflicts|profitable|Allocno a\d+r|hard_regs|nrefs|Pushing|Popping|freq=', l):
            print(l[:260])
