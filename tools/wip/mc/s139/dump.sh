# dump.sh NAME : profile_estimate + bbro dumps of v/NAME.c into dd/NAME/
cd /c/Users/Win11VM/Documents/GitHub/xebuildBugFix/tools/wip/mc/s139; R=/c/Users/Win11VM/Documents/GitHub/xebuildBugFix; export PATH=$R/tools/toolchain-4745/mingw32/bin:$PATH
mkdir -p dd/$1; cp v/$1.c dd/$1/pm.c; cd dd/$1
gcc -S -masm=intel -I$R/src -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50 -fno-asynchronous-unwind-tables -fdump-tree-profile_estimate-blocks-details -fdump-rtl-bbro-details -fdump-tree-optimized pm.c -o x.s
awk '/^;; Function mode_client/{f=1;next} f&&/^;; Function /{f=0} f' pm.c.274r.bbro > mc.bbro
awk '/^;; Function mode_client/{f=1;next} f&&/^;; Function /{f=0} f' pm.c.042t.profile_estimate > mc.pe
