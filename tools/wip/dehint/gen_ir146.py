"""scanMobiles without exp_scan: `int del = len & 0x8000` with a second use at forwprop1 stays `del != 0` (no predictor, 50%) at profile_estimate; fre1 folds that use (del is 0 there), forwprop2 then makes it the sign test, whose flags the zero test reuses."""
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
D = 'int del = len & 0x8000;\n'
F = {
 'nest': f'{D} if (del) {{ {ADV} }} if (!del) {{ if (!len) goto next; }}',
 'el': f'{D} if (del) {{ {ADV} }} else if (!del) {{ if (!len) goto next; }}',
 'an': f'{D} if (del) {{ {ADV} }} if (!len && !del) goto next;',
 'na': f'{D} if (del) {{ {ADV} }} if (!del && !len) goto next;',
 'or': f'{D} if (del) {{ {ADV} }} if (!(len | del)) goto next;',
 'eq': f'{D} if (del) {{ {ADV} }} if (len == del) goto next;',
 'sum': f'{D} if (del) {{ {ADV} }} if (!(len + del)) goto next;',
 'mx': f'int low = len & 0x7fff; {D} if (del) {{ {ADV} }} if (!low) goto next;',
 'mx2': f'{D} int low = len - del; if (del) {{ {ADV} }} if (!low) goto next;',
 'mx3': f'{D} int low = len ^ del; if (del) {{ {ADV} }} if (!low) goto next;',
 'mx4': f'{D} if (del) {{ {ADV} }} else {{ int low = len - del; if (!low) goto next; }}',
 'mx5': f'{D} if (del) {{ {ADV} }} else {{ int low = len ^ del; if (!low) goto next; }}',
 'mx6': f'{D} if (del) {{ {ADV} }} else {{ int low = len & ~del; if (!low) goto next; }}',
}
AXES = [[(k, [(OLD, v + '\n')]) for k, v in F.items()]]
