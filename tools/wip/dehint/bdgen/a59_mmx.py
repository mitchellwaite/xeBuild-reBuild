"""Attempt 59: on the memmove base (mm_N_all), the other memcpy sites as memmove (inline-size lever),
crossed with the remaining hints.  python tools/wip/dehint/bdgen/a58lib.py tools/wip/dehint/bdgen/a59_mmx.py -o "-;exp_pr;vol_fail;lab_devgl;exp_devgl" """
import importlib.util, os
s = importlib.util.spec_from_file_location('m', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'a59_mm.py'))
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
BASE = m.V['mm_N_all'][1]
SITES = {
    'sfd': '\tmemcpy(e->data, data, size);\n',
    'aap1': '\tmemcpy(buf, e->data, size);\n',
    'aap2': '\t\t\t\t\tmemcpy(buf + size, a->data, a->size);\n',
    'esc': '\t\t\tmemcpy(e->data + j * 0x200, buf + i + j * 0x210, 0x200);\n',
    'blmod': '\t\tmemcpy(xb.files[cbb].data + off, blmod, size);\n',
}
V = {'base': ({}, BASE)}
for k, a in SITES.items():
    V[k] = ({}, BASE + [(a, a.replace('memcpy', 'memmove'))])
V['aap12'] = ({}, BASE + [(SITES[k], SITES[k].replace('memcpy', 'memmove')) for k in ('aap1', 'aap2')])
