"""addBlsToImage: the skip tests in flag forms, in place of `continue` with exp_t24's always-true test."""
import itertools

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
RET = 'log_printf(1, "retail image, skipping %s\\n", e->name);\n'
DEV = 'log_printf(1, "devkit/testkit image, skipping %s\\n", e->name);\n'
ROOM = 'log_printf(0, "***** WARNING: skipping xell, there doesn\'t appear to be enough room!\\n");\n'
TEST = 'type == 25 && e->offset < imgSize()'
F = {
    'plain': 'if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {\n' + RET + 'continue;\n} else if (xb.type > BUILD_DEVGL16) {\nif (type == 23 || type == 25) {\n' + DEV + 'continue;\n}\n} else if (' + TEST + ') {\n' + ROOM + 'continue;\n}\n',
    'nest': 'if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {\n' + RET + 'continue;\n} else if (xb.type > BUILD_DEVGL16) {\nif (type == 23 || type == 25) {\n' + DEV + 'continue;\n}\n} else if (type == 25) {\nif (e->offset < imgSize()) {\n' + ROOM + 'continue;\n}\n}\n',
    'ty': 'if (type == 23 || type == 25) {\nif (xb.type == BUILD_RETAIL) {\n' + RET + 'continue;\n}\nif (xb.type > BUILD_DEVGL16) {\n' + DEV + 'continue;\n}\nif (' + TEST + ') {\n' + ROOM + 'continue;\n}\n}\n',
    'sep': 'if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {\n' + RET + 'continue;\n}\nif (xb.type > BUILD_DEVGL16 && (type == 23 || type == 25)) {\n' + DEV + 'continue;\n}\nif (xb.type <= BUILD_DEVGL16 && ' + TEST + ') {\n' + ROOM + 'continue;\n}\n',
    'sz': 'if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {\n' + RET + 'continue;\n} else if (xb.type > BUILD_DEVGL16) {\nif (type == 23 || type == 25) {\n' + DEV + 'continue;\n}\n} else if (type == 25) {\nuint32_t sz = imgSize();\n\nif (e->offset < sz) {\n' + ROOM + 'continue;\n}\n}\n',
    'ne24': 'if (xb.type == BUILD_RETAIL && (type == 23 || type == 25)) {\n' + RET + 'continue;\n} else if (xb.type > BUILD_DEVGL16) {\nif (type == 23 || type == 25) {\n' + DEV + 'continue;\n}\n} else if (type == 25 && type != 24 && e->offset < imgSize()) {\n' + ROOM + 'continue;\n}\n',
}
TAILA = '''		if (type != 10 && type != 16 && type != 24)
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\\n",
				   e->name, off, e->size, off + e->size);
		if (type == 10) {
			j = findFile(9);'''


def CASES(base):
    out = []
    for k, s in F.items():
        out.append((k, base.replace(OLD, s)))
        # flag forms: skip set by the arms, the rest under !skip
        g = s.replace('continue;\n', 'skip = 1;\n')
        t = base.replace(OLD, g + 'if (skip)\ncontinue;\n')
        t = t.replace('\tint type, j, off = 0;\n\n\tfor (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {\n\t\te = &xb.files[i];\n\t\ttype = e->type;\n\t\tif (e->offset != 0xffffffff)', '\tint type, j, skip, off = 0;\n\n\tfor (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {\n\t\te = &xb.files[i];\n\t\ttype = e->type;\n\t\tskip = 0;\n\t\tif (e->offset != 0xffffffff)', 1)
        out.append((k + ' flag', t))
    return out
