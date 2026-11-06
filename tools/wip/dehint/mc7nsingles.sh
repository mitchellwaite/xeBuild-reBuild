#!/bin/sh
# mode_client attempt 7: mc1 singles on a near-miss base (= pairs of that near miss with
# every mc1 edit).  sh tools/wip/dehint/mc7nsingles.sh build/mc/w7/n14.c TAG
# -> build/mc/w7_ns_TAG.json, nearest 25 printed.
cd "$(dirname "$0")/../../.."
MC2SINGLES=w7_ns_$2.json MCBASE=$1 python tools/wip/dehint/mc2.py singles -j 4 > build/mc/w7/ns_$2.log 2>&1
python - "$2" <<'EOF'
import json, re, sys
d = json.load(open('build/mc/w7_ns_%s.json' % sys.argv[1]))
def tot(v):
    if v['ok']:
        return 0
    m = re.match(r'(\d+)', v['r'])
    return int(m.group(1)) if m else 99999
for t, c, k in sorted((tot(v), v['count'], k) for k, v in d.items())[:25]:
    print(t, c, k)
EOF
