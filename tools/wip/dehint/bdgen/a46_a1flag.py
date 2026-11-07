A1 = '''					if (xb.type == BUILD_JTAG || xb.glitch2mfg) {'''
V = {
 'gfirst': [(A1, '''					if (xb.glitch2mfg || xb.type == BUILD_JTAG) {''')],
 'flag': [(A1, '''					g = xb.glitch2mfg;
					if (xb.type == BUILD_JTAG)
						g = 1;
					if (g) {'''), ('''			int type = e->type;
''', '''			int type = e->type;
			int g;
''')],
 'flag2': [(A1, '''					g = xb.type == BUILD_JTAG || xb.glitch2mfg;
					if (g) {'''), ('''			int type = e->type;
''', '''			int type = e->type;
			int g;
''')],
 'flag3': [(A1, '''					g = 0;
					if (xb.type == BUILD_JTAG || xb.glitch2mfg)
						g = 1;
					if (g) {'''), ('''			int type = e->type;
''', '''			int type = e->type;
			int g;
''')],
}
