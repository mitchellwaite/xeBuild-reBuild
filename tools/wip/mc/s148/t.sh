# t.sh NAME : f2 + r4 tail after 143
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s148; R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix
cp c0.ref $1.ref; f=$(sh ../s101/f2.sh $1.c)
export PATH=$R/tools/toolchain-4745/mingw32/bin:$PATH; mkdir -p dd/$1; cp $1.c dd/$1/pm.c; cd dd/$1
gcc -S -masm=intel -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -fno-asynchronous-unwind-tables -fdump-rtl-bbro-details pm.c -o x.s 2>/dev/null
awk '/^;; Function mode_client/{f=1;next} f&&/^;; Function /{f=0} f' pm.c.*r.bbro > mc.bbro; rm -f pm.c.*r.bbro
echo "$1 f2=$f r4: $(python ../../../s86/r4sim.py mc.bbro | tail -1 | cut -d' ' -f14-34)"
