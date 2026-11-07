"""Attempt 58: build.c's own callee return types (the loaders' r is uint32_t), on the post-pin src.
python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a58_ret.py"""
XH = 'xebuild.h'
def R(old, new):
    return ({}, [(old, new)])
V = {
    'lif_u': R('int loadInputFile(const char *name, struct fileent *e, int pad, int crc, uint8_t *meta,', 'uint32_t loadInputFile(const char *name, struct fileent *e, int pad, int crc, uint8_t *meta,'),
    'chk_u': R('int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)', 'uint32_t checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)'),
    'lbin_u': R('int loadBinFile(struct fileent *e)\n{', 'uint32_t loadBinFile(struct fileent *e)\n{'),
    'lloc_u': R('int loadLocalFile(struct fileent *e)\n{', 'uint32_t loadLocalFile(struct fileent *e)\n{'),
    'esc_u': R('int extractSmcConfig(struct fileent *e, uint8_t *buf, int size)\n{', 'uint32_t extractSmcConfig(struct fileent *e, uint8_t *buf, int size)\n{'),
    'd60_u': ({}, [('static int defaultBl60(struct fileent *e)\n', 'static uint32_t defaultBl60(struct fileent *e)\n')]),
    'xell_u': ({}, [('static int loadXell(struct fileent *e)\n', 'static uint32_t loadXell(struct fileent *e)\n')]),
    'b24_u': ({}, [('static int loadBl24(struct fileent *e)\n', 'static uint32_t loadBl24(struct fileent *e)\n')]),
    'helpers_u': ({}, [('static int defaultBl60(struct fileent *e)\n', 'static uint32_t defaultBl60(struct fileent *e)\n'),
                       ('static int loadXell(struct fileent *e)\n', 'static uint32_t loadXell(struct fileent *e)\n'),
                       ('static int loadBl24(struct fileent *e)\n', 'static uint32_t loadBl24(struct fileent *e)\n')]),
    'data_c': ({XH: [('\tuint32_t offset;\n\tuint8_t *data;', '\tuint32_t offset;\n\tchar *data;')]}, []),
    'smccfg_u': ({XH: [('\tstruct netfile smcConfig;', '\tstruct { uint8_t *data; uint32_t size; } smcConfig;')]}, []),
    'kv_u': ({XH: [('\tstruct netfile kv;\n\tstruct netfile kvAlt;', '\tstruct { uint8_t *data; uint32_t size; } kv, kvAlt;')]}, []),
    'smc_u': ({XH: [('\tstruct netfile smc;', '\tstruct { uint8_t *data; uint32_t size; } smc;')]}, []),
}
