"""mode_client attempt 4: mc1's whole-construct groups (G_dy, G_dz, G_dv, G_efail, G_hdd,
G_dsp, G_kk) with the slot names of the current base (mc1's hard-coded indices are stale).

python tools/wip/dehint/mc4groups.py [BASE.c]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

base = mc1lib.read_src(sys.argv[1] if len(sys.argv) > 1 else mc1.BASE)
t = mc1.build_template(base)
L = t.lists
def lists_with(lab):
    return {nm: [lab] for nm, v in L.items() if lab in v[1]}
def cps_to(lab):
    return {nm: list(v[1]) for nm, v in L.items() if nm.startswith('cp_') and nm.endswith('') and lab in nm}
G = {}
var = t.var
G['G_dz'] = ({'dz': 1}, lists_with('dz'))
G['G_dv'] = ({'dv': 1}, lists_with('dv'))
d = lists_with('dy'); 
G['G_dy'] = ({'cebi_dy': 1, 'cp_dy_0': 1}, d)
G['G_efail'] = ({}, lists_with('efail'))
h = {}
for lab in ('hdd4', 'hdd5'):
    for k, v in lists_with(lab).items():
        h.setdefault(k, []).extend(v)
G['G_hdd'] = ({}, h)
G['G_dsp'] = ({}, lists_with('dsp'))
G['G_kk'] = ({'mc_kk': 1, 'r_memset': 1, 'r_ifkk': 1}, {})
for k, (st, dr) in G.items():
    st = {a: b for a, b in st.items() if a in var}
    s = mc1.score(t, st, dr)
    print('%-8s %s %s %s' % (k, st, dr, mc1lib.fmt(s)[:120]), flush=True)
