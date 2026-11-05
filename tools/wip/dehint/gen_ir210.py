"""findAnchor: lit_anchor off, types of ok0, ok1, v0, v1 on the current shape (attempt 14)."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt14.c'
FOCUS = ['_findAnchor']
LIT = '''		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
'''
D = '	uint32_t v0, v1;\n	uint32_t ok0, ok1;\n'
AXES = [[('l', [(LIT, '')])],
        [(a + '.' + b, [(D, '	%s v0, v1;\n	%s ok0, ok1;\n' % (a, b))]) for a in ('uint32_t', 'int', 'unsigned long') for b in ('uint32_t', 'int', 'char', 'unsigned long')]]
