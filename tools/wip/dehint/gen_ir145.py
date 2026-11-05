"""scanMobiles without exp_scan, from gen_ir144 if.sd (1 loose line: a second `cmp WORD PTR [esp+0x44],0`, the reference reuses the flags): how the switch tests the delete bit, len's type."""
FOCUS = ['_scanMobiles']
BASE = 'tools/wip/dehint/drafts/image_read_attempt8.c'
OLD = '''			/* lays the advance block after the found path's stores */
			if (__builtin_expect(len & 0x8000, 1)) {
				page++;
				goto align;
			}
			if (!len)
				goto next;
'''
ADV = 'page++; goto align;'
Z = 'if (!len) goto next;'
F = {
 'sd': f'switch (len & 0x8000) {{ case 0: break; default: {ADV} }} {Z}',
 'sa': f'switch (len & 0x8000) {{ case 0x8000: {ADV} }} {Z}',
 'sb': f'switch (len >> 15) {{ case 0: break; default: {ADV} }} {Z}',
 'sb1': f'switch (len >> 15) {{ case 1: {ADV} }} {Z}',
 'sc': f'switch ((short)len < 0) {{ case 0: break; default: {ADV} }} {Z}',
 'sc1': f'switch ((short)len < 0) {{ case 1: {ADV} }} {Z}',
 'se': f'switch ((len & 0x8000) != 0) {{ case 0: break; default: {ADV} }} {Z}',
 'sf': f'switch (len) {{ case 0x8000 ... 0xffff: {ADV} case 0: goto next; }}',
 'sf2': f'switch (len) {{ case 0: goto next; case 0x8000 ... 0xffff: {ADV} }}',
 'sg': f'switch ((short)len) {{ case -32768 ... -1: {ADV} case 0: goto next; }}',
 'sh': f'switch ((short)len) {{ case 0: goto next; case -32768 ... -1: {ADV} }}',
 'si': f'switch ((short)len >> 15) {{ case 0: break; default: {ADV} }} {Z}',
 'sj': f'switch ((short)len & 0x8000) {{ case 0: break; default: {ADV} }} {Z}',
 'sk': f'switch (len & 0x8000) {{ case 0: if (!len) goto next; break; default: {ADV} }}',
 'n1': f'if ((len & 0x8000) == 0) {{ {Z} }} else {{ {ADV} }}',
 'n2': f'if ((short)len >= 0) {{ {Z} }} else {{ {ADV} }}',
 'n3': f'if ((short)len < 0) {{ {ADV} }} else {{ {Z} }}',
 'n4': f'if ((short)len > 0) {{ }} else if ((short)len < 0) {{ {ADV} }} else goto next;',
 'n5': f'if (len) {{ if ((short)len < 0) {{ {ADV} }} }} else goto next;',
}
F.update({
 'i1': f'if (len >> 15) {{ {ADV} }} {Z}',
 'i2': f'if ((len >> 15) & 1) {{ {ADV} }} {Z}',
 'i3': f'if ((len >> 8) & 0x80) {{ {ADV} }} {Z}',
 'i4': f'if ((len & 0x8000) >> 15) {{ {ADV} }} {Z}',
 'i5': f'if ((len >> 15) == 1) {{ {ADV} }} {Z}',
 'i6': f'int del = len & 0x8000; if (del) {{ {ADV} }} {Z}',
 'i7': f'uint32_t del = len & 0x8000; if (del) {{ {ADV} }} {Z}',
 'i8': f'uint16_t del = len & 0x8000; if (del) {{ {ADV} }} {Z}',
 'i9': f'int del = len >> 15; if (del) {{ {ADV} }} {Z}',
 'j1': f'int del = len & 0x8000; if (!del) {{ {Z} }} else {{ {ADV} }}',
 'j2': f'int del = (len & 0x8000) != 0; if (del) {{ {ADV} }} {Z}',
 'j3': f'int del = len >> 15; if (!del) {{ {Z} }} else {{ {ADV} }}',
})
AXES = [[(k, [(OLD, v + '\n')]) for k, v in F.items()]]
