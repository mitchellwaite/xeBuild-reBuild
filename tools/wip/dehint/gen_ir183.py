"""getImageSmc, `ok &&` gone: not-sane arm in x.c's block order, P(not sane) 80.9 from positive 73 + the early return on the sane arm only (no return on the not-sane path)."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('	if (ok && addr < 528 * xb.dumpPages)\n')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
BADA = OLD[OLD.index('badAddr:'):OLD.rindex('}')]
NL = chr(10)
NOT = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image' + chr(92) + 'n", addr, size);' + NL
L = '528 * xb.dumpPages'
OK1 = '		ok = 1;' + NL
LOAD = 'loadSmc(addr, size);'
TT = '	if (t != 0x1000) {' + NL + '		if (t != 0x800)' + NL + '			goto badAddr;' + NL + '	}' + NL + 'fixSize:' + NL
FLAG = {
 'gt': (f'int out = addr >= {L};', 'out > 0', 'out <= 0'),
 'le': (f'int in = addr < {L};', 'in <= 0', 'in > 0'),
}
SH = {}
for k, (d, tn, ts) in FLAG.items():
    SH['s1' + k] = '{ ' + d + ' if (' + tn + ') ' + NOT + 'else { ' + LOAD + ' return; } }' + NL + 'goto end;' + NL + BADA + 'end: ;' + NL + '}' + NL + NL
    SH['s2' + k] = '{ ' + d + ' if (' + ts + ') { ' + LOAD + ' return; } }' + NL + NOT + 'goto end;' + NL + BADA + 'end: ;' + NL + '}' + NL + NL
    SH['s3' + k] = '{ ' + d + ' if (' + ts + ') { ' + LOAD + ' return; } else ' + NOT + '}' + NL + 'if (0) {' + NL + BADA + '}' + NL + '}' + NL + NL
    SH['s4' + k] = '{ ' + d + ' if (' + ts + ') { ' + LOAD + ' return; } }' + NL + NOT + '}' + NL + NL
ARM = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000' + chr(92) + 'n", addr);' + NL + 'addr = 0x1000;' + NL
TI = '	if (t != 0x1000) {' + NL + '		if (t != 0x800) {' + NL + ARM + '		}' + NL + '	}' + NL
AX = []
for k, s in SH.items():
    e = [(OLD, s), (OK1, '')]
    if k.startswith('s4'):
        e.append((TT, TI))
    AX.append((k, e))
AXES = [AX]
