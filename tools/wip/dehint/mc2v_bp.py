# clientBinPatch: the edi refs and the count pin
D = '''					/* code-free hints: edi refs raise LRA's edi usage so the
					   post-loop len - 512 reload takes esi; the count use
					   orders its reload thread before start's (count esi) */
					{ int r; __asm__ volatile("" : "=D"(r)); __asm__ volatile("" :: "D"(r)); }
					{ int r; __asm__ volatile("" : "=D"(r)); __asm__ volatile("" :: "D"(r)); }
'''
R = '''					__asm__("" :: "r"(count));
'''
V = {
    'noD': [(D, '')],
    'noR': [(R, '')],
    'none': [(D, ''), (R, '')],
}
