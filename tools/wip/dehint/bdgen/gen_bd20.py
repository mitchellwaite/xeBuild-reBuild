"""checkBl's crc expects as a static helper: with no-early-inlining it's still a call at
profile_estimate, so `crc != c` gets no PRED_OPCODE_NONEQUAL (4.8% -> 2%)"""
FOCUS = ['_checkBl']
E = '__builtin_expect(crc != c, 0)'
D = '''__attribute__((optimize("no-early-inlining")))
int checkBl('''
HELP = {
    'eq': 'static int crcSame(uint32_t a, uint32_t b)\n{\n	return a == b;\n}\n\n',
    'ne': 'static int crcDiff(uint32_t a, uint32_t b)\n{\n	return a != b;\n}\n\n',
}
LAST = '''		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	default:'''
A = [
    ('same', [(D, HELP['eq'] + D), (E, '!crcSame(crc, c)')]),
    ('diff', [(D, HELP['ne'] + D), (E, 'crcDiff(crc, c)')]),
    ('same8', [(D, HELP['eq'] + D), (E, '!crcSame(crc, c)'), (LAST, LAST.replace('crc != c', '!crcSame(crc, c)'))]),
    ('diff8', [(D, HELP['ne'] + D), (E, 'crcDiff(crc, c)'), (LAST, LAST.replace('crc != c', 'crcDiff(crc, c)'))]),
]
AXES = [A]
