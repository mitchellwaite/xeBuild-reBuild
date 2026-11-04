"""flfinal.py: build drafts/filelist_ini_final.c from src/filelist_ini.c and the accepted edits,
and check it.  Importable: edits(s) applies everything but parseIni's generator."""
import re, sys
import fllib as L, flpi as P

OPT = '''/* copy the base dir's casing of the smc, kv and patches file names; IRA's
   regional allocation keeps &st rather than dir in a register (ira-region=one) */
__attribute__((optimize("ira-region=one")))
void fixFileCase(void)
{
	char dir[1024], path[1024];
	struct stat st;
	DIR *d;
'''
OPT2 = '''/* copy the base dir's casing of the smc, kv and patches file names */
void fixFileCase(void)
{
	char dir[1024];
	DIR *d;
'''
LOOP = '''	while ((de = readdir(d)) != NULL) {
		strcpy(path, dir);
'''
LOOP2 = '''	while ((de = readdir(d)) != NULL) {
		char path[1024];
		struct stat st;

		strcpy(path, dir);
'''
FLAGS = ['-O3']
DEAD = ('off1', 'off2')
PI = ('else', 'after', 'nest', 'asm', 'else')


PPC = '''/* strip comments and invalid characters; returns the new size.  Needs
   -fno-tree-loop-vectorize (with it, PRE drops the validChars loop's
   PHI <'A', validChars[j+1]>) */
'''
PPC2 = '''/* strip comments and invalid characters; returns the new size */
'''
EXP = """		/* 35% (builtin-expect-probability=65, build.sh): the comment
		   block's memcpy path is then hot enough for the default
		   align-threshold to align it after the ret */
		if (__builtin_expect(buf[i] == ';', 0)) {
"""
EXP2 = """		if (buf[i] == ';') {
"""
VC = """		for (j = 0; j < (int)sizeof(validChars); j++)
			if ((char)buf[i] == (char)validChars[j])
				break;
		if (j == sizeof(validChars))
			buf[i] = ' ';
"""
VC2 = """		for (j = 0; j < (int)sizeof(validChars); j++)
			if ((char)buf[i] == (char)validChars[j])
				j = sizeof(validChars) + 1;
		if (j == sizeof(validChars))
			buf[i] = ' ';
"""
DA = """	/* dead (VRP drops it): its freed SSA name puts the comment loop's
	   header copy in 0xff-first order */
	if (i < 0)
		buf[0] = 1;
"""
DB = """		/* dead (VRP drops it, then the empty loop), but the profile is
		   estimated with it as the hottest block: that scales the comment
		   block and its inner loop's preheader to equal REG_FREQs, so LRA
		   assigns the inheritance of i (ebx) before &buf[i] (ecx) */
		for (j = 0; j < 44; j++)
			if (i < 0)
				buf[j] = 1;
"""


def edits(s):
    s = L.sub(s, OPT, OPT2)
    s = L.sub(s, LOOP, LOOP2)
    s = L.sub(s, PPC, PPC2)
    s = L.sub(s, EXP, EXP2)
    s = L.sub(s, VC, VC2)
    s = L.sub(s, DA, '')
    s = L.sub(s, DB, '')
    return s


def full(pi=PI, dead=DEAD, post=None):
    s = P.gen(*pi, dead=dead)
    s = edits(s)
    if post:
        s = post(s)
    return s


HDR = s0 = '''   gcc emits a function's literals in expand-time block order, so the
   original's .rdata order shows its shape: [version] and the bl label are
   tested for success with the error in the else, and [rawpatch] nests its
   name-length check.  Where the shape is pinned by layout or by the dead
   stores below, an empty asm with "i" operands emits literals early
   without changing the code. */
'''
HDR2 = '''   gcc emits a function's literals in expand-time block order, so the
   original's .rdata order shows its shape: each section is tested for
   success with the error in the else, and so are its length checks.  The
   [flashfs] path check doesn't yet (see its empty asm). */
'''


def indent(s, a, b):
    """one more tab on every line of s[a:b]"""
    t = s[a:b]
    t = ''.join('\t' + l if l.strip() else l for l in t.splitlines(True))
    return s[:a] + t + s[b:]


def block(s, start, stop):
    """indent the lines after the text `start` up to the text `stop`."""
    a = s.index(start) + len(start)
    return indent(s, a, s.index(stop, a))


def tidy(s):
    s = L.sub(s, HDR, HDR2)
    ff = '	if (off != -1) {\n'
    # [flashfs]
    k = s.index('	off = memFindStr(buf, size, "[flashfs]", 1);\n')
    s = s[:k] + s[k:].replace('	}\n\n	} else {\n	log_printf(0, "\\n******* ERROR: could not find label [flashfs]',
                              '	}\n	} else {\n	log_printf(0, "\\n******* ERROR: could not find label [flashfs]', 1)
    E1 = '	} else {\n	log_printf(0, "\\n******* ERROR: could not find label [flashfs]'
    a = s.index(ff, k) + len(ff)
    b = s.index(E1, a)
    s = indent(s, a, b)
    # its else
    a = s.index(E1, a) + len('	} else {\n')
    b = s.index('	}\n', a)
    s = indent(s, a, b)
    # [security]: name check first (its error arm is already indented)
    k = s.index('	off = memFindStr(buf, size, "[security]", 1);\n')
    a = s.index('		if (len <= 21) {\n', k) + len('		if (len <= 21) {\n')
    b = s.index('		} else {\n			log_printf(0, "\\n******* ERROR: file in [security]', a)
    s = indent(s, a, b)
    a = s.index(ff, k) + len(ff)
    b = s.index(E1, a)
    s = indent(s, a, b)
    a = s.index(E1, a) + len('	} else {\n')
    b = s.index('	}\n', a)
    s = indent(s, a, b)
    return s


if __name__ == '__main__':
    s = tidy(full())
    open(L.DRAFT, 'w', newline='\n').write(s)
    o = L.compile(s, FLAGS, 'final')
    print(L.score(o)[:4], L.same(o))
