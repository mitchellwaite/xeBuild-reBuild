"""scanMobiles without exp_scan: the older arm's (and the newer arm's) tests as switches; the older arm tests the delete bit first."""
FOCUS = ['_scanMobiles']
BASE = 'tools/wip/dehint/drafts/image_read_attempt8.c'
OLD = '''			if (!len)
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
ST = '''mobiles[n].found = 1;
			mobiles[n].version = ver;
			mobiles[n].spare = page * 16;
			mobiles[n].page = page;
			mobiles[n].len = len;
			mobiles[n].offset = off;
'''
NEW = {
 'if': 'if (!len) goto next; if (len & 0x8000) { mobiles[n].found = 0; page++; goto align; }\n' + ST,
 'sz': 'switch (len) { case 0: goto next; default: break; } if (len & 0x8000) { mobiles[n].found = 0; page++; goto align; }\n' + ST,
 'sd': 'if (!len) goto next; switch (len & 0x8000) { case 0: break; default: mobiles[n].found = 0; page++; goto align; }\n' + ST,
 'sds': 'if (!len) goto next; switch (len & 0x8000) { default: mobiles[n].found = 0; page++; goto align; case 0: break; }\n' + ST,
 'szd': 'switch (len) { case 0: goto next; default: break; } switch (len & 0x8000) { case 0: break; default: mobiles[n].found = 0; page++; goto align; }\n' + ST,
}
OLDA = {
 'if': 'if (len & 0x8000) { page++; goto align; } if (!len) goto next;',
 'sdz': 'switch (len & 0x8000) { case 0: if (!len) goto next; break; default: page++; goto align; }',
 'sd': 'switch (len & 0x8000) { case 0: break; default: page++; goto align; } if (!len) goto next;',
 'sds': 'switch (len & 0x8000) { default: page++; goto align; case 0: break; } if (!len) goto next;',
 'sz': 'if (len & 0x8000) { page++; goto align; } switch (len) { case 0: goto next; default: break; }',
 'szd': 'switch (len & 0x8000) { case 0: break; default: page++; goto align; } switch (len) { case 0: goto next; default: break; }',
 'ss': 'if ((short)len < 0) { page++; goto align; } if (!len) goto next;',
 'sss': 'switch ((short)len < 0) { case 0: break; default: page++; goto align; } if (!len) goto next;',
 'ng': 'if (!(len & 0x8000)) { if (!len) goto next; } else { page++; goto align; }',
 'ngs': 'if (!(len & 0x8000)) { switch (len) { case 0: goto next; default: break; } } else { page++; goto align; }',
}
AX = []
for kn, n in NEW.items():
    for ko, o in OLDA.items():
        AX.append((kn + '.' + ko, [(OLD, n + '\t\t} else {\n' + o + '\n}\n')]))
AXES = [AX]
