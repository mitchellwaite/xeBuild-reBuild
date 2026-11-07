import sys
sys.path.insert(0,'tools/wip/dehint'); import bdrun
t=open('build/bd/a45/n1.c').read()
A2='''						/* For review: r = 0 stands for what r = loadBl60(e) did on
						   success; it is live, and the shape is chosen for the match */
						r = 0;
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}'''
A1='''					if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}'''
V={
'else0': [(A2,'''						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
						else
							r = 0;
					}''')],
'else0b': [(A2,'''						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
						else
							r = 0;
					}'''),(A1,A1.replace('''							r = defaultBl60(e);
					}''','''							r = defaultBl60(e);
						else
							r = 0;
					}'''))],
'ifelse': [(A2,'''						if (!loadBaseFile(e->name, e) && e->size == 0x60)
							r = 0;
						else
							r = defaultBl60(e);
					}''')],
'nest1': [(A1,'''					if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
						if (!loadBaseFile(e->name, e)) {
							if (e->size != 0x60)
								r = defaultBl60(e);
						} else
							r = defaultBl60(e);
					}''')],
'jg': [(A1,A1.replace('xb.type == BUILD_JTAG || xb.glitch2mfg','xb.type == BUILD_JTAG || xb.glitch2mfg != 0'))],
'r0first': [(A1,'''					r = 0;
'''+A1)],
}
for k,v in V.items():
    s=t
    for a,b in v: s=bdrun.sub(s,a,b,1)
    for p in (98,99):
        r=bdrun.score(s,['--param','builtin-expect-probability=%d'%p])
        print(k,p, 'IDENT' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r['L'], r['notes']))
