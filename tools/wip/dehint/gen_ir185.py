"""getImageSmc, `ok &&` gone: bad arm placed in the chain after the size arms and before the sane test, so T's branch edge is the bad arm (cse's path) and notSane still sits just before the return block."""
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
TAILS = {
 'a': 'goto check;' + NL + BADA + 'check:' + NL + '{ int out = addr >= ' + L + '; if (out <= 0) { ' + LOAD + ' return; } }' + NL + NOT + '}' + NL + NL,
 'b': 'goto check;' + NL + BADA + 'check:' + NL + 'if (addr >= ' + L + ' <= 0) { ' + LOAD + ' return; }' + NL + NOT + '}' + NL + NL,
 'c': 'if (0) {' + NL + BADA + '}' + NL + '{ int out = addr >= ' + L + '; if (out <= 0) { ' + LOAD + ' return; } }' + NL + NOT + '}' + NL + NL,
 'd': 'goto check;' + NL + BADA + 'check:' + NL + '{ int in = addr < ' + L + '; if (in > 0) { ' + LOAD + ' return; } }' + NL + NOT + '}' + NL + NL,
}
AXES = [[(k, [(OLD, v), (OK1, '')]) for k, v in TAILS.items()]]
