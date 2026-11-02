# t.sh FILE.c : f2 + r4 tail; run from a dir under build/v/mc150 (per-name subdir)
R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; n=$(basename $1 .c); d=$(dirname $1); cd $d
f=$(sh $R/tools/wip/mc/s101/f2.sh $n.c)
export PATH=$R/tools/toolchain-4745/mingw32/bin:$R/tools/toolchain-4745/bin:$PATH; mkdir -p dd_$n; cp $n.c dd_$n/pm.c; cd dd_$n
gcc -S -masm=intel -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -fno-asynchronous-unwind-tables -fdump-rtl-bbro-details pm.c -o x.s 2>/dev/null
awk '/^;; Function mode_client/{f=1;next} f&&/^;; Function /{f=0} f' pm.c.*r.bbro > mc.bbro; rm -f pm.c.*r.bbro
echo "$n f2=$f r4: $(python $R/tools/wip/mc/s86/r4sim.py mc.bbro | tail -1 | cut -d' ' -f14-44)"
