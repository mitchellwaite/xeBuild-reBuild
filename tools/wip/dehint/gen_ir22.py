"""getImageSmc: as gen_ir21, flipping which arm of the two validity tests is written first."""
import importlib.util, os
s = importlib.util.spec_from_file_location('g21', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ir21.py'))
g = importlib.util.module_from_spec(s); s.loader.exec_module(g)
FOCUS = g.FOCUS
BASE = g.BASE
BAD, S800, S000, TAIL, NS, OLD, mk, D = g.BAD, g.S800, g.S000, g.TAIL, g.NS, g.OLD, g.mk, g.D
A = dict(g.A)
A.update({
    'eq': f'if (!addr) {{\n{BAD}}}\nif (addr == 0x800 || addr == 0x1000) {{\n}} else {{\n{BAD}}}\n',
    'eqret': f'if (!addr) {{\n{BAD}}} else if (addr == 0x800 || addr == 0x1000) {{\n}} else {{\n{BAD}}}\n',
    'and1': f'if (addr != 0x1000 && addr != 0x800) {{\n{BAD}}}\n',
    'zlast': f'if (addr != 0x800 && addr != 0x1000) {{\n{BAD}}}\nif (!addr) {{\n{BAD}}}\n',
    'zin': f'if (addr != 0x800 && addr != 0x1000) {{\nif (!addr) {{\n{BAD}}} else {{\n{BAD}}}\n}}\n',
})
B = dict(g.B)
B.update({
    'eq': f'if (size == 0x3000 || size == 0x3800) {{\n}} else {{\nif (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n}}\n',
    'eq2': f'if (size == 0x3000 || size == 0x3800) {{\n}} else if (addr == 0x800) {{\n{S800}}} else {{\n{S000}}}\n',
    'tern': 'if (size != 0x3000 && size != 0x3800) {\nsize = addr == 0x800 ? 0x3800 : 0x3000;\nlog_printf(1, addr == 0x800 ? "smc.bin should not be 0x%x bytes, using 0x3800\n" : "smc.bin should not be 0x%x bytes, using 0x3000\n", size);\n}\n',
})
C = dict(g.C)
C['uc'] = f'if ((uint32_t)addr < 528 * xb.dumpPages) {{\n{TAIL}}} else {{\n{NS}}}\n'
C['sw'] = f'if (528 * xb.dumpPages > addr) {{\n{TAIL}}} else {{\n{NS}}}\n'
AXES = [[(f'{dk}.{ak}.{bk}.{ck}', [(OLD, mk(d, a, b, c))])
         for dk, d in {'ii': D['ii']}.items() for ak, a in A.items() for bk, b in B.items() for ck, c in C.items()]]
