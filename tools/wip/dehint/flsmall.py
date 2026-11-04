"""flsmall.py: what each trick's plain removal costs, one at a time and by group."""
import fllib as L

s = L.base()
UN = """			if (j == len) {
				unsigned char *q = &buf[i + len];

				if (q == 0)
					__builtin_unreachable();
				if (*q != 0)
					return i + len;
			}
"""
PIN = '	__asm__("" :: "b"(val));\n'
A1 = s[s.index('	__asm__("" :: "i"("[rawpatch]")'):s.index('	off = memFindStr(buf, size, "[rawpatch]", 1);')]
A2 = '		__asm__("" :: "i"("\\n******* ERROR: file in [flashfs] has greater than %d chars in it\'s name!\\n"), "i"("\\n        Line: %s\\n"));\n'
A3 = '	__asm__("" :: "i"("\\n******* ERROR: file in [security] has greater than %d chars in it\'s name!\\n"));\n'
OPTI = '__attribute__((optimize("ira-region=one")))\n'
V = {}
V['base'] = s
V['unreach->plain'] = L.sub(s, UN, """			if (j == len && buf[i + len] != 0)
				return i + len;
""")
V['unreach->q'] = L.sub(s, UN, """			if (j == len) {
				unsigned char *q = &buf[i + len];

				if (*q != 0)
					return i + len;
			}
""")
V['pin'] = L.sub(s, PIN, '')
V['opt'] = L.sub(s, OPTI, '')
V['a1'] = L.sub(s, A1, '')
V['a2'] = L.sub(s, A2, '')
V['a3'] = L.sub(s, A3, '')
V['nofiv'] = (s, [f for f in L.ALLFLAGS if f != '-fno-tree-loop-vectorize'])
V['noebb'] = (s, ['-O3', '-fno-tree-loop-vectorize', '--param', 'builtin-expect-probability=65'])
V['noprob'] = (s, ['-O3', '-fno-tree-loop-vectorize', '--param', 'lra-inheritance-ebb-probability-cutoff=60'])
V['noexpect'] = L.sub(s, "__builtin_expect(buf[i] == ';', 0)", "buf[i] == ';'")
V['deadA'] = L.sub(s, "	if (i < 0)\n		buf[0] = 1;\n", '')
V['deadB'] = L.sub(s, "		for (j = 0; j < 44; j++)\n			if (i < 0)\n				buf[j] = 1;\n", '')
L.sweep(V, prefix='small')
