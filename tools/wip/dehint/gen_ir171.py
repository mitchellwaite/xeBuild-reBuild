"""parseDump: the dead `blk >= 0` was for P(not -2) in 73-78 (natural 72): a flag gives opcode positive 73 with no dead test."""
FOCUS = ['_parseDump', '_loadDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt10.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
OLD = '''		if (dst == -2) {
			if (blk >= 0)
				continue;
		}
'''
assert OLD in src
F = {
 'le': '		{ int used = dst != -2; if (used <= 0) continue; }\n',
 'lt': '		{ int used = dst != -2; if (used < 1) continue; }\n',
 'gt': '		{ int used = dst != -2; if (used > 0) { } else continue; }\n',
 'gl': '		if ((dst != -2) <= 0) continue;\n',
 'dc': '		used = dst != -2; if (used <= 0) continue;\n',
}
DECL = '	int blk, dst, p;\n	uint32_t i;\n	uint8_t *src;\n'
assert DECL in src
AX = [(k, [(OLD, v)] + ([(DECL, DECL + '	int used;\n')] if k == 'dc' else [])) for k, v in F.items()]
AXES = [AX]
