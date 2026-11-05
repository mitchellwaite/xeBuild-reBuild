"""exp_t9, exp_t10: the CF/CG fallback as a static function shared by both loaders (calls inside, not early inlined)."""
L1 = '''		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
'''
L2 = '''				if (r) {
					if (__builtin_expect(type == 9, 0)) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
					if (r)
						break;
				}
'''
HEAD = '/* the default 0x60-byte bootloader (type 24) */\n'
H = {
    'a': '''/* a CF or CG missing from disk: from the system update, if there is one */
static int loadFromUpdate(struct fileent *e, int type)
{
	if (type == 9)
		return suGetCF(&e->data, &e->size);
	if (type == 10)
		return suGetCG(&e->data, &e->size);
	return 0;
}

''',
    'b': '''/* a CF or CG missing from disk: from the system update, if there is one */
static int loadFromUpdate(struct fileent *e, int type)
{
	int r = 0;

	if (type == 9)
		r = suGetCF(&e->data, &e->size);
	else if (type == 10)
		r = suGetCG(&e->data, &e->size);
	return r;
}

''',
}
CONSOLE = '''				if (r) {
					if (loadFromUpdate(e, type))
						r = 0;
					if (r)
						break;
				}
'''
CONSOLE2 = '''				if (r) {
					if (!loadFromUpdate(e, type))
						break;
					r = 0;
				}
'''
BL = {
    'orig': None,
    'h': '''		if (*pr) {
			if (!loadFromUpdate(e, type))
				break;
			if (type == 10)
				goto chk;
		}
''',
}
A = []
for hk, h in H.items():
    for ck, c in (('c1', CONSOLE), ('c2', CONSOLE2)):
        A.append((hk + ck, [(HEAD, h + HEAD), (L2, c)]))
        A.append((hk + ck + 'bl', [(HEAD, h + HEAD), (L2, c), (L1, BL['h'])]))
    A.append((hk + 'blonly', [(HEAD, h + HEAD), (L1, BL['h'])]))
AXES = [A]
