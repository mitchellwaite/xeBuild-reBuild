# attempt 24: gen_iw301's forms x attempt 23's name moves undone one at a time.
# `IWB=build/iw/a24/nt.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw302.py -n 30 -t 4`
import importlib.util, os
sp = importlib.util.spec_from_file_location('g301', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_iw301.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g)
FO = [x for x in g.FO if x[0]]
E2 = [('', []), ('ne', [('\tlog_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n\tlen = i * 0x400;\n', '\tlen = i * 0x400;\n\tlog_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n')])]
UI = [('', []), ('nu', [('\tuint32_t i;\n\tuint32_t len;\n', '\tint i;\n\tuint32_t len;\n')])]
T0 = [('', []), ('nt', [('\t\tif (rem < 0x4000)\n\t\t\ttail = rem;\n\t\telse\n\t\t\ttail = rem % 0x4000;\n', '\t\ttail = rem;\n\t\tif (rem >= 0x4000)\n\t\t\ttail = rem % 0x4000;\n')])]
BL = [('', []), ('nb', [('\tuint32_t b;\n\tuint32_t i;\n', '\tuint32_t b, blk;\n\tuint32_t i;\n'), ('(struct spb *)s)->b2lo = (start + b) >> 8', '(struct spb *)s)->b2lo = blk >> 8'), ('\t\t\tmemset(s, 0, 16);\n\t\t\tif (xb.bigBlock) {', '\t\t\tblk = start + b;\n\t\t\tmemset(s, 0, 16);\n\t\t\tif (xb.bigBlock) {')])]
AXES = [FO, E2, UI, T0, BL]
