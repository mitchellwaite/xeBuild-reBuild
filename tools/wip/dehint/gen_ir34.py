"""getImageSmc: lit_smc only fixes the string order; bring the zero arm (and/or the bad arm) up in the source so the
string is expanded first, no asm."""
FOCUS = ['_getImageSmc']
LIT = '''	/* code-free: emits the zero/bad arms' string (at the end) first, as the original */
	__asm__("" : : "i"("smc.bin should not be at 0x%x, trying 0x1000\\n"));
'''
Z0 = '''	if (!addr)
		goto zero;
	else {
		vhot: __attribute__((hot));
	}
zback:
'''
ZEND = '''zero:
	log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
	addr = 0x1000;
	goto zback;
'''
AX1 = [
    ('a', [(LIT, ''), (Z0, '''	if (!addr) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
	} else {
		vhot: __attribute__((hot));
	}
'''), (ZEND, '')]),
    ('b', [(LIT, ''), (Z0, '''	if (addr)
		goto vhot;
	log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
	addr = 0x1000;
	goto zback;
vhot: __attribute__((hot));
zback:
'''), (ZEND, '')]),
    ('c', [(LIT, ''), (Z0, '''	if (!addr) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
		goto zback;
	} else {
		vhot: __attribute__((hot));
	}
zback:
'''), (ZEND, '')]),
    ('d', [(LIT, ''), (Z0, '''	if (!addr) {
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
	}
	else {
		vhot: __attribute__((hot));
	}
	if (0) {
bad:
		bhot: __attribute__((hot));
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
		goto bback;
	}
'''), (ZEND, ''), ('''bad:
	bhot: __attribute__((hot));
	log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
	addr = 0x1000;
	goto bback;
}''', '}')]),
]
AXES = [AX1]
