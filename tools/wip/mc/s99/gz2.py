# gz2.py BASE OUT OLD NEW TAIL : replace OLD by NEW and append TAIL after mode_client's final return 0;
import sys
b,o,old,new,tail=sys.argv[1:6]
s=open(b).read()
if old:
    assert s.count(old)==1,(old,s.count(old)); s=s.replace(old,new)
i=s.find('return 0;',s.find('connect to xbox server'))+len('return 0;')
s=s[:i]+' '+tail+s[i:]
open(o,'w',newline='\n').write(s)
