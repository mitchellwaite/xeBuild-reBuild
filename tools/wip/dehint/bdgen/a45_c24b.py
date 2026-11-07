import sys
sys.path.insert(0,'tools/wip/dehint'); import bdrun
t=open('build/bd/a45/n1.c').read()
V={'gfirst':[('if (xb.type == BUILD_JTAG || xb.glitch2mfg) {','if (xb.glitch2mfg || xb.type == BUILD_JTAG) {')],
   'dvfirst':[('if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {','if (xb.type == BUILD_DEVGL16 || xb.type == BUILD_DEVGL) {')],
   'dvrange':[('if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {','if (xb.type >= BUILD_DEVGL && xb.type <= BUILD_DEVGL16) {')],
   'jtag_ne':[('if (xb.type == BUILD_JTAG || xb.glitch2mfg) {','if (!(xb.type != BUILD_JTAG && !xb.glitch2mfg)) {')],
}
for k,v in V.items():
    s=t
    for a,b in v: s=bdrun.sub(s,a,b,1)
    r=bdrun.score(s,['--param','builtin-expect-probability=99'])
    print(k, 'IDENT' if r.get('identical') else (sum(r['L'].values()), sum(r['S'].values()), r['L'], r['notes']))
