"""getImageSmc: no dead test on the sane check.  P(not sane) window 78-91 measured; a flag (positive 73, calls in both arms cancel) with early return (61) on the sane arm: 80.8."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('	if (ok && addr < 528 * xb.dumpPages)\n')
j = src.index('badAddr:\n')
OLD = src[i:j]
NOT = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);\n'
LIM = '528 * xb.dumpPages'
F = {
 'o1': f'{{ int out = addr >= {LIM}; if (out <= 0) {{ loadSmc(addr, size); return; }} {NOT} return; }}\n',
 'o2': f'{{ int out = addr >= {LIM}; if (out > 0) {{ {NOT} return; }} loadSmc(addr, size); return; }}\n',
 'o3': f'{{ int out = addr >= {LIM}; if (out > 0) {{ {NOT} }} else {{ loadSmc(addr, size); return; }} return; }}\n',
 'o4': f'{{ int out = addr >= {LIM}; if (out <= 0) {{ loadSmc(addr, size); }} else {{ {NOT} }} return; }}\n',
 'o5': f'{{ int out = addr >= {LIM}; if (out > 0) {{ {NOT} }} else {{ loadSmc(addr, size); }} return; }}\n',
 'n1': f'{{ int in = addr < {LIM}; if (in) {{ loadSmc(addr, size); return; }} {NOT} return; }}\n',
 'n2': f'if (addr < {LIM}) {{ loadSmc(addr, size); return; }} {NOT} return;\n',
 'n3': f'if (addr >= {LIM}) {{ {NOT} return; }} loadSmc(addr, size); return;\n',
 'u1': f'{{ int out = (unsigned)addr >= {LIM}; if (out <= 0) {{ loadSmc(addr, size); return; }} {NOT} return; }}\n',
 'u2': f'{{ int out = {LIM} <= addr; if (out <= 0) {{ loadSmc(addr, size); return; }} {NOT} return; }}\n',
}
K = {'k': (), 'd': (('		ok = 1;\n', ''),)}
AX = []
for k, v in F.items():
    for kk, e in K.items():
        AX.append((k + '.' + kk, [(OLD, v)] + list(e)))
AXES = [AX]
