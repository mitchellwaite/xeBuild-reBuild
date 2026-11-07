"""Attempt 26, vol_fail on the and9 base (gen_bd370's PRE), barrier off: where `fail:` sits in the source.  mergephi2
removes fail (it has a virtual PHI) by splitting its predecessors' edges into new forwarders, and split_edge_bb_loc puts
each new block after its source only when fail's prev_bb falls into fail; otherwise they all go where fail was, after
the size log, so at RTL every wholly matched -1 block has a higher index than the size log and crossjump can't share
the size log's -1 (attempt 10's rule).  So: put fail where the block before it falls into it.
Positions: `end` (src), `c2` (case 2 ends `if (e->offset) break; fail: *pr = -1; break;`), `c23` (the size log falls
into `fail: *pr = -1; break;` inside its if), `c2b` (case 2 as `if (!e->offset) { fail: *pr = -1; }` then break).
Crossed with the tail (src's t5le + `*pr` expect, without either, both off, plain break) and case 2 moved before case
23 or not.  Runs on src as of 9744ca00."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdrun
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd370 as g0

PRE = g0.PRE
C2_HEAD = '\tcase 2:\n\t\t*pr = loadBaseFile(e->name, &xb.files[xb.nFlashFiles]);\n'


def case_span(b, head, nxt):
    i = b.index(head)
    j = b.index(nxt, i)
    return i, j


def mk(b, pos, tk, lab, exp, move):
    b = bdrun.sub(b, g0.TAIL_OLD, g0.tail(tk, lab, exp), 1)
    end = '}\n'
    if pos == 'end':
        end = g0.END_OLD.replace('\t__asm__ __volatile__("");\n', '')
    elif pos == 'c2':
        b = bdrun.sub(b, g0.SMC_OLD, '''		if (e->offset)
			break;
	fail:
		*pr = -1;
		break;
	default:''', 1)
    elif pos == 'c2b':
        b = bdrun.sub(b, g0.SMC_OLD, '''		if (!e->offset) {
	fail:
			*pr = -1;
		}
		break;
	default:''', 1)
    elif pos == 'c23':
        b = bdrun.sub(b, g0.SIZE_OLD, g0.LOG + '\tfail:\n\t\t\t*pr = -1;\n\t\t\tbreak;\n', 1)
    b = bdrun.sub(b, g0.END_OLD, '\treturn;\n' + end if pos == 'end' else '\treturn;\n}\n', 1)
    if pos == 'end':
        b = b.replace('\treturn;\n\treturn;\n', '\treturn;\n')
    if move:
        i, j = case_span(b, C2_HEAD, '\tdefault:')
        c2 = b[i:j]
        b = b[:i] + b[j:]
        k = b.index('\tcase 23:\n\t\tif (xb.type == BUILD_RETAIL)')
        b = b[:k] + c2 + b[k:]
    return b


def CASES(base):
    out = []
    for pos, (tk, lab, exp), move in itertools.product(['end', 'c2', 'c2b', 'c23'],
                                                       [('g', 1, 1), ('g', 0, 1), ('g', 1, 0), ('g', 0, 0), ('plain', 0, 0)],
                                                       [0, 1]):
        out.append(('%s %s%s%s%s' % (pos, tk, ' lab' if lab else '', ' exp' if exp else '', ' mv2' if move else ''),
                    lambda b, a=(pos, tk, lab, exp, move): mk(b, *a)))
    return out


FOCUS = ['_loadBlFiles']
