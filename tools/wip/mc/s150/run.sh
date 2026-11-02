# run.sh : climb singles on build/v/mc150/cm/base.c (s146/e gen+climb, f2.sh path absolute)
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/build/v/mc150/cm; export GBASE=base.c NJ=${NJ:-4}
python climb.py singles > singles.out 2>&1
python - <<'P'
import json, gen; b=list(gen.evaluate([])); S=json.load(open('singles.json'))
json.dump([[r,e] for r,e in S if r[0]<9999 and r!=b], open('nonin.json','w'))
print(b)
P
echo done > done.txt
