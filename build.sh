#!/bin/sh
# Build every object in src/objects.txt (src/<obj>.c with gcc if it exists,
# else src/<obj>.s with as), link them with ld's default script into build/xeBuild.exe
# and check it against the reference.  Run from the repo root in Git Bash after
# tools/fetch_toolchain.sh.
set -e
TC=tools/toolchain-4745/mingw32/bin
OBJ=build/obj
ROOT=$PWD
# gcc finds cc1/as and their DLLs through PATH
PATH="$PWD/$TC:$PATH"
# ccp <gcc flags>: compile src/$f.c (as $orig) in $p, assembly to stdout
ccp() {
  (cd "$p" && { printf '#line 1 "%s"\n' "$orig"; cat "$ROOT/src/$f.c"; } |
    "$ROOT/$TC/gcc.exe" -S "$@" -I"$ROOT/src/$(dirname "$f")" -x c - -o -)
}
# fdo <gcda.py args> <gcc flags>: profile build of src/$f.c, assembly to stdout.
# An instrumented compile gives the .gcno and the guessed profile, re/gcda.py
# the .gcda. All compiles run in $p with `-o -`: the .gcda name and static
# functions' profile ids come from the aux name
fdo() {
  p="$OBJ/$f.fdo"
  mkdir -p "$p"
  pw=$(cd "$p" && { pwd -W 2>/dev/null || pwd; })
  pa=$1; shift
  ccp $cflags $uw "$@" -fprofile-arcs -ftest-coverage \
    -fdump-tree-profile_estimate-blocks-details >/dev/null
  python re/gcda.py "$p/-.gcno" "$p/-.042t.profile_estimate" "$p/-.gcda" \
    $pa --src="src/$f.c" >/dev/null
  ccp $cflags $uw "$@" -fbranch-probabilities -fprofile-dir="$pw"
}
objs=
for f in $(grep -v '^#' src/objects.txt | tr -d '\r'); do
  mkdir -p "$OBJ/$(dirname "$f")"
  if [ -f "src/$f.c" ]; then
    prof= fprof= ffns=
    fflags="-DBUILD_FDO -fno-ipa-profile -fno-reorder-functions -ftoplevel-reorder -Wno-aggressive-loop-optimizations"
    case "$f" in
      # original build path, for __FILE__ in assert(); fed through stdin so
      # the #line can name it (gcc 6 has no -ffile-prefix-map)
      # src/crypto is XeCrypt's tree (headers include "bign/bigdigits.h" etc.)
      crypto/*) orig="H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/${f#crypto/}.c"
                cflags="-O3 -Isrc/crypto" ;;
      # readFileIn's __builtin_expect hints are tuned to this probability
      app/fileutil) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=65" ;;
      # kvCheckHash's __builtin_expect needs a weak hint (51-60 match)
      app/keyvault) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=55" ;;
      # showInfoKeys aligns a block at frequency 61 of 9412 (default 100
      # would need 95); 155 and up match
      app/consoleinfo) orig="$f.c"
             cflags="-O3 --param align-threshold=200" ;;
      # getConsoleFiles' netMount hint needs 68 (66-70 in other forms).
      # mode_update's cold blocks are laid out by frequency ties that no
      # guessed profile we found gives (wip/README.md), so it and the static
      # updateNand it inlines are built with a crafted profile: gcc's guessed
      # one with these edges changed (profile_estimate bb numbers; re/gcda.py).
      # The other functions are optimize("no-branch-probabilities") and keep
      # the guessed profile; -fno-ipa-profile keeps their hot test, and
      # -fno-reorder-functions keeps mode_update out of .text.hot.
      app/mode_update) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder --param builtin-expect-probability=68 -fno-ipa-profile -fno-reorder-functions"
             prof="mode_update:59>3=97.9 mode_update:65>66=16 mode_update:67>68=16
                   mode_update:69>70=30 mode_update:75>76=21 mode_update:79>80=80.5
                   mode_update:80>82=17 updateNand:2>3=49.5 updateNand:13>18=27
                   updateNand:19>20=60 updateNand:24>25=14.5 --only=mode_update,updateNand" ;;
      # fcrtEncrypt's offset hint needs 60 (and setFuseCpuKey's NULL hint
      # then aligns that block; align-threshold=200 would also align
      # smcChecksum's count == 0 block, which the original doesn't);
      # -fno-toplevel-reorder emits the key buffers and string arrays in
      # definition order
      app/keys) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder --param builtin-expect-probability=60" ;;
      # console_hdd's __builtin_expect hints are tuned to this probability;
      # sendAvatarData's loop is aligned (1 and 2 align other loops too)
      app/console_hdd) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=80 --param align-loop-iterations=3" ;;
      # parseOption's setBoolOption and vlen hints (82 and 84 lay out the
      # done/incomplete blocks differently). applyIniOptions has a crafted
      # profile like mode_update (src/app/options.prof, from
      # wip/aiodesign.py); the rest keep the guessed one
      app/options) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=83 -fno-ipa-profile -fno-reorder-functions"
             prof="@src/app/options.prof --only=applyIniOptions" ;;
      # iniPreParse: vectorization makes PRE drop a PHI; its ';' hint (65-66)
      # makes its memcpy block hot enough to be aligned; parseIni needs
      # LRA's EBBs to stop at a 50% fallthrough (51-70 work);
      # -fno-toplevel-reorder emits parseIni's string arrays and the tables
      # in definition order
      app/filelist_ini) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder -fno-tree-loop-vectorize --param builtin-expect-probability=65
                     --param lra-inheritance-ebb-probability-cutoff=60" ;;
      # imgAddMobile's 50/50 imgFits hint
      app/image_write) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=50" ;;
      # its string arrays are defined in the original's .rdata order, which
      # -fno-toplevel-reorder keeps
      app/bootloaders) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder" ;;
      # same for its string arrays (made by wip/irwhole.py) and data
      app/image_read) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder" ;;
      # netSendFile's !name hint (55-65), netRecvVerbose's verbose hint (65).
      # No -fno-toplevel-reorder: netRecv is netRecvVerbose's IPA-CP clone,
      # which only the default order emits first (as the original)
      app/net) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=65" ;;
      # loadFileCrc's verbose hint (92-99); 98 for wip/'s checkBl draft.
      # loadBlFiles' type-11 block is laid out by frequencies no guessed
      # profile gives (dom2's FSM threader zeroes it; wip/README.md): it comes
      # from a second compile (fprof) with -DBUILD_FDO and a crafted profile
      # for it and the static loadBl it inlines (and loadBl60); NOPROF keeps
      # the guessed one for the rest. -DBUILD_FDO also shrinks xb.files' bound
      # (the loop's iteration estimate decides an ivopts tie), hence the
      # warning flag. --consistent: exact zero counts. --runs=0: no block is
      # never executed, so the no-key log (hot for its alignment, through
      # dead edges) keys 0 in bb-reorder like the zero-count chains it follows.
      # -fno-toplevel-reorder emits the functions, strings and .data in
      # definition order
      app/build) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder --param builtin-expect-probability=98"
             fprof="@src/app/build.prof --only=loadBlFiles,loadBl,loadBl60 --consistent --runs=0"
             ffns=_loadBlFiles ;;
      # mode_client's layout comes from a second compile (fprof) with
      # -DBUILD_FDO: empty asm-goto edges and a crafted profile for it and
      # the clientEraseBlock it inlines (src/app/mode_client.c's head
      # comment; wip/mc/s18/NOTES.md); align-loop-iterations=100 aligns its
      # loop like the original. -fno-toplevel-reorder emits the string
      # arrays and data in definition order
      app/mode_client) orig="$f.c"
             cflags="-O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions --param builtin-expect-probability=50"
             fprof="@src/app/mode_client.prof --only=mode_client,clientEraseBlock --threshold=64"
             fflags="-DBUILD_FDO --param align-loop-iterations=100"
             ffns=_mode_client ;;
      # original path unknown (no assert in the app); timeutil needs -O3
      app/*) orig="$f.c"
             cflags="-O3" ;;
      # the COMMON block in address order (src/globals.c's head comment)
      globals) orig="$f.c"
             cflags="-O3 -fno-common -fno-toplevel-reorder -fno-ident" ;;
      *) echo "build.sh: no flags for $f" >&2; exit 1 ;;
    esac
    uw=
    [ -f "src/$f.s" ] && uw=-fno-asynchronous-unwind-tables
    if [ -n "$prof" ]; then
      fdo "$prof" > "$OBJ/$f.c.s"
    elif [ -n "$uw$fprof" ]; then
      { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
        "$TC/gcc.exe" -S $cflags $uw -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.c.s"
    fi
    # a second compile with -DBUILD_FDO and a profile for the functions in $ffns
    # (-ftoplevel-reorder: with -fno-toplevel-reorder ipa-reference doesn't
    # see the never-set statics as read-only, so ccp2 keeps their tests);
    # these are app/build's flags, a case may set its own $fflags
    fs=
    if [ -n "$fprof" ]; then
      fdo "$fprof" $fflags > "$OBJ/$f.fdo.s"
      for n in $ffns; do fs="$fs $n=$OBJ/$f.fdo.s"; done
    fi
    if [ -n "$uw" ]; then
      # mixed object: splice the C functions into the .s (re/splice.py)
      python re/splice.py "src/$f.s" "$OBJ/$f.c.s" "$OBJ/$f.s" $fs
      "$TC/as.exe" --32 "$OBJ/$f.s" -o "$OBJ/$f.o"
    elif [ -n "$fprof" ]; then
      # whole object: the $ffns functions from the second compile
      python re/splice.py --whole "$OBJ/$f.c.s" "$OBJ/$f.s" $fs
      "$TC/as.exe" --32 "$OBJ/$f.s" -o "$OBJ/$f.o"
    elif [ -n "$prof" ]; then
      "$TC/as.exe" --32 "$OBJ/$f.c.s" -o "$OBJ/$f.o"
    else
      { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
        "$TC/gcc.exe" -c $cflags -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.o"
    fi
  else
    "$TC/as.exe" --32 "src/$f.s" -o "$OBJ/$f.o"
  fi
  objs="$objs $OBJ/$f.o"
done
# ld's default i386pe link script, image base, entry point and subsystem
"$TC/ld.exe" -m i386pe -s --no-insert-timestamp -Map build/xeBuild.map \
  -o build/xeBuild.exe $objs
# original link time; ld 2.27 can't take a fixed timestamp itself
python re/stamp.py build/xeBuild.exe 0x5DCAB029
python re/execmp.py xeBuild.exe build/xeBuild.exe
sha256sum build/xeBuild.exe
