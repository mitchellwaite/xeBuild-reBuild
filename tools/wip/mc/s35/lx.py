"""lx.py STATE.json : loop-exit dead edge (bcp goto from option-loop top to label lx after the loop) forms; measure."""
import json, sys, os, copy
os.environ['DUP'] = '1'; os.environ['LU'] = '1'
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs2, ev, k67, ebl
k67.inj48.W.update(ebl.W)
st = json.load(open(sys.argv[1])) if __name__ == "__main__" else None
A = '\tif (NO_MODE_ARG(mode, arg)) {'
def mk(w, arm='top'):
    t = gs2.build(st); t = t.replace(A, '\tlx: ;\n' + A, 1)
    return k67.inj(t, arm, w, 900, 'lx')
def run(x):
    i, (arm, w) = x
    r = ev.ev(mk(w, arm), 'lx%d' % (i % 4), True)
    import hsim
    return arm, w, r and r['score'], r and r['fncmp'], r and ' '.join(map(str, r['o'][12:]))
if __name__ == "__main__":
  J = [(a, w) for a in sys.argv[2].split(',') for w in ['b', 'p', 'q', 'pp', 'qq', 'ppp', 'pppp', 'qqq', 'pqq']]
  with ThreadPoolExecutor(4) as ex:
      for r in ex.map(run, enumerate(J)): print(*r, flush=True)
