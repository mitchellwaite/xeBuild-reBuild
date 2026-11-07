"""Attempt 45 helpers: loadBlFiles written like loadConsoleBlFiles (the switch in the loop, `r` a loop-body local, one
`r = -1` site, r tested once after the switch), built from src's own loadBl arms so every lesson since attempt 9 is in it
(case 23's `(e->size & ~3) != e->size`, case 27's `*pr` sequence, the hints' current spellings).

loop(text, fb=, fail=, tail=, c6=, rdecl=, none=, off=()) -> text with loadBl gone and loadBlFiles replaced.
  fb:   'src' (nested, CG `goto chk`), 'and9' (attempt 25's), 'con2' (loadConsoleBlFiles': r = 0 on a good fallback,
        then `if (r) break;`), 'con' (console's exactly: `if (!r) r = checkBl(..)` with the SE test inside)
  fail: 'c2' (fail: closes case 2, as attempt 26's c2), 'c23' (closes case 23, the size log falling into it),
        'each' (`r = -1` at every site, as loadConsoleBlFiles), 'post' (a label after the switch, reached only by goto,
        `if (0)`-free: the switch is followed by `if (r) { if (r == (uint32_t)-1) ..` is not used; see 'post' below)
  tail: 'src' (`if (xb.type <= 5) { if (r) goto fail; break; }`), 'plain' (`if (xb.type <= 5) break;`),
        'and' (`if (xb.type > 5 && type == 14)`)
  off:  any of exp_t10 exp_pr lab_t5le vol_fail etype cp (cp: the constant_p entry as `if (0)`)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

LB = 'static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)'
LBF = 'int loadBlFiles(void)'
COMMENT = '/* load the input file e (xb.files[i]) by its type */\n'

FB_SRC = '''			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
'''
FB_AND9 = '''			if (type == 9 && suGetCF(&e->data, &e->size))
				;
			else if (__builtin_expect(type == 10, 0) && suGetCG(&e->data, &e->size))
				goto chk;
			else
				break;
'''
# console's: a good fallback clears r; then one test
FB_CON2_HEAD = '''		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (r) {
			if (type == 9) {
				if (suGetCF(&e->data, &e->size))
					r = 0;
			} else if (__builtin_expect(type == 10, 0)) {
				if (suGetCG(&e->data, &e->size))
					r = 0;
			}
		}
		if (r)
			break;
'''
TAIL_SRC = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(r != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
TAIL_PLAIN = '''		if (xb.type <= BUILD_DEVGL16)
			break;
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
TAIL_AND = '''		if (xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
C6 = '''	case 6:
		if (!xb.cbb)
			break;
		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!r)
			r = checkBl(e->data, e->size, 6, e->crc);
		break;
'''


EXTRA = {}
FBX = {}


def arms(text):
    """loadBl's switch with *pr -> r (and the comment/blank lines kept)"""
    i, j = bdrun.fnspan(text, LB)
    f = text[i:j]
    a = f.index('\tswitch (type) {\n')
    b = f.index('\treturn;\n')
    sw = f[a:b]
    return sw.replace('*pr', 'r')


