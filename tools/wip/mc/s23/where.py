"""where.py INJ-JSON TAG: compile, then list the sequence of distinctive log strings in mode_client's .s
(final layout), to see where a block analyze.py calls 'missing' actually lands."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ext, table
inj = [tuple(x) for x in json.loads(sys.argv[1])]; tag = sys.argv[2]
r = table.meas(inj, tag)
s = open(os.path.join(table.D, 'slot_' + tag, 'fdo.s')).read()
strs = dict(re.findall(r'^(LC\d+):\n\s*\.ascii "(.{0,30})', s, re.M))
body = s[s.index('_mode_client:'):]; body = body[:body.index('.def', 10) if '.def' in body[10:] else len(body)]
seq = []
for l in body.split('\n'):
    m = re.search(r'OFFSET FLAT:(LC\d+)', l)
    if m: seq.append(strs.get(m.group(1), m.group(1))[:24])
    m = re.search(r'call\s+_(\w+)', l)
    if m and m.group(1) not in ('log_printf', 'strnicmp'): seq.append('>' + m.group(1))
print(r['inv'], r['needmiss']); print('\n'.join(seq))
