# gm.py: main-region structural variants on top of b.c (best). Writes v_<name>.c, prints names.
import sys
src = open('b.c').read()
V = {}
C12 = """				AT(c12) if (arg == dummy || ({JMP(p0); 0;}))
					{ AT(i0) { i0_c: __attribute__((cold)); } clientInfo(NULL); }
				else
					{ AT(i1) clientInfo(arg); }
				break;"""
V['m01'] = [(C12, """				AT(c12) if (arg != dummy && !({JMP(p0); 0;}))
					{ AT(i1) clientInfo(arg); }
				else
					{ AT(i0) { i0_c: __attribute__((cold)); } clientInfo(NULL); }
				break;""")]
V['m02'] = [(C12, """				AT(c12) if (arg == dummy || ({JMP(p0); 0;}))
					{ AT(i0) { i0_c: __attribute__((cold)); } arg = NULL; }
				AT(i1) clientInfo(arg);
				break;""")]
V['m03'] = [(C12, """				AT(c12) { if (({JMP(p0); 0;})) goto i0; clientInfo(arg == dummy ? NULL : arg); if (0) { i0: i1: clientInfo(NULL); } }
				break;""")]
V['m04'] = [(C12, """				AT(c12) if (({JMP(p0); 0;}) || arg == dummy)
					{ AT(i0) { i0_c: __attribute__((cold)); } clientInfo(NULL); }
				else
					{ AT(i1) clientInfo(arg); }
				break;""")]
V['m05'] = [(C12, """				AT(c12) if (arg == dummy || ({JMP(p0); 0;}))
					{ AT(i0) { i0_c: __attribute__((cold)); } clientInfo(NULL); break; }
				AT(i1) clientInfo(arg);
				break;""")]
C7 = """				AT(c7)  if (arg == dummy)
					{ AT(p0) { p0c: __attribute__((cold)); } clientPatches(NULL); JUMP(i0); }
				else
					{ AT(p1) clientPatches(arg); }
				break;"""
V['m06'] = [(C7, """				AT(c7)  if (arg != dummy)
					{ AT(p1) clientPatches(arg); }
				else
					{ AT(p0) { p0c: __attribute__((cold)); } clientPatches(NULL); JUMP(i0); }
				break;""")]
V['m07'] = [(C7, """				AT(c7)  if (arg == dummy)
					{ AT(p0) { p0c: __attribute__((cold)); } clientPatches(NULL); break; }
				AT(p1) clientPatches(arg);
				break;""")]
V['m08'] = [(C7, """				AT(c7)  if (arg == dummy)
					{ AT(p0) { p0c: __attribute__((cold)); } arg = NULL; }
				AT(p1) clientPatches(arg);
				break;""")]
C11 = """			case 11:
				AT(c11) clientBinPatch(arg, start);
				break;"""
C10 = """			case 10:
				AT(c10) clientEraseBlockI(arg);
				break;"""
# case order swaps (switch case text order)
V['m09'] = [(C10 + "\n" + C11, C11 + "\n" + C10)]
V['m10'] = [(C11, ""), ("			case 12:", C11 + "\n			case 12:")]
V['m11'] = [(C10, ""), ("			case 12:", C10 + "\n			case 12:")]
V['m12'] = [(C11, ""), ("			case 1:\n", C11 + "\n			case 1:\n")]
V['m13'] = [(C10, ""), ("			case 1:\n", C10 + "\n			case 1:\n")]
# -r: polarity / structure
R0 = """			if (mode) { r5x: client_usage(5, argv[i]); }
			arg = argv[++i];
			log_printf(0, "setting read filename to %s\\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;
			mode = 1;"""
V['m14'] = [(R0, """			if (!mode) {
			arg = argv[++i];
			log_printf(0, "setting read filename to %s\\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;
			mode = 1; } else { r5x: client_usage(5, argv[i]); }""")]
V['m15'] = [(R0, """			if (mode) { r5x: client_usage(5, argv[i]); }
			mode = 1;
			arg = argv[++i];
			log_printf(0, "setting read filename to %s\\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;""")]
V['m16'] = [(R0, """			if (mode) { r5x: client_usage(5, argv[i]); }
			i++;
			arg = argv[i];
			log_printf(0, "setting read filename to %s\\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;
			mode = 1;""")]
V['m17'] = [(R0, """			if (mode) { r5x: client_usage(5, argv[i]); }
			arg = a; i++;
			log_printf(0, "setting read filename to %s\\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;
			mode = 1;""")]
# 10/11 cases combined via fallthrough-free goto structure
V['m18'] = [(C10 + "\n" + C11, """			case 10:
				AT(c10) clientEraseBlockI(arg);
				break;
			case 11:
				AT(c11) { clientBinPatch(arg, start); }
				break;""")]
V['m19'] = [(C11, """			case 11:
				AT(c11) clientBinPatch(arg, start);
				__asm__ goto ("" :::: dsp); break;""")]
V['m20'] = [(C10, """			case 10:
				AT(c10) clientEraseBlockI(arg);
				__asm__ goto ("" :::: dsp); break;""")]
names = sys.argv[1:] or sorted(V)
for n in names:
    s = src
    for o, nw in V[n]:
        assert o in s, (n, o[:60])
        s = s.replace(o, nw, 1)
    open('v_%s.c' % n, 'w', newline='\n').write(s)
    print(n)
