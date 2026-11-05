"""addBlsToImage: the xell room test as its own `if` after the type chain, as addUpdateBls has it, and other chain shapes (exp_t24 off)."""
OLD = '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			log_printf(1, "retail image, skipping %s\\n", e->name);
			continue;
		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				log_printf(1, "devkit/testkit image, skipping %s\\n", e->name);
				continue;
			}
		} else if (type == 25 && __builtin_expect(type != 24, 1) && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
		}
'''
R = '''log_printf(1, "retail image, skipping %s\\n", e->name);
			continue;
'''
D = '''log_printf(1, "devkit/testkit image, skipping %s\\n", e->name);
				continue;
'''
W = '''log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
'''
F = {
    'plain': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		} else if (type == 25 && e->offset < imgSize()) {
			%s		}
''' % (R, D, W),
    'sep': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		}
		if (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)) {
			%s		}
		if (type == 25 && e->offset < imgSize()) {
			%s		}
''' % (R, D, W),
    'sep2': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		}
		if (type == 25 && e->offset < imgSize()) {
			%s		}
''' % (R, D, W),
    'nest25': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		} else if (type == 25) {
			if (e->offset < imgSize()) {
				%s			}
		}
''' % (R, D, W),
    'gsize': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		} else if (type == 25) {
			uint32_t room = imgSize();

			if (e->offset < room) {
				%s			}
		}
''' % (R, D, W),
    'neq': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		} else if (type == 25) {
			if (e->offset >= imgSize())
				goto add;
			%s		}
add:
''' % (R, D, W),
    'goto': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		} else if (type == 25 && e->offset < imgSize())
			goto noroom;
		if (0) {
noroom:
			%s		}
''' % (R, D, W),
    'tail': '''		if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {
			%s		} else if (xb.type > BUILD_DEVGL16) {
			if (type == 23 || type == 25) {
				%s			}
		} else if (type == 25 && e->offset < imgSize())
			goto noroom;
''' % (R, D),
}


def CASES(base):
    out = []
    for k, v in F.items():
        t = base.replace(OLD, v)
        if k == 'tail':
            a = t.index('void addBlsToImage(void)')
            b = t.index('\n	if (xb.seReplacesCf) {', a)
            # the log at the end of the loop body
            c = t.rindex('		off += e->size;\n	}\n', a, b + 1)
            t = t[:c] + '		off += e->size;\n		continue;\nnoroom:\n			' + W.replace('			continue;\n', '') + '	}\n' + t[c + len('		off += e->size;\n	}\n'):]
        out.append((k, t))
    return out
