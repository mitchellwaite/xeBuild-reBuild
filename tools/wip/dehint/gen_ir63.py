"""copyMmcImage: the reference's standalone copy isn't hoisted (P(ok) <= 50%), loadDump's inlined one is (>= 50%, within 10% of even).  Test spellings with other opcode predictions; notZeropair's own form."""
import importlib.util, os
_s = importlib.util.spec_from_file_location('g62', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ir62.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
FOCUS = ['_copyMmcImage', '_loadDump']
BASE = _m.BASE
ATTR, USE, LOG, HEAD = _m.ATTR, _m.USE, _m.LOG, _m.HEAD
TESTS = {
    'nz': ('notZeropair()', False),
    'e1': ('notZeropair() == 1', False),
    'g0': ('notZeropair() > 0', False),
    'ne0': ('notZeropair() != 0', False),
    'z': ('notZeropair() == 0', True),
    'le': ('notZeropair() <= 0', True),
    'lt1': ('notZeropair() < 1', True),
    'n1': ('notZeropair() != 1', True),
    'm': ('memcmp(zeropair, xb.dump + 16, 14)', False),
    'mz': ('memcmp(zeropair, xb.dump + 16, 14) == 0', True),
}
B = {}
for k, (c, bad) in TESTS.items():
    if bad:
        B[k + '.ret'] = HEAD + '	if (' + c + ') {\n		' + LOG + '		return 0;\n	}\n	return 1;\n}\n'
        B[k + '.els'] = HEAD + '	if (' + c + ') {\n		' + LOG + '		return 0;\n	} else\n		return 1;\n}\n'
    else:
        B[k + '.ret'] = HEAD + '	if (' + c + ')\n		return 1;\n	' + LOG + '	return 0;\n}\n'
        B[k + '.els'] = HEAD + '	if (' + c + ')\n		return 1;\n	else {\n		' + LOG + '		return 0;\n	}\n}\n'
AXB = [(k, [(ATTR, v)]) for k, v in B.items()]
AXU = [('if', [(USE, _m.U['if'])]), ('nif', [(USE, _m.U['nif'])])]
AXT = [('', []),
       ('ib', [('int notZeropair(void)\n', 'static int notZeropair_(void);\nint notZeropair(void)\n')]) if False else ('ul', [('uint32_t copyMmcImage(uint8_t *raw)', 'int copyMmcImage(uint8_t *raw)')]),
       ]
AXES = [AXB, AXU]
