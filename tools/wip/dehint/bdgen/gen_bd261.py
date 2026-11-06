"""Attempt 15, lab_badsize: the patch size test written as a compare of two non-constants, so the opcode heuristic
(nonequal, 72%) adds to the early return's 61% (together about 80%: appendAddonPatches' block would fall to round 4).
It only helps if fold doesn't turn it back into `(size & 3) != 0` before profile_estimate.  Runs on src/build.c as of
4c988f7c."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bdhints, bdrun

OLD = '''		if (e->size & 3) {
		badsize: __attribute__((hot));
'''
FORMS = {
    'andnot': '		if ((e->size & ~3) != e->size) {\n',
    'andnot2': '		if (e->size != (e->size & ~3)) {\n',
    'divmul': '		if (e->size / 4 * 4 != e->size) {\n',
    'shift': '		if ((e->size >> 2 << 2) != e->size) {\n',
    'andnotu': '		if ((e->size & ~3u) != e->size) {\n',
    'mod': '		if (e->size % 4) {\n',
    'andfc': '		if ((e->size & 0xfffffffc) != e->size) {\n',
}


def CASES(base):
    out = []
    for k, v in FORMS.items():
        out.append((k, lambda b, v=v: bdrun.sub(b, OLD, v, 1)))
    return out


FOCUS = ['_loadBlFiles', '_loadConsoleBlFiles']