def loop(text, fb='src', fail='c2', tail='src', c6=False, rdecl='body', none='src', barrier=True, off=(), sz='src', helper=False, **more):
    sw = arms(text)
    if sz == 'and3':
        sw = bdrun.sub(sw, '(e->size & ~3) != e->size', 'e->size & 3', 1)
    for k, v in more.items():
        sw = EXTRA[k](sw, v)
    # the update arm's fallback
    old_tail = sw[sw.index('\t\tif (xb.type <= BUILD_DEVGL16) {\n'):sw.index('\tcase 6:')]
    sw = sw.replace(old_tail, {'src': TAIL_SRC, 'plain': TAIL_PLAIN, 'and': TAIL_AND}[tail], 1)
    if fb == 'and9':
        sw = bdrun.sub(sw, FB_SRC, FB_AND9, 1)
    elif fb == 'con2':
        head = '''		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (r) {
''' + FB_SRC + '''		}
'''
        sw = bdrun.sub(sw, head, FB_CON2_HEAD, 1)
    elif fb in FBX:
        # FBX[fb]: replaces the load and its fallback, up to the SE test (SE kept); 'SE' in the text moves the SE test
        head = '''		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (r) {
''' + FB_SRC + '''		}
'''
        se = sw[sw.index("\t\tif (type == 9 && e->data[0] == 'S'"):sw.index('\tchk:\n')]
        new = FBX[fb]
        if 'SE\n' in new:
            sw = sw.replace(se, '', 1)
            new = new.replace('SE\n', se)
        sw = bdrun.sub(sw, head, new, 1)
    elif fb != 'src':
        raise ValueError(fb)
    # the -1 site
    if fail == 'c2':
        sw = bdrun.sub(sw, '''		e->offset = smcSetLoad(e->size);
		if (!e->offset)
			goto fail;
		break;
''', '''		e->offset = smcSetLoad(e->size);
		if (e->offset)
			break;
	fail:
		__asm__ __volatile__("");
		r = -1;
		break;
''', 1)
    elif fail == 'c23':
        sw = bdrun.sub(sw, '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
		}
		appendAddonPatches(e);
		break;
''', '''			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
	fail:
			__asm__ __volatile__("");
			r = -1;
			break;
		}
		appendAddonPatches(e);
		break;
