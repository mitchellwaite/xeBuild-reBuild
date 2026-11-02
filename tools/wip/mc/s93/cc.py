# cc.py BASE : list constant_p chains ; cc.py BASE OUT IDX DELTA : change term count
import sys,re
s=open(sys.argv[1]).read()
pat=re.compile(r'if \(((?:\(char \*\))?__builtin_constant_p\((\w+) \+ \d+\)(?: == \(char \*\)1)?(?: && (?:\(char \*\))?__builtin_constant_p\(\w+ \+ \d+\)(?: == \(char \*\)1)?)*)\) (goto \w+|mode = \d+)')
ms=list(pat.finditer(s))
if len(sys.argv)==2:
    for i,m in enumerate(ms): print(i,m.group(1).count('constant_p'),m.group(3),s.count('\n',0,m.start())+1)
    sys.exit()
o,idx,d=sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
m=ms[idx]; terms=m.group(1).split(' && '); v=m.group(2)
n=len(terms)+d
if n<1: sys.exit(1)
if d<0: terms=terms[:n]
else:
    for k in range(d): terms.append('__builtin_constant_p(%s + %d)'%(v,777000+idx*100+k))
s=s[:m.start(1)]+' && '.join(terms)+s[m.end(1):]
open(o,'w',newline='\n').write(s)
