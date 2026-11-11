# Compile every object in OBJECTS (src/<obj>.c with gcc), link them with the
# toolchain's runtime into build/xeBuild.exe and check it against the
# reference.  GNU make; on Windows run it from the repo root in Git Bash after
# tools/fetch_toolchain.sh (build.sh runs `make check`).
#
#   make            build build/xeBuild.exe
#   make check      build, compare with xeBuild.exe and check the SHA256
#   make clean      remove build/obj and the linked exe
#
# Only the pinned toolchain on Windows reproduces the reference bytes.  Other
# hosts can override CC, CFLAGS, LDFLAGS, PYTHON and SHA256SUM (on the command
# line or in an untracked config.mk) and set TC_BIN empty when CC is already
# on PATH; their build won't match.

-include config.mk

# The pinned toolchain (CLAUDE.md).  gcc finds cc1/as and their DLLs through
# PATH, so recipes that run it put TC_BIN first.
TC_BIN    ?= tools/toolchain-4745/mingw32/bin
CC        ?= $(TC_BIN)/gcc.exe
PYTHON    ?= python
SHA256SUM ?= sha256sum
# extra flags after each object's own (empty for the matching build)
CFLAGS    ?=
LDFLAGS   ?=

# (pwd -P: a native Windows make hands sh a C:/ style $PWD, whose colon
# would split the PATH entry)
ifneq ($(strip $(TC_BIN)),)
TC_ENV = PATH="$$(pwd -P)/$(TC_BIN):$$PATH"
endif

# make's built-in CC default is `cc`: treat it as unset
ifeq ($(origin CC),default)
CC = $(TC_BIN)/gcc.exe
endif

OBJ := build/obj
EXE := build/xeBuild.exe
REF := xeBuild.exe
REF_SHA256 := 10dac648197fa5cdbb82d975ab9ff11f64075c9686908dfd9a33edc533f1971c
# original link time; ld 2.27 can't take a fixed timestamp itself
LINK_TIME := 0x5DCAB029

# The program's objects in the original's link order (its .eh_frame CIE
# order; tools/re/split.py's NAMES has the evidence for each).  ld lays out
# .text/.rdata/.data in this order.
OBJECTS := \
	bootloaders mode_update stfs mode_client filelist_ini \
	timeutil smc sysupdate main mode_extract xboxrom \
	image_write keyvault image_read mode_ini mode_build \
	keys net fileutil options build consoleinfo \
	console_hdd log crc32 \
	globals crypto/xecrypt crypto/xecryptBn \
	crypto/aes/aes_modes crypto/aes/aestab crypto/aes/aescrypt crypto/aes/aeskey \
	crypto/bign/mpSubtract crypto/bign/pkcs1-rsa crypto/bign/mpMultiply \
	crypto/bign/mpShortMod crypto/bign/mpModExp crypto/bign/mpSetZero \
	crypto/bign/mpShortDiv crypto/bign/base64 crypto/bign/hash \
	crypto/bign/mpModInv crypto/bign/mpModulo crypto/bign/mpShortSub \
	crypto/bign/mpSizeof crypto/bign/mpCompare crypto/bign/common \
	crypto/bign/mpSetDigit crypto/bign/mpIsPrime crypto/bign/mpIsZero \
	crypto/bign/mpShiftLeft crypto/bign/spMultiply crypto/bign/mpAdd \
	crypto/bign/mpModMult crypto/bign/bigdUtils crypto/bign/mpShortAdd \
	crypto/rc4/rc4_enc crypto/rc4/rc4_skey crypto/sha/sha1dgst crypto/md5/md5 \
	crypto/des/des \
	crypto/bign/mpSetEqual crypto/bign/mpShiftRight crypto/bign/mpDivide \
	crypto/bign/spDivide crypto/bign/mpShortCmp crypto/bign/spPseudoRand
OBJS := $(OBJECTS:%=$(OBJ)/%.o)

# gcc's default libraries, as the gcc driver passes them
LIBS := -lmingw32 -lgcc -lgcc_eh -lmoldname -lmingwex -lmsvcrt -lpthread \
	-ladvapi32 -lshell32 -luser32 -lkernel32

.PHONY: all check clean
.DELETE_ON_ERROR:

all: $(EXE)

# $(call compile,original path,flags): compile $< to $@.  The source goes
# through stdin so the #line can name the original build path, for __FILE__
# in assert() (gcc 6 has no -ffile-prefix-map).  -MMD records the headers.
define compile
	@mkdir -p $(@D)
	{ printf '#line 1 "%s"\n' '$(1)'; cat $<; } | \
	  $(TC_ENV) $(CC) -c $(2) $(CFLAGS) -I$(<D) \
	  -MMD -MP -MF $(@:.o=.d) -MT $@ -x c - -o $@
endef

# src/crypto is XeCrypt's tree (headers include "bign/bigdigits.h" etc.)
$(OBJ)/crypto/%.o: src/crypto/%.c $(MAKEFILE_LIST)
	$(call compile,H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/$*.c,-O3 -Isrc/crypto)

# the rest of the app: original path unknown (no assert in the app)
$(OBJ)/%.o: src/%.c $(MAKEFILE_LIST)
	$(call compile,$*.c,-O3)

# Link as gcc does: crt2.o and crtbegin.o, the program, the libraries (gcc's
# defaults, ws2_32), the default manifest and crtend.o, with ld's default
# script (tools/fetch_toolchain.sh rebuilds the kernel32 and msvcrt import
# libraries as the original had them).  globals.o goes after the libraries,
# so its .bss follows theirs like the original's COMMON block
# (src/globals.c).  The stamp is part of the link so an unstamped exe is
# never up to date.
$(EXE): $(OBJS)
	$(TC_ENV) $(CC) -s -o $@ $(OBJS) -lws2_32 $(LIBS) $(LDFLAGS) \
	  -Wl,--no-insert-timestamp,-Map,build/xeBuild.map
	$(PYTHON) tools/re/stamp.py $@ $(LINK_TIME)

check: $(EXE)
	$(PYTHON) tools/re/execmp.py $(REF) $(EXE)
	@$(SHA256SUM) $(EXE)
	@[ "$$($(SHA256SUM) $(EXE) | cut -d' ' -f1)" = $(REF_SHA256) ] || \
	  { echo "SHA256 differs from $(REF_SHA256)" >&2; exit 1; }

clean:
	rm -f $(OBJS) $(OBJS:.o=.d) $(EXE) build/xeBuild.map

-include $(OBJS:.o=.d)
