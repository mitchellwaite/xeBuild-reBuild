"""getImageSmc from gen_ir155's near miss: B by the bad arm's place in the block chain.  cse's make_regs_eqv makes addr's pseudo canonical only if its last use is past the end of the path, in insn order, so the bad log's block should come before addr's last use."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt9.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('void getImageSmc(void)')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
k = OLD.index('if (!addr)')
e = OLD.index('unsigned t = addr;')
HEAD = OLD[:k]
Z = OLD[k:e]
k = OLD.index('if (size != 0x3000')
e = OLD.index('if (t && addr')
SZ = OLD[k:e]
e2 = OLD.index('return;\nbad:')
SA = OLD[OLD.index('if (t && addr'):e2]
SA_R = SA.replace('loadSmc(addr, size); } else {', 'loadSmc(addr, size); return; }\n').rstrip()
assert SA_R.endswith('}')
SA_R = SA_R[:-1] + '\n'
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\n'
BAD = f'bad:\n{LL}goto bback;\n'
LIM = 'addr < 528 * xb.dumpPages'
NOT = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
FORMS = {
 'end': f'{Z}{T}bback:\n{SZ}{SA}return;\n{BAD}}}\n\n',
 'p1': f'{Z}{T}goto bback;\n{BAD}bback:\n{SZ}{SA}}}\n\n',
 'p2': f'{Z}{T}bback:\n{SZ}goto check;\n{BAD}check:\n{SA}}}\n\n',
 'p3': f'{Z}{T}bback:\n{SZ}if (t && addr < 528 * xb.dumpPages) {{ loadSmc(addr, size); return; }}\n goto ns;\n{BAD}ns:\n log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n}}\n\n',
 'p4': f'{T}bback:\n{SZ}{SA}return;\n{BAD}}}\n\n'.replace(T, Z + T),
 'p5': f'{Z}{T}bback:\n{SZ}if (t && {LIM}) goto sane;\n{NOT}goto done;\n{BAD}sane:\n loadSmc(addr, size);\ndone:;\n}}\n\n',
 'p6': f'{Z}{T}bback:\n{SZ}if (t && {LIM}) goto sane;\n{NOT}return;\n{BAD}sane:\n loadSmc(addr, size);\n}}\n\n',
 'p7': f'{Z}{T}bback:\n{SZ}if (t) {{ if ({LIM}) goto sane; }}\n{NOT}goto done;\n{BAD}sane:\n loadSmc(addr, size);\ndone:;\n}}\n\n',
 'p8': f'{Z}{T}bback:\n{SZ}if (t && {LIM}) goto sane;\n{NOT}goto done;\n{BAD}sane:\n loadSmc(addr, size);\n return;\ndone:;\n}}\n\n',
}
AXES = [[(k2, [(OLD, HEAD + v)]) for k2, v in FORMS.items()]]
