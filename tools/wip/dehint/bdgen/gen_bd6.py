"""checkBl: natural literal order (the size error after the crc one) with its hints still on"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bdtricks

REMOVE = ['lit_chk']
FOCUS = ['_checkBl']
SZ = 'log_printf(0, "\\n\\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\\n", blsize, size);'
BAD = 'log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'
MAG = 'log_printf(0, "\\n\\n***** ERROR: BL magic check %c%c for type %d failed!\\n", bl[0], bl[1], type);'
H = '''	if (blsize > size) {
		size_err: __attribute__((hot));
		''' + SZ + '''
		return -3;
	}
	cb_hint(&dead);
	m = bl[0];
'''
T = '''	return 0;
bad:
	''' + BAD + '''
	return -2;
magic:
	''' + MAG + '''
	return -1;
}
'''
TGOTO = '''	return 0;
bad:
	''' + BAD + '''
	return -2;
toobig:
	@L''' + SZ + '''
	return -3;
magic:
	''' + MAG + '''
	return -1;
}
'''
TLE = '''	return 0;
bad:
	''' + BAD + '''
	return -2;
	}
	@L''' + SZ + '''
	return -3;
magic:
	''' + MAG + '''
	return -1;
}
'''
LBL = 'size_err: __attribute__((hot));\n\t'


def shape(name, head, tail, hot, cb):
    head = head.replace('@C', '\tcb_hint(&dead);\n' if cb else '')
    tail = tail.replace('@L', LBL if hot else '')
    return ('%s%s%s' % (name, '+hot' if hot else '', '+cb' if cb else ''), [(H, head), (T, tail)])


shapes = []
for hot in (1, 0):
    for cb in (1, 0):
        shapes.append(shape('goto', '''	if (blsize > size)
		goto toobig;
@C	m = bl[0];
''', TGOTO, hot, cb))
        shapes.append(shape('le', '''	if (blsize <= size) {
@C	m = bl[0];
''', TLE, hot, cb))

crcs = ['crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']


def off(names):
    def f(text):
        return bdtricks.apply(text, names)[0]
    return f


class Off:
    """an edit-like wrapper: bdsweep's build() wants (old, new) pairs"""


AXES = [shapes, [
    ('', []),
    ('nocrc', [(EXP, 'crc != c') for EXP in ['__builtin_expect(crc != c, 0)']]),
    ('nocrcpin', [('__builtin_expect(crc != c, 0)', 'crc != c'), ('	__asm__("" : : "D"(type));\n', '')]),
    ('pintype', [('	__asm__("" : : "D"(type));\n', '')]),
]]
