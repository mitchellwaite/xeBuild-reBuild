# tw.sh SLOT KEY=VAL...  : tweak s10 best.json, run, show fncmp/inv and round-2 pops
S=$1; shift
python - "$@" > build/s12/$S.json <<'P'
import json,sys;d=json.load(open('tools/wip/mc/s10/best.json'))
for a in sys.argv[1:]:
    k,v=a.split('=');d[k]=float(v)
print(json.dumps(d))
P
python tools/wip/mc/s10/run.py $S build/s12/$S.json | grep -v overr
awk '/^;; Function mode_client/,/^;; Function [^m]/' build/${MCD:-mcsp}/slot$S/m.c.274r.bbro | grep "STC\|Getting" | head -${N:-30} | tr '\n' ' '; echo
