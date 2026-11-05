"""getImageSmc: the size test as a switch (no REG_BR_PROB note: no ce1/ce3 hoist), attribute subsets."""
FOCUS = ['_getImageSmc']
NL = chr(10)
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc(void)'
def at(*o):
    return '__attribute__((optimize(%s))) ' % ', '.join('"%s"' % x for x in o) if o else ''
I1, I2, TM = 'no-if-conversion', 'no-if-conversion2', 'no-tree-tail-merge'
ATTRS = {'a0': at(), 'tm': at(TM), 'i2': at(I2), 'tmi': at(TM, I2), 'a3': at(I1, I2, TM), 'i1m': at(I1, TM), 'i1': at(I1), 'i12': at(I1, I2)}
AX = [(k, [(A3, q + 'void getImageSmc(void)')]) for k, q in ATTRS.items()]

OLD = '''	bad = size != 0x3000 && size != 0x3800;
	if (bad > 0) {
		o = addr != 0x800;
		if (o <= 0) {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		} else {
			size = 0x3000;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
		}
	} else {
		__asm__("" : "+D"(addr));
	}
'''
ARM = '''		o = addr != 0x800;
		if (o <= 0) {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		} else {
			size = 0x3000;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
		}
'''
PIN = '''		__asm__("" : "+D"(addr));
'''
FORMS = {
 'if': OLD,
 'mask_def_last': '	switch (size & ~0x800) {' + NL + '	case 0x3000:' + NL + PIN + '		break;' + NL + '	default:' + NL + ARM + '	}' + NL,
 'mask_def_first': '	switch (size & ~0x800) {' + NL + '	default:' + NL + ARM + '		break;' + NL + '	case 0x3000:' + NL + PIN + '	}' + NL,
 'two_def_last': '	switch (size) {' + NL + '	case 0x3000:' + NL + '	case 0x3800:' + NL + PIN + '		break;' + NL + '	default:' + NL + ARM + '	}' + NL,
 'two_def_first': '	switch (size) {' + NL + '	default:' + NL + ARM + '		break;' + NL + '	case 0x3000:' + NL + '	case 0x3800:' + NL + PIN + '	}' + NL,
 'flag_sw': '	bad = size != 0x3000 && size != 0x3800;' + NL + '	switch (bad) {' + NL + '	case 0:' + NL + PIN + '		break;' + NL + '	default:' + NL + ARM + '	}' + NL,
 'flagm_sw': '	bad = (size & ~0x800) != 0x3000;' + NL + '	switch (bad) {' + NL + '	case 0:' + NL + PIN + '		break;' + NL + '	default:' + NL + ARM + '	}' + NL,
 'maskif': OLD.replace('	bad = size != 0x3000 && size != 0x3800;', '	bad = (size & ~0x800) != 0x3000;'),
}
F = [(k, [(OLD, v)]) for k, v in FORMS.items()]
AXES = [F, AX]
