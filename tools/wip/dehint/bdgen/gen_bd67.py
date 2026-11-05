"""checkBl: gen_bd66's same+hot sums to 1003; bad must be under 1000.  Type 14's test through crcSame too."""
import importlib.util, os
s = importlib.util.spec_from_file_location('g66', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_bd66.py'))
g = importlib.util.module_from_spec(s)
s.loader.exec_module(g)
C14 = '''		c = crc32(bl, blsize);
		if (crc != c)
			goto bad;
		break;
	default:
'''
T14 = [('', []),
       ('g14', [(C14, C14.replace('crc != c', '!crcSame(c, crc)'))]),
       ('m14', [(C14, '		c = crc32(bl, blsize);\n		if (!crcSame(c, crc)) {\n			' + g.MSG + '\n			return -2;\n		}\n		break;\n	default:\n')]),
       ]
AXES = [g.ARMS[:2], g.SIZE, T14]
FOCUS = ['_checkBl']
