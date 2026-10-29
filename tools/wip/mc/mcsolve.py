"""tools/wip/fibsolve.py for mode_client: search the last STC round for keys that give the
original's round-4 trace order (tools/wip/mc/mcsim2.py's WANT, the draft's bb numbers).
python tools/wip/mc/mcsolve.py <mode_client-only bbro dump> [max K]   (env as fibsolve: FIBD FIBALL FIBFIX)
The dump must start at mode_client's 'Reordering with the STC algorithm.' (awk the function out
of v.c.274r.bbro first)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip', 'mc'))
import fibsolve, mcsim2

# the cases (priority keys) come first and are not symbols; every other round-4 start is constrained
fibsolve.WANT = list(mcsim2.WANT)
fibsolve.FLEX = set(int(b) for b in os.environ.get('FLEX', '').split(',') if b)

if __name__ == '__main__':
    fibsolve.main()
