import sys
sys.path.insert(0,'tools/wip/dehint'); import bdrun
t=open('build/bd/a45/n1.c').read()
A='''					if (r) {
						if (type == 9) {
							if (suGetCF(&e->data, &e->size))
								r = 0;
						} else if (__builtin_expect(type == 10, 0)) {
							if (suGetCG(&e->data, &e->size))
								r = 0;
						}
					}'''
V={'cgfirst':'''					if (r) {
						if (__builtin_expect(type == 10, 0)) {
							if (suGetCG(&e->data, &e->size))
								r = 0;
						} else if (type == 9) {
							if (suGetCF(&e->data, &e->size))
								r = 0;
						}
					}''',
'cfeq':A.replace('if (suGetCF(&e->data, &e->size))\n','if (suGetCF(&e->data, &e->size) == 1)\n'),
'r0':A.replace('if (r) {','if (r != 0) {'),
'two':'''					if (r && type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (r && __builtin_expect(type == 10, 0)) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}''',
}
for k,b in V.items():
    s=bdrun.sub(t,A,b,1)
    for p in (98,99):
        r=bdrun.score(s,['--param','builtin-expect-probability=%d'%p])
        print(k,p, 'IDENT' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r['L'], r['notes']))
