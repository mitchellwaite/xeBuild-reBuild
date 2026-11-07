"""Attempt 58: findFile* return / loop types (build.h's prototypes and their bodies).
python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a58_ff.py -o "-;pin_size" """
BH = 'build.h'
FO = [('uint32_t findFileOffset(int type);', 'int findFileOffset(int type);')], [('uint32_t findFileOffset(int type)\n{', 'int findFileOffset(int type)\n{')]
FS = [], [('uint32_t findFileSize(int type)\n{', 'int findFileSize(int type)\n{')]
I = lambda fn, t: ('%s(int type)\n{\n\tint i;\n' % fn, '%s(int type)\n{\n\t%s i;\n' % (fn, t))
V = {
    'fo_i': ({BH: FO[0]}, FO[1]),
    'fs_i': ({}, FS[1]),
    'fofs_i': ({BH: FO[0]}, FO[1] + FS[1]),
    'fo_iu': ({}, [I('uint32_t findFileOffset', 'uint32_t')]),
    'fs_iu': ({}, [I('uint32_t findFileSize', 'uint32_t')]),
    'ff_iu': ({}, [I('int findFile', 'uint32_t')]),
}
