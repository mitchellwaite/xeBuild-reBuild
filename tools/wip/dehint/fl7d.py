"""fl7d.py: natural shape changes in [flashfs]: loop end, order of the error arms, the name check's nesting and its base-name search, flag and
crc forms, a local for the entry, at every subset of the dead tests T1-T3.
  python fl7d.py single            one edit at each subset
  python fl7d.py pair              pairs among the edits that moved anything, at each subset
  python fl7d.py show 'T1,T3|e1'   diff
Labels: `tests dropped|edit+edit`."""
import itertools, re, sys
import fllib as L, fl6lib as F, fl7lib as K

FA, FB = F.SECS['flash']
E = {}


def e(name, old, new, count=1):
    E.setdefault(name, []).append((old, new, count))


ENDT = "\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n"
e('brk', ENDT, "\t\t\tif (pos >= size)\n\t\t\t\tbreak;\n")
e('pos1st', "\t\t\t\tpos = pos + len + 1;\n\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
  "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\t\tpos = pos + len + 1;\n")
# name check
e('ge22', "if (len > 21) {", "if (len >= 22) {")
SEARCH = ("\t\t\t\t\ts = strrchr(xb.firmware[i], '/');\n@@T2@@\t\t\t\t\tif (s == NULL)\n\t\t\t\t\t\ts = strrchr(xb.firmware[i], '\\\\');\n\t\t\t\t\ts = s ? s + 1 : xb.firmware[i];\n")
TAIL1 = "\t\t\t\t\ts = s ? s + 1 : xb.firmware[i];\n"
e('sif', TAIL1, "\t\t\t\t\tif (s != NULL)\n\t\t\t\t\t\ts++;\n\t\t\t\t\telse\n\t\t\t\t\t\ts = xb.firmware[i];\n")
e('sifn', TAIL1, "\t\t\t\t\tif (s == NULL)\n\t\t\t\t\t\ts = xb.firmware[i];\n\t\t\t\t\telse\n\t\t\t\t\t\ts++;\n")
e('sinline', TAIL1 + "\t\t\t\t\tif (strlen(s) > 21) {", "\t\t\t\t\tif (strlen(s ? s + 1 : xb.firmware[i]) > 21) {")
LONG = ("\t\t\t\t\tif (strlen(s) > 21) {\n\t\t\t\t\t\tlog_printf(0, \"\\n******* ERROR: file in [flashfs] has greater than %d chars in it's name!\\n\", 21);\n"
        "\t\t\t\t\t\tlog_printf(0, \"\\n        Line: %s\\n\", xb.firmware[i]);\n\t\t\t\t\t\tfree(buf);\n\t\t\t\t\t\treturn 0;\n\t\t\t\t\t}\n")
e('slen', LONG, LONG.replace("if (strlen(s) > 21) {", "n = strlen(s);\n\t\t\t\t\tif (n > 21) {"))
e('slenge', LONG, LONG.replace("strlen(s) > 21", "strlen(s) >= 22"))
# flag and length
HD = "\t\t\tnoCrc = 1;\n\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n"
e('hnest', HD, "\t\t\tnoCrc = 1;\n\t\t\tlen = nul;\n\t\t\tif (comma >= 0) {\n\t\t\t\tif (comma < nul) {\n\t\t\t\t\tlen = comma;\n\t\t\t\t\tnoCrc = 0;\n\t\t\t\t}\n\t\t\t}\n")
e('helse', HD, "\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t} else {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n")
e('hor', HD, "\t\t\tif (comma < 0 || comma >= nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t} else {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n")
e('hswap', HD, "\t\t\tlen = nul;\n\t\t\tnoCrc = 1;\n\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n")
e('hne', HD, HD.replace("comma >= 0 &&", "comma != -1 &&"))
e('cfirst', "\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnoCrc = 1;", "\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tnoCrc = 1;")
# the crc
CRC_NZ = ("\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n\t\t\t\t\telse if (n != 8) {")
e('crc2', "crc = xb.firmwareCrc[i] = 0;", "crc = 0;\n@@\t\t\t\t\txb.firmwareCrc[i] = 0;", 2)
e('crcv', "crc = xb.firmwareCrc[i] = myatox32(tmp, 0);", "crc = myatox32(tmp, 0);\n\t\t\t\t\t\txb.firmwareCrc[i] = crc;")
e('crcrr', "\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware, xb.firmware[i], crc);", "\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware, xb.firmware[i], xb.firmwareCrc[i]);")
e('incr', "\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware, xb.firmware[i], crc);", "\t\t\t\txb.nFirmware++;\n\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", xb.nFirmware, xb.firmware[i], crc);")
e('pospp', "\t\t\t\tpos = pos + len + 1;\n", "\t\t\t\tpos += len + 1;\n")
e('last', "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
  "\t\t\t\tif (xb.firmware[i][len - 1] == '1')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\t\telse if (xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n")
