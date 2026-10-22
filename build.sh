#!/bin/sh
# Build every object in src/objects.txt (src/<obj>.c with gcc if it exists,
# else src/<obj>.s with as), link them with src/link.ld into build/xeBuild.exe
# and check it against the reference.  Run from the repo root in Git Bash after
# tools/fetch_toolchain.sh.
set -e
TC=tools/toolchain-4745/mingw32/bin
OBJ=build/obj
ROOT=$PWD
# gcc finds cc1/as and their DLLs through PATH
PATH="$PWD/$TC:$PATH"
objs=
for f in $(grep -v '^#' src/objects.txt | tr -d '\r'); do
  mkdir -p "$OBJ/$(dirname "$f")"
  if [ -f "src/$f.c" ]; then
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
      # getBadBlocks aligns its error block, which the default (100) doesn't;
      # getConsoleFiles' netMount hint needs 68 (66-70 in other forms)
      app/mode_update) orig="$f.c"
             cflags="-O3 --param align-threshold=200 --param builtin-expect-probability=68" ;;
      # fcrtEncrypt's offset hint needs 60 (and setFuseCpuKey's NULL hint
      # then aligns that block; align-threshold=200 would also align
      # smcChecksum's count == 0 block, which the original doesn't)
      app/keys) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=60" ;;
      # console_hdd's __builtin_expect hints are tuned to this probability;
      # sendAvatarData's loop is aligned (1 and 2 align other loops too)
      app/console_hdd) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=80 --param align-loop-iterations=3" ;;
      # parseOption's setBoolOption and vlen hints (82 and 84 lay out the
      # done/incomplete blocks differently)
      app/options) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=83" ;;
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
      # netSendFile's !name hint (55-65), netRecvVerbose's verbose hint (65)
      app/net) orig="$f.c"
             cflags="-O3 --param builtin-expect-probability=65" ;;
      # original path unknown (no assert in the app); timeutil needs -O3
      app/*) orig="$f.c"
             cflags="-O3" ;;
      *) echo "build.sh: no flags for $f" >&2; exit 1 ;;
    esac
    if [ -f "src/$f.s" ]; then
      # mixed object: splice the C functions into the .s (re/splice.py)
      { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
        "$TC/gcc.exe" -S $cflags -fno-asynchronous-unwind-tables \
          -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.c.s"
      fdo=
      if [ "$f" = app/mode_update ]; then
        # mode_update's cold blocks are laid out by frequency ties that no
        # guessed profile we found gives (wip/README.md): re/gcda.py writes the
        # guessed profile with these edges changed (profile_estimate bb
        # numbers), and only mode_update is taken from the profile build.
        # Both compiles use `-o -`: the .gcda name and static functions'
        # profile ids come from the aux name. pf keeps the profile from
        # changing inlining and placement (wip/README.md); at the object's
        # align-threshold=200 the profile build aligns two more labels.
        p="$OBJ/$f.fdo"
        mkdir -p "$p"
        pw=$(cd "$p" && { pwd -W 2>/dev/null || pwd; })
        pf="-fno-inline-small-functions -fno-partial-inlining -fno-ipa-profile -fno-reorder-functions --param align-threshold=100"
        (cd "$p" && { printf '#line 1 "%s"\n' "$orig"; cat "$ROOT/src/$f.c"; } |
          "$ROOT/$TC/gcc.exe" -S $cflags $pf -fno-asynchronous-unwind-tables -I"$ROOT/src/app" \
            -fprofile-arcs -ftest-coverage -fdump-tree-profile_estimate-blocks-details \
            -x c - -o - >/dev/null)
        python re/gcda.py "$p/-.gcno" "$p/-.042t.profile_estimate" "$p/-.gcda" \
          mode_update:59\>3=97.9 mode_update:65\>66=16 mode_update:67\>68=16 \
          mode_update:69\>70=30 mode_update:75\>76=21 mode_update:79\>80=80.5 \
          mode_update:80\>82=17 updateNand:2\>3=49.5 updateNand:13\>18=27 \
          updateNand:19\>20=60 updateNand:24\>25=14.5 \
          --only=mode_update,updateNand --src="src/$f.c" >/dev/null
        (cd "$p" && { printf '#line 1 "%s"\n' "$orig"; cat "$ROOT/src/$f.c"; } |
          "$ROOT/$TC/gcc.exe" -S $cflags $pf -fno-asynchronous-unwind-tables -I"$ROOT/src/app" \
            -fbranch-probabilities -fprofile-dir="$pw" -x c - -o -) > "$OBJ/$f.fdo.s"
        fdo="_mode_update=$OBJ/$f.fdo.s"
      fi
      python re/splice.py "src/$f.s" "$OBJ/$f.c.s" "$OBJ/$f.s" $fdo
      "$TC/as.exe" --32 "$OBJ/$f.s" -o "$OBJ/$f.o"
    else
      { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
        "$TC/gcc.exe" -c $cflags -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.o"
    fi
  else
    "$TC/as.exe" --32 "src/$f.s" -o "$OBJ/$f.o"
  fi
  objs="$objs $OBJ/$f.o"
done
"$TC/ld.exe" -m i386pe -T src/link.ld --image-base 0x400000 -e __EntryPoint \
  --subsystem console -s --no-insert-timestamp -Map build/xeBuild.map \
  -o build/xeBuild.exe $objs
# original link time; ld 2.27 can't take a fixed timestamp itself
python re/stamp.py build/xeBuild.exe 0x5DCAB029
python re/execmp.py xeBuild.exe build/xeBuild.exe
sha256sum build/xeBuild.exe
