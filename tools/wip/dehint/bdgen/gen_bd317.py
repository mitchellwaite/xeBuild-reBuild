"""Attempt 20, pin_d (loadBl case 27's tail, pin off): lifetime and scope of d and the size, not address spellings
(gen_bd271 did those).  d in the block, at loadBl's top, assigned in the test, absent (loadConsoleBlFiles' form); the size
in a local read before or after d; a file-entry pointer for the tail only; an early break.  Runs on src after attempt
20's loadFileCrc landing."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

TAIL = '''		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
	case 2:
'''
N = 'xb.files[xb.nFlashFiles]'
FORMS = {
    'src': TAIL,
    'none': '''		if (%s.data)
			*pr = extractSmcConfig(e, %s.data, %s.size);
		break;
	case 2:
''' % (N, N, N),
    'brk': '''		if (!%s.data)
			break;
		*pr = extractSmcConfig(e, %s.data, %s.size);
		break;
	case 2:
''' % (N, N, N),
    'assign': '''		{
			uint8_t *d;

			if ((d = %s.data))
				*pr = extractSmcConfig(e, d, %s.size);
		}
		break;
	case 2:
''' % (N, N),
    'dsz': '''		{
			uint8_t *d = %s.data;
			uint32_t sz = %s.size;

			if (d)
				*pr = extractSmcConfig(e, d, sz);
		}
		break;
	case 2:
''' % (N, N),
    'szd': '''		{
			uint32_t sz = %s.size;
			uint8_t *d = %s.data;

			if (d)
				*pr = extractSmcConfig(e, d, sz);
		}
		break;
	case 2:
''' % (N, N),
    'dszin': '''		{
			uint8_t *d = %s.data;

			if (d) {
				int sz = %s.size;

				*pr = extractSmcConfig(e, d, sz);
			}
		}
		break;
	case 2:
''' % (N, N),
    'ptr': '''		{
			struct fileent *c = &%s;

			if (c->data)
				*pr = extractSmcConfig(e, c->data, c->size);
		}
		break;
	case 2:
''' % N,
    'ptrbrk': '''		{
			struct fileent *c = &%s;

			if (!c->data)
				break;
			*pr = extractSmcConfig(e, c->data, c->size);
		}
		break;
	case 2:
''' % N,
    'dvoid': TAIL.replace('uint8_t *d', 'void *d'),
    'dconst': TAIL.replace('uint8_t *d', 'const uint8_t *d').replace('extractSmcConfig(e, d,', 'extractSmcConfig(e, (uint8_t *)d,'),
}


def mk(b, k):
    t = bdhints.off(b, 'pin_d')
    return bdrun.sub(t, TAIL, FORMS[k])


def CASES(base):
    return [(k, lambda b, k=k: mk(b, k)) for k in FORMS]


FOCUS = ['_loadBlFiles']