e('lastc', "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
  "\t\t\t\t{\n\t\t\t\t\tchar c = xb.firmware[i][len - 1];\n\n\t\t\t\t\tif (c == '1' || c == '2')\n\t\t\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\t\t}\n")
e('lastp', "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
  "\t\t\t\ts = &xb.firmware[i][len - 1];\n\t\t\t\tif (*s == '1' || *s == '2')\n\t\t\t\t\t*s = 0;\n")
e('lastsw', "\t\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n",
  "\t\t\t\tswitch (xb.firmware[i][len - 1]) {\n\t\t\t\tcase '1':\n\t\t\t\tcase '2':\n\t\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n")


def rewrite(t):
    return t.replace('@@', '')


def flip_nocrc(t):
    """if (noCrc) {zero} else {...}"""
    m = re.search(r"\t\t\t\tif \(!noCrc\) \{\n(.*?)\t\t\t\t\} else\n\t\t\t\t\tcrc = xb\.firmwareCrc\[i\] = 0;\n", t, re.S)
    return t[:m.start()] + "\t\t\t\tif (noCrc)\n\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n\t\t\t\telse {\n" + m.group(1) + "\t\t\t\t}\n" + t[m.end():]


def lenbad(t):
    """the path check returns first"""
    m = re.search(r"\t\t\tif \(len <= 1023\) \{\n(.*?)\t\t\t\} else \{\n(\t\t\t\tlog_printf\(0, \"\\n\*+ ERROR: file in \[flashfs\] has greater than %d chars in it's path!.*?)\t\t\t\}\n", t, re.S)
    return t[:m.start()] + "\t\t\tif (len > 1023) {\n" + m.group(2) + "\t\t\t}\n" + re.sub(r"(?m)^\t", '', m.group(1)) + t[m.end():]


def crcfirst8(t):
    """n == 8 first"""
    m = re.search(r"\t\t\t\t\tif \(n == 0\)\n\t\t\t\t\t\tcrc = xb\.firmwareCrc\[i\] = 0;\n\t\t\t\t\telse if \(n != 8\) \{\n(.*?)\t\t\t\t\t\} else \{\n(.*?)\t\t\t\t\t\}\n", t, re.S)
    return t[:m.start()] + "\t\t\t\t\tif (n == 8) {\n" + m.group(2) + "\t\t\t\t\t} else if (n == 0)\n\t\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n\t\t\t\t\telse {\n" + m.group(1) + "\t\t\t\t\t}\n" + t[m.end():]


def crcbad(t):
    """bad size first and returning, then the two good arms"""
    m = re.search(r"\t\t\t\t\tif \(n == 0\)\n\t\t\t\t\t\tcrc = xb\.firmwareCrc\[i\] = 0;\n\t\t\t\t\telse if \(n != 8\) \{\n(.*?)\t\t\t\t\t\} else \{\n(.*?)\t\t\t\t\t\}\n", t, re.S)
    return t[:m.start()] + "\t\t\t\t\tif (n != 0 && n != 8) {\n" + m.group(1) + "\t\t\t\t\t}\n\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n\t\t\t\t\telse {\n" + m.group(2) + "\t\t\t\t\t}\n" + t[m.end():]


def fwlocal(t):
    t = t.replace('xb.firmware[i]', 'fw')
    return t.replace("\t\t\tp = &buf[pos];\n", "\t\t\tchar *fw = xb.firmware[i];\n\n\t\t\tp = &buf[pos];\n", 1)


def namehelp(t):
    """name too long as an early exit inside the len check, without a second level of block"""
    return t


FN = {'flip': flip_nocrc, 'lenbad': lenbad, 'crc8': crcfirst8, 'crcbad': crcbad, 'fw': fwlocal}
ALL = sorted(E) + sorted(FN)


def src(lb):
    d, _, a = lb.partition('|')
    s = F.drop(F.S0, [x for x in d.split(',') if x])
    i, j = s.index(FA), s.index(FB)
    t = s[i:j]
    for nm in sorted((x for x in a.split('+') if x), key=lambda x: x in FN):
        if nm in E:
            for old, new, c in E[nm]:
                t = rewrite(L.sub(t, old, new, c))
        else:
            t = FN[nm](t)
    return s[:i] + t + s[j:]


SUBS = [','.join(c) for n in range(4) for c in itertools.combinations(('T1', 'T2', 'T3'), n)]

if __name__ == '__main__':
    m = sys.argv[1]
    if m == 'show':
        K.diff(src(sys.argv[2]))
    elif m == 'single':
        V = {}
        for d in SUBS:
            V[d + '|'] = src(d + '|')
            for a in ALL:
                V[d + '|' + a] = src(d + '|' + a)
        print(len(V))
        K.run(V, 'd1', 40)
    elif m == 'pair':
        names = sys.argv[2].split(',') if len(sys.argv) > 2 else ALL
        V = {}
        for d in SUBS:
            for a, b in itertools.combinations(names, 2):
                V[d + '|' + a + '+' + b] = src(d + '|' + a + '+' + b)
        print(len(V))
        K.run(V, 'd2', 40)
