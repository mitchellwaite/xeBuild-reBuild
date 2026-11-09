/* globals: the program's COMMON block, the uninitialized globals near the end
   of .bss.

   The original objects declared these without initializers, so gcc made them
   COMMON symbols, and ld laid them out after every object's .bss: each
   object's in link order (crt2's and crtbegin's, then the program's, then the
   libraries': atonexit's, natstart's and libgcc's _ctors), and within an
   object in the order of its symbol hash table (which depends on names we
   don't know), aligning the big ones to 32 bytes.  This file defines the
   program's in that address order instead, and crt2's and crtbegin's, which
   come before them; build.sh links it after the libraries, so it follows
   their .bss, and the libraries' own COMMON symbols follow it.  The zero
   initializers make them real definitions (not COMMON), which net.c's
   netStartTime and xecrypt.c's XeCryptRandomState, still tentative, resolve
   to; gcc emits them in reverse definition order, so they are defined from
   the highest address down.  Its `GCC:` ident stands for a
   data-only program object of the original (one ident more than the objects
   we know).  Every variable is aligned(4) like the block, and the pad arrays
   stand for ld's alignment padding.  The types come from xebuild.h. */
#include <time.h>
#include "crypto/rc4/rc4.h"
#include "xebuild.h"

#define A4 __attribute__((aligned(4)))
/* static, but in place: gcc would emit a plain static as .lcomm, which gas
   puts after all of .bss */
#define PAD __attribute__((used, section(".bss")))

_Static_assert(sizeof(struct xebuild) == 0x4f910, "struct xebuild");

RC4_KEY XeCryptRandomState A4 = {0};		/* 50e880 crypto/xecrypt */
static char pad50e86c[20] PAD;
struct manifest manifest A4 = {0};		/* 4cdc60 console_hdd */
char unused4cd860[0x400] A4 = {0};		/* 4cd860 nothing references it */
static char pad4cd848[24] PAD;
time_t netStartTime A4 = {0};			/* 4cd844 net */
uint32_t imgEnd A4 = {0};			/* 4cd840 */
struct flashhdr hdrTemplate A4 = {0};		/* 4cd7c0 */
uint16_t fsTable[0x1000] A4 = {0};		/* 4cb7c0 */
struct fsent fsFiles[256] A4 = {0};		/* 4c97c0 image_write */
static char pad4c97b0[16] PAD;
struct xebuild xb A4 = {0};			/* 479ea0 */
static char pad479e88[24] PAD;
int *blOrder A4 = {0};			/* 479e84 filelist_ini: one of the bl* tables */
/* crt2.o (mingw-w64's crtexe.c) and crtbegin.o (libgcc's cygming-crtbegin.c) */
void *hmod_libgcc A4 = {0};			/* 479e80 */
void *__mingw_winmain_hInstance A4 = {0};	/* 479e7c */
char *__mingw_winmain_lpCmdLine A4 = {0};	/* 479e78 */
