"""f5.py OUT opts: from n1.c; inner function (off test onward); optIniBool = flags test + inner."""
import re,sys
t=open(__file__.replace('f5.py','n1.c'),newline='').read()
opts=set(sys.argv[2].split(','))
i=t.index('_Bool optIniBool('); j=t.index('int optIniInt(')
b=t[i:j]
inner=b.replace('_Bool optIniBool(','static _Bool optIniInner(').replace('if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))','if (xb.bootFlagsOff & set)')
outer='''_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)
{
	if (xb.bootFlags & set)
		return 0;
	return optIniInner(name, set, clear, def);
}

'''
t=t[:i]+inner+outer+t[j:]
t=t.replace('#define OPT(name, set, clear) if (!(xb.bootFlags & (set))) optIniBool(name, set, clear, 0)','#define OPT(name, set, clear) if (!(xb.bootFlags & (set))) optIniInner(name, set, clear, 0)')
open(sys.argv[1],'w',newline='\n').write(t)
