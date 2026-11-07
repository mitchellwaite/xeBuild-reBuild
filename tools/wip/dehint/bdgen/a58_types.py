"""Attempt 58: shared declarations' types, one at a time (build.o only; other objects checked by a full
build for the ones that matter).
python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a58_types.py"""
XH = 'xebuild.h'
V = {
    'src': ({}, []),
    # struct fileent
    'fe_type_u': ({XH: [('\tuint32_t crc;\n\tint type;', '\tuint32_t crc;\n\tuint32_t type;')]}, []),
    'fe_size_i': ({XH: [('\tuint8_t *data;\n\tuint32_t size;\n\tuint8_t key[16];', '\tuint8_t *data;\n\tint size;\n\tuint8_t key[16];')]}, []),
    'fe_off_i': ({XH: [('\tint type;\n\tuint32_t offset;', '\tint type;\n\tint offset;')]}, []),
    'fe_crc_i': ({XH: [('\tuint32_t crc;\n\tint type;', '\tint crc;\n\tint type;')]}, []),
    'fe_data_v': ({XH: [('\tuint32_t offset;\n\tuint8_t *data;', '\tuint32_t offset;\n\tunsigned char *data;')]}, []),
    # struct netfile
    'nf_size_u': ({XH: [('\tuint8_t *data;\n\tint size;\n};', '\tuint8_t *data;\n\tuint32_t size;\n};')]}, []),
    # struct xebuild
    'g2mfg_u': ({XH: [('\tint glitch2mfg;', '\tuint32_t glitch2mfg;')]}, []),
    'g2_u': ({XH: [('\tint glitch2;\n', '\tuint32_t glitch2;\n')]}, []),
    'cbb_i': ({XH: [('\tuint32_t cbb;', '\tint cbb;')]}, []),
    'serc_i': ({XH: [('\tuint32_t seReplacesCf;', '\tint seReplacesCf;')]}, []),
    'fromc_u': ({XH: [('\tint fromConsole;', '\tuint32_t fromConsole;')]}, []),
    'nfiles_u': ({XH: [('\tint nFiles;\n\tint nFlashFiles;', '\tuint32_t nFiles;\n\tint nFlashFiles;')]}, []),
    'nflash_u': ({XH: [('\tint nFiles;\n\tint nFlashFiles;', '\tint nFiles;\n\tuint32_t nFlashFiles;')]}, []),
    'type_i': ({XH: [('\tuint32_t type;\t\t\t/* build type */', '\tint type;\t\t\t/* build type */')]}, []),
    # cross-object prototypes
    'su_i': ({'sysupdate.h': [('uint32_t suGetCF(', 'int suGetCF('), ('uint32_t suGetCG(', 'int suGetCG(')]}, []),
    'cbv_u': ({'xboxrom.h': [('int cbVerifySig(', 'uint32_t cbVerifySig(')]}, []),
    'smcl_i': ({'image_write.h': [('uint32_t smcSetLoad(uint32_t size)', 'int smcSetLoad(uint32_t size)')]}, []),
    'smcl_ia': ({'image_write.h': [('uint32_t smcSetLoad(uint32_t size)', 'uint32_t smcSetLoad(int size)')]}, []),
    'cfsz_i': ({'image_write.h': [('uint32_t imgCfSize(void)', 'int imgCfSize(void)')]}, []),
    'slot_v': ({'image_write.h': [('uint32_t setPatchSlot(uint32_t off)', 'void setPatchSlot(uint32_t off)')]}, []),
    'slot_i': ({'image_write.h': [('uint32_t setPatchSlot(uint32_t off)', 'uint32_t setPatchSlot(int off)')]}, []),
    'flb_u': ({'image_write.h': [('void setFlashBuild(uint16_t build)', 'void setFlashBuild(uint32_t build)')]}, []),
    'be16_u': ({'fileutil.h': [('unsigned short getBeU16(', 'unsigned int getBeU16(')]}, []),
    'log_i': ({'log.h': [('void log_printf(unsigned int level,', 'void log_printf(int level,')]}, []),
    # build.h / build.c's own
    'ff_u': ({'build.h': [('int findFile(int type);', 'uint32_t findFile(int type);')]}, [('\nint findFile(int type)\n', '\nuint32_t findFile(int type)\n')]),
    'ffo_u': ({'build.h': [('uint32_t findFileOffset(int type);', 'uint32_t findFileOffset(uint32_t type);')]},
              [('uint32_t findFileOffset(int type)\n', 'uint32_t findFileOffset(uint32_t type)\n'), ('uint32_t findFileSize(int type)\n', 'uint32_t findFileSize(uint32_t type)\n')]),
    'lbf_u': ({}, [('static int loadBaseFile(const char *name, struct fileent *e)', 'static uint32_t loadBaseFile(const char *name, struct fileent *e)')]),
}
