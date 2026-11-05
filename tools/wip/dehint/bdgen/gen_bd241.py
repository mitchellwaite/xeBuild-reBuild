"""loadFileCrc (attempt 13): the padded size through a local, which the Linux build's pad path suggests (it keeps
the padded size in r8 and compares it with size), crossed with which size calloc and the log use.  No expect, no pin.
The reference keeps the dead `size != e->size` compare in the pad path and reloads e->size after the pad log."""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdhints

FOCUS = ['_loadFileCrc']
OLD = '''	e->size = size;
	if (pad && (size & 15))
		e->size = align16(size);
	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
	   (build.sh's expect probability, 92-99); the pin sets e's register in the
	   out-of-line copy only (callers with pad == 0 drop this block) */
	if (verbose) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, align16(size));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
	e->data = calloc(e->size + 0x10000, 1);
'''

SET = {
    'two': '\tlen = size;\n\tif (pad && (size & 15))\n\t\tlen = align16(size);\n\te->size = len;\n',
    'tern': '\tlen = pad && (size & 15) ? align16(size) : size;\n\te->size = len;\n',
    'late': '\tlen = size;\n\tif (pad && (size & 15))\n\t\tlen = align16(size);\n',
}
CMP = {'len': 'size != len', 'esz': 'size != e->size', 'lenr': 'len != size'}
PADARG = {'len': 'len', 'al': 'align16(size)'}
ALLOC = {'esz': 'e->size', 'len': 'len'}


def CASES(base):
    b = bdhints.off(base, 'exp_verbose', 'pin_e')
    assert OLD in b
    b = b.replace('\tsize_t size;\n\tuint32_t c;\n', '\tsize_t size, len;\n\tuint32_t c;\n', 1)
    out = []
    for (sk, s), (ck, c), (pk, p), (ak, a) in itertools.product(SET.items(), CMP.items(), PADARG.items(), ALLOC.items()):
        if sk == 'late' and (ck == 'esz' or ak == 'esz'):
            continue
        body = s + ('\tif (verbose) {\n\t\tif (%s)\n\t\t\tlog_printf(1, "reading %%s (0x%%x b pad 0x%%x b)", name, size, %s);\n'
                    '\t\telse\n\t\t\tlog_printf(1, "reading %%s (0x%%x bytes)", name, size);\n\t}\n' % (c, p))
        if sk == 'late':
            body += '\te->size = len;\n'
        body += '\te->data = calloc(%s + 0x10000, 1);\n' % a
        out.append(('%s %s %s %s' % (sk, ck, pk, ak), b.replace(OLD, body)))
    return out
