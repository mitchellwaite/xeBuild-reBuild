"""scanMobiles without exp_scan: forms of the older-version arm, whole newer/older test polarity; the reference tests `(short)len < 0` first in the older arm and `!len` first in the newer."""
FOCUS = ['_scanMobiles']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
OLD = '''		if (ver >= mobiles[n].version || !mobiles[n].found) {
			if (!len)
				goto next;
			if (len & 0x8000) {
				mobiles[n].found = 0;
				page++;
				goto align;
			}
			mobiles[n].found = 1;
			mobiles[n].version = ver;
			mobiles[n].spare = page * 16;
			mobiles[n].page = page;
			mobiles[n].len = len;
			mobiles[n].offset = off;
		} else {
			/* lays the advance block after the found path's stores */
			if (__builtin_expect(len & 0x8000, 1)) {
				page++;
				goto align;
			}
			if (!len)
				goto next;
		}
'''
STORE = '''			mobiles[n].found = 1;
			mobiles[n].version = ver;
			mobiles[n].spare = page * 16;
			mobiles[n].page = page;
			mobiles[n].len = len;
			mobiles[n].offset = off;
'''
NEWER = '''			if (!len)
				goto next;
			if (len & 0x8000) {
				mobiles[n].found = 0;
				page++;
				goto align;
			}
'''
ADV = 'page++;\n goto align;\n'
ELSES = {
    'e0': f'if (len & 0x8000) {{ {ADV} }}\n if (!len) goto next;\n',
    'e1': f'if (!len) goto next;\n if (len & 0x8000) {{ {ADV} }}\n',
    'e2': f'if (!(len & 0x8000)) {{ if (!len) goto next; }} else {{ {ADV} }}\n',
    'e3': f'if (len & 0x8000) {{ {ADV} }} else if (!len) goto next;\n',
    'e4': f'if ((short)len < 0) {{ {ADV} }}\n if (!len) goto next;\n',
    'e5': f'if (len >= 0x8000) {{ {ADV} }}\n if (!len) goto next;\n',
    'e6': f'if (len < 0x8000) {{ if (!len) goto next; }} else {{ {ADV} }}\n',
    'e7': f'if (!len) goto next;\n if (!(len & 0x8000)) ; else {{ {ADV} }}\n',
    'e8': f'if (!(len & 0x7fff)) ; if (len & 0x8000) {{ {ADV} }}\n if (!len) goto next;\n',
    'e9': f'del = len & 0x8000;\n if (del) {{ {ADV} }}\n if (!len) goto next;\n',
}
SHAPES = {
    'ab': lambda e: f'if (ver >= mobiles[n].version || !mobiles[n].found) {{ {NEWER} {STORE} }} else {{ {e} }}\n',
    'ba': lambda e: f'if (ver < mobiles[n].version && mobiles[n].found) {{ {e} }} else {{ {NEWER} {STORE} }}\n',
    'nf': lambda e: f'if (ver < mobiles[n].version) {{ if (mobiles[n].found) {{ {e} goto adv; }} }}\n {NEWER} {STORE} adv:\n',
    'fl': lambda e: f'newer = ver >= mobiles[n].version || !mobiles[n].found;\n if (newer) {{ {NEWER} {STORE} }} else {{ {e} }}\n',
    'fn': lambda e: f'newer = 1;\n if (ver < mobiles[n].version && mobiles[n].found) newer = 0;\n if (newer) {{ {NEWER} {STORE} }} else {{ {e} }}\n',
    'nn': lambda e: f'if (ver >= mobiles[n].version) {{ newer: {NEWER} {STORE} }} else if (!mobiles[n].found) goto newer; else {{ {e} }}\n',
}
D = '		uint32_t ver;\n\n		/* sink moves'
AX = [(s + '.' + e, [(OLD, f(v)), (D, '		uint32_t ver;\n		int newer, del;\n\n		/* sink moves')]) for s, f in SHAPES.items() for e, v in ELSES.items()]
AXES = [AX]
