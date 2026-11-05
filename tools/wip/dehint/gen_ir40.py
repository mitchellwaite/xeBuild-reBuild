"""detectController: pin_lo2 exists to keep lo2's load before pin_lo's asm (TER would sink it past, eax is free then and the load takes it).
One asm doing both?  And spellings that keep lo2 un-TERed: a second real use of lo2 in the same test."""
FOCUS = ['_detectController']
BASE = 'tools/wip/dehint/drafts/image_read_attempt2.c'
OLD = '''				int lo2 = b[512];

				/* lo kept live past its add, so the sum takes hi's
				   register (ebp) */
				__asm__("" : : "a"(lo));
				if (lo2 + (b[513] & 0xf) * 256 == i) {
					__asm__("" : : "d"(lo2));
'''
V = {
 'two': '''				int lo2 = b[512];
				int hi2 = (b[513] & 0xf) * 256;

				__asm__("" : : "a"(lo), "d"(lo2));
				if (lo2 + hi2 == i) {
''',
 'lo2-in': '''				int lo2 = b[512];

				__asm__("" : : "a"(lo), "d"(lo2));
				if (lo2 + (b[513] & 0xf) * 256 == i) {
''',
 'both-after': '''				int lo2 = b[512];

				if (lo2 + (b[513] & 0xf) * 256 == i) {
					__asm__("" : : "a"(lo));
''',
 'r': '''				int lo2 = b[512];

				__asm__("" : : "a"(lo), "r"(lo2));
				if (lo2 + (b[513] & 0xf) * 256 == i) {
''',
 'mem': '''				int lo2 = b[512];
				int c = b[513] & 0xf;

				__asm__("" : : "a"(lo) : "memory");
				if (lo2 + c * 256 == i) {
''',
}
AXES = [[(k, [(OLD, v)]) for k, v in V.items()]]
