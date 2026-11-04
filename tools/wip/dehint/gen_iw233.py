# attempt 16: gen_iw207's blk positions crossed with gen_iw231's left forms and the low-line pages spellings on a15_dead: c4 + `blk` inside the page loop has writeFsTable clean, imgAdd 2.
import os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
def L(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(here, n + '.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g); return g
g7, g1, g8 = L('gen_iw207'), L('gen_iw231'), L('gen_iw228')
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15_dead.c')
CA = [c for c in g1.CA if c[0] in ('c3', 'c4', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14', 'c0')]
AB = [a for a in g8.AB if a[0] in ('ba', 'bm')]
AS = [a for a in g8.AS if a[0] in ('st', 'si')]
AXES = [CA, AB, AS] + g7.AXES[:3] + [g7.AXES[4]]
FLAGS = []
