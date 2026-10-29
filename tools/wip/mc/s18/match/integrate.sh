# integrate.sh: whole-object mode_client from C (s13 route), mode_client from the FDO compile.
#  1. tools/wip/mcwhole.py: draft -> plain whole C, matching FDO source -> FDO whole C (mc_<addr> string arrays)
#  2. plain compile of the whole C (-O3 -fno-toplevel-reorder, param 50) -> plain.s
#  3. FDO compile of the FDO whole C (mcfdo flags, NOPROF on the other functions, gcda.py with
#     overrides.txt) -> fdo.s
#  4. tools/re/splice.py --whole plain.s out.s _mode_client=fdo.s ; as ; compare with build/obj/mode_client.o
set -e
cd "$(dirname "$0")/../../../../.."
ROOT=$(cygpath -w "$PWD")
TC=tools/toolchain-4745/mingw32/bin
export PATH="$PWD/$TC:$PATH"
O=build/mcint
mkdir -p $O
python tools/wip/mcwhole.py tools/wip/mode_client.c $O/plain_whole.c
python tools/wip/mcwhole.py tools/wip/mc/s18/match/mode_client_fdo.c $O/fdo_whole.c
# data padding of the original object: cinfo at a 32-aligned .bss slot of 32 bytes, 16 zero bytes after .rdata
python - <<'EOF'
p = 'build/mcint/plain_whole.c'
s = open(p).read()
a = 'static struct consoleinfo *cinfo;'
assert s.count(a) == 1
s = s.replace(a, 'static struct consoleinfo *cinfo __attribute__((aligned(32)));\nstatic char mc_bsspad[28] __attribute__((used));')
s += '\nstatic const char mc_rdpad[16] __attribute__((used)) = {0};\n'
open(p, 'w', newline='\n').write(s)
EOF
FL="-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50"
# 2. plain
{ printf '#line 1 "%s"\n' "mode_client.c"; cat $O/plain_whole.c; } |
  $TC/gcc.exe -S $FL -Isrc -Iwip -x c - -o $O/plain.s
# 3. FDO (same aux name/dir handling as tools/wip/mcfdo.py: compiles of m.c in its dir with -o -)
export EXTRA='--param builtin-expect-probability=50'
python -c "import sys;sys.path.insert(0,'tools/wip');import mcfdo;mcfdo.prep(r'$ROOT\\build\\mcint\\fdo','build/mcint/fdo_whole.c')"
python tools/re/gcda.py $O/fdo/-.gcno $O/fdo/m.c.042t.profile_estimate $O/fdo/-.gcda $(cat tools/wip/mc/s18/match/overrides.txt | tr -d '\r') \
  --only=mode_client,clientEraseBlock --threshold=64 >/dev/null
(cd $O/fdo && "$OLDPWD/$TC/gcc.exe" -S -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions \
   --param builtin-expect-probability=50 $FDOX -I"$OLDPWD/wip" \
   -fbranch-probabilities -fprofile-dir=. "$ROOT\\build\\mcint\\fdo\\m.c" -o - > ../fdo.s)
# 4. splice + assemble + compare
python tools/re/splice.py --whole $O/plain.s $O/out.s _mode_client=$O/fdo.s
$TC/as.exe --32 $O/out.s -o $O/mode_client.o
$TC/objdump.exe -d --no-show-raw-insn $O/mode_client.o | sed -n '/^Disassembly/,$p' | sed -E 's/^ *[0-9a-f]+:\t//' > $O/new.dis
$TC/objdump.exe -d --no-show-raw-insn build/obj/mode_client.o | sed -n '/^Disassembly/,$p' | sed -E 's/^ *[0-9a-f]+:\t//' > $O/ref.dis
echo "text diff lines: $(diff $O/ref.dis $O/new.dis | grep -c '^[<>]')"
for s in .text .rdata .data .bss; do
  a=$($TC/objdump.exe -h build/obj/mode_client.o | awk -v s=$s '$2==s{print $3}')
  b=$($TC/objdump.exe -h $O/mode_client.o | awk -v s=$s '$2==s{print $3}')
  echo "$s size ref=$a new=$b"
done
