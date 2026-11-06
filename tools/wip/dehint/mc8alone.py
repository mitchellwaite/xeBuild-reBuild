"""mode_client attempt 8: every mc8comp removal alone on a base (score only).
python tools/wip/dehint/mc8alone.py BASE.c"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib, mc8comp

t = mc1lib.read_src(sys.argv[1])
todo = [(n, mc8comp.remove(t, n)) for n in mc8comp.REMOVALS if n != 'none']
todo = [x for x in todo if x[1]]
with ThreadPoolExecutor(4) as ex:
    for n, s in ex.map(lambda it: (it[0], mc1lib.score_text(it[1], [])), todo):
        print(n, mc1lib.fmt(s)[:70], flush=True)
