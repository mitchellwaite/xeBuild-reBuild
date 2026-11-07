import sys
sys.path.insert(0,'tools/wip/dehint'); import bdrun
t=open('build/bd/a45/n1.c').read()
A='''					if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)'''
for k,b in {'sz':A.replace('else if (e->size != 0x60)','else if (__builtin_expect(e->size != 0x60, 0))'),
            'gl':A.replace('xb.glitch2mfg)','__builtin_expect(xb.glitch2mfg, 0))'),
            'lb':A.replace('if (loadBaseFile(e->name, e))','if (__builtin_expect(loadBaseFile(e->name, e), 0))')}.items():
    s=bdrun.sub(t,A,b,1)
    r=bdrun.score(s,['--param','builtin-expect-probability=99'])
    print(k, 'IDENT' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r['L'], r['notes']))
