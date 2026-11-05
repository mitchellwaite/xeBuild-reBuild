"""getImageSmc from gen_ir155's near miss: where pin_addr sits, and (candidate only) a second asm reading addr in the bad arm, for B."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt9.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('void getImageSmc(void)')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LOG0 = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n'
LL = LOG0 + ' addr = 0x1000;\n'
PIN = '__asm__("" : "+D"(addr));'
RD = '__asm__("" : : "D"(addr));'
ELSE = '} else {' + PIN + '}\n'
BAD = 'bad:\n' + LL
FORMS = {
 'base': [],
 'r1': [(BAD, f'bad:\n{LOG0}{RD}\n addr = 0x1000;\n')],
 'r2': [(BAD, f'bad:\n{RD}\n{LL}')],
 'p2': [(BAD, f'bad:\n{PIN}\n{LL}')],
 'p3': [(BAD, f'bad:\n{LOG0}{PIN}\n addr = 0x1000;\n')],
 'mv1': [(ELSE, '}\n'), (BAD, f'bad:\n{LOG0}{PIN}\n addr = 0x1000;\n')],
 'mv2': [(ELSE, '}\n'), ('bback:\n', f'bback:\n{PIN}\n')],
 'mv3': [(ELSE, '}\n'), ('unsigned t = addr;\n', f'{PIN}\n unsigned t = addr;\n')],
 'mv4': [(ELSE, '}\n'), (' if (t != 0x1000) { if (t != 0x800) goto bad; }\n', f' if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\n {PIN}\n')],
 'mv5': [(ELSE, '}\n'), (' if (t != 0x1000) { if (t != 0x800) goto bad; }\n', f' {PIN}\n if (t != 0x1000) {{ if (t != 0x800) goto bad; }}\n')],
}
AXES = [[(k, v) for k, v in FORMS.items()]]
