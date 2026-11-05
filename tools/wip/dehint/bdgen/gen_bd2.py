Q='''		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
'''
FOCUS=['_buildFlash']
def v(s): return [(Q,s)]
AXES=[[
 ('plain',v('''		fuse = xb.glitch2mfg != 0;
		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			fuse = 1;
''')),
 ('sep',v('''		fuse = xb.glitch2mfg != 0;
		if (xb.type == BUILD_DEVGL)
			fuse = 1;
		if (xb.type == BUILD_DEVGL16)
			fuse = 1;
''')),
 ('elif',v('''		fuse = xb.glitch2mfg != 0;
		if (xb.type == BUILD_DEVGL)
			fuse = 1;
		else if (xb.type == BUILD_DEVGL16)
			fuse = 1;
''')),
 ('ternary',v('''		fuse = xb.glitch2mfg != 0;
		fuse = (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) ? 1 : fuse;
''')),
 ('or',v('''		fuse = xb.glitch2mfg != 0 || xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16;
''')),
 ('or2',v('''		fuse = xb.glitch2mfg != 0;
		fuse |= xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16;
''')),
 ('flag',v('''		int dev = xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16;

		fuse = xb.glitch2mfg != 0;
		if (dev)
			fuse = 1;
''')),
 ('flag2',v('''		int dev = xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16;

		fuse = xb.glitch2mfg != 0;
		fuse = dev ? 1 : fuse;
''')),
 ('sub',v('''		fuse = xb.glitch2mfg != 0;
		if ((uint32_t)xb.type - BUILD_DEVGL <= 1)
			fuse = 1;
''')),
 ('rng',v('''		fuse = xb.glitch2mfg != 0;
		if (xb.type >= BUILD_DEVGL && xb.type <= BUILD_DEVGL16)
			fuse = 1;
''')),
 ('else',v('''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			fuse = 1;
		else
			fuse = xb.glitch2mfg != 0;
''')),
 ('notif',v('''		fuse = xb.glitch2mfg != 0;
		if (xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)
			;
		else
			fuse = 1;
''')),
 ('tmp',v('''		int t = xb.glitch2mfg != 0;

		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			t = 1;
		fuse = t;
''')),
 ('gt0',v('''		fuse = xb.glitch2mfg != 0;
		if ((xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) > 0)
			fuse = 1;
''')),
 ('nest',v('''		fuse = xb.glitch2mfg != 0;
		if (xb.type >= BUILD_DEVGL) {
			if (xb.type <= BUILD_DEVGL16)
				fuse = 1;
		}
''')),
]]
