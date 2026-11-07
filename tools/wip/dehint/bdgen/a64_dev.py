"""Attempt 64: buildFlash's fuse decision without the devgl expect, natural spellings.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a64_dev.py -p 99 -o "-" """
FUSE = ('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
        '\t\tif (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))\n\t\t\tfuse = 1;\n\t}\n')
DEV = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
def F(body):
    return [(FUSE, body)]
V1 = {
    'noexp': F(FUSE.replace('__builtin_expect(%s, 0)' % DEV, DEV)),
    'notfuse': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tif (!fuse && (%s))\n\t\t\tfuse = 1;\n\t}\n' % DEV),
    'notfuse2': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tif (!fuse) {\n\t\t\tif (%s)\n\t\t\t\tfuse = 1;\n\t\t}\n\t}\n' % DEV),
    'range': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tif (xb.type >= BUILD_DEVGL && xb.type <= BUILD_DEVGL16)\n\t\t\tfuse = 1;\n\t}\n'),
    'switch1': F('\tswitch (xb.type) {\n\tcase BUILD_JTAG:\n\tcase BUILD_DEVGL:\n\tcase BUILD_DEVGL16:\n\t\tfuse = 1;\n\t\tbreak;\n'
                 '\tdefault:\n\t\tfuse = xb.glitch2mfg != 0;\n\t}\n'),
    'switch2': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tswitch (xb.type) {\n\t\tcase BUILD_DEVGL:\n\t\tcase BUILD_DEVGL16:\n\t\t\tfuse = 1;\n\t\t}\n\t}\n'),
    'ternary': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = (%s) ? 1 : xb.glitch2mfg != 0;\n' % DEV),
    'or2': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tfuse |= %s;\n\t}\n' % DEV),
    'gl_if': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = 0;\n\t\tif (xb.glitch2mfg || %s)\n\t\t\tfuse = 1;\n\t}\n' % DEV),
    'local_t': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tint t = xb.type;\n\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tif (t == BUILD_DEVGL || t == BUILD_DEVGL16)\n\t\t\tfuse = 1;\n\t}\n'),
    'jt_last': F('\tfuse = xb.glitch2mfg != 0;\n\tif (%s)\n\t\tfuse = 1;\n\tif (xb.type == BUILD_JTAG)\n\t\tfuse = 1;\n' % DEV),
    'devfirst': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG && !(%s))\n\t\tfuse = xb.glitch2mfg != 0;\n' % DEV),
    'bool': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = !!xb.glitch2mfg;\n'
                 '\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n' % DEV),
    'gtest': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = 0;\n\t\tif (xb.glitch2mfg)\n\t\t\tfuse = 1;\n'
                 '\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n' % DEV),
}
V2 = {
    'tern_g': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG)\n\t\tfuse = xb.glitch2mfg ? 1 : (%s);\n' % DEV),
    'devvar': F('\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tint dev = %s;\n\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tif (dev)\n\t\t\tfuse = 1;\n\t}\n' % DEV),
    'bool_t': [(FUSE, '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                '\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n' % DEV), ('\tint fuse, blocks, r, cf,', '\tint blocks, r, cf,'),
               ('\tuint16_t t;\n\tchar last;\n\n\tmemset(salt', '\tuint16_t t;\n\tchar last;\n\tBOOL fuse;\n\n\tmemset(salt')],
    'u8_t': [(FUSE, '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                '\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n' % DEV), ('\tint fuse, blocks, r, cf,', '\tint blocks, r, cf,'),
               ('\tuint16_t t;\n\tchar last;\n\n\tmemset(salt', '\tuint16_t t;\n\tchar last;\n\tuint8_t fuse;\n\n\tmemset(salt')],
    'else_g': F('\tif (xb.type == BUILD_JTAG)\n\t\tfuse = 1;\n\telse {\n\t\tfuse = xb.glitch2mfg != 0;\n'
                 '\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n' % DEV),
    'tern2': F('\tfuse = xb.type == BUILD_JTAG ? 1 : xb.glitch2mfg != 0;\n\tif (%s)\n\t\tfuse = 1;\n' % DEV),
}
V = dict(V1, **V2)
