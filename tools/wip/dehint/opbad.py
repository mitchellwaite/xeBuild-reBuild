"""parseOption: arms that print the bad-value error themselves instead of `goto bad`
(crossjump can merge the copies; the call itself gives PRED_CALL on the edge).
python opbad.py [extra trick names]   (po1, po2, po_nei always applied)"""
import itertools, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, optricks

ARMS = ['cpuTemp', 'gpuTemp', 'edramTemp', 'overCpuTemp', 'overGpuTemp', 'overEdramTemp',
        'cpuFan', 'gpuFan', 'avRegion', 'gameRegion', 'dvdRegion']
BAD = '''			if (xb.%s == -1)
				goto bad;
'''
COPY = '''			if (xb.%s == -1) {
				log_printf(1, "\\n\\n***** ERROR: parsing option '%%s', value '%%s' is incorrect!\\n", opt, val);
				return 0;
			}
'''


def variant(b, arms):
    for a in arms:
        b = b.replace(BAD % a, COPY % a)
    return b


def main():
    extra = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    b, got = optricks.apply(optricks.base(), ['po1', 'po2', 'po_nei'] + extra)
    sets = [('cpuTemp', 'gpuFan'), ('cpuTemp',), ('gpuFan',), tuple(ARMS)]
    sets += [tuple(ARMS[:k]) for k in range(2, 11)]
    for s in sets:
        r = optlib.score_text(variant(b, s), optricks.flags_for(got))
        print('%-40s %s' % ('+'.join(s)[:40], optlib.fmt(r)[:120]), flush=True)


main()
