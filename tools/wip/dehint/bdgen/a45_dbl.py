import sys
sys.path.insert(0,'tools/wip/dehint'); import bdrun
t=open('build/bd/a45/n1.c').read()
OLD='''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}'''
V={
'd1':'''static int defaultBl60(struct fileent *e)
{
	int r = 1;

	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		r = 0;
	}
	return r;
}''',
'd2':'''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data) {
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
		return 0;
	}
	return 1;
}''',
'd4':'''static int defaultBl60(struct fileent *e)
{
	uint8_t *d = malloc(0x60);

	e->data = d;
	if (!d)
		return 1;
	e->size = 0x60;
	memcpy(d, defBl60, 0x60);
	return 0;
}''',
'd5':'''static int defaultBl60(struct fileent *e)
{
	if ((e->data = malloc(0x60)) == NULL)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}''',
'd6':'''static int defaultBl60(struct fileent *e)
{
	e->data = malloc(0x60);
	if (e->data == NULL)
		return 1;
	e->size = 0x60;
	memcpy(e->data, defBl60, 0x60);
	return 0;
}''',
}
for k,v in V.items():
    r=bdrun.score(bdrun.sub(t,OLD,v,1),['--param','builtin-expect-probability=99'])
    print(k, 'IDENT' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r['L'], r['notes']))
