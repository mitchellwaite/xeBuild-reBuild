"""Attempt 8, the helper lever on loadBl's pins: the "take the console's (or the scratch entry's) data" moves written out 9
times in loadBl and loadConsoleBlFiles as one natural helper.  Axes: which groups use it (N1 loadBl's kv/kvAlt/smc, N2
the console's, N3 both smcConfig moves, F the fileent moves in loadBl's cases 2/3/4), the helper's statement order, and
pin_d on or off."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

HELPN = {
    'a': '''/* take over the data of n (the console's copy) for e */
static void takeData(struct fileent *e, struct netfile *n)
{
	if (e->data)
		free(e->data);
	e->data = n->data;
	e->size = n->size;
	n->data = NULL;
	n->size = 0;
}

''',
    'b': '''/* take over the data of n (the console's copy) for e */
static void takeData(struct fileent *e, struct netfile *n)
{
	if (e->data)
		free(e->data);
	e->data = n->data;
	n->data = NULL;
	e->size = n->size;
	n->size = 0;
}

''',
}
HELPF = '''/* take over the data of src for e */
static void takeFile(struct fileent *e, struct fileent *src)
{
	if (e->data)
		free(e->data);
	e->data = src->data;
	e->size = src->size;
	src->data = NULL;
	src->size = 0;
}

'''


def mv(ind, dst, src, field_dst='e'):
    return ('%sif (%s->data)\n%s	free(%s->data);\n%s%s->data = %s.data;\n%s%s->size = %s.size;\n%s%s.data = NULL;\n%s%s.size = 0;\n'
            % (ind, dst, ind, dst, ind, dst, src, ind, dst, src, ind, src, ind, src))


def sites_n1():
    out = []
    for src in ('xb.kv', 'xb.kvAlt', 'xb.smc'):
        out.append((mv('\t\t\t', 'e', src), '\t\t\ttakeData(e, &%s);\n' % src))
    return out


def sites_n2():
    return [(mv('\t\t\t\t\t', 'e', src), '\t\t\t\t\ttakeData(e, &%s);\n' % src) for src in ('xb.kv', 'xb.kvAlt', 'xb.smc')]


def sites_n3():
    a = ('\t\t\t\t\tif (xb.files[xb.nFlashFiles].data)\n\t\t\t\t\t\tfree(xb.files[xb.nFlashFiles].data);\n'
         '\t\t\t\t\txb.files[xb.nFlashFiles].data = xb.smcConfig.data;\n\t\t\t\t\txb.files[xb.nFlashFiles].size = xb.smcConfig.size;\n'
         '\t\t\t\t\txb.smcConfig.data = NULL;\n\t\t\t\t\txb.smcConfig.size = 0;\n')
    b = ('\t\t\tif (xb.files[xb.nFlashFiles].data)\n\t\t\t\tfree(xb.files[xb.nFlashFiles].data);\n'
         '\t\t\txb.files[xb.nFlashFiles].data = xb.smcConfig.data;\n\t\t\txb.smcConfig.data = NULL;\n'
         '\t\t\txb.files[xb.nFlashFiles].size = xb.smcConfig.size;\n\t\t\txb.smcConfig.size = 0;\n')
    return [(a, '\t\t\t\t\ttakeData(&xb.files[xb.nFlashFiles], &xb.smcConfig);\n'),
            (b, '\t\t\ttakeData(&xb.files[xb.nFlashFiles], &xb.smcConfig);\n')]


def sites_f():
    a = ('\t\t\tif (e->data)\n\t\t\t\tfree(e->data);\n\t\t\te->data = xb.files[xb.nFlashFiles].data;\n'
         '\t\t\te->size = xb.files[xb.nFlashFiles].size;\n\t\t\txb.files[xb.nFlashFiles].data = NULL;\n\t\t\txb.files[xb.nFlashFiles].size = 0;\n')
    return [(a, '\t\t\ttakeFile(e, &xb.files[xb.nFlashFiles]);\n')]


G = {'N1': sites_n1, 'N2': sites_n2, 'N3': sites_n3, 'F': sites_f}


def make(base, groups, order, pin):
    t = base
    for g in groups:
        for old, new in G[g]():
            if old not in t:
                raise ValueError('%s: %r' % (g, old[:80]))
            t = t.replace(old, new)
    anchor = '/* the default 0x60-byte bootloader (type 24) */\n'
    h = ''
    if set(groups) & {'N1', 'N2', 'N3'}:
        h += HELPN[order]
    if 'F' in groups:
        h += HELPF
    t = t.replace(anchor, h + anchor)
    if not pin:
        t = bdhints.off(t, 'pin_d')
    return t


def CASES(base):
    out = []
    for n in range(1, 5):
        for groups in itertools.combinations(('N1', 'N2', 'N3', 'F'), n):
            for order in ('a', 'b'):
                if not set(groups) & {'N1', 'N2', 'N3'} and order == 'b':
                    continue
                for pin in (1, 0):
                    out.append(('%s %s pin%d' % ('+'.join(groups), order, pin), lambda b, g=groups, o=order, p=pin: make(b, g, o, p)))
    return out
