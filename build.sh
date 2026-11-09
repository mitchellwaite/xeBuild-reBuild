#!/bin/sh
# Compile every object in $objects and src/globals.c (src/<obj>.c with gcc),
# link them with the toolchain's runtime into build/xeBuild.exe and check it
# against the reference.  Run from the repo root in Git Bash after
# tools/fetch_toolchain.sh.
set -e
TC=tools/toolchain-4745/mingw32/bin
OBJ=build/obj
# gcc finds cc1/as and their DLLs through PATH
PATH="$PWD/$TC:$PATH"
# The program's objects in the original's link order (its .eh_frame CIE
# order; tools/re/split.py's NAMES has the evidence for each).  ld lays out
# .text/.rdata/.data in this order.
objects="
  bootloaders mode_update stfs mode_client filelist_ini
  timeutil smc sysupdate main mode_extract xboxrom
  image_write keyvault image_read mode_ini mode_build
  keys net fileutil options build consoleinfo
  console_hdd log crc32
  crypto/xecrypt crypto/xecryptBn
  crypto/aes/aes_modes crypto/aes/aestab crypto/aes/aescrypt crypto/aes/aeskey
  crypto/bign/mpSubtract crypto/bign/pkcs1-rsa crypto/bign/mpMultiply
  crypto/bign/mpShortMod crypto/bign/mpModExp crypto/bign/mpSetZero
  crypto/bign/mpShortDiv crypto/bign/base64 crypto/bign/hash
  crypto/bign/mpModInv crypto/bign/mpModulo crypto/bign/mpShortSub
  crypto/bign/mpSizeof crypto/bign/mpCompare crypto/bign/common
  crypto/bign/mpSetDigit crypto/bign/mpIsPrime crypto/bign/mpIsZero
  crypto/bign/mpShiftLeft crypto/bign/spMultiply crypto/bign/mpAdd
  crypto/bign/mpModMult crypto/bign/bigdUtils crypto/bign/mpShortAdd
  crypto/rc4/rc4_enc crypto/rc4/rc4_skey crypto/sha/sha1dgst crypto/md5/md5
  crypto/des/des
  crypto/bign/mpSetEqual crypto/bign/mpShiftRight crypto/bign/mpDivide
  crypto/bign/spDivide crypto/bign/mpShortCmp crypto/bign/spPseudoRand"
objs=
for f in $objects globals; do
  mkdir -p "$OBJ/$(dirname "$f")"
  [ -f "src/$f.c" ] || { echo "build.sh: no src/$f.c" >&2; exit 1; }
  case "$f" in
    # original build path, for __FILE__ in assert(); fed through stdin so
    # the #line can name it (gcc 6 has no -ffile-prefix-map)
    # src/crypto is XeCrypt's tree (headers include "bign/bigdigits.h" etc.)
    crypto/*) orig="H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/${f#crypto/}.c"
              cflags="-O3 -Isrc/crypto" ;;
    # for the remaining expects (parseButtonX's power test needs 82.1-83.1%,
    # and the rev feeds); applyIniOptions' layout comes
    # from dead hints in the source (tools/wip/aio/p1/NOTES.md)
    options) orig="$f.c"
           cflags="-O3 --param builtin-expect-probability=83" ;;
    image_write) orig="$f.c"
           cflags="-O3" ;;
    # its data is defined in the original's .data/.bss order, reversed
    image_read) orig="$f.c"
           cflags="-O3" ;;
    build) orig="$f.c"
           cflags="-O3" ;;
    # the COMMON block in address order (src/globals.c's head comment)
    globals) orig="$f.c"
           cflags="-O3" ;;
    # the rest of the app: original path unknown (no assert in the app);
    # timeutil needs -O3
    *) orig="$f.c"
       cflags="-O3" ;;
  esac
  { printf '#line 1 "%s"\n' "$orig"; cat "src/$f.c"; } |
    "$TC/gcc.exe" -c $cflags -I"src/$(dirname "$f")" -x c - -o "$OBJ/$f.o"
  [ "$f" = globals ] || objs="$objs $OBJ/$f.o"
done
# Link as gcc does: crt2.o and crtbegin.o, the program, the libraries (gcc's
# defaults, ws2_32), the default manifest and crtend.o, with ld's default
# script (tools/fetch_toolchain.sh rebuilds the kernel32 and msvcrt import
# libraries as the original had them).  globals.o goes after the libraries,
# so its .bss follows theirs like the original's COMMON block
# (src/globals.c).
libs="-lmingw32 -lgcc -lgcc_eh -lmoldname -lmingwex -lmsvcrt -lpthread
      -ladvapi32 -lshell32 -luser32 -lkernel32"
"$TC/gcc.exe" -s -o build/xeBuild.exe $objs -lws2_32 $libs $OBJ/globals.o \
  -Wl,--no-insert-timestamp,-Map,build/xeBuild.map
# original link time; ld 2.27 can't take a fixed timestamp itself
python tools/re/stamp.py build/xeBuild.exe 0x5DCAB029
python tools/re/execmp.py xeBuild.exe build/xeBuild.exe
sha256sum build/xeBuild.exe
