# Compile every object in OBJECTS (src/<obj>.c), link them into an
# executable and, for the reference platform, check it against xeBuild.exe.
# GNU make (gmake on BSD).
#
#   make            build for the detected platform (on Windows: build and
#                   check, as `make check`)
#   make check      win32 only: build, compare with xeBuild.exe, check SHA256
#   make win32latest   build with the gcc on PATH (a current MSYS2), same as
#                   `make PLATFORM=win32latest`
#   make clean      remove the platform's objects and executable
#
# PLATFORM is detected, or set it on the command line or in an untracked
# config.mk:
#
#   win32        Windows (detected): the pinned toolchain in
#                tools/toolchain-4745 (run tools/fetch_toolchain.sh first,
#                from Git Bash); the only build that reproduces the reference
#                bytes.  Outputs build/obj/, build/xeBuild.exe.
#   win32latest  Windows with the latest MSYS2 gcc on PATH.  The gcc driver
#                picks its own default target and libraries: a MINGW32 shell
#                builds a 32-bit exe like the original, a MINGW64 or UCRT64
#                one a 64-bit exe.  Never matches.
#   linux        Linux (detected): the installed gcc.
#   macos        macOS (detected): the installed clang.
#
# Only win32 fixes the bitness (its toolchain is i686-only).  The others set
# no -m32/-m64 or target and build for the compiler's default, 32- or
# 64-bit; pass e.g. CFLAGS=-m32 LDFLAGS=-m32 for a different one.
#
# The platforms other than win32 write to build/<platform>/ so the matching
# objects in build/obj/ aren't touched.  CC, CFLAGS, LDFLAGS, LDLIBS, PYTHON
# and SHA256SUM can be overridden as usual; CFLAGS and LDFLAGS are added after
# the platform's own flags (empty for win32, which must stay as it is).
# macOS needs no _FILE_OFFSET_BITS: its off_t is always 64-bit.

-include config.mk

# --- platform detection ---------------------------------------------------

ifeq ($(OS),Windows_NT)
DETECTED_PLATFORM := win32
else
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
DETECTED_PLATFORM := macos
else ifeq ($(UNAME_S),Linux)
DETECTED_PLATFORM := linux
else
DETECTED_PLATFORM := unknown
endif
endif
PLATFORM ?= $(DETECTED_PLATFORM)

# make's built-in CC default is `cc`: treat it as unset, so each platform
# section can pick its compiler while CC=... on the command line still wins
ifeq ($(origin CC),default)
CC_UNSET := 1
endif

PYTHON    ?= python
SHA256SUM ?= sha256sum
CFLAGS    ?=
LDFLAGS   ?=
LDLIBS    ?=

# Each section sets:
#   TC_BIN         toolchain bin/ to put first on PATH (empty: CC is on PATH)
#   CC             compiler (unless given)
#   OBJ, EXE       object directory and executable
#   PLAT_CFLAGS    compile flags (before CFLAGS; empty unless set)
#   PLAT_LDFLAGS   link flags (before the objects)
#   PLAT_LIBS      libraries (after the objects)
#   MAP_FLAGS      linker map to build/<...>.map
#   STAMP          1 to stamp the reference link time into the exe
#   CHECK          1 when `make check` can reproduce the reference

# --- win32: the pinned toolchain (reference build) -------------------------
ifeq ($(PLATFORM),win32)
TC_BIN ?= tools/toolchain-4745/mingw32/bin
ifdef CC_UNSET
CC := $(TC_BIN)/gcc.exe
endif
OBJ := build/obj
EXE := build/xeBuild.exe
# Link as gcc 6.2.0 does: crt2.o and crtbegin.o, the program, the libraries
# (ws2_32, then gcc's defaults, spelled out as that driver passes them), the
# default manifest and crtend.o, with ld's default script
# (tools/fetch_toolchain.sh rebuilds the kernel32 and msvcrt import libraries
# as the original had them).  globals.o goes after the libraries, so its .bss
# follows theirs like the original's COMMON block (src/globals.c).
PLAT_LDFLAGS := -s
PLAT_LIBS := -lws2_32 -lmingw32 -lgcc -lgcc_eh -lmoldname -lmingwex -lmsvcrt \
	-lpthread -ladvapi32 -lshell32 -luser32 -lkernel32
MAP_FLAGS := -Wl,--no-insert-timestamp,-Map,build/xeBuild.map
STAMP := 1
CHECK := 1

