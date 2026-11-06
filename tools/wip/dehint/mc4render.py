"""mode_client attempt 4: render a hit from build/mc/m2_hits.json on MCBASE to a file.

python tools/wip/dehint/mc4render.py 'HIT KEY' OUT.c"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1, mc1lib

key, out = sys.argv[1], sys.argv[2]
h = json.load(open(os.path.join(mc1lib.BUILD, 'm2_hits.json')))[key]
t = mc1.build_template(mc1lib.read_src(mc1.BASE))
text = mc1.render(t, h['state'], h['drops'], h.get('post', []))
open(out, 'w', newline='\n').write(text)
print(mc1lib.fmt(mc1lib.score_text(text)), mc1.count(text)['total'])
