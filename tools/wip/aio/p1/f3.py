"""f3.py OUT opts: natural source: OPT = guard + optIniBool, plain helpers. opts: two = two-statement set, noasm"""
import re,sys
t=open(__file__.replace('f3.py','n0.c'),newline='').read()
opts=set(sys.argv[2].split(','))
old=t[t.index('	{\n		/* the original ORs into eax'):t.index('	return 1;\n}\n\nint optIniInt')]
if 'two' in opts:
    t=t.replace(old,'	xb.bootFlags &= ~clear;\n	xb.bootFlags |= set;\n')
open(sys.argv[1],'w',newline='\n').write(t)
