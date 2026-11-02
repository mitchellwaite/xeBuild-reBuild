import re,sys
t=open(__file__.replace('f2.py','base.c'),newline='').read()
opts=set(sys.argv[2].split(','))
body='if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0)'
if 'plain' in opts: body='optIniBool(name, set, clear, 0)'
i=t.index('#define OPT(name, set, clear) do {'); j=t.index('} while (0)\n',i)+len('} while (0)\n')
t=t[:i]+'#define OPT(name, set, clear) '+body+'\n'+t[j:]
A=t.index('void applyIniOptions(void)')
h,t=t[:A],t[A:]
if 'int' in opts: t=t.replace('optIniIntI(','optIniInt(')
if 'mac' in opts: t=t.replace('macidSetI()','macidSet()')
if 'strip' in opts: t=t.replace('stripColonsI(','stripColons(')
if 'but' in opts: t=re.sub(r'parseButtonI\((getIniValue\("\w+"\)), 0\)',r'parseButton(\1)',t)
t=h+t
open(sys.argv[1],'w',newline='\n').write(t)
