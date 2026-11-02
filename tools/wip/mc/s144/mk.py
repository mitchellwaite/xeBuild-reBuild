# mk.py : source variants for the shape recipe (a) p0 edge later, (b) r3x/r5x order
import sys
A = {
 'b': [('r5x, r3x); 0;})', 'r3x, r5x); 0;})')],
 'a0': [('||  ({JMP(p0); 0;}))', '))')],
 'au': [('{ AT(u2) client_usage(2, NULL); }', '{ AT(u2) JMP(p0); client_usage(2, NULL); }')],
 'au2': [('{ AT(u2) client_usage(2, NULL); }', '{ AT(u2) client_usage(2, NULL); JMP(p0); }')],
 'ah': [('does not exist!\n"); } }\n\t\t\t\t__asm__ goto ("" :::: dsp); break;', 'does not exist!\n"); JMP(p0); } }\n\t\t\t\t__asm__ goto ("" :::: dsp); break;')],
}
A['ah'] = [(r'cannot send avatar data when a HDD does not exist!\n"); } }', r'cannot send avatar data when a HDD does not exist!\n"); JMP(p0); } }')]
A['aw'] = [(r'log_printf(0, "setting write filename to %s\n", arg);', r'log_printf(0, "setting write filename to %s\n", arg); JMP(p0);')]
A['aw0'] = [('if (mode) { w5x: client_usage(5, argv[i]); }', 'JMP(p0); if (mode) { w5x: client_usage(5, argv[i]); }')]
A['ac'] = [('AT(c12) if (arg == dummy || ({JMP(p0); 0;}))', 'AT(c12) if (({JMP(p0); 0;}) || arg == dummy)')]
A['a0'] = [('if (arg == dummy || ({JMP(p0); 0;}))', 'if (arg == dummy)')]
base, name, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
s = open(base).read()
for k in keys:
    for a, b in A[k]:
        assert a in s, (k, a); s = s.replace(a, b, 1)
open(name + '.c', 'w', newline='\n').write(s)
