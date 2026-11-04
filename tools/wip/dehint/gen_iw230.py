# attempt 16: bo in the big arm's live code (imgAdd clean, imgAddFile 4: one name short at ccp2) x both pages spellings x tail: look for a dead-arm spelling that gives imgAddFile its name back. Base: a15.
import os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
def L(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(here, n + '.py')); g = importlib.util.module_from_spec(sp); sp.loader.exec_module(g); return g
g8, g9 = L('gen_iw228'), L('gen_iw229')
BASE = os.environ.get('IWB', 'tools/wip/dehint/drafts/image_write_a15.c')
PL = [p for p in g9.PL if p[0] in ('big', 'bt')]
U0 = [g9.US[0]]
LF = [('', []),
      ('l1', [('						left = pages;\n						if (left & 3)\n							left = (left + 4) & ~3;\n', '						left = pages & 3 ? (pages + 4) & ~3 : pages;\n')]),
      ('l2', [('						left = pages;\n						if (left & 3)\n							left = (left + 4) & ~3;\n', '						if (pages & 3)\n							left = (pages + 4) & ~3;\n						else\n							left = pages;\n')])]
AXES = [PL, U0, g9.TL, g8.AB, g8.AS, LF]
FLAGS = []
