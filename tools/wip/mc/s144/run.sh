# run.sh DIR : climb singles, pairs(top 100), 2 SA chains on DIR/base.c
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s144/$1; export GBASE=base.c NJ=${NJ:-4}
python climb.py singles > singles.out 2>&1
python - <<'P'
import json, gen; b=list(gen.evaluate([])); S=json.load(open('singles.json'))
json.dump([[r,e] for r,e in S if r[0]<9999 and r!=b], open('nonin.json','w'))
P
SJ=nonin.json python climb.py pairs 100 > pairs.out 2>&1
SJ=nonin.json python climb.py sa 1 600 1500 > sa1.out 2>&1
SJ=nonin.json python climb.py sa 2 600 1500 > sa2.out 2>&1
echo done > done.txt
