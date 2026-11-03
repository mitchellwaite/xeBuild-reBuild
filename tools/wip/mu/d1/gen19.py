"""gen19.py: natural spellings of the split tail on the local-ret helper (the store conditional on ret), and whether pret / code can be simplified."""
import axes as a
import gen14
import gen16
import gen18 as g
import sw

LOGT = """			log_printf(0, "%s image built, info:\\n", xb.outName);
"""
vs = []
vs.append(('store0', g.c_local(g.base(tail=LOGT + """			*pret = 0;
			if (ret)
				*pret = ret;
"""))))
c = g.c_local(g.base(tail=LOGT + """			if (ret)
				*pret = ret;
"""))
assert 'int i, ret, code;' in c
vs.append(('cond_code0', c.replace('int i, ret, code;', 'int i, ret, code = 0;')))
vs.append(('ifelse', g.c_local(g.base(tail=LOGT + """			if (!ret)
				*pret = 0;
			else
				*pret = ret;
"""))))
vs.append(('ifelse5', g.c_local(g.base(tail=LOGT + """			if (ret)
				*pret = 5;
			else
				*pret = 0;
"""))))
c2 = g.c_local(g.base(tail=LOGT + """			if (ret)
				*pret = 5;
"""))
vs.append(('cond5_code0', c2.replace('int i, ret, code;', 'int i, ret, code = 0;')))
sw.run(vs, '-O3', save='gen19')
