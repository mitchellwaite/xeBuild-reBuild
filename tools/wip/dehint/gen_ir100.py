"""fsGetFile calls the real fsFindFile (its fsValid == 1 test inlined) instead of a written-out copy with a pinned local; return forms."""
FOCUS = ['_fsGetFile']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
OLD = '''	int v = fsValid;

	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
	if (v != 1)
		return 0;
	if (!fsFind(name, &block, &len, &t, 1))
		return 0;
'''
NEW = '''
	if (!fsFindFile(name, &block, &len, &t, 1))
		return 0;
'''
NEW2 = '''
	if (fsFindFile(name, &block, &len, &t, 1) == 0)
		return 0;
'''
NEW3 = '''
	int found = fsFindFile(name, &block, &len, &t, 1);

	if (!found)
		return 0;
'''
OLDR = '''	*time = t;
	return 1;
}
'''
AXES = [[('c', [(OLD, NEW)]), ('c2', [(OLD, NEW2)]), ('f', [(OLD, NEW3)])],
        [('r1', [])]]
