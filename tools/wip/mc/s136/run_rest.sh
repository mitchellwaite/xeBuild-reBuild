# run after main singles: pairs+SA on main, then singles/pairs/SA on nma_2 and rb_ifelse
set -x
for d in . nma_2 rb_ifelse; do
  cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s136/$d
  [ -f singles.json ] || python climb.py singles > singles.out 2>&1
  python nonin.py 100 > nonin.out 2>&1
  SJ=nonin.json python climb.py pairs 100 > pairs.out 2>&1
  for s in 1 2 3 4; do SJ=singles.json python climb.py sa $s 450 4000 > sa$s.out 2>&1; done
done
