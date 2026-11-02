# fin.py: final (post connect_traces) layout, ours vs profiled mapped into our numbering
import re
from ord import m as PM
def final(f):
    L = open(f).read().split('\n')
    rs = [i for i, l in enumerate(L) if l.startswith('Reordered sequence')][0]
    out = []
    for l in L[rs+1:rs+400]:
        mm = re.match(r'\s*(\d+) (?:bb (\d+)|duplicate of (\d+))', l)
        if mm: out.append(int(mm.group(2)) if mm.group(2) else 'd%s' % mm.group(3))
        elif out: break
    return out
if __name__ == '__main__':
  o = final('dd/mc.bbro'); p = [PM.get(b, '?%s' % b) if isinstance(b, int) else 'd%s' % PM.get(int(b[1:]), '?') for b in final('pf/mc.bbro')]
  print('ours', ' '.join(map(str, o))); print('prof', ' '.join(map(str, p)))
  import difflib
  for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, o, p, autojunk=False).get_opcodes():
      if t != 'equal': print(t, o[i1:i2], '->', p[j1:j2])
