"""Attempt 58: calcBlAreaSize with fileent.size's type changes and local types (pin kept / off).
python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a58_cba.py -o "-;pin_size" """
XH = 'xebuild.h'
FS = ('\tuint8_t *data;\n\tuint32_t size;\n\tuint8_t key[16];', '\tuint8_t *data;\n\t%s size;\n\tuint8_t key[16];')
D = '\tuint32_t size, xs, x;\n'
V = {}
for t in ['unsigned long', 'long', 'size_t', 'unsigned', 'int32_t', 'signed']:
    V['fs_' + t.replace(' ', '_')] = ({XH: [(FS[0], FS[1] % t)]}, [])
for d in ['int size; uint32_t xs, x;', 'uint32_t size, xs; int x;', 'unsigned long size; uint32_t xs, x;',
          'size_t size; uint32_t xs, x;', 'uint32_t size, x; int xs;', 'int size, xs, x;',
          'uint32_t size; int xs, x;']:
    V['loc_' + d.replace(' ', '').replace(';', '_').replace(',', '')] = ({}, [(D, '\t' + d + '\n')])
