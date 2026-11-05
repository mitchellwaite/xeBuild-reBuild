"""loadBl: case 23 forms with lab_badsize off; the signature part and the xb.type <= 5 tail as helpers or other nestings with lab_t5le and exp_pr off."""
import itertools

C23 = '''		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (e->size & 3) {
		badsize: __attribute__((hot));
			log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			goto fail;
		}
		appendAddonPatches(e);
		break;
'''
LOG = 'log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);\n'
F23 = {
    'keep': C23,
    'plain': C23.replace('		badsize: __attribute__((hot));\n', ''),
    'else': '		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if (e->size & 3) {\n			' + LOG + '			goto fail;\n		} else\n			appendAddonPatches(e);\n		break;\n',
    'rev': '		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if (!(e->size & 3)) {\n			appendAddonPatches(e);\n			break;\n		}\n		' + LOG + '		goto fail;\n',
    'nest': '		*pr = loadBinFile(e);\n		if (!*pr) {\n			if (e->size & 3) {\n				' + LOG + '				goto fail;\n			}\n			appendAddonPatches(e);\n		}\n		break;\n',
    'nest2': '		*pr = loadBinFile(e);\n		if (!*pr) {\n			if (!(e->size & 3)) {\n				appendAddonPatches(e);\n				break;\n			}\n			' + LOG + '			goto fail;\n		}\n		break;\n',
    'r4': '		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if (e->size % 4) {\n			' + LOG + '			goto fail;\n		}\n		appendAddonPatches(e);\n		break;\n',
    'size': '		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if ((e->size & 3) != 0) {\n			' + LOG + '			goto fail;\n		}\n		appendAddonPatches(e);\n		break;\n',
    'pr1': '		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if (e->size & 3) {\n			' + LOG + '			*pr = -1;\n			break;\n		}\n		appendAddonPatches(e);\n		break;\n',
    'pr2': '		*pr = loadBinFile(e);\n		if (*pr)\n			break;\n		if (e->size & 3) {\n			' + LOG + '			*pr = -1;\n			return;\n		}\n		appendAddonPatches(e);\n		break;\n',
}
TAIL = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''
FT = {
    'keep': TAIL,
    'plain': TAIL.replace('		t5le: __attribute__((hot));\n', '').replace('__builtin_expect(*pr != 0, 0)', '*pr != 0'),
    't5': TAIL.replace('		t5le: __attribute__((hot));\n', ''),
    'pr': TAIL.replace('__builtin_expect(*pr != 0, 0)', '*pr != 0'),
    'nopr': TAIL.replace('		t5le: __attribute__((hot));\n', '').replace('__builtin_expect(*pr != 0, 0)', '*pr'),
    'else': '		if (xb.type > BUILD_DEVGL16) {\n			if (type == 14)\n				setFlashBuild(getBeU16(xb.files[i].data + 2));\n		} else if (*pr != 0)\n			goto fail;\n		break;\n',
    'rev': '		if (xb.type <= BUILD_DEVGL16) {\n			if (!*pr)\n				break;\n			goto fail;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n',
    'pos': '		if (xb.type <= BUILD_DEVGL16) {\n			if ((int)*pr < 0)\n				goto fail;\n			break;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n',
    'firstpr': '		if (xb.type > BUILD_DEVGL16 && type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		else if (xb.type <= BUILD_DEVGL16 && *pr)\n			goto fail;\n		break;\n',
    'ty14': '		if (xb.type <= BUILD_DEVGL16) {\n			if (*pr != 0)\n				goto fail;\n		} else if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n',
    'pm1': '		if (xb.type <= BUILD_DEVGL16) {\n			if (*pr == (uint32_t)-1)\n				goto fail;\n			break;\n		}\n		if (type == 14)\n			setFlashBuild(getBeU16(xb.files[i].data + 2));\n		break;\n',
}


def CASES(base):
    out = []
    for a, b in itertools.product(F23, FT):
        if a != 'keep' and b != 'keep':
            continue
        t = base
        if C23 not in t or TAIL not in t:
            raise ValueError('base')
        t = t.replace(C23, F23[a]).replace(TAIL, FT[b])
        out.append(('c23=%s tail=%s' % (a, b), t))
    return out
