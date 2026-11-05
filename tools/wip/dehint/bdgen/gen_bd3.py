Q = '''		} else if (type == 25 && __builtin_expect(type != 24, 1) && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
		}
'''
FOCUS = ['_addBlsToImage']
W = '''log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;'''


def v(s):
    return [(Q, s)]


AXES = [[
    ('plain', v('''		} else if (type == 25 && e->offset < imgSize()) {
			%s
		}
''' % W)),
    ('nest', v('''		} else if (type == 25) {
			if (e->offset < imgSize()) {
			%s
			}
		}
''' % W)),
    ('nest24', v('''		} else if (type == 25 || type == 24) {
			if (type == 25 && e->offset < imgSize()) {
			%s
			}
		}
''' % W)),
    ('dead', v('''		} else if (type == 25 && type != 24 && e->offset < imgSize()) {
			%s
		}
''' % W)),
    ('size', v('''		} else if (type == 25) {
			uint32_t room = imgSize();

			if (e->offset < room) {
			%s
			}
		}
''' % W)),
    ('rev', v('''		} else if (type == 25 && imgSize() > e->offset) {
			%s
		}
''' % W)),
    ('sep', v('''		}
		if (xb.type <= BUILD_DEVGL16 && type == 25 && e->offset < imgSize()) {
			%s
		}
''' % W)),
    ('sep2', v('''		}
		if (type == 25 && xb.type <= BUILD_DEVGL16 && e->offset < imgSize()) {
			%s
		}
''' % W)),
    ('sep3', v('''		}
		if (type == 25 && e->offset < imgSize()) {
			%s
		}
''' % W)),
    ('sep4', v('''		}
		if (type == 25) {
			if (e->offset < imgSize()) {
			%s
			}
		}
''' % W)),
    ('off', v('''		} else if (type == 25) {
			uint32_t o = e->offset;

			if (o < imgSize()) {
			%s
			}
		}
''' % W)),
]]
