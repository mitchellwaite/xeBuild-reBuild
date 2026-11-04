# attempt 25, pin_t: spellings around the nested form (gen_iw313 q1), which is 8 lines of compare order only (.constprop.1 2, writeFsTable 6). Base: build/iw/a25/q1.c
# `IWB=build/iw/a25/q1.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw314.py -n 30 -t 2`
S = "\t\tsmall = type != 0 && type != '0';\n\t\tpartial = len < 0x4000;\n"
AXES = [
    [('', []),
     ('o1', [(S, "\t\tpartial = len < 0x4000;\n\t\tsmall = type != 0 && type != '0';\n")]),
     ('o2', [(S, "\t\tpartial = len < 0x4000;\n"), ('\t\t\tif (small) {', "\t\t\tsmall = type != 0 && type != '0';\n\t\t\tif (small) {")]),
     ('o3', [(S, "\t\tpartial = len < 0x4000;\n"), ('\t\t\tif (small) {', "\t\t\tif (type != 0 && type != '0') {"), ('\t_Bool small;\n', '')]),
     ('o4', [(S, "\t\tpartial = len < 0x4000;\n"), ('\t\t\tif (small) {', "\t\t\tif (type && type != '0') {"), ('\t_Bool small;\n', '')]),
     ('o5', [(S, ''), ('\t\tif (partial > 0) {\n\t\t\tif (small) {', "\t\tpartial = len < 0x4000;\n\t\tif (partial > 0) {\n\t\t\tsmall = type != 0 && type != '0';\n\t\t\tif (small) {")]),
     ],
    [('', []),
     ('t1', [('\tint partial;\n', '\tint partial;\n'.replace('int partial', 'int partial = 0'))]),
     ('t2', [('\tint partial;\n', '\tshort partial;\n')]),
     ('t3', [('\tint partial;\n', '\tsigned char partial;\n')]),
     ('t4', [('\tint partial;\n', '\tlong partial;\n')]),
     ],
]
