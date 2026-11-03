# attempt 6: r0: hot label lnp2 gone: shapes of npages' computation (shape of the branch decides the guard's frequency)
import os
N = '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
		else {
			/* imgAddFile's clone: keeps DOM2's threading from zeroing the npages guard edge */
			lnp2: __attribute__((hot));
		}
'''
CALC = '''if (len % 512)
				npages = (len + 512) / 512;
			else
				npages = len / 512;
'''
F = {
 'plain': '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (!partial)
			npages = 32;
''',
 'le': '''		if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
		if (partial <= 0)
			npages = 32;
''',
 'n1': '		if (partial) {\n			' + CALC + '		} else\n			npages = 32;\n',
 'n2': '		npages = 32;\n		if (partial) {\n			' + CALC + '		}\n',
 'n3': '''		if (!partial)
			npages = 32;
		else if (len % 512)
			npages = (len + 512) / 512;
		else
			npages = len / 512;
''',
 'n4': '		npages = partial ? (len % 512 ? (len + 512) / 512 : len / 512) : 32;\n',
 'n5': '		npages = !partial ? 32 : len % 512 ? (len + 512) / 512 : len / 512;\n',
 'n6': '''		npages = 32;
		if (partial)
			npages = len % 512 ? (len + 512) / 512 : len / 512;
''',
 'n7': '''		npages = len / 512;
		if (len % 512)
			npages = (len + 512) / 512;
		if (!partial)
			npages = 32;
''',
 'n8': '''		npages = 32;
		if (partial) {
			npages = len / 512;
			if (len % 512)
				npages = (len + 512) / 512;
		}
''',
 'n9': '''		if (partial)
			npages = len % 512 ? (len + 512) / 512 : len / 512;
		else
			npages = 32;
''',
}
PART = "		partial = (len < 0x4000) & (type != 0) & (type != '0');\n"
P2 = {
 '': PART,
 'pa': "		partial = len < 0x4000 && type != 0 && type != '0';\n",
 'pb': "		partial = type != 0 && type != '0' && len < 0x4000;\n",
}
AXES = [
 [(k, [(N, v)]) for k, v in F.items()],
 [(k, [(PART, v)] if k else []) for k, v in P2.items()],
]
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
FLAGS = []
