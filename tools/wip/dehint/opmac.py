"""applyIniOptions' macid block in other test orders, without the literal-order asm.
python opmac.py [extra trick names]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

START = '			if (strlen(s) != 12) {\n'
END = '''				}
			}
		}
	}
	if (xb.type - BUILD_JTAG <= 3) {'''
LEN = '''log_printf(0, "***** WARNING: invalid length macid '");
showHexPairs(0, s);
log_printf(0, "' provided in ini file! Discarding!\\n", s);
'''
CHR = '''__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));
__asm__ goto ("" :::: dzc1);
log_printf(0, "***** WARNING: invalid characters in macid '");
showHexPairs(0, s);
log_printf(0, "' provided in ini file! Discarding!\\n", s);
'''
CHR_NOHINT = '\n'.join(CHR.split('\n')[2:])
LOOP = '''/* keeps if-conversion from hoisting i = 0 above the test */
__asm__("");
for (i = 0; i < 6; i++) {
	xb.macid[i] = myatox8(s);
	s += 2;
}
'''
LOOP_NOBAR = '\n'.join(LOOP.split('\n')[2:])


def ind(s, n):
    return ''.join(('\t' * n + l if l else l) + '\n' for l in s.rstrip('\n').split('\n'))


def forms(chr_, loop):
    return {
        'cur': START + ind(LEN, 4) + '\t\t\t} else if (!validateString(s)) {\n' + ind(chr_, 4) +
               '\t\t\t} else {\n' + ind(loop, 4) + '\t\t\t}\n',
        'nest_ok': '\t\t\tif (strlen(s) == 12) {\n\t\t\t\tif (validateString(s)) {\n' + ind(loop, 5) +
                   '\t\t\t\t} else {\n' + ind(chr_, 5) + '\t\t\t\t}\n\t\t\t} else {\n' + ind(LEN, 4) + '\t\t\t}\n',
        'nest_bad': '\t\t\tif (strlen(s) == 12) {\n\t\t\t\tif (!validateString(s)) {\n' + ind(chr_, 5) +
                    '\t\t\t\t} else {\n' + ind(loop, 5) + '\t\t\t\t}\n\t\t\t} else {\n' + ind(LEN, 4) + '\t\t\t}\n',
        'eq_chain': '\t\t\tif (strlen(s) == 12) {\n\t\t\t\tif (validateString(s)) {\n' + ind(loop, 5) +
                    '\t\t\t\t} else {\n' + ind(chr_, 5) + '\t\t\t\t}\n\t\t\t} else {\n' + ind(LEN, 4) + '\t\t\t}\n',
        'len_ok_else': '\t\t\tif (strlen(s) == 12 && validateString(s)) {\n' + ind(loop, 4) +
                       '\t\t\t} else if (strlen(s) == 12) {\n' + ind(chr_, 4) + '\t\t\t} else {\n' + ind(LEN, 4) + '\t\t\t}\n',
    }


def main():
    extra = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    b, got = optricks.apply(optricks.base(), ['lit_mac'] + extra)
    i = b.find(START)
    j = b.find(END, i)
    tail = b[j + len('				}\n			}\n'):]
    for hint in ('all', 'nobar', 'nochr', 'none'):
        c = CHR_NOHINT if hint in ('nochr', 'none') else CHR
        lp = LOOP_NOBAR if hint in ('nobar', 'none') else LOOP
        for n, f in forms(c, lp).items():
            t = b[:i] + f + tail
            if 'dzc1' not in t.split('if (0) { dzc1')[0]:
                t = t.replace('	if (0) { dzc1: ; goto dz1; dz1:', '	if (0) { goto dz1; dz1:')
            print('%-6s %-12s %s' % (hint, n, optlib.fmt(optlib.score_text(t, optricks.flags_for(got)))[:150]), flush=True)


main()
