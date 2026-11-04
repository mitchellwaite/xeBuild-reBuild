"""python tools/wip/dehint/iw23one.py <draft.c>: the attempt 23 draft with one thing changed at a time: spellings of the arm's table loop, and each move put back as src has it. Prints lines for each."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
t = open(sys.argv[1], newline='').read().replace('\r\n', '\n')
I = '\t' * 7
TAB = I + 'uint32_t used[2] = { (off & 0x1ffff) / 512, 0 };\n'
LOOP = I + 'left = 256;\n' + I + 'for (k = 0; k < 2; k++)\n'
V = {
 'k!=2': [('k < 2', 'k != 2')],
 'ku': [(I + 'int k;\n', I + 'uint32_t k;\n')],
 'nint': [(TAB, TAB.replace('uint32_t used', 'int used'))],
 'one iteration, {256, x}': [(TAB, I + 'uint32_t used[2] = { 256, (off & 0x1ffff) / 512 };\n'), (LOOP, I + 'left = used[0];\n' + I + 'for (k = 1; k != 2; k++)\n')],
 'no table': [(TAB + I + 'int k;\n\n' + LOOP + I + '\tleft -= used[k];\n', I + 'left = 256 - (off & 0x1ffff) / 512;\n')],
 'no s1': [('\t\t\t\t\t\tleft -= pages;\n\t\t\t\t\t\ts[9] = left >> 2;\n', '\t\t\t\t\t\ts[9] = (left - pages) >> 2;\n')],
 'no e2': [('\tlog_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + 0x4000);\n\tlen = i * 0x400;\n', '\tlen = i * 0x400;\n\tlog_printf(1, "offset 0x%x len 0x4000 (end 0x%x)...", off, off + len);\n')],
 'no ui': [('\tuint32_t i;\n\tuint32_t len;\n', '\tint i;\n\tuint32_t len;\n')],
 'no t0': [('\t\tif (rem < 0x4000)\n\t\t\ttail = rem;\n\t\telse\n\t\t\ttail = rem % 0x4000;\n', '\t\ttail = rem;\n\t\tif (rem >= 0x4000)\n\t\t\ttail = rem % 0x4000;\n')],
 'no bl': [('\tuint32_t b;\n\tuint32_t i;\n', '\tuint32_t b, blk;\n\tuint32_t i;\n'), ('(struct spb *)s)->b2lo = (start + b) >> 8', '(struct spb *)s)->b2lo = blk >> 8'), ('\t\t\tmemset(s, 0, 16);\n\t\t\tif (xb.bigBlock) {', '\t\t\tblk = start + b;\n\t\t\tmemset(s, 0, 16);\n\t\t\tif (xb.bigBlock) {')],
}
for k, ed in V.items():
    u = t
    for a, b in ed:
        if a not in u:
            print(k, 'MISSING', a[:40])
            break
        u = u.replace(a, b)
    else:
        print(k, iwlib.fmt(iwlib.score_text(u, []))[:120])
