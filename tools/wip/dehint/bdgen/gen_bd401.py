"""Attempt 29, DIAGNOSTIC (not candidates): how far block 116 falls when the CG failure and the other types' `else break`
lose PRED_TREE_EARLY_RETURN, without the result-test join of gen_bd400 (which moves the whole tail).  The two failures
go to a label at the very end of loadBl whose block holds an empty asm (so it isn't a forwarder) and is the return
block's prev_bb: predict.c skips the early-return prediction for a pred whose single successor is the return block
when it is the return block's prev (`e->dest != bb->next_bb`).  Variants keep fail at the end (then fail loses the
exemption) or move it before `out`.  Run with bddup.py on the near miss (gen_bd390's PRE).  Runs on src as of 1caeb924."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_bd390 import PRE

FB = '''			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
'''
END = '''fail:
	__asm__ __volatile__("");
	*pr = -1;
}
'''


def fb(cg, other):
    return '''			} else if (type == 10) {
				if (!suGetCG(&e->data, &e->size))
					%s;
				goto chk;
			} else
				%s;
		}
''' % (cg, other)


ENDS = {
    'after_fail': END[:-2] + '\n\treturn;\nout:\n\t__asm__ __volatile__("");\n}\n',
    'before_fail': 'out:\n\t__asm__ __volatile__("");\n\treturn;\n' + END,
}
ARMS = {
    'both': ('goto out', 'goto out'),
    'cg': ('goto out', 'break'),
    'else': ('break', 'goto out'),
}


def mk(b, a, e):
    b = bdrun.sub(b, FB, fb(*ARMS[a]), 1)
    return bdrun.sub(b, END, ENDS[e], 1)


def CASES(base):
    return [('src', lambda b: b)] + [('%s %s' % (a, e), lambda b, a=a, e=e: mk(b, a, e)) for a in ARMS for e in ENDS]


FOCUS = ['_loadBlFiles']
