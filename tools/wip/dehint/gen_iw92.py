# attempt 6: gen_iw15's writeFsTable forms on r0 (IWB= other base)
import importlib.util, os
_s = importlib.util.spec_from_file_location('g15', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_iw15.py'))
_m = importlib.util.module_from_spec(_s)
_s.loader.exec_module(_m)
BASE = os.environ.get('IWB', 'build/iw/a6/r0.c')
AXES = [_m.AXES[0][:1]] + _m.AXES[1:]
FLAGS = []
