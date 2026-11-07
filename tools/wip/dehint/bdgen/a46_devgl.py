import os, re
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
t = open(BASE, newline='').read()
i = t.index('\t\t\t\tif (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {\n\t\t\t\t\t/* the hot label')
j = t.index('\t\t\t\t}\n\t\t\t\tbreak;\n\t\t\tcase 1:', i)
OLD = t[i:j + 6]
BODY = '''					r = 0;
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
'''
assert BODY in OLD


def arm(head, tail='\t\t\t\t}\n', body=BODY):
    return [(OLD, head + body + tail)]


V = {
 'nohot': arm('\t\t\t\tif (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {\n'),
 'sw': arm('\t\t\t\tswitch (xb.type) {\n\t\t\t\tcase BUILD_DEVGL:\n\t\t\t\tcase BUILD_DEVGL16:\n'),
 'swd': arm('\t\t\t\tswitch (xb.type) {\n\t\t\t\tcase BUILD_DEVGL:\n\t\t\t\tcase BUILD_DEVGL16:\n', '\t\t\t\t\tbreak;\n\t\t\t\tdefault:\n\t\t\t\t\tbreak;\n\t\t\t\t}\n'),
 'swb': arm('\t\t\t\tswitch (xb.type) {\n\t\t\t\tcase BUILD_DEVGL:\n\t\t\t\tcase BUILD_DEVGL16:\n', '\t\t\t\t\tbreak;\n\t\t\t\t}\n'),
 'ne': arm('\t\t\t\tif (!(xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)) {\n'),
 'sub': arm('\t\t\t\tif ((uint32_t)(xb.type - BUILD_DEVGL) < 2) {\n'),
 'gt': arm('\t\t\t\tif (xb.type > BUILD_GLITCH && xb.type < BUILD_DEVKIT) {\n'),
}
