import json, os, sys
os.environ['DUP']='1'; os.environ['LU']='1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gs, ev
for nm in sys.argv[1:]:
    st=json.load(open(nm)); tag=os.path.basename(nm)[:-5]
    r=ev.ev(gs.build(st), tag, True)
    print(nm, r['score'], r['fncmp'], ' '.join(map(str,r['o'][12:])))
