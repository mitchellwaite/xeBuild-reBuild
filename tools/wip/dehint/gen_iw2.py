# buildImage: `test` scratch comes from peephole2's rotating search: swap the JTAG/other arms
import re, os
FOCUS = ['_buildImage']
s = open(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src', 'image_write.c'), newline='').read().replace('\r\n', '\n')
a = s.index('	if (xb.type == BUILD_JTAG) {\n		hdrTemplate.cbOffset = 0x800000;')
b = s.index('	} else {\n		hdrTemplate.cbOffset = xb.type - BUILD_TESTKIT < 2')
c = s.index('	if (xb.type > BUILD_DEVGL16) {\n		copyright[9]')
jtag = s[a:b]
other = s[b:c]
jbody = jtag.split('\n', 1)[1]
obody = other.split('\n', 1)[1]
obody = obody[:obody.rindex('	}\n')]
swapped = '	if (xb.type != BUILD_JTAG) {\n' + obody + '	} else {\n' + jbody + '	}\n'
PIN = '''			bb = xb.bigBlock;
			__asm__("" :: "b"(bb));
			if (bb)
'''
AXES = [[
    ('', []),
    ('swap', [(jtag + other, swapped)]),
], [
    ('pin', []),
    ('nopin', [(PIN, '			if (xb.bigBlock)\n'), ('cf, bb;', 'cf;')]),
]]
