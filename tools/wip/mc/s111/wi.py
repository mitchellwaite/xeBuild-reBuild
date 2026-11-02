# wi.py: r4sim what-ifs on best's dump: 141 pushed to round 4 (entry-threshold lever) + key overrides
import sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s86')
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\tools\wip\mc\s104')
import fibsim, r4sim, srch
def push141(pre, K, blk=141):
    out = []; r = 0; skip = False
    for e in pre:
        if e[0] == 'round': r = e[1]
        if r == 3 and e == ('get', blk): out.append(('get', blk)); out.append(('push', blk, K)); skip = True; continue
        if skip and e == ('visit', blk): skip = False; continue
        out.append(e)
    return out
if __name__ == '__main__':
    pre, g, first = r4sim.load(sys.argv[1])
    print('base', srch.dist(srch.sim(pre, g)))
    for K in [-1000310, -1000309, -1000308, -1000307, -1000306, -1000305, -1000304, -1000210, -1000208, -10, -9, -8, -7, -6, -5]:
        p2 = push141(pre, K)
        o = srch.sim(p2, g); print(K, srch.dist(o), ' '.join(map(str, o)))
