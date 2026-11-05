"""loadBl's t5le label and *pr expect (2 lines together)"""
REMOVE = []
FOCUS = ['_loadBlFiles']
Q = '''		if (xb.type <= BUILD_DEVGL16) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
'''


def v(s):
    return [(Q, s)]


AXES = [[
    ('plain', v('''		if (xb.type <= BUILD_DEVGL16) {
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('plainz', v('''		if (xb.type <= BUILD_DEVGL16) {
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
		} else if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('gt', v('''		if (xb.type > BUILD_DEVGL16) {
			if (type == 14)
				setFlashBuild(getBeU16(xb.files[i].data + 2));
			break;
		}
		if (__builtin_expect(*pr != 0, 0))
			goto fail;
		break;
''')),
    ('gt2', v('''		if (xb.type > BUILD_DEVGL16) {
			if (type == 14)
				setFlashBuild(getBeU16(xb.files[i].data + 2));
		} else if (__builtin_expect(*pr != 0, 0))
			goto fail;
		break;
''')),
    ('and', v('''		if (xb.type <= BUILD_DEVGL16 && *pr != 0)
			goto fail;
		if (xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('pr1', v('''		if (*pr != 0) {
			if (xb.type <= BUILD_DEVGL16)
				goto fail;
			break;
		}
		if (xb.type > BUILD_DEVGL16 && type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('prm', v('''		if (xb.type <= BUILD_DEVGL16) {
			if (__builtin_expect(*pr == 0, 1))
				break;
			goto fail;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('prneg', v('''		if (xb.type <= BUILD_DEVGL16) {
			if ((int)*pr < 0)
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('prne1', v('''		if (xb.type <= BUILD_DEVGL16) {
			if (*pr == (uint32_t)-1)
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('t14', v('''		if (xb.type <= BUILD_DEVGL16 && *pr != 0)
			goto fail;
		if (type == 14 && xb.type > BUILD_DEVGL16)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('t14b', v('''		if (xb.type > BUILD_DEVGL16) {
			if (type != 14)
				break;
			setFlashBuild(getBeU16(xb.files[i].data + 2));
			break;
		}
		if (__builtin_expect(*pr != 0, 0))
			goto fail;
		break;
''')),
    ('le_notype', v('''		if (xb.type <= BUILD_DEVGL16) {
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		} else if (type != 14)
			break;
		setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('assign', v('''		if (xb.type <= BUILD_DEVGL16) {
			uint32_t r = *pr;

			if (r)
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
    ('ret', v('''		if (xb.type <= BUILD_DEVGL16) {
			if (__builtin_expect(*pr != 0, 0))
				*pr = -1;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
''')),
]]
