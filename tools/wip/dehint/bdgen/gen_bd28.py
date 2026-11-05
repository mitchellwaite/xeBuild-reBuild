# checkBl: each arm with its own crc-error log and return, as an author might write it; tail merge or
# crossjump folds them.  Their returns' predictions (PRED_NEGATIVE_RETURN) should take `bad` under 10%.
REMOVE = ['cb5', 'lab_size', 'crc5', 'crc7', 'crc8', 'crc9', 'crc10', 'crc12', 'crc13']
FOCUS = ['_checkBl']
MSG = '''log_printf(0, "\\n\\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\\n", c, crc);'''
GOTO = 'if (crc != c)\n\t\t\tgoto bad;\n'
PER = 'if (crc != c) {\n\t\t\t' + MSG + '\n\t\t\treturn -2;\n\t\t}\n'
DEF = '''	default:
		c = 0;
		goto bad;
	}
	return 0;
bad:
	''' + MSG + '''
	return -2;
'''
A = [
    ('g', []),
    ('per', [(GOTO, PER)]),
    ('perdef', [(GOTO, PER), (DEF, '''	default:
		''' + MSG.replace(', c, crc', ', 0, crc') + '''
		return -2;
	}
	return 0;
''')]),
    ('peronly', [(GOTO, PER), (DEF, '''	default:
		c = 0;
		''' + MSG + '''
		return -2;
	}
	return 0;
''')]),
]
B = [('', []), ('nopt', [('	__asm__("" : : "D"(type));\n', '')])]
C = [('', []), ('nom', [('	__asm__("" :: "a"(m));\n', '')])]
AXES = [A, B, C]
