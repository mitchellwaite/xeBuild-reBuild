"""lb6: case 6 falls into the shared bootloader case (or tests itself inside it), so the shared path has an entry with a type that isn't a constant.  That's what the constant_p entry imitated."""
import itertools, importlib.util, os, re
d = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g144', os.path.join(d, 'gen_bd144.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

BASE = 'build/bd/a5/lb6.c'
HEAD = '\tcase 5: case 7: case 8: case 9: case 10: case 11: case 12: case 13:\n\tcase 14: case 15: case 16: case 17: case 18: case 19: case 20: case 21:\n'
C6 = '''	case 6:
		if (!xb.cbb)
			break;
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr) {
			uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);

			*pr = r6;
		}
		break;
'''
H6 = {
    'fall': '\tcase 6:\n\t\tif (!xb.cbb)\n\t\t\tbreak;\n' + HEAD,
    'in': '\tcase 5: case 6: case 7: case 8: case 9: case 10: case 11: case 12: case 13:\n\tcase 14: case 15: case 16: case 17: case 18: case 19: case 20: case 21:\n\t\tif (type == 6 && !xb.cbb)\n\t\t\tbreak;\n',
    'keep': HEAD,
}


def CASES(base):
    out = []
    names = list(g.H)
    for h6 in H6:
        for n in range(len(names) + 1):
            for s in itertools.combinations(names, n):
                if 'cp' in s and h6 != 'keep':
                    continue
                for k, f in g.TAIL.items():
                    t = base
                    if h6 != 'keep':
                        t = t.replace(C6, '').replace(HEAD, H6[h6], 1)
                    for x in s:
                        t = g.H[x](t)
                    if f:
                        t = f(t)
                    out.append((','.join((h6,) + s + (k,)), t))
    return out
