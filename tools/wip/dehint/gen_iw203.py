# attempt 13: rerun any older generator on a new base, plain -O3, sorted by total lines (no FOCUS, no probe flag).
# IWG=tools/wip/dehint/gen_iwN.py IWB=<base.c> python tools/wip/dehint/iwsweep.py tools/wip/dehint/gen_iw203.py -n 8
import importlib.util, os
_s = importlib.util.spec_from_file_location('inner', os.environ['IWG'])
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
AXES = _m.AXES
BASE = os.environ['IWB']
FLAGS = []
