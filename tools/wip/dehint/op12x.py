"""Attempt 12: build's late levers (types, nested ifs, helper shapes, loop ends) crossed with
single trick removals, on the current src/options.c.

python tools/wip/dehint/op12x.py [levers|cross|show L1,L2+R1,R2] [names..]
  levers: every lever alone (should be IDENTICAL to be useful as a base)
  cross:  every lever (or lever pair with PAIRS=1) x every removal
  show:   one combination; OUT=file writes it, -v diffs it
Results sorted by score."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

# trick removals (each one is a counted trick or group of them)
RM = {
    'rv2': [('			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n', '')],
    'rv2i': [('if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }',
              'if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) goto dz2;')],
    'rv1': [('			if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; return; }\n', '')],
    'bxe': [('if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {', 'if (!strnicmp(s, "power", 5)) {')],
    'bxz': [('		if (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n', '')],
    'pbe': [('else if (__builtin_expect(!strnicmp(s, "winbutton", 9), 1))', 'else if (!strnicmp(s, "winbutton", 9))')],
    'ms': [('					__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n', '')],
    'po1': [('if (__builtin_expect(setBoolOption(opt, val) == 1, 0)) {', 'if (setBoolOption(opt, val) == 1) {')],
    'po2': [('if (__builtin_expect(vlen, 0)) {', 'if (vlen) {')],
    'dz2': [('			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n', ''),
            ('				__asm__ goto ("" :::: dz2);\n', ''), ('dz2:\n\t__builtin_unreachable();\n', '')],
}

XB1 = '''		if (!xb.xellButton && (xb.bootFlags & 4)) {
			xb.xellButton = parseButtonX(getIniValue("xellbutton"));
			if (!xb.xellButton) {
				log_printf(1, "default console DVD eject button is being used to start xell\\n");
				xb.xellButton = 0x12;
			}
		}
'''
XB2 = '''		if (!xb.xellAltButton && (xb.bootFlags & 4)) {
			/* a dead edge into the remopower test: its block keeps a
			   count above its edge's */
			xb.xellAltButton = parseButton(getIniValue("xellbutton2"));
			if (!xb.xellButton)
				log_printf(1, "alternate xell button is disabled\\n");
		}
'''

# levers: natural edits that may change pass inputs without changing the code
LV = {
    # nested ifs for && in applyIniOptions
    'nx1': [(XB1, '''		if (!xb.xellButton) {
			if (xb.bootFlags & 4) {
				xb.xellButton = parseButtonX(getIniValue("xellbutton"));
				if (!xb.xellButton) {
					log_printf(1, "default console DVD eject button is being used to start xell\\n");
					xb.xellButton = 0x12;
				}
			}
		}
''')],
    'nx2': [(XB2, '''		if (!xb.xellAltButton) {
			if (xb.bootFlags & 4) {
				xb.xellAltButton = parseButton(getIniValue("xellbutton2"));
				if (!xb.xellButton)
					log_printf(1, "alternate xell button is disabled\\n");
			}
		}
''')],
    'ndk': [('''		s = getIniValue("dvdkey");
		if (s && kvSetDvdKey(s))
			xb.bootFlags |= 0x2000000;
''', '''		s = getIniValue("dvdkey");
		if (s) {
			if (kvSetDvdKey(s))
				xb.bootFlags |= 0x2000000;
		}
''')],
    # optIniBool's || as nested ifs / two tests
    'nib': [('''	if ((xb.bootFlags & set) || (xb.bootFlagsOff & set))
		on = 0;
	else if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\\n", name);
		on = 1;
	} else {
		bad = iniBoolInvalid(name);
		if (!bad) {
			on = getIniBool(name, def);
			if (on)
				log_printf(1, "Using %s option (ini file)\\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad);
			return 0;
		}
	}
''', '''	if (xb.bootFlags & set)
		on = 0;
	else if (xb.bootFlagsOff & set)
		on = 0;
	else if (perboxExists(name)) {
		log_printf(1, "Using %s option (perbox file)\\n", name);
		on = 1;
	} else {
		bad = iniBoolInvalid(name);
		if (!bad) {
			on = getIniBool(name, def);
			if (on)
				log_printf(1, "Using %s option (ini file)\\n", name);
		} else {
			log_printf(0, "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\\n", name, bad);
			return 0;
		}
	}
''')],
    # return / local types
    'tib': [('_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\t_Bool on;',
             'int optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\tint on;')],
    'tibr': [('_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{',
              'int optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{')],
    'tg': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\t_Bool on;',
            'static int optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\tint on;')],
    'tgr': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{',
             'static int optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{')],
    'tgv': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{',
             'static void optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{'),
            ('\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n}\n\n\n\n\nint optIniInt', '\t\txb.bootFlags |= set;\n\t}\n}\n\n\n\n\nint optIniInt')],
    'tbx': [('static int parseButtonX(const char *s)\n{\n\tint b = 0;', 'static uint32_t parseButtonX(const char *s)\n{\n\tuint32_t b = 0;')],
    'tbxr': [('static int parseButtonX(const char *s)', 'static uint32_t parseButtonX(const char *s)')],
    'tbxb': [('static int parseButtonX(const char *s)\n{\n\tint b = 0;', 'static int parseButtonX(const char *s)\n{\n\tuint32_t b = 0;')],
    'tpb': [('int parseButton(const char *s)\n{\n\tint b = 0;', 'int parseButton(const char *s)\n{\n\tuint32_t b = 0;')],
    'tpp': [('int parseButtonPart(const char *s)\n{\n\tint b = 0;', 'int parseButtonPart(const char *s)\n{\n\tuint32_t b = 0;')],
    'tii': [('\tint v; \\\n', '\tuint32_t v; \\\n')],
    'tmi': [('''int macidSet(void)
{
	int i;
''', '''int macidSet(void)
{
	uint32_t i;
''')],
    'tai': [('''void applyIniOptions(void)
{
	char *s;
	int i;
''', '''void applyIniOptions(void)
{
	char *s;
	uint32_t i;
''')],
    # macidSet with a result and `i = 6`
    'mi6': [('''	for (i = 0; i < 6; i++)
		if (xb.macid[i] != 0xff)
			return 1;
	return 0;
''', '''	int set = 0;

	for (i = 0; i < 6; i++)
		if (xb.macid[i] != 0xff) {
			set = 1;
			i = 6;
		}
	return set;
''')],
    # parseButtonX: !s nested / power arm as early return
    'bxr': [('''	if (__builtin_expect(!strnicmp(s, "power", 5), 1)) {
		b = 0x11;
	} else {''', '''	if (__builtin_expect(!strnicmp(s, "power", 5), 1))
		return 0x11;
	{''')],
    'bxi': [('''	if (!s) {
z:
		return 0;
	}
''', '''	if (s == NULL) {
z:
		return 0;
	}
''')],
    # memmove in stripColons? (no memcpy in options) -- the macid loop with i = 6 style index
    'mac2': [('''					for (i = 0; i < 6; i++) {
						xb.macid[i] = myatox8(s);
						s += 2;
					}
''', '''					for (i = 0; i < 6; i++)
						xb.macid[i] = myatox8(s + i * 2);
''')],
    # cfldv block: nested
    'cfn': [('''	if (!xb.cfLdv) {
		INI_INT(xb.cfLdv, "cfldv", 0);
		if (xb.cfLdv > 32) {''', '''	if (xb.cfLdv == 0) {
		INI_INT(xb.cfLdv, "cfldv", 0);
		if (xb.cfLdv > 32) {''')],
    'jt': [('	if (xb.type - BUILD_JTAG <= 3) {', '	if (xb.type >= BUILD_JTAG && xb.type <= BUILD_JTAG + 3) {')],
    'dbn': [('''		if (!xb.dualButton) {
			xb.dualButton = parseButton(getIniValue("dualboot"));''', '''		if (xb.dualButton == 0) {
			xb.dualButton = parseButton(getIniValue("dualboot"));''')],
    # non-PHI statements in the inlined helpers' return blocks (build attempt 68-70)
    'gr1': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\t_Bool on;',
             'static int optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\tint on;'),
            ('\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n}\n\n\n\n\nint optIniInt', '\t\txb.bootFlags |= set;\n\t}\n\treturn on & 1;\n}\n\n\n\n\nint optIniInt')],
    'gr2': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\t_Bool on;',
             'static int optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\tint on;'),
            ('\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n}\n\n\n\n\nint optIniInt', '\t\txb.bootFlags |= set;\n\t}\n\treturn on != 0;\n}\n\n\n\n\nint optIniInt')],
    'gr3': [('\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n}\n\n\n\n\nint optIniInt', '\t\txb.bootFlags |= set;\n\t}\n\treturn on ? 1 : 0;\n}\n\n\n\n\nint optIniInt')],
    'gr4': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\t_Bool on;',
             'static uint32_t optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\tuint32_t on;')],
    'gr5': [('static _Bool optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\t_Bool on;',
             'static int optIniBoolG(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\tint on;'),
            ('\t\txb.bootFlags |= set;\n\t}\n\treturn on;\n}\n\n\n\n\nint optIniInt', '\t\txb.bootFlags |= set;\n\t}\n\treturn on > 0;\n}\n\n\n\n\nint optIniInt')],
    # parseButtonX: result tested by the caller through a value, b as the return block's statement
    'bxv': [('static int parseButtonX(const char *s)\n{\n\tint b = 0;', 'static uint8_t parseButtonX(const char *s)\n{\n\tint b = 0;')],
    'bxv2': [('static int parseButtonX(const char *s)\n{\n\tint b = 0;', 'static int parseButtonX(const char *s)\n{\n\tuint8_t b = 0;')],
    'rvn': [('''			s = getIniValue("rev");
			if (s) {''', '''			s = getIniValue("rev");
			if (s != NULL) {''')],
}


def apply(text, names, table):
    for n in names:
        for old, new in table[n]:
            if old not in text:
                return None
            text = text.replace(old, new, 1)
    return text


def build(levers, rms):
    t = optlib.read_src(os.environ.get('OPBASE', optlib.SRC))
    t = apply(t, levers, LV)
    if t is None:
        return None
    return apply(t, rms, RM)


def run(c):
    lv, rm = c
    t = build(lv, rm)
    if t is None:
        return c, {'compile': 'edit missing'}
    fl = [] if 'param' in rm else optlib.P83
    return c, optlib.score_text(t, fl)


def show(res):
    for (lv, rm), r in sorted(res, key=lambda x: x[1].get('total', 99999)):
        print('%-16s %-10s %s' % (','.join(lv) or '-', ','.join(rm) or '-', optlib.fmt(r)))


def main():
    a = sys.argv[1:]
    mode = a.pop(0) if a else 'levers'
    if mode == 'show':
        lv, _, rm = a[0].partition('+')
        lv = [x for x in lv.split(',') if x]
        rm = [x for x in rm.split(',') if x]
        t = build(lv, rm)
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(t)
        if '-v' in a:
            optlib.vdiff(t, [] if 'param' in rm else optlib.P83)
        else:
            show([run((lv, rm))])
        return
    lvs = a or list(LV)
    if mode == 'levers':
        combos = [([l], []) for l in lvs]
    else:
        rms = os.environ.get('RMS', ','.join(RM)).split(',')
        base = [[l] for l in lvs]
        if os.environ.get('PAIRS'):
            base += [list(p) for p in itertools.combinations(lvs, 2)]
        combos = [(l, [r]) for l in base for r in rms] + [([], [r]) for r in rms]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, combos))
    show(res)


if __name__ == '__main__':
    main()
