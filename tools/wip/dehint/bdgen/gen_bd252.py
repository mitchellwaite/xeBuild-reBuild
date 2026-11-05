"""Attempt 14: lab_t5le alone costs only the no-key log's .p2align (0 loose, 7 strict).  compute_alignments aligns it
when its frequency (17) is over 10x its layout predecessor's, fixup_reorder_chain's jmp block after the SE copy, whose
frequency is freq(SE copy) * P(>5).  Attempt 11 attacked P(>5); here the other factor: forms of the SE test, which
set the SE copy's own frequency.  Runs on src/build.c as of eb75581."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

SE_SRC = "		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {\n"
BODY = ("			/* an SE where the CF goes */\n			e->type = type = 14;\n			xb.cfLdv = 0;\n"
        "			xb.seReplacesCf = 1;\n		}\n")
SE = {
    's0': SE_SRC + BODY,
    'nest': "		if (type == 9) {\n			if (e->data[0] == 'S' && e->data[1] == 'E') {\n" + BODY.replace('\n			', '\n				').replace('		}\n', '			}\n		}\n'),
    'nest2': "		if (type == 9 && e->data[0] == 'S') {\n			if (e->data[1] == 'E') {\n" + BODY.replace('\n			', '\n				').replace('		}\n', '			}\n		}\n'),
    'memcmp': "		if (type == 9 && !memcmp(e->data, \"SE\", 2)) {\n" + BODY,
    'strncmp': "		if (type == 9 && !strncmp((const char *)e->data, \"SE\", 2)) {\n" + BODY,
    'swap': "		if (type == 9 && e->data[1] == 'E' && e->data[0] == 'S') {\n" + BODY,
    'loc': "		if (type == 9 && (p = e->data)[0] == 'S' && p[1] == 'E') {\n" + BODY,
}


def mk(t, se, lab, pr):
    t = bdrun.sub(t, SE_SRC + BODY, SE[se], 1)
    if se == 'loc':
        t = bdrun.sub(t, '	int type;\n\n	type = e->type;', '	int type;\n	uint8_t *p;\n\n	type = e->type;', 1)
    if lab == 'nl':
        t = bdhints.off(t, 'lab_t5le')
    if pr == 'np':
        t = bdhints.off(t, 'exp_pr')
    return t


def CASES(base):
    out = []
    for se, lab, pr in itertools.product(SE, ('l', 'nl'), ('p', 'np')):
        out.append(('%s %s %s' % (se, lab, pr), lambda b, s=se, l=lab, p=pr: mk(b, s, l, p)))
    return out


FOCUS = ['_loadBlFiles']
