"""f8.py OUT VARIANT: from n1.c: variants of optIniBool's head"""
import re,sys
t=open(__file__.replace('f8.py','n1.c'),newline='').read()
old='''	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (perboxExists(name)) {'''
assert old in t
V={
'a':'''	if (xb.bootFlags & set) {
		if (__builtin_constant_p(xb.bootFlags + 1))
			goto p;
		return 0;
	}
	if (__builtin_expect(xb.bootFlagsOff & set, 1))
		return 0;
p:
	if (perboxExists(name)) {''',
'b':'''	if (xb.bootFlags & set) {
		if (__builtin_constant_p(xb.bootFlags + 1))
			goto p;
		return 0;
	}
	if (xb.bootFlagsOff & set)
		return 0;
p:
	if (perboxExists(name)) {''',
'c':'''	if (xb.bootFlags & set) {
		if (__builtin_expect(__builtin_constant_p(xb.bootFlags + 1), 1))
			goto p;
		return 0;
	}
	if (__builtin_expect(xb.bootFlagsOff & set, 1))
		return 0;
p:
	if (perboxExists(name)) {''',
}
t=t.replace(old,V[sys.argv[2]])
open(sys.argv[1],'w',newline='\n').write(t)
