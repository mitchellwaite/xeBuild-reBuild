"""Attempt 47: the none test through a predicate helper (devgl label off and on).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a47_none.py"""
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
DEV = ('\t\t\t\tdevgl: __attribute__((hot));\n', '')
T = '\t\tif (strnicmp(e->name, "none", 4) || e->crc) {\n'
HEAD = '/* the default 0x60-byte bootloader (type 24) */\n'
P1 = '''/* a "none" entry with no crc is a slot left empty */
static int isNone(struct fileent *e)
{
	return !strnicmp(e->name, "none", 4) && !e->crc;
}

'''
P2 = '''/* a "none" entry with no crc is a slot left empty */
static int isNone(struct fileent *e)
{
	if (strnicmp(e->name, "none", 4))
		return 0;
	return e->crc == 0;
}

'''
P3 = '''/* a "none" entry with no crc is a slot left empty */
static int isUsed(struct fileent *e)
{
	return strnicmp(e->name, "none", 4) || e->crc;
}

'''
V = {}
for k, p, t in (('n1', P1, '\t\tif (!isNone(e)) {\n'), ('n2', P2, '\t\tif (!isNone(e)) {\n'), ('u', P3, '\t\tif (isUsed(e)) {\n')):
    V[k + '_lbf'] = [(HEAD, p + HEAD), (T, t)]
    V[k + '_both'] = lambda s, p=p, t=t: s.replace(HEAD, p + HEAD, 1).replace(T, t)
    V[k + '_lbf-dev'] = [(HEAD, p + HEAD), (T, t), DEV]
    V[k + '_both-dev'] = lambda s, p=p, t=t: s.replace(HEAD, p + HEAD, 1).replace(T, t).replace(DEV[0], '')
