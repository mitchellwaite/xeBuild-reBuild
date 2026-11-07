"""Attempt 21: the signature block without the dead `else if (type)`, which raises the signature-failed share S / Xc of the
flow into the `xb.type <= 5` test from 15.8% to 27.2% (the verify becomes 50/50), enough by attempt 18's formula for
t5le (needs 21.6%).  What breaks is bb-reorder's tie on the 50/50 verify (the failed log becomes the fallthrough), so
the axes are the verify's polarity and arm order (passed arm first puts it next in the block order, which better_edge_p
uses on a tie), where `*pr = -1` goes, and t5le / the `*pr` expect on or off."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
'''
F = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);'
P = 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);'
FORMS = {
    'neg_else': '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					@F1@
				} else
					@P@
''',
    'pos_first': '''				if (cbVerifySig(e->data, xb.pub1bl))
					@P@
				else {
					@F1@
				}
''',
    'pos_first_ne': '''				if (cbVerifySig(e->data, xb.pub1bl) != 0)
					@P@
				else {
					@F1@
				}
''',
}
FAIL = {'log_first': F + '\n\t\t\t\t\t*pr = -1;', 'set_first': '*pr = -1;\n\t\t\t\t\t' + F}
HS = [(), ('lab_t5le',), ('exp_pr',), ('lab_t5le', 'exp_pr')]


def mk(b, form, fl, hs):
    f = FORMS[form].replace('@F1@', FAIL[fl]).replace('@P@', P)
    t = bdrun.sub(b, OLD, f)
    return bdhints.off(t, *hs) if hs else t


def CASES(base):
    out = []
    for form, fl, hs in itertools.product(FORMS, FAIL, HS):
        out.append(('%s %s -%s' % (form, fl, ','.join(hs)), lambda b, c=(form, fl, hs): mk(b, *c)))
    return out


FOCUS = ['_loadBlFiles']
