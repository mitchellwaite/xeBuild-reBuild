import json, sys, os
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, r'..\s18')
import lx, ev, hsim
for w in sys.argv[3].split(','):
    lx.st = json.load(open(sys.argv[1]))
    r = ev.ev(lx.mk(w, sys.argv[2]), 'lxf', True)
    R, k = hsim.load(r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\build\v\mc35\slot_lxf'); f, P = hsim.measured(k)
    print(w, r['score'], r['fncmp'], {b: f.get(b) for b in [49,115,112,103,55,126,125,61,33,29,67,127,117,130,35,42,53,77,79]})
