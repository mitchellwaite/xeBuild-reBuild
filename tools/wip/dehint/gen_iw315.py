# attempt 25, pin_t: attempt 23's name moves toggled on the nested form (gen_iw313 q1, 8 lines of compare order), since they were chosen for the old flag test. Base: build/iw/a25/q1.c
# `IWB=build/iw/a25/q1.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw315.py -n 25 -t 2`
L1 = '\tlog_printf(1, "offset'
AXES = [
    [('', []),
     ('sl', [('left -= pages;\n\t\t\t\t\t\ts[9] = left >> 2;', 's[9] = (left - pages) >> 2;')])],
    [('', []),
     ('ta', [('if (rem < 0x4000)\n\t\t\ttail = rem;\n\t\telse\n\t\t\ttail = rem % 0x4000;', 'tail = rem % 0x4000;')]),
     ('tb', [('if (rem < 0x4000)\n\t\t\ttail = rem;\n\t\telse\n\t\t\ttail = rem % 0x4000;', 'tail = rem < 0x4000 ? rem : rem % 0x4000;')])],
    [('', []),
     ('bk', [('((struct spb *)s)->b2lo = (start + b) >> 8;', '{ uint32_t blk = start + b; ((struct spb *)s)->b2lo = blk >> 8; }')])],
    [('', []),
     ('u1', [('uint32_t used[2] = { (off & 0x1ffff) / 512, 0 };', 'int used[2] = { (off & 0x1ffff) / 512, 0 };')]),
     ('k1', [('for (k = 0; k < 2; k++)\n\t\t\t\t\t\t\t\tleft -= used[k];', 'for (k = 1; k >= 0; k--)\n\t\t\t\t\t\t\t\tleft -= used[k];')])],
    [('', []),
     ('p1', [('\t\t\tpg = start * 32;\n\t\t\ts = xb.spare + (pg + p + b * 32) * 16;', '\t\t\ts = xb.spare + (start * 32 + p + b * 32) * 16;')])],
]
