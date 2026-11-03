"""gen17.py: cleaner helper shapes on the MATCH base (plain reboot test, c3 -ip).  Tests the `ret` parameter, an int return, and spellings of the writeImage test."""
import axes as a
import cur2
import gen14
import gen16
import sw

E = cur2.ERR
IP = gen16.FORMS['c3']
OKS = {
    'lt_init': """			if (dumpDir) {
				int r = writeImage(xb.outName);
				int ok = r == 0;

				if (ok < 1)
					%s
				log_printf(0, separator);
			}
""" % E,
    'le_init': """			if (dumpDir) {
				int r = writeImage(xb.outName);
				int ok = !r;

				if (ok <= 0)
					%s
				log_printf(0, separator);
			}
""" % E,
    'plain': a.ERRS['plain'],
}


def base(ok):
    return a.build(a.HEAD, a.REB['plain'], ok, IP)


TAIL_OLD = '\t*pret = ret;\n'
vs = []
for ok_k, ok_v in OKS.items():
    s0 = base(ok_v)
    # A: param ret, void (current)
    a0 = gen14.split(s0)
    a0 = a0.replace('{\n\tint r;\n\n\tnetUnmount', '{\n\tnetUnmount') if 'int r = writeImage' in a0 else a0
    vs.append(('A_param_' + ok_k, a0))
    # B: returns ret instead of the store
    b0 = gen14.split(s0, 'static int flashConsole(char *dumpDir, int ret)', '*pret = flashConsole(dumpDir, ret);')
    b0 = b0.replace('{\n\tint r;\n\n\tnetUnmount', '{\n\tnetUnmount') if 'int r = writeImage' in b0 else b0
    assert TAIL_OLD in b0
    b0 = b0.replace(TAIL_OLD, '\treturn ret;\n')
    vs.append(('B_ret_' + ok_k, b0))
    # C: local ret = 0, no param
    c0 = gen14.split(s0, 'static void flashConsole(char *dumpDir, int *pret)', 'flashConsole(dumpDir, pret);')
    c0 = c0.replace('{\n\tint r;\n\n\tnetUnmount', '{\n\tint r;\n\tint ret = 0;\n\n\tnetUnmount')
    if 'int r = writeImage' in c0:
        c0 = c0.replace('\tint r;\n\tint ret = 0;', '\tint ret = 0;')
    vs.append(('C_local_' + ok_k, c0))
    # D: local ret = 0, returned
    d0 = gen14.split(s0, 'static int flashConsole(char *dumpDir)', '*pret = flashConsole(dumpDir);')
    d0 = d0.replace('{\n\tint r;\n\n\tnetUnmount', '{\n\tint r;\n\tint ret = 0;\n\n\tnetUnmount')
    if 'int r = writeImage' in d0:
        d0 = d0.replace('\tint r;\n\tint ret = 0;', '\tint ret = 0;')
    d0 = d0.replace(TAIL_OLD, '\treturn ret;\n')
    vs.append(('D_localret_' + ok_k, d0))
sw.run(vs, '-O3', save='gen17')
