"""flpi.py: parseIni's tail as a generator over natural shapes.

gen(flash, sec, seclen, flen, raw, dead) -> whole source.
  flash: cur (goto noFlashfs) | nest (if != -1 {all} else err) | early (if == -1 {err})
         | else (if != -1 {loop} else err, closed before [security])
  sec:   cur | nest (if != -1 {...return 1} else err) | early | after (else err; then ok tail)
  seclen: goto (secName at the end) | nest | inline
  flen:  asm (string hint + early check) | nest (if <= 1023 {rest} else err) | plain
  raw:   asm (string hint + "not found" first) | else (found first, else not found) | plain
  dead:  all | set of names to remove (see DEAD)
"""
import itertools, re, sys
import fllib as L

DEAD = {
 'off1': '\t\t\t\tif (off < -1)\n\t\t\t\t\tbuf[0] = 1;\n',                       # devkit arm
 'comma': '\t\tif (comma < -1) {\n\t\t\tbuf[0] = 1;\n\t\t\tbuf[1] = 1;\n\t\t}\n',
 'i': '\tif (i < -1)\n\t\tbuf[0] = 1;\n',
 'off2': '\t\t\tif (off < -1)\n\t\t\t\tbuf[0] = 1;\n\t\t\tnul = memFindChar(p, 0, size - pos);\n',  # rawpatch loop (special)
 'nul': '\t\tif (nul < -1)\n\t\t\tbuf[0] = 1;\n',
 'off3': '\t\tif (off < -1)\n\t\t\tbuf[0] = 1;\n\t\tif (len > 21) {\n',
 'off4': '\t\t\tif (off < -1)\n\t\t\t\tbuf[0] = 1;\n\t\t\t/* dead only',
 't': '\t\t\t{\n\t\t\t\tchar t_[4];\n\t\t\t\tstrcpy(t_, "ab");\n\t\t\t\tif (strlen(t_) != 2)\n\t\t\t\t\tbuf[0] = 1;\n\t\t\t}\n',
 'len': '\t\t\tif (len < -1)\n\t\t\t\tbuf[0] = 1;\n',
 'off5': '\t\t\t\tif (off < -1)\n\t\t\t\t\tbuf[0] = 1;\n\t\t\t\treturn 0;\n',
}
KEEP = {
 'off2': '\t\t\tnul = memFindChar(p, 0, size - pos);\n',
 'off3': '\t\tif (len > 21) {\n',
 'off4': '\t\t\t/* dead only',
 'off5': '\t\t\t\treturn 0;\n',
}
ALLDEAD = list(DEAD)


def rmdead(s, names):
    for n in names:
        if n in ('off1',):
            # the only one directly after the devk sprintf
            o = 'sprintf(tmp, "%s_devk_%s.bin", xb.kernelStr, xb.outName);\n'
            s = L.sub(s, o + DEAD[n], o)
        else:
            s = L.sub(s, DEAD[n], KEEP.get(n, ''))
    return s


NOSEC = '''log_printf(0, "\\n******* ERROR: could not find label [flashfs] in file list ini\\n");
	free(buf);
	return 0;
'''
SECNAME = '''log_printf(0, "\\n******* ERROR: file in [security] has greater than %d chars in it's name!\\n", 21);
	free(buf);
	return 0;
'''
OK = '''free(buf);
	log_printf(1, "------ ini parsing completed ------\\n\\n");
	return 1;
'''


def secloop(seclen):
    head = '''	xb.nFlashFiles2 = 0;
	log_printf(1, "\\nini: label [security] found\\n");
	end = off + memFindChar(&buf[off], '[', size - off);
	pos = off;
	for (i = 0; i < 10; i++) {
		p = &buf[pos];
		comma = memFindChar(p, ',', size - pos);
		nul = memFindChar(p, 0, size - pos);
		if (comma > nul) {
			noCrc = 1;
			len = nul;
		} else {
			noCrc = 0;
			len = comma;
		}
'''
    body = '''		strncpy(xb.flashFiles[i], (char *)p, len);
		xb.flashFiles[i][len] = 0;
		pos = pos + len + 1;
		if (!noCrc) {
			n = memFindChar(&buf[pos], 0, size - pos);
			if (n == 0)
				xb.flashCrc[i] = 0;
			else if (n != 8) {
				/* sic: names the [flashfs] file */
				log_printf(0, "\\n******* ERROR: crc data for file '%s' in ini is incorrect size!\\n", xb.firmware[i]);
				free(buf);
				return 0;
			} else {
				strncpy(tmp, (char *)&buf[pos], 8);
				tmp[8] = 0;
				xb.flashCrc[i] = myatox32(tmp, 0);
			}
			pos = pos + n + 1;
		} else
			xb.flashCrc[i] = 0;
		/* re-read, not a crc variable: FRE's later PHI orders the n == 0
		   path's copies crc first */
		log_printf(1, "found (%d) '%s' crc: 0x%08x\\n", ++xb.nFlashFiles2, xb.flashFiles[i], xb.flashCrc[i]);
		if (pos >= end)
			i = 10;
	}
'''
    if seclen == 'goto':
        return head + '		if (len > 21)\n			goto secName;\n' + body
    if seclen == 'inline':
        return head + '		if (len > 21) {\n			' + SECNAME.replace('\n\t', '\n\t\t\t') + '		}\n' + body
    # nest: the good path in the if, the error in the else
    bl = body.rindex('		if (pos >= end)')
    return (head + '		if (len <= 21) {\n' + body[:bl] + '		} else {\n			' +
            SECNAME.replace('\n\t', '\n\t\t\t') + '		}\n' + body[bl:])


