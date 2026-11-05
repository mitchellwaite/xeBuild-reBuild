"""exp_upd off: the rotation exit must be the bit test's edge, not type == 23's: no `continue` for the not-an-update path,
and forms of the second and third continue."""
REMOVE = ['exp_upd']
FOCUS = ['_addUpdateBls']
A = '''		if (!isUpdateBl(type))
			continue;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
'''
HEAD = '''		if (isUpdateBl(type)) {
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
'''
HEAD2 = '''		if (isUpdateBl(type)) {
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (strnicmp(e->name, "none", 4) || e->crc) {
'''
HEAD3 = '''		if (isUpdateBl(type) && (e->offset != 0xffffffff ? (off = e->offset, 1) : 1)) {
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
'''
T = '''		off += e->size;
	}
}

int logPowerButton'''
T1 = '''		off += e->size;
		}
	}
}

int logPowerButton'''
T2 = '''		off += e->size;
		}
		}
	}
}

int logPowerButton'''
W = '''		if (type == 25 && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\\n");
			continue;
		}
'''
AXES = [[
    ('nest', [(A, HEAD), (T, T1)]),
    ('nest2', [(A, HEAD2), (T, T2)]),
    ('goto', [(A, A.replace('continue;', 'goto next;')), (T, '		off += e->size;\n	next:\n		;\n	}\n}\n\nint logPowerButton')]),
    ('goto1', [(A, A.replace('continue;\n		if (e->offset', 'goto next;\n		if (e->offset')), (T, '		off += e->size;\n	next:\n		;\n	}\n}\n\nint logPowerButton')]),
]]
HELP = [
    ('', []),
    ('ret', [('return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
              'if (type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25)\n\t\treturn 1;\n\treturn 0;')]),
    ('ifelse', [('return type == 23 || type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;',
              'if (type == 23)\n\t\treturn 1;\n\treturn type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;')]),
]
AXES.append(HELP)
