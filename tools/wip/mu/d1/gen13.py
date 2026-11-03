"""gen13.py: split the buildImage error arm with a redundant ret test (folded by VRP/DOM after the rebuild), so it no longer sits right before the return block:
no early-return predictor on `if (!ret)`, 50/50, then 128 can pop before 105.  No dummy."""
import itertools

import axes as a
import sw

OLD = """			log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
			*pret = 3;
"""
LOG = """			log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
"""
F = {
    'e1': LOG + """			if (ret)
				*pret = 3;
""",
    'e2': LOG + """			*pret = ret ? 3 : 0;
""",
    'e3': LOG + """			if (ret > 0 || ret < 0)
				*pret = 3;
""",
    'e4': LOG + """			if (!ret)
				*pret = 0;
			else
				*pret = 3;
""",
    'e5': """			if (ret)
				*pret = 3;
""" + LOG,
    'e6': """			if (ret) {
				log_printf(0, "\\n\\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\\n\\n", ret);
				*pret = 3;
			}
""",
}
vs = []
for (fk, fv), (rk, rv), (ek, ev), (ik, iv) in itertools.product(F.items(), a.REB.items(), a.ERRS.items(), a.IPS.items()):
    s = a.build(a.HEAD, rv, ev, iv)
    assert OLD in s
    vs.append(('%s_%s_%s_%s' % (fk, rk, ek, ik), s.replace(OLD, fv)))
print(len(vs))
sw.run(vs, '-O3', save='gen13', top=25)
