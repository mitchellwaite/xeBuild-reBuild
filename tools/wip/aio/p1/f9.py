"""f9.py OUT [opts]: from n1.c: external optIniBool natural (asm pin), static copies optH (others), optN (noecdremap)."""
import re,sys
t=open(__file__.replace('f9.py','n1.c'),newline='').read()
opts=set(sys.argv[2].split(',')) if len(sys.argv)>2 else set()
i=t.index('_Bool optIniBool('); j=t.index('int optIniInt(')
b=t[i:j]
head='''	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		return 0;
	if (perboxExists(name)) {'''
assert head in b
H=b.replace('_Bool optIniBool(','static _Bool optH(').replace(head,'''	if (xb.bootFlags & set) {
		if (__builtin_expect(__builtin_constant_p(xb.bootFlags + 1), 1))
			goto p;
		return 0;
	}
	if (__builtin_expect(xb.bootFlagsOff & set, 1))
		return 0;
p:
	if (perboxExists(name)) {''')
N=b.replace('_Bool optIniBool(','static _Bool optN(').replace(head,'''	if (__builtin_constant_p(xb.bootFlags + 2))
		return 0;
	if (xb.bootFlags & set) {
		if (__builtin_constant_p(xb.bootFlags + 1))
			goto p;
		return 0;
	}
	if (__builtin_expect(xb.bootFlagsOff & set, 1)) {
		if (__builtin_constant_p(xb.bootFlagsOff + 1))
			goto pl;
		return 0;
	}
p:
	if (perboxExists(name)) {
pl:''')
# external keeps the pin form
ext=b.replace('''	xb.bootFlags &= ~clear;
	xb.bootFlags |= set;
''','''	{
		uint32_t f = (xb.bootFlags & ~clear) | set;
		__asm__("" : "+a" (f));
		xb.bootFlags = f;
	}
''')
t=t[:i]+ext+H+N+t[j:]
t=t.replace('if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0)','if (!(xb.bootFlags & (set))) optH(name, set, clear, 0)')
t=t.replace('OPT("noecdremap", 0x80000000, 0);','if (!(xb.bootFlags & 0x80000000)) optN("noecdremap", 0x80000000, 0, 0);')
open(sys.argv[1],'w',newline='\n').write(t)
