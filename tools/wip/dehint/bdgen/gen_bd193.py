"""`else if (type)` (attempt 8): a plain else, with the signature-failed arm going straight to the shared fail block
(the same behaviour: type is 5, 11 or 17 there, so the tail would either break with *pr = -1 or goto fail), or other
shapes that give the failed arm a second predictor so the two PRED_CALLs don't cancel."""
OLD = '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
'''
F = {
    'else': '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				} else
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
''',
    'gofail': '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					goto fail;
				}
				log_printf(1, "loaded %s, signature check passed!\\n", e->name);
''',
    'gofail2': '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					goto fail;
				} else
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
''',
    'pos': '''				if (cbVerifySig(e->data, xb.pub1bl))
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
				else {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					goto fail;
				}
''',
    'ret': '''				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
					return;
				}
				log_printf(1, "loaded %s, signature check passed!\\n", e->name);
''',
}


def CASES(base):
    if OLD not in base:
        raise ValueError('old')
    return [(k, base.replace(OLD, v)) for k, v in F.items()]


FOCUS = ['_loadBlFiles']
