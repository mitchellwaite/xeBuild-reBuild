"""flx3.py: natural-shape axes over parseIni, sampled in combination.

EDITS: named edits as (old, new) replacements, applied once each.  AXES: groups of alternatives
(at most one per group).  sample(N): random combinations over dead subsets, with marginal stats.
python flx3.py <N> <seed> [focus: nest|asm] [keep...]
"""
import random, re, sys
from collections import defaultdict
import fllib as L, flx as X

FLHEAD = "\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n"
FLINIT = "\t\t\tnoCrc = 1;\n\t\t\tlen = nul;\n"
BLHEAD = "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n"
SECHEAD = "\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t} else {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t}\n"
FORBL = "\t\tfor (i = 0; i < nbl; ) {\n"
FORRAW = "\t\tfor (i = xb.nRawPatches; i < 16; i++) {\n"
FORFL = "\t\tfor (i = 0; i < 256; i++) {\n"
FORSEC = "\t\tfor (i = 0; i < 10; i++) {\n"
DECL = "\tint size, off, end, pos, len, nul, comma, n, i, nbl;\n"


def topdel(*names):
    """edit list removing names from the int decl line"""
    return [('__TOPDEL__', ','.join(names))]


AXES = {
 # [flashfs]'s flag head
 'flh': {
  'nested': [(FLHEAD, "\t\t\tif (comma >= 0) {\n\t\t\t\tif (comma < nul) {\n\t\t\t\t\tlen = comma;\n\t\t\t\t\tnoCrc = 0;\n\t\t\t\t}\n\t\t\t}\n")],
  'ne1': [(FLHEAD, FLHEAD.replace('comma >= 0', 'comma != -1'))],
  'swapset': [(FLHEAD, FLHEAD.replace("len = comma;\n\t\t\t\tnoCrc = 0;", "noCrc = 0;\n\t\t\t\tlen = comma;"))],
  'else': [(FLINIT + FLHEAD, FLHEAD[:-1] + " else {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n")],
  'else2': [(FLINIT + FLHEAD, FLHEAD[:-1] + " else {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n")],
  'else3': [(FLINIT + FLHEAD, "\t\t\tif (comma < 0 || comma >= nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t} else {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n")],
  'lenfirst': [(FLINIT, "\t\t\tlen = nul;\n\t\t\tnoCrc = 1;\n")],
  'lencmp': [(FLINIT + FLHEAD, "\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul)\n\t\t\t\tlen = comma;\n"),
             ("\t\t\tif (!noCrc) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb", "\t\t\tif (len == comma) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb")],
  'lencmp2': [(FLINIT + FLHEAD, "\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul)\n\t\t\t\tlen = comma;\n"),
             ("\t\t\tif (!noCrc) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb", "\t\t\tif (len != nul) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb")],
  'commatest': [(FLINIT + FLHEAD, "\t\t\tlen = nul;\n\t\t\tif (comma >= 0 && comma < nul)\n\t\t\t\tlen = comma;\n"),
             ("\t\t\tif (!noCrc) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb", "\t\t\tif (comma >= 0 && comma < nul) {\n\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb")],
 },
 'blh': {
  'swap': [(BLHEAD, "\t\t\tnoCrc = 0;\n\t\t\tlen = comma;\n\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n")],
  'swap2': [(BLHEAD, "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (comma > nul) {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n")],
  'else': [(BLHEAD, "\t\t\tif (comma > nul) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t} else {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n")],
  'sec': [(BLHEAD, SECHEAD)],
  'le': [(BLHEAD, "\t\t\tif (comma <= nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t} else {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n")],
  'lt': [(BLHEAD, "\t\t\tlen = comma;\n\t\t\tnoCrc = 0;\n\t\t\tif (nul < comma) {\n\t\t\t\tlen = nul;\n\t\t\t\tnoCrc = 1;\n\t\t\t}\n")],
  'init1': [(BLHEAD, "\t\t\tlen = nul;\n\t\t\tnoCrc = 1;\n\t\t\tif (comma <= nul) {\n\t\t\t\tlen = comma;\n\t\t\t\tnoCrc = 0;\n\t\t\t}\n")],
 },
 'sech': {
  'swap': [(SECHEAD, SECHEAD.replace("noCrc = 1;\n\t\t\t\tlen = nul;", "len = nul;\n\t\t\t\tnoCrc = 1;"))],
  'swap2': [(SECHEAD, SECHEAD.replace("noCrc = 0;\n\t\t\t\tlen = comma;", "len = comma;\n\t\t\t\tnoCrc = 0;"))],
  'swap3': [(SECHEAD, SECHEAD.replace("noCrc = 1;\n\t\t\t\tlen = nul;", "len = nul;\n\t\t\t\tnoCrc = 1;").replace("noCrc = 0;\n\t\t\t\tlen = comma;", "len = comma;\n\t\t\t\tnoCrc = 0;"))],
  'init': [(SECHEAD, BLHEAD)],
  'le': [(SECHEAD, "\t\t\tif (comma <= nul) {\n\t\t\t\tnoCrc = 0;\n\t\t\t\tlen = comma;\n\t\t\t} else {\n\t\t\t\tnoCrc = 1;\n\t\t\t\tlen = nul;\n\t\t\t}\n")],
 },
 'type': {
  'int': [('\tuint32_t noCrc;\n', '\tint noCrc;\n')],
  'char': [('\tuint32_t noCrc;\n', '\tchar noCrc;\n')],
 },
 'rawend': {'break': [('\t\t\tif (pos >= end)\n\t\t\t\ti = 16;\n', '\t\t\tif (pos >= end)\n\t\t\t\tbreak;\n')]},
 'flend': {'break': [('\t\t\tif (pos >= size)\n\t\t\t\ti = 256;\n', '\t\t\tif (pos >= size)\n\t\t\t\tbreak;\n')]},
 'secend': {'break': [('\t\t\tif (pos >= end)\n\t\t\t\ti = 10;\n', '\t\t\tif (pos >= end)\n\t\t\t\tbreak;\n')]},
 'blfor': {'for': [(FORBL, "\t\tfor (i = 0; i < nbl; i++) {\n"), ('i + 1, xb.files[blOrder[i]].name', 'i + 1, xb.files[blOrder[i]].name'), ('\t\t\ti++;\n\t\t\tif (pos > end) {', '\t\t\tif (pos > end) {')]},
 's': {
  'scope': [('\tchar *s;\n', ''), ("\t\t\t\ts = strrchr(xb.firmware[i], '/');", "\t\t\t\tchar *s = strrchr(xb.firmware[i], '/');")],
  'if': [("\t\t\t\ts = s ? s + 1 : xb.firmware[i];\n", "\t\t\t\tif (s)\n\t\t\t\t\ts++;\n\t\t\t\telse\n\t\t\t\t\ts = xb.firmware[i];\n")],
  'both': [('\tchar *s;\n', ''), ("\t\t\t\ts = strrchr(xb.firmware[i], '/');", "\t\t\t\tchar *s = strrchr(xb.firmware[i], '/');"),
           ("\t\t\t\ts = s ? s + 1 : xb.firmware[i];\n", "\t\t\t\tif (s)\n\t\t\t\t\ts++;\n\t\t\t\telse\n\t\t\t\t\ts = xb.firmware[i];\n")],
  'ifn': [("\t\t\t\ts = s ? s + 1 : xb.firmware[i];\n", "\t\t\t\tif (s == NULL)\n\t\t\t\t\ts = xb.firmware[i];\n\t\t\t\telse\n\t\t\t\t\ts++;\n")],
  'nested': [("\t\t\t\tif (s == NULL)\n\t\t\t\t\ts = strrchr(xb.firmware[i], '\\\\');\n", "\t\t\t\tif (s == NULL) {\n\t\t\t\t\ts = strrchr(xb.firmware[i], '\\\\');\n\t\t\t\t}\n")],
 },
 'e': {'scope': [('\tstruct fileent *e;\n', ''), ('\t\te = &xb.files[i];\n', '\t\tstruct fileent *e = &xb.files[i];\n\n')]},
 'p': {'scope': [('\tunsigned char *buf, *p;\n', '\tunsigned char *buf;\n'), ('\t\t\tp = &buf[pos];\n', '\t\t\tunsigned char *p = &buf[pos];\n', 'all')]},
 'n': {'scope': [('__TOPDEL__', 'n'), ('\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n', '\t\t\t\tint n = memFindChar(&buf[pos], 0, size - pos);\n', 'all')]},
 'cn': {'scope': [('__TOPDEL__', 'comma,nul'),
          (FORBL, FORBL + '\t\t\tint comma, nul;\n\n'), (FORRAW, FORRAW + '\t\t\tint nul, comma;\n\n'),
          (FORFL, FORFL + '\t\t\tint nul, comma;\n\n'), (FORSEC, FORSEC + '\t\t\tint comma, nul;\n\n')]},
 'lenc': {'scope': [('__TOPDEL__', 'len,noCrcL'),
          ('\tuint32_t noCrc;\n', ''),
          ('\t\tmemset(xb.kernelStr, 0, sizeof(xb.kernelStr));\n', '\t\tint len;\n\n\t\tmemset(xb.kernelStr, 0, sizeof(xb.kernelStr));\n'),
          (FORBL, FORBL + '\t\t\tint len;\n\t\t\tuint32_t noCrc;\n\n'),
          (FORFL, FORFL + '\t\t\tint len;\n\t\t\tuint32_t noCrc;\n\n'), (FORSEC, FORSEC + '\t\t\tint len;\n\t\t\tuint32_t noCrc;\n\n')]},
 'crc': {
  'scope': [('\tuint32_t crc;\n', ''), (FORFL, FORFL + '\t\t\tuint32_t crc;\n\n')],
  'late': [('\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n', '\t\t\t\t\tcrc = 0;\n'),
           ('\t\t\t\t\tcrc = xb.firmwareCrc[i] = myatox32(tmp, 0);\n', '\t\t\t\t\tcrc = myatox32(tmp, 0);\n'),
           ('\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n', '\t\t\t\tcrc = 0;\n'),
           ("\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware", "\t\t\txb.firmwareCrc[i] = crc;\n\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware")],
  'init': [('\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n', '\t\t\t\t\tcrc = 0;\n'),
           ('\t\t\t\t\tcrc = xb.firmwareCrc[i] = myatox32(tmp, 0);\n', '\t\t\t\t\tcrc = myatox32(tmp, 0);\n'),
           ('\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n', '\t\t\t\tcrc = 0;\n'),
           ("\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware, xb.firmware[i], crc);", "\t\t\txb.firmwareCrc[i] = crc;\n\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", ++xb.nFirmware, xb.firmware[i], xb.firmwareCrc[i]);")],
  'noL': [('\tuint32_t crc;\n', ''),
           ('\t\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n', '\t\t\t\t\txb.firmwareCrc[i] = 0;\n'),
           ('\t\t\t\t\tcrc = xb.firmwareCrc[i] = myatox32(tmp, 0);\n', '\t\t\t\t\txb.firmwareCrc[i] = myatox32(tmp, 0);\n'),
           ('\t\t\t\tcrc = xb.firmwareCrc[i] = 0;\n', '\t\t\t\txb.firmwareCrc[i] = 0;\n'),
           ("++xb.nFirmware, xb.firmware[i], crc);", "++xb.nFirmware, xb.firmware[i], xb.firmwareCrc[i]);")],
 },
 'last': {
  'else': [("\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\txb.firmware[i][len - 1] = 0;", "\t\t\tif (xb.firmware[i][len - 1] == '1')\n\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\telse if (xb.firmware[i][len - 1] == '2')\n\t\t\t\txb.firmware[i][len - 1] = 0;")],
  'after': [("\t\t\tpos = pos + len + 1;\n\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\txb.firmware[i][len - 1] = 0;\n", "\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\txb.firmware[i][len - 1] = 0;\n\t\t\tpos = pos + len + 1;\n")],
 },
 # temporaries FRE/DOM merge (names freed late, no code left behind)
 'blleft': {'l': [(FORBL, FORBL + '\t\t\tint left = size - pos;\n\n'),
   ("\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tlen = comma;", "\t\t\tcomma = memFindChar(p, ',', left);\n\t\t\tnul = memFindChar(p, 0, left);\n\t\t\tlen = comma;")]},
 'rawleft': {'l': [(FORRAW, FORRAW + '\t\t\tint left = size - pos;\n\n'),
   ("\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, ',', size - pos);\n\t\t\tif (comma == -1", "\t\t\tnul = memFindChar(p, 0, left);\n\t\t\tcomma = memFindChar(p, ',', left);\n\t\t\tif (comma == -1")]},
 'flname': {'n': [(FORFL, FORFL + '\t\t\tchar *name = xb.firmware[i];\n\n'),
   ("\t\t\tstrncpy(xb.firmware[i], (char *)p, len);\n\t\t\txb.firmware[i][len] = 0;", "\t\t\tstrncpy(name, (char *)p, len);\n\t\t\tname[len] = 0;"),
   ("s = strrchr(xb.firmware[i], '/');", "s = strrchr(name, '/');"),
   ("s = strrchr(xb.firmware[i], '\\\\');", "s = strrchr(name, '\\\\');"),
   ("xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n\t\t\t\txb.firmware[i][len - 1] = 0;", "name[len - 1] == '1' || name[len - 1] == '2')\n\t\t\t\tname[len - 1] = 0;")],
  'c': [(FORFL, FORFL + '\t\t\tchar *name = xb.firmware[i];\n\n'),
   ("\t\t\tstrncpy(xb.firmware[i], (char *)p, len);\n\t\t\txb.firmware[i][len] = 0;", "\t\t\tstrncpy(name, (char *)p, len);\n\t\t\tname[len] = 0;")],
 },
 'flc': {'c': [("\t\t\tif (xb.firmware[i][len - 1] == '1' || xb.firmware[i][len - 1] == '2')\n", "\t\t\tc = xb.firmware[i][len - 1];\n\t\t\tif (c == '1' || c == '2')\n"), ('\tchar label[50];\n', '\tchar c;\n\tchar label[50];\n')]},
 'cnt': {
  'fl': [("++xb.nFirmware, xb.firmware[i]", "xb.nFirmware, xb.firmware[i]"), ("\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", xb.nFirmware", "\t\t\txb.nFirmware++;\n\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", xb.nFirmware")],
  'sec': [("++xb.nFlashFiles2, xb.flashFiles[i]", "xb.nFlashFiles2, xb.flashFiles[i]"), ("\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", xb.nFlashFiles2", "\t\t\t\txb.nFlashFiles2++;\n\t\t\t\tlog_printf(1, \"found (%d) '%s' crc: 0x%08x\\n\", xb.nFlashFiles2")],
 },
 'rawcnt': {'r': [("++xb.nRawPatches, xb.rawPatch[i].name", "xb.nRawPatches, xb.rawPatch[i].name"), ("\t\t\t\tif (xb.rawPatch[i].offset != (uint32_t)-1)\n\t\t\t\t\tlog_printf", "\t\t\t\tif (xb.rawPatch[i].offset != (uint32_t)-1) {\n\t\t\t\t\txb.nRawPatches++;\n\t\t\t\t\tlog_printf"), ("xb.rawPatch[i].offset);\n\t\t\t\telse {", "xb.rawPatch[i].offset);\n\t\t\t\t} else {")]},
 'blp': {'p': [("\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\txb.files", "\t\t\t\tp = &buf[pos];\n\t\t\t\tn = memFindChar(p, 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\txb.files")]},
 'flp': {'p': [("\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb", "\t\t\t\tp = &buf[pos];\n\t\t\t\tn = memFindChar(p, 0, size - pos);\n\t\t\t\tif (n == 0)\n\t\t\t\t\tcrc = xb")]},
 'rawpp': {'p': [("\t\t\t\tn = memFindChar(&buf[pos], 0, size - pos);\n\t\t\t\tif (n == 0 || n > 10)", "\t\t\t\tp = &buf[pos];\n\t\t\t\tn = memFindChar(p, 0, size - pos);\n\t\t\t\tif (n == 0 || n > 10)"), ("\t\t\t\tstrncpy(tmp, (char *)&buf[pos], n);", "\t\t\t\tstrncpy(tmp, (char *)p, n);")]},
 'rawval': {'v': [("\t\t\t\txb.rawPatch[i].offset = myatou32(tmp, -1);\n\t\t\t\tif (xb.rawPatch[i].offset != (uint32_t)-1)", "\t\t\t\tcrc = myatou32(tmp, -1);\n\t\t\t\txb.rawPatch[i].offset = crc;\n\t\t\t\tif (crc != (uint32_t)-1)")]},
 'endp': {'p': [("\t\tend = off + memFindChar(&buf[off], '[', size - off);\n\t\tlog_printf(1, \"\\nini: label [rawpatch] found\\n\");", "\t\tp = &buf[off];\n\t\tend = off + memFindChar(p, '[', size - off);\n\t\tlog_printf(1, \"\\nini: label [rawpatch] found\\n\");")]},
 'rawn': {
  'or': [('\t\t\t\tif (n == 0 || n > 10) {', '\t\t\t\tif (n > 10 || n == 0) {')],
 },
 'rawc': {
  'lt': [('\t\t\tif (comma == -1 || comma >= nul) {', '\t\t\tif (comma < 0 || comma >= nul) {')],
  'order': [('\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tcomma = memFindChar(p, \',\', size - pos);\n\t\t\tif (comma == -1', '\t\t\tcomma = memFindChar(p, \',\', size - pos);\n\t\t\tnul = memFindChar(p, 0, size - pos);\n\t\t\tif (comma == -1')],
 },
 'rawp': {
  'off': [('\t\t\t\txb.rawPatch[i].offset = myatou32(tmp, -1);\n\t\t\t\tif (xb.rawPatch[i].offset != (uint32_t)-1)', '\t\t\t\txb.rawPatch[i].offset = myatou32(tmp, -1);\n\t\t\t\tif (xb.rawPatch[i].offset != -1)')],
  'pos': [('\t\t\t\tpos = pos + n + 1;\n\t\t\t\txb.rawPatch[i].offset = myatou32(tmp, -1);\n', '\t\t\t\txb.rawPatch[i].offset = myatou32(tmp, -1);\n\t\t\t\tpos = pos + n + 1;\n')],
 },
}


def apply(s, choices):
    """choices: {axis: value}"""
    tops = []
    for ax, val in choices.items():
        for ed in AXES[ax][val]:
            o, w = ed[0], ed[1]
            if o == '__TOPDEL__':
                tops += w.split(',')
                continue
            if len(ed) > 2:
                s = s.replace(o, w)
            else:
                s = L.sub(s, o, w) if s.count(o) == 1 else s.replace(o, w, 1) if s.count(o) else _fail(ax, val, o)
    if tops:
        names = [x for x in 'size off end pos len nul comma n i nbl'.split() if x not in tops]
        s = L.sub(s, DECL, '\tint ' + ', '.join(names) + ';\n')
    return s


def _fail(ax, val, o):
    raise ValueError('%s=%s: %r' % (ax, val, o[:60]))


def ax_list(names=None):
    return list(names or AXES)


def rnd_choice(rng, p=0.25, axes=None):
    c = {}
    for ax in (axes or AXES):
        if rng.random() < p:
            c[ax] = rng.choice(list(AXES[ax]))
    return c


def label(dead, fl, c):
    return fl + '|' + '+'.join(dead) + '|' + ','.join('%s=%s' % kv for kv in sorted(c.items()))


if __name__ == '__main__':
    N = int(sys.argv[1])
    seed = int(sys.argv[2])
    focus = sys.argv[3].split(',') if len(sys.argv) > 3 else ['nest', 'asm', 'plain']
    import os
    DEADP = float(os.environ.get('DEADP', '0.6'))
    AXP = float(os.environ.get('AXP', '0.25'))
    rng = random.Random(seed)
    V = {}
    meta = {}
    tries = 0
    while len(V) < N and tries < N * 20:
        tries += 1
        fl = rng.choice(focus)
        dead = [d for d in X.ALLDEAD if rng.random() < DEADP]
        c = rnd_choice(rng, AXP)
        if 'comma' not in dead and c.get('cn'):
            continue
        try:
            s = apply(X.gen(dead, fl), c)
        except ValueError as e:
            print('skip', e)
            continue
        n = '%d' % len(V)
        V[n] = s
        meta[n] = (fl, dead, c)
    rs = L.sweep(V, prefix='a%d' % seed, show=0)
    with open(L.BD + '/x3_%d.txt' % seed, 'w', newline='\n') as f:
        for n, (sc, st, fd, sd) in rs:
            fl, dead, c = meta[n]
            f.write('%s\t%s\t%s\t%s\n' % (sc, label(dead, fl, c), fd, sd))
    # report: trick count = 8-len(dead) + asm; print top by score
    for n, (sc, st, fd, sd) in rs[:25]:
        fl, dead, c = meta[n]
        print(sc, fd, sd, label(dead, fl, c))
    print('errors', sum(1 for n, r in rs if r[0] >= 10**7))
