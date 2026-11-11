# Second round (bdrv.py), on bdrv_a's sc_memcpy+r24_call (build/bd/rv/b1.c).
exec(open(HERE + '/bdrv_a.py').read())

CPU_GOTO = (
    '\tif (xb.cpuFan != 0xffffffff) {\n'
    '\t\tif (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {\n'
    '\t\t\tsmc[0x11] = xb.cpuFan | 0x80;\n'
    '\t\t\tpatched = 1;\n'
    '\t\t} else if (xb.cpuFan)\n'
    '\t\t\tgoto cpuwarn;\n'
    '\t\telse if (smc[0x11] != 0x7f) {\n'
    '\t\t\tsmc[0x11] = 0x7f;\n'
    '\t\t\tpatched = 1;\n'
    '\t\t}\n'
    '\t}\n'
    'cpudone:\n')
GPUWARN = ('gpuwarn:\n'
           '\tlog_printf(0, "***** WARNING: gpu fan speed override setting ignored, not between 40 and 100\\n");\n'
           '\tgoto gpudone;\n')
CPUWARN = ('cpuwarn:\n'
           '\tlog_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);\n'
           '\tgoto cpudone;\n')

V2 = [
    ('cf_goto1', [(CPUFAN_CALL, CPU_GOTO), (CPUFAN_HELPER, ''), (GPUWARN, GPUWARN + CPUWARN)]),
    ('cf_goto2', [(CPUFAN_CALL, CPU_GOTO), (CPUFAN_HELPER, ''), (GPUWARN, CPUWARN + GPUWARN)]),
    # initFlash: one statement in the return block without the & 1
    ('if_boolret', [('static int initFlash(uint8_t *salt)', 'static _Bool initFlash(uint8_t *salt)'),
                    ('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_u8', [('\tint fuse = 1;\n\n\tmemset(salt', '\tuint8_t fuse = 1;\n\n\tmemset(salt'),
               ('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_char', [('\tint fuse = 1;\n\n\tmemset(salt', '\tchar fuse = 1;\n\n\tmemset(salt'),
                 ('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_u32ret', [('static int initFlash(uint8_t *salt)', 'static uint32_t initFlash(uint8_t *salt)'),
                   ('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_u32loc', [('\tint fuse = 1;\n\n\tmemset(salt', '\tuint32_t fuse = 1;\n\n\tmemset(salt'),
                   ('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_not2', [('\treturn fuse & 1;\n}\n', '\treturn !!fuse;\n}\n')]),
    ('if_tern', [('\treturn fuse & 1;\n}\n', '\treturn fuse ? 1 : 0;\n}\n')]),
    # useBuiltIn with memmove, and defaultBl60 through it
    ('ub_mm', [('\te->data = malloc(size);\n\tif (!e->data)\n\t\treturn 1;\n\te->size = size;\n\tmemcpy(e->data, data, size);\n',
                '\te->data = malloc(size);\n\tif (!e->data)\n\t\treturn 1;\n\te->size = size;\n\tmemmove(e->data, data, size);\n')]),
    # defaultBl60 through setFileData (calloc), the file's own copy helper
    ('d6_sfd', [('\te->data = malloc(0x60);\n\tif (!e->data)\n\t\treturn 1;\n\te->size = 0x60;\n'
                 '\tmemmove(e->data, defBl60, 0x60);\n\treturn 0;\n',
                 '\treturn setFileData(e, defBl60, 0x60);\n')]),
    # loadFileCrc: fewer redundant terms
    ('fc_pad1', [('\t\tif (pad && (size & 15) && size != e->size)\n', '\t\tif (pad && size != e->size)\n')]),
    ('fc_and15', [('\t\tif (pad && (size & 15) && size != e->size)\n', '\t\tif ((size & 15) && size != e->size)\n')]),
]
V = V + V2
