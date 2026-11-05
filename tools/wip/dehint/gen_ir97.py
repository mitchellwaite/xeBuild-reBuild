"""findAnchor: gen_ir93 clr (the flag of the older block cleared), spelled properly, with lit_anchor's asm kept: only the expects and the barrier go."""
FOCUS = ['_findAnchor']
OLD = '''		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
	}
	if (__builtin_expect(ok0, 1) && (__builtin_expect(!ok1, 1) || v0 >= v1)) {
		log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;
	}
	if (__builtin_expect(ok1, 1)) {
		log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
'''
NEW = '''		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
	}
	/* both valid: the older one is no longer a candidate */
	if (ok0 && ok1) {
		if (v0 < v1)
			ok0 = 0;
		else
			ok1 = 0;
	}
	if (ok0) {
		log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;
	}
	if (ok1) {
		log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
'''
AXES = [[('clr', [(OLD, NEW)])]]
