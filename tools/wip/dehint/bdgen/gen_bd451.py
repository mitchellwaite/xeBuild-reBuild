"""Attempt 33: `else if (type)` by a repeated test of a *local* key (attempt 32's `ok && xb.pub1bl` re-tested the global,
which a call may change, so the reload stayed in the code).  With `key` a local copy of xb.pub1bl the re-test is live
source but foldable: on the verify-passed edge vrp/threading know key != 0, and the passed log's block is reached
through a test block (no call) so only the failed edge gets PRED_CALL, as the dead `type` test does.  Forms:
  and:     if (key && !verify) {failed; -1} else if (key) passed; else nokey;
  andn:    if (key && !verify) {failed; -1} else if (!key) nokey; else passed;
  nest:    src's nesting with the dead test replaced by `else if (key)` (still dead: for the record)
  nestk:   src's nesting, plain else, key local (the local alone)
  ok:      ok = !key || verify; if (!ok) ..; else if (key) passed; else nokey;
key as `struct rsapub *` or `const struct rsapub *`, declared in the block or at loadBl's top.  Every other hint kept,
then each loadBl hint off alone.  Runs on src as of 5a0bc459."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdhints, bdrun

FOCUS = ['_loadBlFiles']

OLD = '''		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					*pr = -1;
				/* Borderline, for review: type is 5, 11 or 17 here, so this test
				   is always true; a plain else costs 54 lines */
				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
			} else
				log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
		}
'''
FAILED = 'log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);'
PASSED = 'log_printf(1, "loaded %s, signature check passed!\\n", e->name);'
NOKEY = 'log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);'


def body(form, decl):
    d = '\t\t\t%s *key = xb.pub1bl;\n\n' % decl if decl else ''
    k = 'key' if decl else 'xb.pub1bl'
    if form == 'and':
        b = '''			if (%s && !cbVerifySig(e->data, %s)) {
				%s
				*pr = -1;
			} else if (%s)
				%s
			else
				%s
''' % (k, k, FAILED, k, PASSED, NOKEY)
    elif form == 'andn':
        b = '''			if (%s && !cbVerifySig(e->data, %s)) {
				%s
				*pr = -1;
			} else if (!%s)
				%s
			else
				%s
''' % (k, k, FAILED, k, NOKEY, PASSED)
    elif form == 'nest':
        b = '''			if (%s) {
				if (!cbVerifySig(e->data, %s)) {
					%s
					*pr = -1;
				} else if (%s)
					%s
			} else
				%s
''' % (k, k, FAILED, k, PASSED, NOKEY)
    elif form == 'nestk':
        b = '''			if (%s) {
				if (!cbVerifySig(e->data, %s)) {
					%s
					*pr = -1;
				} else
					%s
			} else
				%s
''' % (k, k, FAILED, PASSED, NOKEY)
    elif form == 'ok':
        b = '''			int ok = !%s || cbVerifySig(e->data, %s);

			if (!ok) {
				%s
				*pr = -1;
			} else if (%s)
				%s
			else
				%s
''' % (k, k, FAILED, k, PASSED, NOKEY)
    if decl:
        return '\t\tif (type == 5 || type == 17 || type == 11) {\n\t\t\t{\n' + d.replace('\t\t\t', '\t\t\t\t', 1) + \
            b.replace('\n\t\t\t', '\n\t\t\t\t').replace('\t\t\t', '\t\t\t\t', 1) + '\t\t\t}\n\t\t}\n'
    return '\t\tif (type == 5 || type == 17 || type == 11) {\n' + b + '\t\t}\n'


def body2(form, decl):
    """key declared in the type block itself (C89 style, no extra braces)"""
    b = body(form, None).replace('xb.pub1bl', 'key')
    return b.replace('\t\tif (type == 5 || type == 17 || type == 11) {\n',
                     '\t\tif (type == 5 || type == 17 || type == 11) {\n\t\t\t%s *key = xb.pub1bl;\n\n' % decl, 1) \
        .replace('\t\t\tint ok = !key', '\t\t\tint ok;\n\n\t\t\tok = !key') if form == 'ok' else \
        b.replace('\t\tif (type == 5 || type == 17 || type == 11) {\n',
                  '\t\tif (type == 5 || type == 17 || type == 11) {\n\t\t\t%s *key = xb.pub1bl;\n\n' % decl, 1)


OFFS = os.environ.get('BDOFFS', 'none,exp_t10,exp_pr,lab_t5le,vol_fail').split(',')


def off(t, k):
    return t if k == 'none' else bdhints.off(t, k)


def CASES(base):
    out = []
    for form in ('and', 'andn', 'nest', 'nestk', 'ok'):
        for decl in (None, 'struct rsapub', 'const struct rsapub'):
            for k in OFFS:
                if decl and form == 'ok':
                    nb = body2(form, decl)
                elif decl:
                    nb = body2(form, decl)
                else:
                    nb = body(form, None)
                lab = '%s %s|%s' % (form, (decl or 'glob').replace('struct ', '').replace(' ', ''), k)
                out.append((lab, lambda b, nb=nb, k=k: off(bdrun.sub(b, OLD, nb), k)))
    return out
