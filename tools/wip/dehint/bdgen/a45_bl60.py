import sys
sys.path.insert(0,'tools/wip/dehint'); import bdrun
t=open('build/bd/a45/n1.c').read()
CASE='''					if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}
					if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
						/* For review: r = 0 stands for what r = loadBl60(e) did on
						   success; it is live, and the shape is chosen for the match */
						r = 0;
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}'''
NEWCASE='''					if (xb.type == BUILD_JTAG || xb.glitch2mfg)
						r = loadBl60(e);
					if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
						r = loadBl60(e);'''
CON='''				if (loadBaseFile(e->name, e))
					r = defaultBl60(e);
				else if (e->size != 0x60)
					r = defaultBl60(e);
				break;'''
H={
'h1':'''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;''',
'h2':'''	if (loadBaseFile(e->name, e) || e->size != 0x60)
		return defaultBl60(e);
	return 0;''',
'h3':'''	if (!loadBaseFile(e->name, e) && e->size == 0x60)
		return 0;
	return defaultBl60(e);''',
'h4':'''	int r = 0;

	if (loadBaseFile(e->name, e))
		r = defaultBl60(e);
	else if (e->size != 0x60)
		r = defaultBl60(e);
	return r;''',
'h5':'''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	else if (e->size != 0x60)
		return defaultBl60(e);
	return 0;''',
}
DEF='static int defaultBl60(struct fileent *e)\n{'
i=t.index(DEF); j=t.index('\n}\n',i)+3
for k,body in H.items():
  for con in (0,1):
    s=t[:j]+'\n/* the base file if it is a 0x60-byte bootloader, else the default one */\nstatic int loadBl60(struct fileent *e)\n{\n'+body+'\n}\n'+t[j:]
    s=bdrun.sub(s,CASE,NEWCASE,1)
    if con: s=bdrun.sub(s,CON,'''				r = loadBl60(e);
				break;''',1)
    open('build/bd/a45/bl60_%s%d.c'%(k,con),'w',newline='\n').write(s)
    for p in (98,99):
        r=bdrun.score(s,['--param','builtin-expect-probability=%d'%p])
        print(k,con,p, 'IDENT' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r['L'], r['notes']) if 'L' in r else r)
