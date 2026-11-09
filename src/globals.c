/* globals: the program's COMMON block, the uninitialized globals near the end
   of .bss.

   The original objects declared these without initializers, so gcc made them
   COMMON symbols, and ld lays them out after every object's .bss: each
   object's in link order (crt2's and crtbegin's, filelist_ini's blOrder, then these, then
   XeCrypt's XeCryptRandomState and the libraries'), and within an object in
   the order of ld's symbol hash table (4051 buckets, bfd_hash_hash of the
   name), aligning the big ones to 32 bytes.  The original names are unknown;
   these are picked so their buckets ascend in the original's address order
   (xb 2672, fsFileEnts 2710, fsChain 2883, flashHdr 2960,
   imgUsed 3065, netTimeStart 3139, spareBuf 3286, consoleManifest 3312), so a
   rename has to keep that order.  build.sh links this object before
   XeCrypt's.  Its `GCC:` ident stands for a data-only program object of the
   original.  The types come from xebuild.h. */
#include <time.h>
#include "xebuild.h"

_Static_assert(sizeof(struct xebuild) == 0x4f910, "struct xebuild");

struct xebuild xb;			/* 479ea0 */
struct fsent fsFileEnts[256];		/* 4c97c0 image_write */
uint16_t fsChain[0x1000];		/* 4cb7c0 */
struct flashhdr flashHdr;		/* 4cd7c0 */
uint32_t imgUsed;			/* 4cd840 */
time_t netTimeStart;			/* 4cd844 net */
char spareBuf[0x400];			/* 4cd860 nothing references it */
struct manifest consoleManifest;	/* 4cdc60 console_hdd */
