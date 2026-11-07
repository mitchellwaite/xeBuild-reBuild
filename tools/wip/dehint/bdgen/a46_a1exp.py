A1 = 'if (xb.type == BUILD_JTAG || xb.glitch2mfg) {'
V = {
 'expg0': [(A1, 'if (xb.type == BUILD_JTAG || __builtin_expect(xb.glitch2mfg, 0)) {')],
 'expj0': [(A1, 'if (__builtin_expect(xb.type == BUILD_JTAG, 0) || xb.glitch2mfg) {')],
 'expor0': [(A1, 'if (__builtin_expect(xb.type == BUILD_JTAG || xb.glitch2mfg, 0)) {')],
 'g1': [(A1, 'if (xb.type == BUILD_JTAG || xb.glitch2mfg == 1) {')],
 'nestg': [(A1 + '''
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}''', '''if (xb.type == BUILD_JTAG) {
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					} else if (xb.glitch2mfg) {
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}''')],
}