# --- win32latest: the latest MSYS2 gcc on PATH -----------------------------
else ifeq ($(PLATFORM),win32latest)
TC_BIN ?=
ifdef CC_UNSET
CC := gcc
endif
OBJ := build/win32latest/obj
EXE := build/win32latest/xeBuild.exe
PLAT_LDFLAGS := -s
PLAT_LIBS := -lws2_32
MAP_FLAGS := -Wl,-Map,build/win32latest/xeBuild.map

# --- linux: the installed gcc ----------------------------------------------
else ifeq ($(PLATFORM),linux)
TC_BIN ?=
ifdef CC_UNSET
CC := gcc
endif
OBJ := build/linux/obj
EXE := build/linux/xeBuild
PLAT_LDFLAGS := -s
PLAT_LIBS :=
# 64-bit off_t for fseeko/ftello on 32-bit Linux too (xebuild.h maps the
# code's fseeko64/ftello64 to them)
PLAT_CFLAGS := -D_FILE_OFFSET_BITS=64
MAP_FLAGS := -Wl,-Map,build/linux/xeBuild.map

# --- macos: the installed clang --------------------------------------------
else ifeq ($(PLATFORM),macos)
TC_BIN ?=
ifdef CC_UNSET
CC := clang
endif
OBJ := build/macos/obj
EXE := build/macos/xeBuild
# ld64 strips with -Wl,-x (-s is obsolete there) and spells the map -map
PLAT_LDFLAGS := -Wl,-x
PLAT_LIBS :=
MAP_FLAGS := -Wl,-map,build/macos/xeBuild.map

else
$(error unknown PLATFORM '$(PLATFORM)': use win32, win32latest, linux or macos)
endif

# gcc finds cc1/as and their DLLs through PATH, so recipes that run it put
# TC_BIN first (pwd -P: a native Windows make hands sh a C:/ style $PWD, whose
# colon would split the PATH entry)
ifneq ($(strip $(TC_BIN)),)
TC_ENV = PATH="$$(pwd -P)/$(TC_BIN):$$PATH"
endif

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

.PHONY: all check clean win32latest
.DELETE_ON_ERROR:

ifeq ($(CHECK),1)
.DEFAULT_GOAL := check
else
.DEFAULT_GOAL := all
endif

all: $(EXE)

# $(call compile,original path,flags): compile $< to $@.  The source goes
# through stdin so the #line can name the original build path, for __FILE__
# in assert() (gcc 6 has no -ffile-prefix-map).  -MMD records the headers.
define compile
	@mkdir -p $(@D)
	{ printf '#line 1 "%s"\n' '$(1)'; cat $<; } | \
	  $(TC_ENV) $(CC) -c $(2) $(PLAT_CFLAGS) $(CFLAGS) -I$(<D) \
	  -MMD -MP -MF $(@:.o=.d) -MT $@ -x c - -o $@
endef

# src/crypto is XeCrypt's tree (headers include "bign/bigdigits.h" etc.)
$(OBJ)/crypto/%.o: src/crypto/%.c $(MAKEFILE_LIST)
	$(call compile,H:/x360sdk/__NAND/nandbuild_trin/XeCrypt/$*.c,-O3 -Isrc/crypto)

# the rest of the app: original path unknown (no assert in the app)
$(OBJ)/%.o: src/%.c $(MAKEFILE_LIST)
	$(call compile,$*.c,-O3)

# The stamp is part of the link so an unstamped exe is never up to date.
$(EXE): $(OBJS)
	$(TC_ENV) $(CC) $(PLAT_LDFLAGS) -o $@ $(OBJS) $(PLAT_LIBS) $(LDLIBS) \
	  $(LDFLAGS) $(MAP_FLAGS)
ifeq ($(STAMP),1)
	$(PYTHON) tools/re/stamp.py $@ $(LINK_TIME)
endif

ifeq ($(CHECK),1)
check: $(EXE)
	$(PYTHON) tools/re/execmp.py $(REF) $(EXE)
	@$(SHA256SUM) $(EXE)
	@[ "$$($(SHA256SUM) $(EXE) | cut -d' ' -f1)" = $(REF_SHA256) ] || \
	  { echo "SHA256 differs from $(REF_SHA256)" >&2; exit 1; }
else
check:
	@echo "make check: only PLATFORM=win32 (the pinned toolchain) reproduces" \
	  "the reference; this is $(PLATFORM)" >&2; exit 1
endif

win32latest:
	$(MAKE) PLATFORM=win32latest

clean:
	rm -f $(OBJS) $(OBJS:.o=.d) $(EXE) $(basename $(EXE)).map

-include $(OBJS:.o=.d)