''', 1)
    elif fail == 'each':
        sw = sw.replace('''			goto fail;
		}
		appendAddonPatches(e);''', '''			r = -1;
			break;
		}
		appendAddonPatches(e);''', 1)
        sw = sw.replace('''		if (!e->offset)
			goto fail;''', '''		if (!e->offset)
			r = -1;''', 1)
        if 'goto fail' in sw:
            sw = sw.replace('goto fail;', '{ r = -1; break; }')
    if not barrier:
        sw = sw.replace('		__asm__ __volatile__("");\n', '').replace('			__asm__ __volatile__("");\n', '')
    if c6:
        sw = sw.replace(C6.replace('\tr = ', '\tr = '), '', 1)
        sw = sw.replace('\tswitch (type) {\n\tcase 5:', '\tswitch (type) {\n' + C6 + '\tcase 5:', 1)
    # hints off
    for k in off:
        if k == 'exp_t10':
            sw = bdrun.sub(sw, '__builtin_expect(type == 10, 0)', 'type == 10', 1)
        elif k == 'exp_pr':
            sw = bdrun.sub(sw, '__builtin_expect(r != 0, 0)', 'r != 0', 1)
        elif k == 'lab_t5le':
            sw = bdrun.sub(sw, '		t5le: __attribute__((hot));\n', '', 1)
        elif k == 'etype':
            sw = bdrun.sub(sw, '				} else if (type)\n', '				} else\n', 1)
        elif k == 'cp':
            s2 = re.sub(r'if \(\(char \*\)__builtin_constant_p\([^)]*\) == \(char \*\)1 && [^{]*\) \{', 'if (0) {', sw, 1)
            if s2 == sw:
                raise ValueError('cp')
            sw = s2
        elif k == 'vol_fail':
            if '__asm__ __volatile__("");\n' not in sw:
                raise ValueError('vol_fail')
            sw = sw.replace('		__asm__ __volatile__("");\n', '').replace('			__asm__ __volatile__("");\n', '')
        else:
            raise ValueError(k)
    if helper in ('log', 'store', 'logret', 'ret', 'cstore'):
        # the switch in a helper with r a local: 'log' logs inside and stores r once, 'store' only stores it;
        # 'logret' / 'ret' return r instead (int loadBl(e, i))
        log = '\tif (r)\n\t\tlog_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n'
        tailx = {'log': log + '\t*pr = r;\n', 'store': '\t*pr = r;\n', 'logret': log + '\treturn r;\n',
                 'ret': '\treturn r;\n', 'cstore': '\tif (r)\n\t\t*pr = r;\n'}[helper]
        rt = 'void' if helper in ('log', 'store', 'cstore') else 'uint32_t'
        args = 'struct fileent *e, uint32_t i, uint32_t *pr' if rt == 'void' else 'struct fileent *e, uint32_t i'
        nf = ('static %s loadBl(%s)\n{\n\tuint32_t r = 0;\n\tint type;\n\n\ttype = e->type;\n' % (rt, args)) + sw + tailx + '}\n'
        i, j = bdrun.fnspan(text, LB)
        t = text[:i] + nf + text[j:]
        call = 'loadBl(e, i, &r);' if rt == 'void' else 'r = loadBl(e, i);'
        lbf = (LBF + '\n{\n\tstruct fileent *e;\n\tuint32_t i;\n\tuint32_t r;\n\n\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n'
               '\t\te = &xb.files[i];\n\t\tr = 0;\n\t\tif (strnicmp(e->name, "none", 4) || e->crc)\n\t\t\t' + call + '\n')
        if helper in ('log', 'logret'):
            lbf += '\t\tif (r)\n\t\t\treturn -1;\n'
        else:
            lbf += ('\t\tif (r) {\n\t\t\tlog_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n'
                    '\t\t\treturn -1;\n\t\t}\n')
        lbf += '\t}\n\treturn 0;\n}\n'
        i, j = bdrun.fnspan(t, LBF)
        return t[:i] + lbf + t[j:]
    if helper:
        # the same arms back in src's helper (`*pr`), loadBlFiles as src
        sw2 = re.sub(r'\br\b', '*pr', sw)
        i, j = bdrun.fnspan(text, LB)
        f = text[i:j]
        a = f.index('\tswitch (type) {\n')
        b = f.index('\treturn;\n')
        end = '}\n' if fail in ('c2', 'c23', 'each') else f[b:]
        if fail == 'end':
            end = f[b:]
        nf = f[:a] + sw2 + end
        if fail != 'end' and not barrier:
            pass
        return text[:i] + nf + text[j:]
    # indent one level for the loop (cosmetic only)
    sw = ''.join(('\t\t\t' + l if l.strip() else l) for l in sw.splitlines(True))
    rd = '\t\tuint32_t r = 0;\n\n' if rdecl == 'body' else ''
    rset = '' if rdecl == 'body' else '\t\tr = 0;\n'
    top = '' if rdecl == 'body' else '\tuint32_t r;\n'
    rtest = ('\t\tif (r) {\n\t\t\tlog_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n\t\t\treturn -1;\n'
             '\t\t}\n')
    head = '\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n\t\t\tint type = e->type;\n\n'
    if none == 'src':
        guard = head + sw + '\t\t}\n' + rtest
    elif none == 'rin':
        guard = head + sw + rtest.replace('\n\t', '\n\t\t').replace('\t\tif (r)', '\t\t\tif (r)', 1) + '\t\t}\n'
    elif none == 'cont':
        guard = '\t\tif (!strnicmp(e->name, "none", 4) && !e->crc)\n\t\t\tcontinue;\n\t\ttype = e->type;\n' + sw + rtest
        top += '\tint type;\n'
    body = (LBF + '\n{\n\tstruct fileent *e;\n\tuint32_t i;\n' + top + '\n\tfor (i = 1; i < (uint32_t)xb.nFiles; i++) {\n' + rd +
            '\t\te = &xb.files[i];\n' + rset + guard + '\t}\n\treturn 0;\n}\n')
    i, j = bdrun.fnspan(text, LB)
    t = text[:i] + text[j:]
    t = t.replace(COMMENT, '', 1)
    t = t.replace('\n\n\n' + LBF, '\n\n' + LBF)
    i, j = bdrun.fnspan(t, LBF)
    return t[:i] + body + t[j:]


if __name__ == '__main__':
    import bdlib
    # python tools/wip/dehint/bdgen/a45lib.py out.c k=v ..; off=a+b; True/False for c6 (attempt 45's n1:
    # fb=con2 sz=and3 off=etype+cp+lab_t5le, the base the a45_*.py scripts read from build/bd/a45/n1.c)
    kw = dict(a.split('=', 1) for a in sys.argv[2:])
    if 'off' in kw:
        kw['off'] = tuple(filter(None, kw['off'].split('+')))
    for k in ('c6', 'barrier'):
        if k in kw:
            kw[k] = kw[k] == 'True'
    t = loop(bdlib.read_src(), **kw)
    open(sys.argv[1], 'w', newline='\n').write(t)
