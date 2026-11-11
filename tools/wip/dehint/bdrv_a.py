# Each of build.c's 16 borderline shapes made plain on its own (bdrv.py; 46fb4f14's src).
T = '\t'

ALIGN = ('static uint32_t align16(uint32_t v)\n{\n\treturn (v + 15) & ~15;\n}\n')

CPUFAN_HELPER = (
    'static int patchCpuFan(uint8_t *smc)\n{\n'
    '\tif (xb.cpuFan != 0xffffffff) {\n'
    '\t\tif (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {\n'
    '\t\t\tsmc[0x11] = xb.cpuFan | 0x80;\n'
    '\t\t\treturn 1;\n'
    '\t\t}\n'
    '\t\tif (xb.cpuFan)\n'
    '\t\t\tlog_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);\n'
    '\t\telse if (smc[0x11] != 0x7f) {\n'
    '\t\t\tsmc[0x11] = 0x7f;\n'
    '\t\t\treturn 1;\n'
    '\t\t}\n'
    '\t}\n'
    '\treturn 0;\n}\n')
CPUFAN_PLAIN = (
    'static int patchCpuFan(uint8_t *smc)\n{\n'
    '\tif (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {\n'
    '\t\tsmc[0x11] = xb.cpuFan | 0x80;\n'
    '\t\treturn 1;\n'
    '\t}\n'
    '\tif (xb.cpuFan)\n'
    '\t\tlog_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);\n'
    '\telse if (smc[0x11] != 0x7f) {\n'
    '\t\tsmc[0x11] = 0x7f;\n'
    '\t\treturn 1;\n'
    '\t}\n'
    '\treturn 0;\n}\n')
CPUFAN_CALL = ('\tif (xb.cpuFan != 0xffffffff) {\n'
               '\t\tif (patchCpuFan(smc))\n'
               '\t\t\tpatched = 1;\n'
               '\t}\n')
CPUFAN_INPLACE = (
    '\tif (xb.cpuFan != 0xffffffff) {\n'
    '\t\tif (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {\n'
    '\t\t\tsmc[0x11] = xb.cpuFan | 0x80;\n'
    '\t\t\tpatched = 1;\n'
    '\t\t} else if (xb.cpuFan)\n'
    '\t\t\tlog_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\\n", xb.cpuFan);\n'
    '\t\telse if (smc[0x11] != 0x7f) {\n'
    '\t\t\tsmc[0x11] = 0x7f;\n'
    '\t\t\tpatched = 1;\n'
    '\t\t}\n'
    '\t}\n')

UB_PAY = '\t\t\t\tr = useBuiltIn(e, defPayload, 0x200);\n'
UB_CORE = '\t\t\t\tr = useBuiltIn(e, defCore, 0xd40);\n'


def ub_out(src, n):
    return ('\t\t\t\te->data = malloc(%s);\n'
            '\t\t\t\tif (!e->data) {\n'
            '\t\t\t\t\tr = 1;\n'
            '\t\t\t\t\tbreak;\n'
            '\t\t\t\t}\n'
            '\t\t\t\te->size = %s;\n'
            '\t\t\t\tmemcpy(e->data, %s, %s);\n' % (n, n, src, n))


BL24 = ('\tif (loadBaseFile(e->name, e))\n\t\treturn defaultBl60(e);\n'
        '\tif (e->size != 0x60)\n\t\treturn defaultBl60(e);\n\treturn 0;\n')
BL24_OR = ('\tif (loadBaseFile(e->name, e) || e->size != 0x60)\n'
           '\t\treturn defaultBl60(e);\n\treturn 0;\n')

KIT = ('static int setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n'
       '\t\tsetFlashBuild(getBeU16(xb.files[i].data + 2));\n\treturn type == 14;\n}\n')
KIT_VOID = ('static void setKitBuild(uint32_t i, int type)\n{\n\tif (type == 14)\n'
            '\t\tsetFlashBuild(getBeU16(xb.files[i].data + 2));\n}\n')

R24 = ('\t\t\t\t\tr = 0;\n'
       '\t\t\t\t\tif (loadBaseFile(e->name, e))\n'
       '\t\t\t\t\t\tr = defaultBl60(e);\n'
       '\t\t\t\t\telse if (e->size != 0x60)\n'
       '\t\t\t\t\t\tr = defaultBl60(e);\n')

