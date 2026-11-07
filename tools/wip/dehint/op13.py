"""Attempt 13: applyIniOptions' cold layout.  Stretches of applyIniOptions grouped into
static helpers (IPA-inlined with their own profile), crossed with single trick removals.

python tools/wip/dehint/op13.py [alone|cross|show V+R1,R2] [variants..]
  alone: each variant by itself; cross: each variant x each removal (RMS=a,b to narrow)
  show V1,V2+R1,R2 [-v]: one combination (OUT=file writes it)"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op12x

RM = dict(op12x.RM)
FEED1 = '			if (__builtin_constant_p(xb.blSuffix[1] + 1)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 2), 0)) goto dz1; return; }\n'
FEED2 = '			if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n'
MS = '					__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG1 = '					__asm__ goto ("" :::: dz1);\n'
AG2 = '				__asm__ goto ("" :::: dz2);\n'
U1 = 'dz1:\n\t__builtin_unreachable();\n'
U2 = 'dz2:\n\t__builtin_unreachable();\n'
RM['dz1'] = [(FEED1, ''), (MS, ''), (AG1, ''), (U1, '')]
RM['dz1k'] = [(FEED1, ''), (AG1, ''), (U1, '')]          # memset kept (it is plain C then? no: cp)
RM['dzall'] = RM['dz1'] + [(FEED2, ''), (AG2, ''), (U2, '')]
RM['feeds'] = [(FEED1, ''), (FEED2, '')]
RM['ag1'] = [(AG1, ''), (MS, '')]
RM['ag2'] = [(AG2, '')]
RM['rv1ms'] = [(FEED1, ''), (MS, '')]

REVBLK = '''	if (!xb.blSuffix[0]) {
		s = getIniValue("rev");
		if (s) {
			sprintf(xb.blSuffix, "_%s", s);
			/* dead feeds that key the dummies dz1 and dz2; dz1's return
			   takes its flow off dz2's feed, which settles the demon and
			   patchsmc getIniBool tie (no dummy in parseButtonX needed) */
''' + FEED1 + FEED2 + '''		}
	}
'''
assert REVBLK  # checked against the source at run time

MACBLK = '''	if (!macidSet()) {
		s = getIniValue("macid");
		if (s) {
			stripColons(s);
			if (strlen(s) == 12) {
				if (validateString(s)) {
					for (i = 0; i < 6; i++) {
						xb.macid[i] = myatox8(s);
						s += 2;
					}
				} else {
''' + MS + AG1 + '''					log_printf(0, "***** WARNING: invalid characters in macid '");
					showHexPairs(0, s);
					log_printf(0, "' provided in ini file! Discarding!\\n", s);
				}
			} else {
				log_printf(0, "***** WARNING: invalid length macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\\n", s);
			}
		}
	}
'''

DUALBLK = '''		if (!xb.dualButton) {
			xb.dualButton = parseButton(getIniValue("dualboot"));
			if (xb.xellButton == xb.dualButton) {
				log_printf(1, "dualboot setting ignored!\\n");
''' + AG2 + '''				xb.dualButton = 0;
			}
		}
'''

DVDBLK = '''	if (!(xb.bootFlags & 0x2000000)) {
		s = getIniValue("dvdkey");
		if (s && kvSetDvdKey(s))
			xb.bootFlags |= 0x2000000;
	}
'''

CFBLK = '''	if (!xb.cfLdv) {
		INI_INT(xb.cfLdv, "cfldv", 0);
		if (xb.cfLdv > 32) {
			log_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\\n", xb.cfLdv);
			xb.cfLdv = 32;
		}
	}
'''

XB1 = op12x.XB1
XB2 = op12x.XB2
ANCHOR = '/* options from perbox files and options.ini that the command line didn\'t'


def helper(code):
    """insert a helper before applyIniOptions"""
    return (ANCHOR, code + '\n' + ANCHOR)


V = {}

# ---- rev ----
for name, body, call in [
    ('rev_v', 'static void setRev(void)\n{\n\tchar *s = getIniValue("rev");\n\n\tif (s)\n\t\tsprintf(xb.blSuffix, "_%s", s);\n}\n',
     '	if (!xb.blSuffix[0])\n		setRev();\n'),
    ('rev_vr', 'static void setRev(void)\n{\n\tchar *s = getIniValue("rev");\n\n\tif (!s)\n\t\treturn;\n\tsprintf(xb.blSuffix, "_%s", s);\n}\n',
     '	if (!xb.blSuffix[0])\n		setRev();\n'),
    ('rev_vt', 'static void setRev(void)\n{\n\tchar *s;\n\n\tif (xb.blSuffix[0])\n\t\treturn;\n\ts = getIniValue("rev");\n\tif (s)\n\t\tsprintf(xb.blSuffix, "_%s", s);\n}\n',
     '	setRev();\n'),
    ('rev_i', 'static int setRev(void)\n{\n\tchar *s = getIniValue("rev");\n\n\tif (!s)\n\t\treturn 0;\n\tsprintf(xb.blSuffix, "_%s", s);\n\treturn 1;\n}\n',
     '	if (!xb.blSuffix[0])\n		setRev();\n'),
    ('rev_s', 'static void setRev(const char *s)\n{\n\tsprintf(xb.blSuffix, "_%s", s);\n}\n',
     '	if (!xb.blSuffix[0]) {\n		s = getIniValue("rev");\n		if (s)\n			setRev(s);\n	}\n'),
    ('rev_ss', 'static void setRev(const char *s)\n{\n\tif (s)\n\t\tsprintf(xb.blSuffix, "_%s", s);\n}\n',
     '	if (!xb.blSuffix[0])\n		setRev(getIniValue("rev"));\n'),
    ('rev_n', 'static void iniSuffix(char *suffix, const char *name)\n{\n\tchar *s = getIniValue(name);\n\n\tif (s)\n\t\tsprintf(suffix, "_%s", s);\n}\n',
     '	if (!xb.blSuffix[0])\n		iniSuffix(xb.blSuffix, "rev");\n'),
]:
    V[name] = [(REVBLK, call), helper(body)]
# rev helper that keeps the feeds in the caller (base check)
V['rev_if'] = [(REVBLK, '''	if (!xb.blSuffix[0]) {
		if (setRev()) {
''' + FEED1 + FEED2 + '''		}
	}
'''), helper('static int setRev(void)\n{\n\tchar *s = getIniValue("rev");\n\n\tif (!s)\n\t\treturn 0;\n\tsprintf(xb.blSuffix, "_%s", s);\n\treturn 1;\n}\n')]

# ---- macid ----
WARN = 'static void macidWarn(const char *msg, const char *s)\n{\n\tlog_printf(0, msg);\n\tshowHexPairs(0, s);\n\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n}\n'
V['mac_w'] = [('''					log_printf(0, "***** WARNING: invalid characters in macid '");
					showHexPairs(0, s);
					log_printf(0, "' provided in ini file! Discarding!\\n", s);
''', '''					macidWarn("***** WARNING: invalid characters in macid '", s);
'''), ('''				log_printf(0, "***** WARNING: invalid length macid '");
				showHexPairs(0, s);
				log_printf(0, "' provided in ini file! Discarding!\\n", s);
''', '''				macidWarn("***** WARNING: invalid length macid '", s);
'''), helper(WARN)]
WARN2 = WARN.replace('const char *msg, const char *s', 'const char *what, const char *s').replace('log_printf(0, msg);', 'log_printf(0, "***** WARNING: invalid %s macid \'", what);')
# (other literals: not the original's .rdata, kept as a probe)
V['mac_loop'] = [('''					for (i = 0; i < 6; i++) {
						xb.macid[i] = myatox8(s);
						s += 2;
					}
''', '''					setMacid(s);
'''), helper('static void setMacid(const char *s)\n{\n\tint i;\n\n\tfor (i = 0; i < 6; i++) {\n\t\txb.macid[i] = myatox8(s);\n\t\ts += 2;\n\t}\n}\n')]
MACBODY = MACBLK.replace('\t' * 2 + 's = getIniValue("macid");', 'XX')
# whole macid read as a helper: the dz1 asm goto and memset go (labels are in the caller)
_mb = MACBLK.replace(MS, '').replace(AG1, '')
_inner = _mb[len('	if (!macidSet()) {\n'):-len('	}\n')]
_inner = '\n'.join(l[1:] if l.startswith('\t') else l for l in _inner.split('\n'))
V['mac_all'] = [(MACBLK, '	if (!macidSet())\n		macidIni();\n'),
                helper('static void macidIni(void)\n{\n\tchar *s;\n\tint i;\n\n' + _inner + '}\n')]
V['mac_alln'] = [(MACBLK, '	if (!macidSet())\n		macidIni();\n'),
                 helper('static void macidIni(void)\n{\n\tchar *s;\n\tint i;\n\n' + _inner.replace('\ts = getIniValue("macid");\n\tif (s) {', '\ts = getIniValue("macid");\n\tif (!s)\n\t\treturn;\n\t{') + '}\n')]
# the helper takes s: caller reads the value
_in2 = MACBLK.replace(MS, '').replace(AG1, '')
V['mac_s'] = [(MACBLK, '	if (!macidSet()) {\n		s = getIniValue("macid");\n		if (s)\n			macidParse(s);\n	}\n'),
              helper('static void macidParse(char *s)\n{\n\tint i;\n\n\tstripColons(s);\n\tif (strlen(s) == 12) {\n\t\tif (validateString(s)) {\n\t\t\tfor (i = 0; i < 6; i++) {\n\t\t\t\txb.macid[i] = myatox8(s);\n\t\t\t\ts += 2;\n\t\t\t}\n\t\t} else {\n\t\t\tlog_printf(0, "***** WARNING: invalid characters in macid \'");\n\t\t\tshowHexPairs(0, s);\n\t\t\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n\t\t}\n\t} else {\n\t\tlog_printf(0, "***** WARNING: invalid length macid \'");\n\t\tshowHexPairs(0, s);\n\t\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n\t}\n}\n')]
# int-returning parse (returns whether set)
V['mac_si'] = [(MACBLK, '	if (!macidSet()) {\n		s = getIniValue("macid");\n		if (s)\n			macidParse(s);\n	}\n'),
               helper('static int macidParse(char *s)\n{\n\tint i;\n\n\tstripColons(s);\n\tif (strlen(s) != 12) {\n\t\tlog_printf(0, "***** WARNING: invalid length macid \'");\n\t\tshowHexPairs(0, s);\n\t\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n\t\treturn 0;\n\t}\n\tif (!validateString(s)) {\n\t\tlog_printf(0, "***** WARNING: invalid characters in macid \'");\n\t\tshowHexPairs(0, s);\n\t\tlog_printf(0, "\' provided in ini file! Discarding!\\n", s);\n\t\treturn 0;\n\t}\n\tfor (i = 0; i < 6; i++) {\n\t\txb.macid[i] = myatox8(s);\n\t\ts += 2;\n\t}\n\treturn 1;\n}\n')]

# ---- dualboot ----
_db = DUALBLK.replace(AG2, '')
V['db_v'] = [(DUALBLK, '		if (!xb.dualButton)\n			dualbootIni();\n'),
             helper('static void dualbootIni(void)\n{\n\txb.dualButton = parseButton(getIniValue("dualboot"));\n\tif (xb.xellButton == xb.dualButton) {\n\t\tlog_printf(1, "dualboot setting ignored!\\n");\n\t\txb.dualButton = 0;\n\t}\n}\n')]
V['db_k'] = [(DUALBLK, '		if (!xb.dualButton) {\n			xb.dualButton = dualbootIni();\n		}\n'),
             helper('static uint32_t dualbootIni(void)\n{\n\tuint32_t b = parseButton(getIniValue("dualboot"));\n\n\tif (xb.xellButton == b) {\n\t\tlog_printf(1, "dualboot setting ignored!\\n");\n\t\treturn 0;\n\t}\n\treturn b;\n}\n')]

# ---- dvdkey ----
V['dvd_v'] = [(DVDBLK, '	if (!(xb.bootFlags & 0x2000000))\n		dvdkeyIni();\n'),
              helper('static void dvdkeyIni(void)\n{\n\tchar *s = getIniValue("dvdkey");\n\n\tif (s && kvSetDvdKey(s))\n\t\txb.bootFlags |= 0x2000000;\n}\n')]
V['dvd_vr'] = [(DVDBLK, '	if (!(xb.bootFlags & 0x2000000))\n		dvdkeyIni();\n'),
               helper('static void dvdkeyIni(void)\n{\n\tchar *s = getIniValue("dvdkey");\n\n\tif (!s)\n\t\treturn;\n\tif (kvSetDvdKey(s))\n\t\txb.bootFlags |= 0x2000000;\n}\n')]
V['dvd_vt'] = [(DVDBLK, '	dvdkeyIni();\n'),
               helper('static void dvdkeyIni(void)\n{\n\tchar *s;\n\n\tif (xb.bootFlags & 0x2000000)\n\t\treturn;\n\ts = getIniValue("dvdkey");\n\tif (s && kvSetDvdKey(s))\n\t\txb.bootFlags |= 0x2000000;\n}\n')]

# ---- cfldv ----
V['cf_v'] = [(CFBLK, '	if (!xb.cfLdv)\n		cfldvIni();\n'),
             helper('static void cfldvIni(void)\n{\n\tINI_INT(xb.cfLdv, "cfldv", 0);\n\tif (xb.cfLdv > 32) {\n\t\tlog_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\\n", xb.cfLdv);\n\t\txb.cfLdv = 32;\n\t}\n}\n')]

# ---- xellbutton2 / xellbutton sites ----
V['xb2_v'] = [(XB2, '''		if (!xb.xellAltButton && (xb.bootFlags & 4))
			xellAltIni();
'''), helper('static void xellAltIni(void)\n{\n\txb.xellAltButton = parseButton(getIniValue("xellbutton2"));\n\tif (!xb.xellButton)\n\t\tlog_printf(1, "alternate xell button is disabled\\n");\n}\n')]

# rev + dualboot + macid helpers combined
V['rev_v_db_v'] = V['rev_v'] + V['db_v']
V['rev_v_mac_s'] = V['rev_v'] + V['mac_s']


def apply(text, edits, strict=True):
    for old, new in edits:
        if old not in text:
            if strict:
                return None
            continue
        text = text.replace(old, new, 1)
    return text


def build(vs, rms):
    t = optlib.read_src(os.environ.get('OPBASE', optlib.SRC))
    for v in vs:
        t = apply(t, V[v])
        if t is None:
            return None
    for r in rms:
        t2 = apply(t, RM[r])
        if t2 is None:
            return None
        t = t2
    return t


def run(c):
    vs, rm = c
    t = build(vs, rm)
    if t is None:
        return c, {'compile': 'edit missing'}
    return c, optlib.score_text(t, optlib.P83)


def show(res):
    for (vs, rm), r in sorted(res, key=lambda x: x[1].get('total', 99999)):
        print('%-22s %-10s %s' % (','.join(vs) or '-', ','.join(rm) or '-', optlib.fmt(r)))


def main():
    a = sys.argv[1:]
    mode = a.pop(0) if a else 'alone'
    if mode == 'show':
        vs, _, rm = a[0].partition('+')
        vs = [x for x in vs.split(',') if x]
        rm = [x for x in rm.split(',') if x]
        t = build(vs, rm)
        if os.environ.get('OUT'):
            open(os.environ['OUT'], 'w', newline='\n').write(t)
        if '-v' in a:
            optlib.vdiff(t, optlib.P83)
        else:
            show([run((vs, rm))])
        return
    vs = a or list(V)
    if mode == 'alone':
        combos = [([v], []) for v in vs]
    else:
        rms = os.environ.get('RMS', ','.join(RM)).split(',')
        combos = [([v], [r]) for v in vs for r in rms] + [([], [r]) for r in rms]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, combos))
    show(res)


if __name__ == '__main__':
    main()
