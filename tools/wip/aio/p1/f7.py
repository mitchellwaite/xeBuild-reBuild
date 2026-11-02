"""f7.py OUT: from n1.c: off-true arm feeds P via dead constant_p"""
import re,sys
t=open(__file__.replace('f7.py','n1.c'),newline='').read()
old='''	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (perboxExists(name)) {'''
assert old in t
new='''	if (xb.bootFlags & set)
		return 0;
	if (xb.bootFlagsOff & set) {
		if (__builtin_constant_p(xb.bootFlagsOff + 1))
			goto p;
		return 0;
	}
p:
	if (perboxExists(name)) {'''
t=t.replace(old,new)
open(sys.argv[1],'w',newline='\n').write(t)
