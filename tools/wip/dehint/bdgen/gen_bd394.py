"""Attempt 28: attempt 21's gen_bd323 (the could-not-read log inside loadBl after the switch) rerun on the exp_t10 near
miss (gen_bd390's PRE).  With the log test after the switch, no break in loadBl reaches a bare return block, so none of
loadBl's tests gets PRED_TREE_EARLY_RETURN; for CG that is P(type == 10) 13.7% and CG success 50%, i.e. CGok about 15
where block 116 needs under about 16.  Everything else in loadBl moves too.  Runs on src as of f2823155."""
import itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_bd323 as g
from gen_bd390 import PRE

CASES = g.CASES
FOCUS = ['_loadBlFiles']
