"""Attempt 45: one hint on n1 (build/bd/a45/n1.c) in place of the four it drops: does any single label/expect close case 24's block?"""
import sys
sys.path.insert(0, 'tools/wip/dehint'); import bdrun
t = open('build/bd/a45/n1.c').read()
CF = '''						if (type == 9) {
							if (suGetCF(&e->data, &e->size))'''
A1 = '''					if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
						if (loadBaseFile(e->name, e))
							r = defaultBl60(e);
						else if (e->size != 0x60)
							r = defaultBl60(e);
					}
'''
V = {
    'cf_cold': [(CF, CF.replace('if (type == 9) {\n', 'if (type == 9) {\n\t\t\t\t\t\t\tcf: __attribute__((cold));\n'))],
    'a1_cold': [(A1, A1.replace('if (xb.type == BUILD_JTAG || xb.glitch2mfg) {\n', 'if (xb.type == BUILD_JTAG || xb.glitch2mfg) {\n\t\t\t\t\t\ta1: __attribute__((cold));\n'))],
    'a1r_cold': [(A1, A1.replace('\t\t\t\t\t}\n', '\t\t\t\t\t\tif (r) {\n\t\t\t\t\t\ta1r: __attribute__((cold));\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n'))],
    'a1r_hot': [(A1, A1.replace('\t\t\t\t\t}\n', '\t\t\t\t\t\tif (r) {\n\t\t\t\t\t\ta1r: __attribute__((hot));\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n'))],
    'sz_exp': [(A1, A1.replace('else if (e->size != 0x60)', 'else if (__builtin_expect(e->size != 0x60, 0))'))],
}
for k, v in V.items():
    s = t
    for a, b in v:
        s = bdrun.sub(s, a, b, 1)
    r = bdrun.score(s, ['--param', 'builtin-expect-probability=99'])
    print(k, 'IDENTICAL' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r.get('L'), r.get('notes'), r.get('err', '')[:200]))