C27 = ('\t\t\t\tif (loadBaseFile(e->name, &xb.files[xb.nFlashFiles])) {\n'
       '\t\t\t\t\tr = loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]);\n'
       '\t\t\t\t\tif (r)\n'
       '\t\t\t\t\t\tr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]);\n'
       '\t\t\t\t\tif (r) {\n')
C27_END = ('\t\t\t\t\t\tr = 0;\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\t{\n')
C27_AND = ('\t\t\t\tif (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&\n'
           '\t\t\t\t    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&\n'
           '\t\t\t\t    (r = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {\n'
           '\t\t\t\t\t{\n')
C27_NEST = ('\t\t\t\tif (loadBaseFile(e->name, &xb.files[xb.nFlashFiles])) {\n'
            '\t\t\t\t\tif (loadBaseFile("config.bin", &xb.files[xb.nFlashFiles])) {\n'
            '\t\t\t\t\t\tr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]);\n'
            '\t\t\t\t\t\tif (r) {\n')
C27_NEST_END = ('\t\t\t\t\t\tr = 0;\n\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t\t{\n')

UPD = ('\tif (type == 23)\n\t\treturn 1;\n\tif (type == 15)\n\t\treturn 1;\n'
       '\treturn type == 16 || type == 9 || type == 10 || type == 24 || type == 25;\n')
UPD_OR = ('\treturn type == 23 || type == 15 || type == 16 || type == 9 || type == 10 ||'
          ' type == 24 || type == 25;\n')

INIT = ('static int initFlash(uint8_t *salt)\n{\n\tint fuse = 1;\n\n\tmemset(salt, 0, 16);\n'
        '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
        '\t\tif (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)\n\t\t\treturn 1;\n'
        '\t}\n\treturn fuse & 1;\n}\n')

