"""where.py file.c sig...: for each signature, the bbro trace (round, members) it sits in"""
import os, re, sys
sys.path.insert(0, r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix\wip\mc')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mcvar, search as S
res, err = mcvar.run(sys.argv[1], S.FLAGS)
d = res['dir']
bbro = mcvar.section(open(os.path.join(d, 'v.c.274r.bbro')).read(), 'mode_client')
cg = mcvar.section(open(os.path.join(d, 'v.c.267r.compgotos')).read(), 'mode_client')
sg = mcvar.sigs(cg, open(os.path.join(d, 'v.s')).read())
for m in re.finditer(r'^Trace (\d+) \(round (\d+)\):(.*)$', bbro, re.M):
    bs = [(int(b), int(f)) for b, f in re.findall(r'(\d+) \[(\d+)\]', m.group(3))]
    hits = [sg.get(b) for b, f in bs if sg.get(b) and any(x in sg.get(b) for x in sys.argv[2:])]
    if hits:
        print('trace', m.group(1), 'round', m.group(2), [(b, f, sg.get(b)) for b, f in bs])
