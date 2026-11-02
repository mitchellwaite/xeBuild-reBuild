"""f6.py OUT opts: from n1.c with edits: exp = expect(off & set, 0)"""
import re,sys
t=open(__file__.replace('f6.py','n1.c'),newline='').read()
opts=set(sys.argv[2].split(','))
if 'exp' in opts:
    t=t.replace('if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))','if ((xb.bootFlags & set) || __builtin_expect(xb.bootFlagsOff & set, 0))')
open(sys.argv[1],'w',newline='\n').write(t)