def tail(flash, sec, seclen, secname_tail=True):
    """text from [security] on; the caller has placed flash's own closing."""
    a3 = ''
    if seclen == 'goto':
        a3 = '''	__asm__("" :: "i"("\\n******* ERROR: file in [security] has greater than %d chars in it's name!\\n"));\n'''
    srch = '	off = memFindStr(buf, size, "[security]", 1);\n'
    loop = secloop(seclen)
    if sec == 'cur':
        t = '	goto secSearch;\nnoSecurity:\n	' + NOSEC + 'secSearch:\n' + srch + '	if (off == -1)\n		goto noSecurity;\n' + loop + a3 + '	' + OK
    elif sec == 'nest':
        t = srch + '	if (off != -1) {\n' + loop + a3 + '	' + OK + '	} else {\n	' + NOSEC + '	}\n'
    elif sec == 'early':
        t = srch + '	if (off == -1) {\n	' + NOSEC + '	}\n' + loop + a3 + '	' + OK
    elif sec == 'after':
        t = srch + '	if (off != -1) {\n' + loop + '	} else {\n	' + NOSEC + '	}\n' + a3 + '	' + OK
    return t


def gen(flash='cur', sec='cur', seclen='goto', flen='asm', raw='asm', dead=(), src=None):
    s = src if src is not None else L.base()
    s = rmdead(s, dead)
    # [security] on
    a = s.index('	/* [security]: name[,crc] */\n')
    fe = s.index('/* offset of the value after `key` in buf, or -1 */')
    t = tail(flash, sec, seclen)
    if flash == 'else':
        t = '	} else {\n	' + NOSEC + '	}\n' + t
    end = ''
    if flash == 'cur':
        end = 'noFlashfs:\n	' + NOSEC
    elif flash == 'nest':
        end = '	} else {\n	' + NOSEC + '	}\n'
    if seclen == 'goto':
        end += 'secName:\n	' + SECNAME
    s = s[:a] + t + end + '}\n\n' + s[fe:]
    # [flashfs] head
    fo = '	if (off == -1)\n		goto noFlashfs;\n	xb.nFirmware = 0;\n'
    if flash in ('nest', 'else'):
        s = L.sub(s, fo, '	if (off != -1) {\n	xb.nFirmware = 0;\n')
    elif flash == 'early':
        s = L.sub(s, fo, '	if (off == -1) {\n	' + NOSEC + '	}\n	xb.nFirmware = 0;\n')
    # flashfs len
    m = re.search(r'\t\t/\* the original checks the path length.*?return 0;\n\t\t\}\n', s, re.S)
    if flen == 'plain':
        s = s[:m.start()] + '''		if (len > 1023) {
			log_printf(0, "\\n******* ERROR: file in [flashfs] has greater than %d chars in it's path!\\n", 1023);
			free(buf);
			return 0;
		}
''' + s[m.end():]
    elif flen in ('nest', 'nest2'):
        s = s[:m.start()] + '		if (len <= 1023) {\n' + s[m.end():]
        k = s.index('		log_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", ++xb.nFirmware')
        k2 = s.index('		if (pos >= size)\n', k)
        if flen == 'nest2':  # the end-of-section test inside the good arm too
            k2 = s.index('			i = 256;\n', k2) + len('			i = 256;\n')
        s = s[:k2] + '''		} else {
			log_printf(0, "\\n******* ERROR: file in [flashfs] has greater than %d chars in it's path!\\n", 1023);
			free(buf);
			return 0;
		}
''' + s[k2:]
    # rawpatch
    if raw != 'asm':
        m = re.search(r'\t/\* the original logs "not found".*?"\[rawpatch\] slots are already full!\\n"\)\);\n'.replace('"\\[rawpatch\\] slots', r'%d of %d \[rawpatch\] slots'), s, re.S)
        s = s[:m.start()] + s[m.end():]
    if raw == 'else':
        o = '	if (off == -1)\n		log_printf(1, "\\n[rawpatch] label not found in ini\\n");\n	else {\n'
        s = L.sub(s, o, '	if (off != -1) {\n')
        k = s.index('	/* [flashfs]: name[,crc]')
        kk = s.rindex('	}\n', 0, k)
        s = s[:kk] + '	} else\n		log_printf(1, "\\n[rawpatch] label not found in ini\\n");\n' + s[kk + 3:]
    return s


if __name__ == '__main__':
    V = {}
    D = {'all': (), 'noT': ('t',), 'nodead': tuple(ALLDEAD)}
    for k in itertools.product(['cur', 'nest', 'early'], ['cur', 'nest', 'early', 'after'], ['goto', 'nest', 'inline'],
                               ['asm', 'nest', 'plain'], ['asm', 'else', 'plain'], D):
        V['_'.join(k)] = gen(*k[:5], dead=D[k[5]])
    print(len(V))
    rs = L.sweep(V, prefix='pi', show=40)
    with open(L.BD + '/pi.txt', 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            f.write('%s %s %s %s\n' % (sc, n, fd, sd))