V = [
    # 1 align16 as a macro (every site)
    ('al_macro', [(ALIGN, '#define align16(v) (((v) + 15) & ~15)\n')]),
    # 2 findFileOffset / findFileSize return uint32_t
    ('ff_u32', [('int findFileOffset(int type)\n{', 'uint32_t findFileOffset(int type)\n{'),
                ('int findFileSize(int type)\n{', 'uint32_t findFileSize(int type)\n{'),
                ('build.h', 'int findFileOffset(int type);', 'uint32_t findFileOffset(int type);')]),
    ('ff_u32size', [('int findFileSize(int type)\n{', 'uint32_t findFileSize(int type)\n{')]),
    ('ff_u32off', [('int findFileOffset(int type)\n{', 'uint32_t findFileOffset(int type)\n{'),
                   ('build.h', 'int findFileOffset(int type);', 'uint32_t findFileOffset(int type);')]),
    # 3 loadFileCrc's log test
    ('fc_size', [('\t\tif (pad && (size & 15) && size != e->size)\n', '\t\tif (size != e->size)\n')]),
    ('fc_esize', [('\t\tif (pad && (size & 15) && size != e->size)\n', '\t\tif (e->size != size)\n')]),
    ('fc_pad', [('\t\tif (pad && (size & 15) && size != e->size)\n', '\t\tif (pad && (size & 15))\n')]),
    # 4 loadInputFile's crc
    ('li_u32', [('int loadInputFile(const char *name, struct fileent *e, int pad, int crc, uint8_t *meta,',
                 'int loadInputFile(const char *name, struct fileent *e, int pad, uint32_t crc, uint8_t *meta,')]),
    # 5 patchCpuFan's repeated test
    ('cf_helper', [(CPUFAN_HELPER, CPUFAN_PLAIN)]),
    ('cf_caller', [(CPUFAN_CALL, '\tif (patchCpuFan(smc))\n\t\tpatched = 1;\n')]),
    ('cf_inplace', [(CPUFAN_CALL, CPUFAN_INPLACE), (CPUFAN_HELPER, '')]),
    # 6 extractSmcConfig
    ('sc_u32', [('int extractSmcConfig(struct fileent *e, uint8_t *buf, int size)',
                 'int extractSmcConfig(struct fileent *e, uint8_t *buf, uint32_t size)')]),
    ('sc_memcpy', [('\t\t\t*(struct smcConfigData *)e->data = *(const struct smcConfigData *)(buf + i);\n',
                    '\t\t\tmemcpy(e->data, buf + i, 0x400);\n')]),
    # 7 useBuiltIn written out
    ('ub_out', [(UB_PAY, ub_out('defPayload', '0x200')), (UB_CORE, ub_out('defCore', '0xd40'))]),
    # 8 defaultBl60
    ('d6_memcpy', [('\tmemmove(e->data, defBl60, 0x60);\n', '\tmemcpy(e->data, defBl60, 0x60);\n')]),
    ('d6_ub', [('\te->data = malloc(0x60);\n\tif (!e->data)\n\t\treturn 1;\n\te->size = 0x60;\n'
                '\tmemmove(e->data, defBl60, 0x60);\n\treturn 0;\n',
                '\treturn useBuiltIn(e, defBl60, 0x60);\n')]),
    # 9 loadBl24's two calls
    ('b24_or', [(BL24, BL24_OR)]),
    # 10 setKitBuild's ignored return
    ('kit_void', [(KIT, KIT_VOID)]),
    # 11 the tail's (int)r < 0
    ('r_ne', [('\t\t\t\t\tif ((int)r < 0)\n', '\t\t\t\t\tif (r)\n')]),
    ('r_int', [('\t\tuint32_t r = 0;\n', '\t\tint r = 0;\n'),
               ('\t\t\t\t\tif ((int)r < 0)\n', '\t\t\t\t\tif (r < 0)\n')]),
    ('r_intne', [('\t\tuint32_t r = 0;\n', '\t\tint r = 0;\n'),
                 ('\t\t\t\t\tif ((int)r < 0)\n', '\t\t\t\t\tif (r)\n')]),
    # 12 case 24's written-out loadBl24
    ('r24_call', [(R24, '\t\t\t\t\tr = loadBl24(e);\n')]),
    ('r24_else', [(R24, '\t\t\t\t\tif (loadBaseFile(e->name, e))\n\t\t\t\t\t\tr = defaultBl60(e);\n'
                        '\t\t\t\t\telse if (e->size != 0x60)\n\t\t\t\t\t\tr = defaultBl60(e);\n'
                        '\t\t\t\t\telse\n\t\t\t\t\t\tr = 0;\n')]),
    ('r24_or', [(R24, '\t\t\t\t\tif (loadBaseFile(e->name, e) || e->size != 0x60)\n'
                      '\t\t\t\t\t\tr = defaultBl60(e);\n\t\t\t\t\telse\n\t\t\t\t\t\tr = 0;\n')]),
    ('r24_both', [('\t\t\t\t\tr = loadBl24(e);\n\t\t\t\tif (xb.type == BUILD_DEVGL',
                   '\t\t\t\t\tr = 0;\n\t\t\t\t\tif (loadBaseFile(e->name, e))\n\t\t\t\t\t\tr = defaultBl60(e);\n'
                   '\t\t\t\t\telse if (e->size != 0x60)\n\t\t\t\t\t\tr = defaultBl60(e);\n'
                   '\t\t\t\tif (xb.type == BUILD_DEVGL')]),
    # 13 case 27's fallbacks
    ('c27_and', [(C27, C27_AND)]),
    ('c27_nest', [(C27, C27_NEST), (C27_END, C27_NEST_END)]),
    # 14 addBlsToImage: 23 before 25
    ('x23', [('BUILD_RETAIL && (type == 25 || type == 23)', 'BUILD_RETAIL && (type == 23 || type == 25)'),
             ('BUILD_DEVGL16 && (type == 25 || type == 23)', 'BUILD_DEVGL16 && (type == 23 || type == 25)')]),
    # 15 isUpdateBl as one || chain
    ('upd_or', [(UPD, UPD_OR)]),
    # 16 initFlash
    ('if_ret', [('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_ne', [('\treturn fuse & 1;\n}\n', '\treturn fuse != 0;\n}\n')]),
    ('if_bool', [('\tint fuse = 1;\n\n\tmemset(salt', '\t_Bool fuse = 1;\n\n\tmemset(salt'),
                 ('\treturn fuse & 1;\n}\n', '\treturn fuse;\n}\n')]),
    ('if_early', [(INIT, 'static int initFlash(uint8_t *salt)\n{\n\tmemset(salt, 0, 16);\n'
                         '\tif (xb.type == BUILD_JTAG)\n\t\treturn 1;\n'
                         '\tif (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)\n\t\treturn 1;\n'
                         '\treturn xb.glitch2mfg != 0;\n}\n')]),
    ('if_inline', [(INIT, ''), ('\tfuse = initFlash(salt);\n',
                                '\tmemset(salt, 0, 16);\n\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n'
                                '\t\tfuse = xb.glitch2mfg != 0;\n'
                                '\t\tif (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)\n'
                                '\t\t\tfuse = 1;\n\t}\n')]),
]
