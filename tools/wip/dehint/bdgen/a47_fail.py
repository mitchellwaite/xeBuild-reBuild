"""Attempt 47: the fail: site without the barrier, on src as of 5877c248 (loop form).
python tools/wip/dehint/bdgen/a46run.py tools/wip/dehint/bdgen/a47_fail.py"""
import os
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'src', 'build.c')
SMC = '''				e->offset = smcSetLoad(e->size);
				if (e->offset)
					break;
				/* one -1 block for the patch size, SMC and (xb.type <=
				   BUILD_DEVGL16) signature failures: the asm keeps it a block
				   of its own (else the -1 is appended to the size log, which
				   crossjump can't then share) */
			fail:
				__asm__ __volatile__("");
				r = -1;
				break;
'''
SZ = '''					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					goto fail;
'''
TL = '''					if (__builtin_expect(r != 0, 0))
						goto fail;
'''
DEF = '''				log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
				break;
			}
'''
SMC_PLAIN = '''				e->offset = smcSetLoad(e->size);
				if (e->offset)
					break;
			fail:
				r = -1;
				break;
'''
V = {
 'nobar': [(SMC, SMC_PLAIN)],
 'smcgoto_end': [(SMC, '''				e->offset = smcSetLoad(e->size);
				if (!e->offset)
					goto fail;
				break;
'''), (DEF, DEF.replace('\t\t\t}\n', '\t\t\tfail:\n\t\t\t\tr = -1;\n\t\t\t\tbreak;\n\t\t\t}\n'))],
 'smcif': [(SMC, '''				e->offset = smcSetLoad(e->size);
				if (!e->offset) {
			fail:
					r = -1;
				}
				break;
''')],
 'f23': [(SMC, '''				e->offset = smcSetLoad(e->size);
				if (e->offset)
					break;
				goto fail;
'''), (SZ, '''					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
			fail:
					r = -1;
					break;
''')],
 'szm1': [(SMC, SMC_PLAIN), (SZ, SZ.replace('goto fail;', 'r = -1;\n\t\t\t\t\tbreak;'))],
 'each': [(SMC, SMC_PLAIN.replace('\t\t\tfail:\n', '')), (SZ, SZ.replace('goto fail;', 'r = -1;\n\t\t\t\t\tbreak;')),
          (TL, TL.replace('goto fail;', 'r = -1;'))],
 'tlm1': [(SMC, SMC_PLAIN), (TL, TL.replace('goto fail;', 'r = -1;'))],
 'sz_rm1first': [(SMC, SMC_PLAIN), (SZ, '''					r = -1;
					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					break;
''')],
}
