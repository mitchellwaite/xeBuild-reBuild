# Third round (bdrv.py), on build/bd/rv/b2.c (sc_memcpy+r24_call+fc_pad1): the tail's test.
exec(open(HERE + '/bdrv_b.py').read())

TAIL = ('\t\t\t\tif (xb.type <= BUILD_DEVGL16) {\n'
        '\t\t\t\t\t/* Borderline, for review: r is 0 or a negative failure\n'
        '\t\t\t\t\t   code here; the signed test (not r != 0) is chosen for\n'
        '\t\t\t\t\t   the match */\n'
        '\t\t\t\t\tif ((int)r < 0)\n'
        '\t\t\t\t\t\tgoto fail;\n'
        '\t\t\t\t\tbreak;\n'
        '\t\t\t\t}\n'
        '\t\t\t\tsetKitBuild(i, type);\n'
        '\t\t\t\tbreak;\n')

V3 = [
    ('t_kitfirst', [(TAIL, '\t\t\t\tif (xb.type > BUILD_DEVGL16) {\n\t\t\t\t\tsetKitBuild(i, type);\n'
                           '\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t\tif (r)\n\t\t\t\t\tgoto fail;\n\t\t\t\tbreak;\n')]),
    ('t_elseif', [(TAIL, '\t\t\t\tif (xb.type > BUILD_DEVGL16)\n\t\t\t\t\tsetKitBuild(i, type);\n'
                         '\t\t\t\telse if (r)\n\t\t\t\t\tgoto fail;\n\t\t\t\tbreak;\n')]),
    ('t_and', [(TAIL, '\t\t\t\tif (xb.type <= BUILD_DEVGL16 && r)\n\t\t\t\t\tgoto fail;\n'
                      '\t\t\t\tif (xb.type > BUILD_DEVGL16)\n\t\t\t\t\tsetKitBuild(i, type);\n\t\t\t\tbreak;\n')]),
    ('t_m1', [('\t\t\t\t\tif ((int)r < 0)\n', '\t\t\t\t\tif (r == -1)\n')]),
    ('t_m1u', [('\t\t\t\t\tif ((int)r < 0)\n', '\t\t\t\t\tif (r == (uint32_t)-1)\n')]),
    ('t_elseif_m1', [(TAIL, '\t\t\t\tif (xb.type > BUILD_DEVGL16)\n\t\t\t\t\tsetKitBuild(i, type);\n'
                            '\t\t\t\telse if (r == -1)\n\t\t\t\t\tgoto fail;\n\t\t\t\tbreak;\n')]),
    ('t_kitfirst_m1', [(TAIL, '\t\t\t\tif (xb.type > BUILD_DEVGL16) {\n\t\t\t\t\tsetKitBuild(i, type);\n'
                              '\t\t\t\t\tbreak;\n\t\t\t\t}\n\t\t\t\tif (r == -1)\n\t\t\t\t\tgoto fail;\n\t\t\t\tbreak;\n')]),
    ('t_elseif_lt', [(TAIL, '\t\t\t\tif (xb.type > BUILD_DEVGL16)\n\t\t\t\t\tsetKitBuild(i, type);\n'
                            '\t\t\t\telse if ((int)r < 0)\n\t\t\t\t\tgoto fail;\n\t\t\t\tbreak;\n')]),
    # loadBl24 with one call, as nested ifs or the good case first
    ('b24_nest', [(BL24, '\tif (!loadBaseFile(e->name, e)) {\n\t\tif (e->size == 0x60)\n\t\t\treturn 0;\n'
                         '\t}\n\treturn defaultBl60(e);\n')]),
    ('b24_good', [(BL24, '\tif (!loadBaseFile(e->name, e) && e->size == 0x60)\n\t\treturn 0;\n'
                         '\treturn defaultBl60(e);\n')]),
    ('b24_r', [(BL24, '\tint r = loadBaseFile(e->name, e);\n\n\tif (r || e->size != 0x60)\n'
                      '\t\tr = defaultBl60(e);\n\treturn r;\n')]),
]
V = V + V3
