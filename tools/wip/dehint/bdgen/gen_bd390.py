"""Attempt 28: exp_t10's near miss (drafts/build_loadBl_t10_weight_nearmiss.patch, PRE) is one bbro duplication away: the
merged checkBl call block 116 (load-ok type 9 non-SE 70.8 + CG success 29) is 99 against connect_traces' threshold 88.
At profile_estimate (bddump.sh .. loadBl t-profile_estimate) the SE test is `type == 9` 28%, 'S' 28%, 'E' 28% (nonequal
each), so P(non-SE | 9) = 92%; A < 59 needs it under 75.5%.  Spellings of the SE test that change those predictors.
Run with bddup.py (prints the Duplicated lines).  Runs on src as of f2823155."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun

NM = [('} else if (__builtin_expect(type == 10, 0)) {', '} else if (type == 10) {'),
      ('&& (char *)__builtin_constant_p(type) == (char *)1)', '&& __builtin_constant_p(type) == 1)')]
SE = "\t\tif (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {\n"


def PRE(b):
    for a, c in NM:
        b = bdrun.sub(b, a, c, 1)
    return b


HELPER = '''/* an SE image (where a CF is expected) */
static int isSe(const uint8_t *d)
{
	return d[0] == 'S' && d[1] == 'E';
}

/* load the input file e (xb.files[i]) by its type */
'''
FORMS = {
    'src': SE,
    'amp': "\t\tif (type == 9 && (e->data[0] == 'S') & (e->data[1] == 'E')) {\n",
    'amp3': "\t\tif ((type == 9) & (e->data[0] == 'S') & (e->data[1] == 'E')) {\n",
    'u16': "\t\tif (type == 9 && *(uint16_t *)e->data == 0x4553) {\n",
    'helper': "\t\tif (type == 9 && isSe(e->data)) {\n",
    'nest': "\t\tif (type == 9)\n\t\tif (e->data[0] == 'S' && e->data[1] == 'E') {\n",
    'ne': "\t\tif (type == 9 && !(e->data[0] != 'S' || e->data[1] != 'E')) {\n",
}


def mk(b, f):
    b = bdrun.sub(b, SE, FORMS[f], 1)
    if f == 'helper':
        b = bdrun.sub(b, '/* load the input file e (xb.files[i]) by its type */\n', HELPER, 1)
    return b


def CASES(base):
    return [(f, lambda b, f=f: mk(b, f)) for f in FORMS]


FOCUS = ['_loadBlFiles']
