"""Grid search over last-round frequency designs for mode_client, scored with mcsim2's replay.
python wip/mc/mcgrid.py <mode_client-only bbro dump> [top N]
Prints the best designs (pre = matching prefix of mcsim2.WANT, inv = inversions) and the order."""
import itertools, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'wip'))
sys.path.insert(0, os.path.join(ROOT, 'wip', 'mc'))
import fibsim, fibwhatif, mcsim2

ev = fibsim.parse(sys.argv[1])
R = fibwhatif.groups(ev)
npre = sum(len(r['order']) for r in R[:3])
top = int(sys.argv[2]) if len(sys.argv) > 2 else 15

# block: candidate frequencies (draft's values: 103=4 112/115=2 55=2 126/127/125/117/130=1 61=1 33/29=1 53/42/35=0 67/77/79/73=0)
GRID = {
    103: (3, 4),          # usage(2)
    'hdd': (3, 4),        # 112 and 115 together
    55: (2, 3, 4),        # -r
    126: (1, 2, 3),       # Block outside
    125: (1, 2, 3),       # Failed to erase
    61: (1, 2),           # -w
    'u43': (0, 1, 2),     # 33 and 29 together (usage 4/3 cx)
    67: (0, 1),           # -e
    127: (0, 1),          # Invalid
    'pi': (0, 1),         # 117 and 130 together (patches/info NULL)
    'u5': (0, 1),         # 35 42 53 together
}
keys = list(GRID)
best = []
n = 0
for vals in itertools.product(*(GRID[k] for k in keys)):
    d = dict(zip(keys, vals))
    if d['hdd'] < d[103]:
        continue
    f = {103: d[103], 112: d['hdd'], 115: d['hdd'], 55: d[55], 126: d[126], 125: d[125], 61: d[61],
         33: d['u43'], 29: d['u43'], 67: d[67], 127: d[127], 117: d['pi'], 130: d['pi'], 35: d['u5'], 42: d['u5'], 53: d['u5']}
    try:
        o = mcsim2.sim(R, f)
    except Exception as e:
        continue
    pre, inv, oo = mcsim2.score(o, npre)
    n += 1
    best.append((inv, -pre, tuple(vals), oo))
    if inv == 0:
        print('PERFECT', dict(zip(keys, vals)), flush=True)
best.sort()
print('designs tried', n)
for inv, mpre, vals, oo in best[:top]:
    print('inv=%2d pre=%2d %s' % (inv, -mpre, dict(zip(keys, vals))))
    print('   ', ' '.join(map(str, oo)))
