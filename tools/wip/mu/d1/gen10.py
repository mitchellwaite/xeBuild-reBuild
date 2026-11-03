"""gen10.py: dead pret test between buildImage and `if (!ret)`, so the folded test merges into the buildImage block and the arms keep the scaled frequency."""
import itertools

import axes as a
import sw

T = {
    'after_ret': """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		ret = buildImage();
		if (!pret)
			return;
		if (!ret) {
""",
    'before_bi': """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		updating = 1;
		if (!pret)
			return;
		ret = buildImage();
		if (!ret) {
""",
    'gcf_ret': """	int ret, r;

	if (getConsoleFiles(dumpDir)) {
		if (!pret)
			return;
		updating = 1;
		ret = buildImage();
		if (!ret) {
""",
}
vs = []
for (tk, tv), (rk, rv), (ek, ev), (ik, iv) in itertools.product(T.items(), a.REB.items(), a.ERRS.items(), a.IPS.items()):
    vs.append(('%s_%s_%s_%s' % (tk, rk, ek, ik), a.build(tv, rv, ev, iv)))
print(len(vs))
sw.run(vs, '-O3', save='gen10', top=25)
