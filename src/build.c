/* build: reading the image's input files (with crc32 checks against the
   ini), bootloader checks, patches and payloads, encoding the flash.
   Built with -fno-toplevel-reorder: functions, .data and strings come out
   in definition order. The strings are literals: gcc emits a function's
   in the order it expands their blocks, so the original's .rdata order
   follows from the code's shape (checkBl keeps an asm "i" hint). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* xb.files' declared bound sets the files loops' trip count estimate */
#define XB_FILES_BOUND 19

#include "crypto/xecrypt.h"
#include "xebuild.h"
#include "build.h"
#include "crc32.h"
#include "fileutil.h"
#include "image_read.h"
#include "image_write.h"
#include "keys.h"
#include "keyvault.h"
#include "log.h"
#include "mode_update.h"
#include "options.h"
#include "smc.h"
#include "sysupdate.h"
#include "timeutil.h"
#include "xboxrom.h"

void showSmcConfig(const uint8_t *smc);

/* .data, in this order (-fno-toplevel-reorder) */
uint8_t defBl60[0x60] = {
	0xc0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x0f, 0x0f, 0x0f, 0x0f,
	0x0f, 0x0f, 0x0f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
};
uint8_t defPayload[0x200] = {
	0x80, 0x13, 0x1d, 0xb0, 0x80, 0x13, 0x03, 0xa0, 0x00, 0x00, 0x00, 0x00,
	0x02, 0x00, 0x00, 0x00, 0x12, 0x00, 0x00, 0x00, 0x80, 0x13, 0x03, 0x74,
	0x80, 0x13, 0x03, 0x74, 0x80, 0x13, 0x03, 0x7c, 0x80, 0x13, 0x03, 0x7c,
	0x80, 0x12, 0x50, 0x20, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0xfd, 0xff, 0xd7, 0xff, 0x38, 0x60, 0x00, 0x10, 0x78, 0x63, 0xc1, 0xc6,
	0xf8, 0x67, 0x00, 0x00, 0x7c, 0xc8, 0x03, 0xa6, 0x38, 0x80, 0xff, 0xff,
	0x7c, 0x89, 0x03, 0xa6, 0x81, 0x05, 0x00, 0x00, 0x91, 0x06, 0x00, 0x00,
	0x7c, 0x00, 0x30, 0x6c, 0x7c, 0x00, 0x37, 0xac, 0x7c, 0x00, 0x04, 0xac,
	0x4c, 0x00, 0x01, 0x2c, 0x38, 0xc6, 0x00, 0x04, 0x38, 0xa5, 0x00, 0x04,
	0x42, 0x00, 0xff, 0xe0, 0x38, 0x60, 0x00, 0x11, 0x78, 0x63, 0xc1, 0xc6,
	0xf8, 0x67, 0x00, 0x00, 0x4e, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00,
	0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x48, 0x00, 0x00, 0x00, 0x00,
	0x80, 0x13, 0x03, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x80, 0x00, 0x00, 0x00,
	0x00, 0x13, 0x03, 0xa0, 0x80, 0x00, 0x02, 0x00, 0xc8, 0x09, 0x00, 0x00,
	0x80, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x80, 0x00, 0x02, 0x00,
	0x00, 0x06, 0x10, 0x10, 0x80, 0x00, 0x02, 0x00, 0xea, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x80, 0x07, 0x01, 0x90, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x07, 0x02, 0x28,
	0x80, 0x07, 0x02, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x90, 0x30,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
};
uint8_t defCore[0xd40] = {
	0x3c, 0x20, 0x80, 0x00, 0x78, 0x21, 0x07, 0xc6, 0x64, 0x21, 0x1e, 0x00,
	0x7f, 0xdf, 0xfa, 0xa6, 0x7b, 0xc4, 0x83, 0xe4, 0x7c, 0x24, 0x08, 0x50,
	0x38, 0x21, 0xff, 0x80, 0x7c, 0x71, 0xfa, 0xa6, 0x38, 0x80, 0x00, 0x01,
	0x78, 0x83, 0x64, 0xce, 0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x71, 0xfb, 0xa6,
	0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x79, 0xfa, 0xa6, 0x38, 0x80, 0x00, 0x08,
	0x78, 0x83, 0x64, 0x0e, 0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x79, 0xfb, 0xa6,
	0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x7e, 0x4a, 0xa6, 0x38, 0x80, 0x00, 0x01,
	0x78, 0x83, 0x55, 0x6c, 0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x7e, 0x4b, 0xa6,
	0x4c, 0x00, 0x01, 0x2c, 0x28, 0x3e, 0x00, 0x00, 0x40, 0x82, 0x00, 0x58,
	0x3d, 0xa0, 0x02, 0x00, 0x7d, 0xa1, 0x01, 0x64, 0x3c, 0x60, 0x80, 0x00,
	0x78, 0x63, 0x07, 0xc6, 0x64, 0x63, 0x1c, 0x00, 0x60, 0x63, 0x0b, 0x00,
	0xe8, 0x43, 0x00, 0x08, 0x48, 0x00, 0x03, 0x69, 0x28, 0x03, 0x00, 0x00,
	0x40, 0x82, 0x00, 0xa8, 0x3f, 0xe0, 0x80, 0x00, 0x7b, 0xff, 0x07, 0xc6,
	0x63, 0xff, 0x01, 0x00, 0x38, 0x60, 0x00, 0x00, 0x4c, 0x00, 0x01, 0x2c,
	0x7c, 0x79, 0x4b, 0xa6, 0x7c, 0x70, 0x4b, 0xa6, 0x7c, 0x71, 0x4b, 0xa6,
	0x4c, 0x00, 0x01, 0x2c, 0x7f, 0xe8, 0x03, 0xa6, 0x4e, 0x80, 0x00, 0x20,
	0x3c, 0x80, 0x80, 0x00, 0x78, 0x84, 0x07, 0xc6, 0x64, 0x84, 0x1c, 0x00,
	0x60, 0x84, 0x0a, 0xa8, 0x7c, 0x7f, 0xfa, 0xa6, 0x54, 0x63, 0x10, 0x3a,
	0x7c, 0x84, 0x1a, 0x14, 0x38, 0xa0, 0x00, 0x01, 0x90, 0xa4, 0x00, 0x00,
	0x3f, 0x80, 0x80, 0x00, 0x7b, 0x9c, 0x07, 0xc6, 0x67, 0x9c, 0x1c, 0x08,
	0x63, 0x9c, 0x00, 0x00, 0x3f, 0xa0, 0x80, 0x00, 0x7b, 0xbd, 0x07, 0xc6,
	0x67, 0xbd, 0x1c, 0x00, 0x63, 0xbd, 0x0a, 0xc8, 0xeb, 0xbd, 0x00, 0x00,
	0x38, 0x00, 0x00, 0x00, 0xf8, 0x1d, 0x00, 0x00, 0xe8, 0x7d, 0x00, 0x00,
	0x28, 0x23, 0x00, 0x00, 0x40, 0x82, 0x00, 0x34, 0x80, 0x7c, 0x00, 0x00,
	0x28, 0x03, 0x00, 0x00, 0x41, 0x82, 0xff, 0xec, 0x3c, 0x60, 0x00, 0x01,
	0x7c, 0x69, 0x03, 0xa6, 0x60, 0x00, 0x00, 0x00, 0x42, 0x00, 0xff, 0xfc,
	0x3f, 0xe0, 0x80, 0x00, 0x7b, 0xff, 0x07, 0xc6, 0x67, 0xff, 0x1c, 0x04,
	0x7f, 0xe8, 0x03, 0xa6, 0x4e, 0x80, 0x00, 0x20, 0x7c, 0x79, 0xfa, 0xa6,
	0x38, 0x80, 0x00, 0x01, 0x78, 0x83, 0x83, 0xce, 0x38, 0x80, 0x00, 0x08,
	0x78, 0x83, 0x64, 0x0e, 0x38, 0x80, 0x00, 0x0e, 0x78, 0x83, 0x16, 0x8e,
	0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x79, 0xfb, 0xa6, 0x7c, 0x00, 0x04, 0xac,
	0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x7e, 0x4a, 0xa6, 0x38, 0x80, 0x00, 0x01,
	0x78, 0x83, 0x0f, 0xac, 0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x7e, 0x4b, 0xa6,
	0x7c, 0x00, 0x04, 0xac, 0x4c, 0x00, 0x01, 0x2c, 0x38, 0x60, 0x03, 0xff,
	0x78, 0x63, 0x07, 0xc6, 0x7c, 0x20, 0x1a, 0x24, 0x7c, 0x00, 0x04, 0xac,
	0x7c, 0x74, 0xfa, 0xa6, 0x38, 0x80, 0x00, 0x3f, 0x78, 0x83, 0x44, 0x8e,
	0x4c, 0x00, 0x01, 0x2c, 0x7c, 0x74, 0xfb, 0xa6, 0x7c, 0x00, 0x04, 0xac,
	0x4c, 0x00, 0x01, 0x2c, 0x38, 0x60, 0x00, 0x00, 0x7c, 0x70, 0x4b, 0xa6,
	0x7c, 0x71, 0x4b, 0xa6, 0x7c, 0x71, 0xfa, 0xa6, 0x38, 0x80, 0x00, 0x01,
	0x78, 0x83, 0xf8, 0x0e, 0x38, 0x80, 0x00, 0x07, 0x78, 0x83, 0xd0, 0xce,
	0x38, 0x80, 0x00, 0x03, 0x78, 0x83, 0xa2, 0x8e, 0x38, 0x80, 0x00, 0x01,
	0x78, 0x83, 0x36, 0x4e, 0x38, 0x80, 0x01, 0x00, 0x78, 0x84, 0x07, 0xc6,
	0x7c, 0xa0, 0x00, 0xa6, 0x38, 0xc0, 0x00, 0x30, 0x7c, 0xa5, 0x30, 0x78,
	0x7c, 0xbb, 0x03, 0xa6, 0x38, 0xc0, 0x01, 0x00, 0x7c, 0xda, 0x03, 0xa6,
	0x7c, 0x71, 0xfb, 0xa6, 0x7c, 0x99, 0x4b, 0xa6, 0x4c, 0x00, 0x00, 0x24,
	0x3c, 0x80, 0x80, 0x00, 0x60, 0x84, 0x02, 0x00, 0x78, 0x84, 0x07, 0xc6,
	0x64, 0x84, 0xea, 0x00, 0x80, 0xa4, 0x10, 0x18, 0x54, 0xa5, 0x01, 0x8d,
	0x41, 0x82, 0xff, 0xf8, 0x54, 0x63, 0xc0, 0x0e, 0x90, 0x64, 0x10, 0x14,
	0x4e, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x38, 0xe0, 0x00, 0x10,
	0x39, 0x21, 0xff, 0xef, 0x39, 0x40, 0x00, 0x00, 0x7c, 0xe9, 0x03, 0xa6,
	0x9d, 0x49, 0x00, 0x01, 0x42, 0x00, 0xff, 0xfc, 0x39, 0x00, 0x00, 0x10,
	0x39, 0x21, 0xff, 0xdf, 0x39, 0x40, 0x00, 0x00, 0x7d, 0x09, 0x03, 0xa6,
	0x9d, 0x49, 0x00, 0x01, 0x42, 0x00, 0xff, 0xfc, 0x3d, 0x00, 0x80, 0x00,
	0x98, 0x61, 0xff, 0xf0, 0x61, 0x08, 0x02, 0x00, 0x79, 0x08, 0x07, 0xc6,
	0x65, 0x08, 0xea, 0x00, 0x61, 0x08, 0x10, 0x84, 0x3d, 0x20, 0x80, 0x00,
	0x81, 0x48, 0x00, 0x00, 0x61, 0x29, 0x02, 0x00, 0x55, 0x4a, 0x01, 0x4a,
	0x79, 0x29, 0x07, 0xc6, 0x2f, 0x8a, 0x00, 0x00, 0x65, 0x29, 0xea, 0x00,
	0x61, 0x29, 0x10, 0x84, 0x41, 0x9e, 0xff, 0xe0, 0x3d, 0x40, 0x80, 0x00,
	0x3d, 0x00, 0x04, 0x00, 0x61, 0x4a, 0x02, 0x00, 0x91, 0x09, 0x00, 0x00,
	0x3d, 0x00, 0x80, 0x00, 0x79, 0x4a, 0x07, 0xc6, 0x80, 0xe1, 0xff, 0xf0,
	0x61, 0x08, 0x02, 0x00, 0x65, 0x4a, 0xea, 0x00, 0x79, 0x08, 0x07, 0xc6,
	0x61, 0x4a, 0x10, 0x80, 0x65, 0x08, 0xea, 0x00, 0x90, 0xea, 0x00, 0x00,
	0x39, 0x60, 0x00, 0x04, 0x80, 0xe1, 0xff, 0xf4, 0x7d, 0x06, 0x43, 0x78,
	0x38, 0xa1, 0xff, 0xec, 0x90, 0xea, 0x00, 0x00, 0x61, 0x08, 0x10, 0x94,
	0x80, 0xe1, 0xff, 0xf8, 0x60, 0xc6, 0x10, 0x90, 0x38, 0x80, 0x00, 0x00,
	0x90, 0xea, 0x00, 0x00, 0x80, 0xe1, 0xff, 0xfc, 0x90, 0xea, 0x00, 0x00,
	0x38, 0xe0, 0x00, 0x00, 0x39, 0x40, 0x00, 0x00, 0x90, 0xe9, 0x00, 0x00,
	0x60, 0x00, 0x00, 0x00, 0x89, 0x21, 0xff, 0xe0, 0x7f, 0x89, 0x18, 0x00,
	0x41, 0x9e, 0x00, 0x50, 0x38, 0xe0, 0x00, 0x10, 0x39, 0x21, 0xff, 0xdf,
	0x7c, 0xe9, 0x03, 0xa6, 0x9d, 0x49, 0x00, 0x01, 0x42, 0x00, 0xff, 0xfc,
	0x81, 0x28, 0x00, 0x00, 0x55, 0x29, 0x01, 0x4a, 0x2f, 0x89, 0x00, 0x00,
	0x41, 0x9e, 0xff, 0xd4, 0x39, 0x21, 0xff, 0xdc, 0x91, 0x68, 0x00, 0x00,
	0x80, 0xe6, 0x00, 0x00, 0x94, 0xe9, 0x00, 0x04, 0x7f, 0xa9, 0x28, 0x00,
	0x40, 0x9e, 0xff, 0xf4, 0x90, 0x88, 0x00, 0x00, 0x89, 0x21, 0xff, 0xe0,
	0x7f, 0x89, 0x18, 0x00, 0x40, 0x9e, 0xff, 0xb8, 0x88, 0x61, 0xff, 0xe1,
	0x4e, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0xfb, 0xe1, 0xff, 0xf8,
	0x7c, 0x08, 0x02, 0xa6, 0xf8, 0x01, 0x00, 0x10, 0x7c, 0x7f, 0x1b, 0x78,
	0xf8, 0x21, 0xff, 0x81, 0x88, 0x63, 0x00, 0x00, 0x2f, 0xa3, 0x00, 0x00,
	0x41, 0x9e, 0x00, 0x18, 0x4b, 0xff, 0xfe, 0x65, 0x60, 0x00, 0x00, 0x00,
	0x8c, 0x7f, 0x00, 0x01, 0x2f, 0xa3, 0x00, 0x00, 0x40, 0x9e, 0xff, 0xf0,
	0x38, 0x21, 0x00, 0x80, 0xe8, 0x01, 0x00, 0x10, 0xeb, 0xe1, 0xff, 0xf8,
	0x7c, 0x08, 0x03, 0xa6, 0x4e, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x01, 0x80, 0x01, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00,
	0x3d, 0x42, 0x00, 0x07, 0x7c, 0x08, 0x02, 0xa6, 0x3d, 0x22, 0x00, 0x07,
	0xf8, 0x01, 0x00, 0x10, 0xfa, 0xc1, 0xff, 0xb0, 0xfa, 0xe1, 0xff, 0xb8,
	0xfb, 0x01, 0xff, 0xc0, 0x39, 0x4a, 0x75, 0x34, 0xfb, 0x21, 0xff, 0xc8,
	0x39, 0x29, 0x75, 0x30, 0x7d, 0x09, 0x50, 0x51, 0xfb, 0x41, 0xff, 0xd0,
	0xfb, 0x61, 0xff, 0xd8, 0xfb, 0x81, 0xff, 0xe0, 0xfb, 0xa1, 0xff, 0xe8,
	0xfb, 0xc1, 0xff, 0xf0, 0xfb, 0xe1, 0xff, 0xf8, 0xf8, 0x21, 0xff, 0x41,
	0x41, 0x82, 0x00, 0x18, 0x39, 0x29, 0xff, 0xff, 0x7d, 0x09, 0x03, 0xa6,
	0x39, 0x40, 0x00, 0x00, 0x9d, 0x49, 0x00, 0x01, 0x42, 0x00, 0xff, 0xfc,
	0x3d, 0x22, 0xff, 0xff, 0x60, 0x00, 0x00, 0x00, 0x3f, 0x40, 0x78, 0x63,
	0x3b, 0x22, 0x80, 0x48, 0x3f, 0x60, 0x7c, 0x68, 0x39, 0x29, 0x75, 0x30,
	0x3f, 0x80, 0x4e, 0x80, 0x3f, 0xa0, 0x4b, 0xff, 0x79, 0x36, 0x84, 0x20,
	0x79, 0x37, 0x84, 0x22, 0x79, 0x29, 0x04, 0x20, 0x3b, 0xd9, 0xff, 0xf8,
	0x66, 0xd6, 0x3c, 0x60, 0x66, 0xf7, 0x64, 0x63, 0x65, 0x38, 0x60, 0x63,
	0x3b, 0x39, 0x00, 0x98, 0x63, 0x5a, 0x07, 0xc6, 0x63, 0x7b, 0x03, 0xa6,
	0x63, 0x9c, 0x00, 0x21, 0x63, 0xbd, 0xff, 0xe8, 0xeb, 0xfe, 0x00, 0x09,
	0x38, 0x80, 0x01, 0x00, 0x38, 0x7f, 0xff, 0x80, 0x48, 0x00, 0x05, 0x6d,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x7f, 0xff, 0xe8, 0x92, 0xdf, 0xff, 0xe8,
	0x38, 0x80, 0x00, 0x18, 0x93, 0x5f, 0xff, 0xec, 0x92, 0xff, 0xff, 0xf0,
	0x93, 0x1f, 0xff, 0xf4, 0x93, 0x7f, 0xff, 0xf8, 0x93, 0x9f, 0xff, 0xfc,
	0x48, 0x00, 0x05, 0x9d, 0x60, 0x00, 0x00, 0x00, 0x7f, 0xe3, 0xfb, 0x78,
	0x93, 0xbf, 0x00, 0x00, 0x38, 0x80, 0x00, 0x80, 0x48, 0x00, 0x05, 0x89,
	0x60, 0x00, 0x00, 0x00, 0x7f, 0xbe, 0xc8, 0x00, 0x40, 0x9e, 0xff, 0xac,
	0x3d, 0x40, 0x80, 0x00, 0x3d, 0x00, 0x00, 0x3e, 0x61, 0x4a, 0x02, 0x00,
	0x3f, 0xe2, 0xff, 0xff, 0x79, 0x4a, 0x07, 0xc6, 0x61, 0x08, 0x00, 0x78,
	0x65, 0x4a, 0x00, 0x05, 0x38, 0xc0, 0x00, 0x00, 0x61, 0x4a, 0x20, 0x10,
	0x39, 0x20, 0x00, 0x00, 0x3b, 0xff, 0x7f, 0xd8, 0xf9, 0x0a, 0x00, 0x00,
	0x38, 0xa0, 0x00, 0x01, 0x60, 0x00, 0x00, 0x00, 0x79, 0x28, 0x17, 0x64,
	0x39, 0x49, 0x00, 0x01, 0x7c, 0xa7, 0x48, 0x30, 0x7d, 0x49, 0x07, 0xb4,
	0x7c, 0xe7, 0x33, 0x78, 0x7d, 0x1f, 0x40, 0x2e, 0x2f, 0x8a, 0x00, 0x06,
	0x2f, 0x08, 0x00, 0x00, 0x41, 0x9a, 0x00, 0x08, 0x7c, 0xe6, 0x07, 0xb4,
	0x40, 0x9e, 0xff, 0xd8, 0x2f, 0x86, 0x00, 0x3f, 0x39, 0x20, 0x00, 0x00,
	0x38, 0xc0, 0x00, 0x00, 0x40, 0x9e, 0xff, 0xc8, 0x3d, 0x40, 0x80, 0x00,
	0x61, 0x4a, 0x02, 0x00, 0x79, 0x4a, 0x07, 0xc6, 0x65, 0x4a, 0xc8, 0x00,
	0x7d, 0x49, 0x53, 0x78, 0x61, 0x4a, 0x00, 0x48, 0x61, 0x29, 0x00, 0x4c,
	0x81, 0x4a, 0x00, 0x00, 0x91, 0x5f, 0x00, 0x18, 0x81, 0x29, 0x00, 0x00,
	0x55, 0x2a, 0x06, 0x3e, 0x91, 0x3f, 0x00, 0x1c, 0x2f, 0x8a, 0x00, 0x00,
	0x40, 0x9e, 0x00, 0x0c, 0x39, 0x20, 0x00, 0x12, 0x99, 0x3f, 0x00, 0x1f,
	0x89, 0x5f, 0x00, 0x1d, 0x55, 0x49, 0x07, 0xfe, 0x2f, 0x89, 0x00, 0x00,
	0x41, 0x9e, 0x00, 0x20, 0x3d, 0x20, 0x80, 0x00, 0x3d, 0x00, 0xae, 0x01,
	0x61, 0x29, 0x02, 0x00, 0x79, 0x29, 0x07, 0xc6, 0x65, 0x29, 0xea, 0x00,
	0x61, 0x29, 0x10, 0x1c, 0x91, 0x09, 0x00, 0x00, 0x55, 0x4a, 0x07, 0x7a,
	0x55, 0x48, 0x06, 0x3e, 0x2c, 0x08, 0x00, 0x00, 0x41, 0x82, 0x00, 0xc4,
	0x38, 0x60, 0x00, 0x01, 0x3b, 0xc0, 0x00, 0x01, 0x4b, 0xff, 0xfc, 0x59,
	0x89, 0x3f, 0x00, 0x1f, 0x7f, 0x89, 0x18, 0x00, 0x41, 0x9e, 0x00, 0x20,
	0x89, 0x3f, 0x00, 0x1e, 0x3b, 0xc0, 0x00, 0x00, 0x2f, 0xa9, 0x00, 0x00,
	0x41, 0x9e, 0x00, 0x10, 0x7c, 0x7e, 0x4a, 0x78, 0x7f, 0xde, 0x00, 0x74,
	0x7b, 0xde, 0xd1, 0x82, 0x89, 0x3f, 0x00, 0x1c, 0x2f, 0xa9, 0x00, 0x00,
	0x41, 0x9e, 0x00, 0xb0, 0x7f, 0x83, 0x48, 0x40, 0x40, 0x9e, 0x00, 0xa8,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x80, 0xe8, 0x4b, 0xff, 0xfd, 0x61,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x80, 0xf0, 0x4b, 0xff, 0xfd, 0x55,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x81, 0x20, 0x4b, 0xff, 0xfd, 0x49,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x81, 0x50, 0x4b, 0xff, 0xfd, 0x3d,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x81, 0x80, 0x4b, 0xff, 0xfd, 0x31,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x81, 0xb0, 0x4b, 0xff, 0xfd, 0x25,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x81, 0xe0, 0x4b, 0xff, 0xfd, 0x19,
	0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x82, 0x10, 0x4b, 0xff, 0xfd, 0x0d,
	0x2f, 0xbe, 0x00, 0x00, 0x40, 0x9e, 0x02, 0x5c, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x82, 0x60, 0x4b, 0xff, 0xfc, 0xf9, 0x48, 0x00, 0x00, 0x98,
	0x38, 0x60, 0x00, 0x0a, 0x4b, 0xff, 0xfb, 0x9d, 0x89, 0x3f, 0x00, 0x1d,
	0x55, 0x29, 0x07, 0xbc, 0x55, 0x2a, 0x06, 0x3e, 0x2c, 0x0a, 0x00, 0x00,
	0x40, 0x82, 0x02, 0x08, 0x68, 0x63, 0x00, 0x62, 0x78, 0x7e, 0x06, 0x20,
	0x7f, 0xde, 0x00, 0xd0, 0x7b, 0xde, 0x0f, 0xe0, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x80, 0xf0, 0x4b, 0xff, 0xfc, 0xbd, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x81, 0x20, 0x4b, 0xff, 0xfc, 0xb1, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x81, 0x50, 0x4b, 0xff, 0xfc, 0xa5, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x81, 0x80, 0x4b, 0xff, 0xfc, 0x99, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x81, 0xb0, 0x4b, 0xff, 0xfc, 0x8d, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x81, 0xe0, 0x4b, 0xff, 0xfc, 0x81, 0x60, 0x00, 0x00, 0x00,
	0x38, 0x62, 0x82, 0x10, 0x4b, 0xff, 0xfc, 0x75, 0x2f, 0xbe, 0x00, 0x00,
	0x40, 0x9e, 0x01, 0xc4, 0x60, 0x00, 0x00, 0x00, 0x38, 0x62, 0x82, 0x30,
	0x4b, 0xff, 0xfc, 0x61, 0x3d, 0x20, 0x80, 0x00, 0x39, 0x00, 0x00, 0x00,
	0x61, 0x29, 0x01, 0xff, 0x39, 0x40, 0xff, 0xff, 0x79, 0x29, 0x07, 0xc6,
	0x61, 0x19, 0x80, 0x00, 0x65, 0x29, 0xff, 0xff, 0x79, 0x4a, 0x00, 0x40,
	0x7f, 0x29, 0x03, 0xa6, 0x61, 0x29, 0xff, 0xff, 0x60, 0x00, 0x00, 0x00,
	0x8d, 0x09, 0x00, 0x01, 0x9d, 0x0a, 0x00, 0x01, 0x42, 0x00, 0xff, 0xf8,
	0x3d, 0x20, 0x80, 0x00, 0x61, 0x29, 0x02, 0x00, 0x79, 0x29, 0x07, 0xc6,
	0x65, 0x29, 0xc8, 0x09, 0x61, 0x29, 0x10, 0x00, 0x81, 0x49, 0x00, 0x00,
	0x3d, 0x20, 0x80, 0x00, 0x2f, 0x8a, 0xff, 0xff, 0x41, 0x9e, 0x01, 0x48,
	0x61, 0x29, 0x02, 0x00, 0x38, 0x80, 0xff, 0xff, 0x79, 0x29, 0x07, 0xc6,
	0x78, 0x84, 0x00, 0x04, 0x65, 0x29, 0xc8, 0x09, 0x61, 0x29, 0x10, 0x04,
	0x81, 0x09, 0x00, 0x00, 0x38, 0xc9, 0x00, 0x04, 0x7d, 0x4a, 0x22, 0x14,
	0x2f, 0xa8, 0x00, 0x00, 0x41, 0x9e, 0x00, 0x34, 0x39, 0x08, 0xff, 0xff,
	0x39, 0x4a, 0xff, 0xfc, 0x79, 0x05, 0x00, 0x20, 0x78, 0xa7, 0x17, 0x64,
	0x7c, 0xe6, 0x3a, 0x14, 0x85, 0x09, 0x00, 0x04, 0x7f, 0xa9, 0x38, 0x00,
	0x95, 0x0a, 0x00, 0x04, 0x40, 0x9e, 0xff, 0xf4, 0x38, 0xa5, 0x00, 0x01,
	0x78, 0xa5, 0x17, 0x64, 0x7c, 0xc6, 0x2a, 0x14, 0x81, 0x46, 0x00, 0x00,
	0x39, 0x26, 0x00, 0x04, 0x2f, 0x8a, 0xff, 0xff, 0x40, 0x9e, 0xff, 0xb0,
	0x3d, 0x40, 0x80, 0x00, 0x39, 0x29, 0xff, 0xfc, 0x79, 0x4a, 0x07, 0xc6,
	0x38, 0xe0, 0x00, 0x00, 0x65, 0x4a, 0x01, 0x00, 0x7d, 0x46, 0x53, 0x78,
	0x48, 0x00, 0x00, 0x0c, 0x2b, 0x87, 0x00, 0x02, 0x41, 0x9d, 0x00, 0x30,
	0x85, 0x09, 0x00, 0x04, 0x2f, 0x88, 0xff, 0xff, 0x91, 0x0a, 0x00, 0x00,
	0x39, 0x4a, 0x00, 0x04, 0x40, 0x9e, 0xff, 0xe8, 0x38, 0xe7, 0x00, 0x01,
	0x78, 0xea, 0x60, 0x28, 0x78, 0xe7, 0x00, 0x20, 0x7d, 0x4a, 0x32, 0x14,
	0x2b, 0x87, 0x00, 0x02, 0x40, 0x9d, 0xff, 0xd8, 0x3d, 0x20, 0x80, 0x00,
	0x3d, 0x40, 0x80, 0x00, 0x61, 0x29, 0x02, 0x00, 0x79, 0x4a, 0x07, 0xc6,
	0x79, 0x29, 0x07, 0xc6, 0x65, 0x4a, 0x01, 0x00, 0x65, 0x29, 0xc8, 0x09,
	0x39, 0x00, 0x00, 0x60, 0x61, 0x4a, 0x2f, 0xff, 0x61, 0x29, 0x4f, 0xff,
	0x7d, 0x09, 0x03, 0xa6, 0x8d, 0x09, 0x00, 0x01, 0x9d, 0x0a, 0x00, 0x01,
	0x42, 0x00, 0xff, 0xf8, 0x38, 0x21, 0x00, 0xc0, 0x38, 0x60, 0x00, 0x00,
	0xe8, 0x01, 0x00, 0x10, 0xea, 0xc1, 0xff, 0xb0, 0xea, 0xe1, 0xff, 0xb8,
	0x7c, 0x08, 0x03, 0xa6, 0xeb, 0x01, 0xff, 0xc0, 0xeb, 0x21, 0xff, 0xc8,
	0xeb, 0x41, 0xff, 0xd0, 0xeb, 0x61, 0xff, 0xd8, 0xeb, 0x81, 0xff, 0xe0,
	0xeb, 0xa1, 0xff, 0xe8, 0xeb, 0xc1, 0xff, 0xf0, 0xeb, 0xe1, 0xff, 0xf8,
	0x4e, 0x80, 0x00, 0x20, 0x68, 0x7e, 0x00, 0x60, 0x7f, 0xde, 0x00, 0x34,
	0x57, 0xde, 0xd9, 0x7e, 0x7b, 0xde, 0x00, 0x20, 0x4b, 0xff, 0xfd, 0xfc,
	0x61, 0x29, 0x02, 0x00, 0x79, 0x29, 0x07, 0xc6, 0x65, 0x29, 0xc8, 0x09,
	0x61, 0x29, 0x10, 0x04, 0x4b, 0xff, 0xff, 0x18, 0x3f, 0xa0, 0x80, 0x00,
	0x60, 0x00, 0x00, 0x00, 0x63, 0xbd, 0x02, 0x00, 0x38, 0x62, 0x82, 0x20,
	0x7b, 0xbd, 0x07, 0xc6, 0x3f, 0x40, 0x02, 0x00, 0x4b, 0xff, 0xfa, 0x91,
	0x3d, 0x40, 0x80, 0x00, 0x7f, 0xa9, 0xeb, 0x78, 0x67, 0xbd, 0xea, 0x00,
	0x79, 0x4a, 0x07, 0xc6, 0x7f, 0xbe, 0xeb, 0x78, 0x7f, 0xbf, 0xeb, 0x78,
	0x7f, 0xab, 0xeb, 0x78, 0x7f, 0xa3, 0xeb, 0x78, 0x7f, 0xa4, 0xeb, 0x78,
	0x7f, 0xa5, 0xeb, 0x78, 0x7f, 0xa6, 0xeb, 0x78, 0x65, 0x4a, 0x1c, 0x03,
	0x65, 0x29, 0xc8, 0x09, 0x38, 0x00, 0x00, 0x00, 0x63, 0xa7, 0x30, 0x20,
	0x63, 0xa8, 0x50, 0x20, 0x3b, 0x60, 0x08, 0x00, 0x3f, 0x80, 0xff, 0xff,
	0x63, 0xbd, 0x30, 0x28, 0x63, 0xde, 0x50, 0x28, 0x63, 0xff, 0x30, 0x60,
	0x90, 0x1d, 0x00, 0x00, 0x61, 0x6b, 0x50, 0x60, 0x90, 0x1e, 0x00, 0x00,
	0x60, 0x63, 0x30, 0x2c, 0x93, 0x47, 0x00, 0x00, 0x60, 0x84, 0x50, 0x2c,
	0x93, 0x48, 0x00, 0x00, 0x60, 0xa5, 0x30, 0x24, 0x93, 0x67, 0x00, 0x00,
	0x60, 0xc6, 0x50, 0x24, 0x93, 0x68, 0x00, 0x00, 0x3f, 0x20, 0x00, 0x01,
	0x90, 0x1f, 0x00, 0x00, 0x61, 0x4a, 0xff, 0xfc, 0x90, 0x0b, 0x00, 0x00,
	0x61, 0x29, 0x50, 0x5c, 0x90, 0x03, 0x00, 0x00, 0x7f, 0x29, 0x03, 0xa6,
	0x90, 0x04, 0x00, 0x00, 0x93, 0x85, 0x00, 0x00, 0x93, 0x86, 0x00, 0x00,
	0x60, 0x00, 0x00, 0x00, 0x85, 0x09, 0x00, 0x04, 0x95, 0x0a, 0x00, 0x04,
	0x42, 0x00, 0xff, 0xf8, 0x38, 0x21, 0x00, 0xc0, 0x3d, 0x22, 0x00, 0x07,
	0x38, 0x60, 0x00, 0x01, 0x39, 0x40, 0x00, 0x01, 0xe8, 0x01, 0x00, 0x10,
	0x91, 0x49, 0x75, 0x30, 0xea, 0xc1, 0xff, 0xb0, 0xea, 0xe1, 0xff, 0xb8,
	0x7c, 0x08, 0x03, 0xa6, 0xeb, 0x01, 0xff, 0xc0, 0xeb, 0x21, 0xff, 0xc8,
	0xeb, 0x41, 0xff, 0xd0, 0xeb, 0x61, 0xff, 0xd8, 0xeb, 0x81, 0xff, 0xe0,
	0xeb, 0xa1, 0xff, 0xe8, 0xeb, 0xc1, 0xff, 0xf0, 0xeb, 0xe1, 0xff, 0xf8,
	0x4e, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01,
	0x80, 0x0a, 0x00, 0x00, 0x3c, 0xa0, 0xff, 0xff, 0x60, 0xa5, 0xff, 0xf1,
	0x7c, 0xa5, 0x18, 0x38, 0x7c, 0x65, 0x18, 0x50, 0x7c, 0x84, 0x1a, 0x14,
	0x7c, 0x00, 0x28, 0x6c, 0x30, 0xa5, 0x00, 0x80, 0x34, 0x84, 0xff, 0x80,
	0x40, 0x80, 0xff, 0xf4, 0x4c, 0x00, 0x01, 0x2c, 0x4e, 0x80, 0x00, 0x20,
	0x3c, 0xa0, 0xff, 0xff, 0x60, 0xa5, 0xff, 0xf1, 0x7c, 0xa5, 0x18, 0x38,
	0x7c, 0x65, 0x18, 0x50, 0x7c, 0x84, 0x1a, 0x14, 0x7c, 0x00, 0x28, 0xac,
	0x30, 0xa5, 0x00, 0x80, 0x34, 0x84, 0xff, 0x80, 0x40, 0x80, 0xff, 0xf4,
	0x4c, 0x00, 0x01, 0x2c, 0x4e, 0x80, 0x00, 0x20, 0x3c, 0xa0, 0xff, 0xff,
	0x60, 0xa5, 0xff, 0xf1, 0x7c, 0xa5, 0x18, 0x38, 0x7c, 0x65, 0x18, 0x50,
	0x7c, 0x84, 0x1a, 0x14, 0x7c, 0x00, 0x28, 0x6c, 0x7c, 0x00, 0x04, 0xac,
	0x7c, 0x00, 0x2f, 0xac, 0x30, 0xa5, 0x00, 0x80, 0x34, 0x84, 0xff, 0x80,
	0x40, 0x80, 0xff, 0xec, 0x7c, 0x00, 0x04, 0xac, 0x4c, 0x00, 0x01, 0x2c,
	0x4e, 0x80, 0x00, 0x20, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x05, 0x41, 0x12,
	0x80, 0x00, 0x00, 0x00, 0x01, 0x00, 0x30, 0x78, 0x80, 0x00, 0x00, 0x00,
	0x1c, 0x00, 0x02, 0x48, 0x80, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x8a, 0xd0,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00,
	0x1c, 0x00, 0x03, 0x98, 0x80, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x8a, 0xd0,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00,
	0x1c, 0x00, 0x03, 0xf0, 0x80, 0x00, 0x00, 0x00, 0x1c, 0x00, 0x8a, 0xd0,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x80, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x80, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0d, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x0f, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x13, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x18, 0x00,
	0x21, 0x53, 0x57, 0x49, 0x54, 0x43, 0x48, 0x00, 0x0a, 0x20, 0x20, 0x5f,
	0x5f, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
	0x20, 0x20, 0x20, 0x20, 0x5f, 0x5f, 0x5f, 0x5f, 0x20, 0x20, 0x20, 0x5f,
	0x5f, 0x5f, 0x20, 0x20, 0x20, 0x5f, 0x5f, 0x5f, 0x20, 0x5f, 0x5f, 0x5f,
	0x5f, 0x5f, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x20, 0x2f, 0x20,
	0x5f, 0x7c, 0x5f, 0x20, 0x5f, 0x5f, 0x20, 0x5f, 0x5f, 0x5f, 0x20, 0x20,
	0x5f, 0x5f, 0x5f, 0x7c, 0x20, 0x5f, 0x5f, 0x20, 0x29, 0x20, 0x2f, 0x20,
	0x5f, 0x20, 0x5c, 0x20, 0x2f, 0x20, 0x5f, 0x20, 0x5c, 0x5f, 0x20, 0x20,
	0x20, 0x5f, 0x7c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x7c, 0x20, 0x7c,
	0x5f, 0x7c, 0x20, 0x27, 0x5f, 0x5f, 0x2f, 0x20, 0x5f, 0x20, 0x5c, 0x2f,
	0x20, 0x5f, 0x20, 0x5c, 0x20, 0x20, 0x5f, 0x20, 0x5c, 0x7c, 0x20, 0x7c,
	0x20, 0x7c, 0x20, 0x7c, 0x20, 0x7c, 0x20, 0x7c, 0x20, 0x7c, 0x7c, 0x20,
	0x7c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x7c, 0x20, 0x20,
	0x5f, 0x7c, 0x20, 0x7c, 0x20, 0x7c, 0x20, 0x20, 0x5f, 0x5f, 0x2f, 0x20,
	0x20, 0x5f, 0x5f, 0x2f, 0x20, 0x7c, 0x5f, 0x29, 0x20, 0x7c, 0x20, 0x7c,
	0x5f, 0x7c, 0x20, 0x7c, 0x20, 0x7c, 0x5f, 0x7c, 0x20, 0x7c, 0x7c, 0x20,
	0x7c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x7c, 0x5f, 0x7c,
	0x20, 0x7c, 0x5f, 0x7c, 0x20, 0x20, 0x5c, 0x5f, 0x5f, 0x5f, 0x7c, 0x5c,
	0x5f, 0x5f, 0x5f, 0x7c, 0x5f, 0x5f, 0x5f, 0x5f, 0x2f, 0x20, 0x5c, 0x5f,
	0x5f, 0x5f, 0x2f, 0x20, 0x5c, 0x5f, 0x5f, 0x5f, 0x2f, 0x20, 0x7c, 0x5f,
	0x7c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x20, 0x20, 0x20,
	0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x5b, 0x76,
	0x30, 0x2e, 0x31, 0x30, 0x20, 0x2d, 0x20, 0x69, 0x6e, 0x73, 0x70, 0x69,
	0x72, 0x65, 0x64, 0x20, 0x62, 0x79, 0x20, 0x69, 0x6b, 0x61, 0x72, 0x69,
	0x5d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x62, 0x6f, 0x6f,
	0x74, 0x69, 0x6e, 0x67, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x78, 0x65, 0x6c, 0x6c, 0x2e, 0x2e, 0x2e, 0x2e, 0x0a, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x66, 0x69, 0x72, 0x6d, 0x77, 0x61, 0x72, 0x65,
	0x20, 0x76, 0x2e, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58,
	0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58,
	0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x58, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x61, 0x6c, 0x74, 0x20, 0x66, 0x69, 0x72, 0x6d,
	0x77, 0x61, 0x72, 0x65, 0x00, 0x00, 0x00, 0x00,
};
/* TODO(prototype cast): blCheckHash and blSign are int in xboxrom.c; as
   uint32_t here verifyBlSigs' inlined findFile(11) counts from blCheckHash's 0
   result instead of a new xor (uncprop) */
uint32_t blSignU32(uint8_t *bl, unsigned int len, const void *pubKey, const void *prvKey,
	      const uint8_t *salt) __asm__("_blSign");
uint32_t blCheckHashU32(uint8_t *bl, unsigned int len, const uint8_t *expect) __asm__("_blCheckHash");
/* TODO(prototype cast): image_write.c's imgAdd takes (..., uint8_t type, uint16_t next,
   int pad) and imgAddRaw returns int; build.c's calls compile to the
   original's code only with these types */
int imgAddInt(uint32_t off, const uint8_t *data, uint32_t len, int f3, int ecc, int f5) __asm__("_imgAdd");
void imgAddRawVoid(const char *name, const void *data, uint32_t len, uint32_t off) __asm__("_imgAddRaw");

uint32_t patchSmcConfig(uint8_t *smc);
int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc);

#define SWAP32(x) (((x) << 24) + ((x) >> 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00))
/* folds to a rotate (not the bswap pass's __builtin_bswap16 call), so as a
   call argument it is computed at its store */
#define SWAP16(x) ((uint16_t)(((uint32_t)(x) << 8) | ((uint32_t)(x) >> 8)))
/* an SMC config fan byte */
struct fan {
	uint8_t speed:7, override:1;
};

/* read baseDir/name into e */
static __attribute__((noinline, noclone)) int loadBaseFile(const char *name, struct fileent *e)
{
	if (xb.baseDir[0]) {
		char path[0x400];

		strcpy(path, xb.baseDir);
		strcat(path, name);
		return loadFileCrc(path, e, 1, 0, 0);
	}
	return -1;
}

uint32_t findFileOffset(int type)
{
	int i;

	for (i = 0; i < xb.nFlashFiles; i++)
		if (xb.files[i].type == type)
			return xb.files[i].offset;
	return 0;
}

uint32_t findFileSize(int type)
{
	int i;

	for (i = 0; i < xb.nFlashFiles; i++)
		if (xb.files[i].type == type)
			return xb.files[i].size;
	return 0;
}

int findFile(int type)
{
	int i;

	for (i = 0; i < xb.nFiles; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
}

int loadFileCrc(const char *name, struct fileent *e, int verbose, int pad, uint32_t crc)
{
	FILE *f;
	size_t size;
	uint32_t c;

	f = fopen(name, "rb");
	if (!f)
		return -1;
	if (e->data)
		free(e->data);
	size = getFileSize(f);
	if (!size) {
		fclose(f);
		log_printf(0, "\n******WARNING: '%s' is a 0 byte file, loading skipped!\n", name);
		return 1;
	}
	e->size = size;
	if (pad && (size & 15))
		e->size = (size + 15) & ~15;
	/* hints: the "bytes" log must be hot enough for bb-reorder's second round
	   (build.sh's expect probability, 92-99); the pin sets e's register in the
	   out-of-line copy only (callers with pad == 0 drop this block) */
	if (__builtin_expect(verbose, 1)) {
		if (size != e->size) {
			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
			__asm__("" : : "S"(e));
		} else
			log_printf(1, "reading %s (0x%x bytes)", name, size);
	}
	e->data = calloc(e->size + 0x10000, 1);
	if (!e->data)
		return -2;
	fread(e->data, size, 1, f);
	fclose(f);
	if (crc) {
		c = crc32(e->data, size);
		log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
		if (crc != c) {
			log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", name, c, crc);
			return 1;
		}
	} else
		log_printf(1, "\n");
	return 0;
}

int readMetaFile(const char *name, uint8_t *meta)
{
	FILE *f;

	f = fopen(name, "rb");
	if (!f)
		return -1;
	fread(meta, 4, 1, f);
	fclose(f);
	return 0;
}

/* the build time as a big-endian FAT date and time */
void makeTimestamp(uint8_t *out, FILETIME *ft)
{
	SYSTEMTIME st;
	FILETIME now;
	WORD date, time;

	if (xb.sysTime) {
		GetSystemTime(&st);
		SystemTimeToFileTime(&st, &now);
	} else {
		log_printf(2, "**** using default time!!! ****\n");
		now.dwHighDateTime = 30268127;
		now.dwLowDateTime = 1903825408;
	}
	FileTimeToDosDateTime(&now, &date, &time);
	if (ft)
		DosDateTimeToFileTime(date, time, ft);
	out[0] = date >> 8;
	out[1] = date;
	out[2] = time >> 8;
	out[3] = time;
}

int timestampToFileTime(const uint16_t *ts, FILETIME *ft)
{
	return DosDateTimeToFileTime(SWAP16(ts[0]), SWAP16(ts[1]), ft);
}

/* the same with its timestamp from name.meta if there is one */
int loadBaseFileMeta(const char *name, struct fileent *e, uint8_t *meta)
{
	if (xb.baseDir[0]) {
		char path[0x400];
		int r;

		strcpy(path, xb.baseDir);
		strcat(path, name);
		r = loadFileCrc(path, e, 1, 0, 0);
		if (!r && meta) {
			strcat(path, ".meta");
			if (!readMetaFile(path, meta))
				log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		}
		return r;
	}
	return -1;
}

int loadCommonFile(const char *name, struct fileent *e, int pad, uint32_t crc, uint8_t *meta)
{
	char path[0x400];
	int r;

	strcpy(path, xb.commonDir);
	strcat(path, name);
	r = loadFileCrc(path, e, 1, pad, crc);
	if (!r && meta) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		else
			makeTimestamp(meta, NULL);
	}
	return r;
}

__attribute__((noclone))
int loadInputFile(const char *name, struct fileent *e, int pad, uint32_t crc, uint8_t *meta,
		  int su, int fs, int common)
{
	char path[0x400];
	const char *base;
	uint32_t c;
	uint32_t r;

	base = strrchr(name, '/');
	if (!base)
		base = strrchr(name, '\\');
	if (base)
		base++;
	else
		base = name;
	if (strrchr(name, ':'))
		strcpy(path, name);
	else {
		strcpy(path, xb.dataDir);
		strcat(path, name);
	}
	r = loadFileCrc(path, e, 1, pad, crc);
	if (meta && !r) {
		strcat(path, ".meta");
		if (!readMetaFile(path, meta))
			log_printf(1, "**** %s metadata found, not using system time *****\n\n", path);
		else
			makeTimestamp(meta, NULL);
	}
	if (su && r) {
		if (suGetFile(base, &e->data, &e->size)) {
			log_printf(1, "extracted SUPD/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc != c)
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				else {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				}
			} else
				log_printf(1, "\n");
		}
	}
	if (fs && r) {
		/* scoped: its clobber keeps the fs-path join a real block, so the r = 0
		   paths reach the common test at PRE (threaded late, not by vrp1/dom2) */
		uint32_t ts;

		if (fsGetFile(base, &e->data, &e->size, &ts)) {
			log_printf(1, "extracted nanddump/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc == c) {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				} else {
					free(e->data);
					e->data = NULL;
					e->size = 0;
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				}
			} else
				log_printf(1, "\n");
		} else if (xb.mode == 2 && updateGetFile(base, &e->data, &e->size)) {
			log_printf(1, "extracted USVR/%s (0x%x bytes)", base, e->size);
			if (crc) {
				c = crc32(e->data, e->size);
				log_printf(1, " (crc32: 0x%08x ini: 0x%08x)\n", c, crc);
				if (crc != c) {
					free(e->data);
					e->data = NULL;
					e->size = 0;
					log_printf(0, "\n******WARNING: '%s' crc32: 0x%08x expected: 0x%08x\n", base, c, crc);
				} else {
					if (meta)
						makeTimestamp(meta, NULL);
					r = 0;
				}
			} else {
				log_printf(1, "\n");
				r = 0;
			}
		}
	}
	if (common && r)
		r = loadCommonFile(base, e, pad, crc, meta);
	return r;
}

/* an addon patch from the bin dir */
int loadBinFile(struct fileent *e)
{
	char path[0x400];

	strcpy(path, xb.binDir);
	strcat(path, e->name);
	return loadFileCrc(path, e, 1, 0, 0);
}

/* e->name as given, else from ./ */
int loadLocalFile(struct fileent *e)
{
	char path[0x400];

	strcpy(path, e->name);
	if (!loadFileCrc(path, e, 1, 0, 0))
		return 0;
	strcpy(path, "./");
	strcat(path, e->name);
	return loadFileCrc(path, e, 1, 0, 0);
}

int setFileData(struct fileent *e, const void *data, size_t size)
{
	e->data = calloc(size, 1);
	if (!e->data)
		return 1;
	e->size = size;
	memcpy(e->data, data, size);
	return 0;
}

void appendAddonPatches(struct fileent *e)
{
	uint32_t size = e->size - 4;
	uint8_t *buf = malloc(0x4000);
	uint32_t added = 0;
	struct fileent *a;
	int i;

	memset(buf, 0xff, 0x4000);
	memcpy(buf, e->data, size);
	if (xb.numPatches)
	for (i = 0; i < xb.numPatches; i++) {
		a = &xb.files[19 + i];
		if (!loadBinFile(a)) {
			if (!(a->size & 3)) {
				if (getBeU32(a->data + a->size - 4) == 0xffffffff)
					a->size -= 4;
				if (size + a->size <= 0x4000) {
					memcpy(buf + size, a->data, a->size);
					added += a->size;
					size += a->size;
				} else
					log_printf(0, "\n***** ERROR: could not append %s%s into patches, not enough room!\n\n",
						   xb.binDir, a->name);
			} else
				log_printf(0, "\n***** ERROR: could %s%s size 0x%x is not a multiple of 4, discarding patch data!\n\n",
					   xb.binDir, a->name, a->size);
		} else
			log_printf(0, "\n***** WARNING: could not load addon patch %s%s!\n\n", xb.binDir, a->name);
	}
	*(uint32_t *)(buf + size) = 0xffffffff;
	setBeU32(added, buf + size + 4);
	size += 8;
	if (e->data)
		free(e->data);
	e->data = buf;
	e->size = size;
	if (xb.numPatches)
		log_printf(1, "added 0x%x bytes to patches via %d external patch files\n    patches now 0x%x bytes total with addon byte count appended\n",
			   added, xb.numPatches, size);
}

void showSmcConfig(const uint8_t *smc)
{
	uint32_t av;
	uint16_t game;
	int i;

	log_printf(1, "Target temps: Cpu: %3d\370C Gpu: %3d\370C Edram: %3d\370C\n", smc[0x29], smc[0x2a], smc[0x2b]);
	log_printf(1, "Max temps   : Cpu: %3d\370C Gpu: %3d\370C Edram: %3d\370C\n", smc[0x2c], smc[0x2d], smc[0x2e]);
	log_printf(1, "Cpu Fan     : ");
	if (((struct fan *)(smc + 0x11))->override)
		log_printf(1, "%d%%%% (overridden)\n", ((struct fan *)(smc + 0x11))->speed);
	else
		log_printf(1, "(auto)\n");
	log_printf(1, "Gpu Fan     : ", smc[0x12] & 0x7f);
	if (((struct fan *)(smc + 0x12))->override)
		log_printf(1, "%d%%%% (overridden)\n", ((struct fan *)(smc + 0x12))->speed);
	else
		log_printf(1, "(auto)\n");
	log_printf(1, "MAC Address : ");
	showMac(1, smc + 0x220);
	av = *(uint32_t *)(smc + 0x228);
	av = SWAP32(av);
	switch (av) {
	case 0x100:
		log_printf(1, "\nAVRegion    : 0x%08x (NTSC-M)\n", av);
		break;
	case 0x200:
		log_printf(1, "\nAVRegion    : 0x%08x (NTSC-J)\n", av);
		break;
	case 0x300:
		log_printf(1, "\nAVRegion    : 0x%08x (PAL50)\n", av);
		break;
	case 0x400:
		log_printf(1, "\nAVRegion    : 0x%08x (PAL60)\n", av);
		break;
	default:
		log_printf(1, "\nAVRegion    : 0x%08x (Unknown)\n", av);
		break;
	}
	game = __builtin_bswap16(*(uint16_t *)(smc + 0x22c));
	log_printf(1, "GameRegion  : 0x%04x ", game);
	switch (game) {
	case 0xff:
		log_printf(1, "(NTSC/US)\n");
		break;
	case 0x1fe:
		log_printf(1, "(NTSC/JAP)\n");
		break;
	case 0x1ff:
		log_printf(1, "(NTSC/JAP)\n");
		break;
	case 0x1fc:
		log_printf(1, "(NTSC/KOR)\n");
		break;
	case 0x101:
		log_printf(1, "(NTSC/HK)\n");
		break;
	case 0x2fe:
		log_printf(1, "(PAL/EU)\n");
		break;
	case 0x201:
		log_printf(1, "(PAL/AUS)\n");
		break;
	case 0x7fff:
		log_printf(1, "(DEVKIT)\n");
		break;
	default:
		log_printf(1, "(Unknown)\n");
		break;
	}
	log_printf(1, "DVDRegion   : %d\n", SWAP32(*(uint32_t *)(smc + 0x234)));
	log_printf(1, "resetKey    : ");
	for (i = 0; i < 4; i++)
		log_printf(1, "%c", smc[0x238 + i]);
	log_printf(1, "\n");
}

/* an ini value is used if it is in range; 0 and -1 mean unset */
int iniRangeOk(const char *name, uint32_t v, uint32_t lo, uint32_t hi)
{
	int ok = 1;

	if (v < lo || v > hi) {
		ok = 0;
		if (v != 0 && v != 0xffffffff)
			log_printf(0, "Ini value %d for %s is out of range (%d-%d), not using\n", v, name, lo, hi);
	}
	return ok;
}

static void cb_hint(int *p)
{
	*p = 1;
}

__attribute__((optimize("no-early-inlining")))
uint32_t patchSmcConfig(uint8_t *smc)
{
	uint32_t patched = 0;
	int i, dead;

	log_printf(1, "Checking for smc config data patches\n");
	if (iniRangeOk("cputemp", xb.cpuTemp, 40, 120)) {
		smc[0x29] = xb.cpuTemp;
		patched = 1;
	}
	if (iniRangeOk("gputemp", xb.gpuTemp, 40, 120)) {
		smc[0x2a] = xb.gpuTemp;
		patched = 1;
	}
	if (iniRangeOk("edramtemp", xb.edramTemp, 40, 120)) {
		smc[0x2b] = xb.edramTemp;
		patched = 1;
	}
	if (iniRangeOk("overcputemp", xb.overCpuTemp, 40, 120)) {
		smc[0x2c] = xb.overCpuTemp;
		patched = 1;
	}
	if (iniRangeOk("overgputemp", xb.overGpuTemp, 40, 120)) {
		smc[0x2d] = xb.overGpuTemp;
		patched = 1;
	}
	if (iniRangeOk("overedramtemp", xb.overEdramTemp, 40, 120)) {
		smc[0x2e] = xb.overEdramTemp;
		patched = 1;
	}
	if (xb.cpuFan != 0xffffffff) {
		if (iniRangeOk("cpufan", xb.cpuFan, 40, 100)) {
			cb_hint(&dead);
			smc[0x11] = xb.cpuFan | 0x80;
			patched = 1;
		} else if (xb.cpuFan)
			log_printf(0, "***** WARNING: cpu fan speed %d override ignored, not between 40 and 100\n", xb.cpuFan);
		else if (smc[0x11] != 0x7f) {
			cb_hint(&dead);
			smc[0x11] = 0x7f;
			patched = 1;
		}
	}
	if (xb.gpuFan != 0xffffffff) {
		if (iniRangeOk("gpufan", xb.gpuFan, 40, 100)) {
			cb_hint(&dead);
			smc[0x12] = xb.gpuFan | 0x80;
			patched = 1;
		} else if (xb.gpuFan)
			goto gpuwarn;
		else {
			cb_hint(&dead);
			smc[0x12] = 0x7f;
		}
	}
gpudone:
	if (xb.avRegion != 0xffffffff) {
		*(uint32_t *)(smc + 0x228) = SWAP32(xb.avRegion);
		patched = 1;
	}
	if (xb.gameRegion != 0xffffffff && (uint16_t)xb.gameRegion) {
		*(uint16_t *)(smc + 0x22c) = __builtin_bswap16(xb.gameRegion);
		patched = 1;
	}
	if (xb.dvdRegion != 0xffffffff) {
		*(uint32_t *)(smc + 0x234) = SWAP32(xb.dvdRegion);
		patched = 1;
	}
	if (!*(uint32_t *)(smc + 0x234)) {
		log_printf(0, "****** Warning! SMC config has dvd region as 0, xbox will not play DVD videos like this... forcing it to 1 (NTSC/USA)\n");
		log_printf(0, "       Please set it in boxdata ini file if you require a different region, and run the builder again\n\n");
		*(uint32_t *)(smc + 0x234) = 0x1000000;
		patched = 1;
	}
	if (macidSet())
		for (i = 0; i < 6; i++) {
			if (smc[0x220 + i] != xb.macid[i])
				patched = 1;
			smc[0x220 + i] = xb.macid[i];
		}
	if (patched) {
		uint32_t sum = calcConfigSum(smc);

		*(uint32_t *)smc = SWAP32(sum);
		log_printf(1, "smc config patched!\n");
	} else
		log_printf(1, "smc config was not patched\n");
	log_printf(1, "---------------------\n");
	return patched;
gpuwarn:
	log_printf(0, "***** WARNING: gpu fan speed override setting ignored, not between 40 and 100\n");
	goto gpudone;
}

__attribute__((noinline)) int extractSmcConfig(struct fileent *e, uint8_t *buf, uint32_t size)
{
	uint32_t i, j;
	int found;

	/* hints (wip/README.md): noinline keeps ipa-split off it once it has
	   C callers (loadConsoleBlFiles); &size makes size SSA late (next <= size in
	   both loops); the bound expects make found the rotated exit; the pin
	   puts next/buf in esi/edi; two hot labels on notfound keep the patched
	   block under bb-reorder's duplication threshold */
	(void)&size;
	if (e->data)
		free(e->data);
	e->size = 0x400;
	e->data = malloc(0x400);
	if (!e->data)
		return -2;
	log_printf(1, "-------------------\n");
	log_printf(1, "checking smc_config\n");
	log_printf(1, "-------------------\n");
	found = 0;
	for (i = 0; __builtin_expect(i + 0x200 <= size, 1); i += 0x200) {
		__asm__("" : : "S"(i + 0x200), "D"(buf));
		if ((found = smcConfigOk(buf + i)) == 1)
			break;
	}
	if (!found) {
		for (i = 0; __builtin_expect(i + 0x210 <= size, 1); i += 0x210)
			if ((found = smcConfigOk(buf + i)) == 1)
				break;
		if (!found)
			goto notfound;
	}
	if (checkZeros(buf + i + 0x20c, 4)) {
		log_printf(1, "extracting config\n");
		if (__builtin_expect(size - i >= 0x400, 1)) {
			uint8_t *src = buf + i;

			/* buf live past src: no IRA copy buf-src, so the raw
			   loop's eax doesn't push dst out of eax (wip/README) */
			__asm__("" : "+r"(src) : "r"(buf));
			memcpy(e->data, src, 0x400);
		}
	} else if (size - i >= 0x4200) {
		log_printf(1, "extracting config raw\n");
		for (j = 0; j < 8; j++)
			memcpy(e->data + j * 0x200, buf + i + j * 0x210, 0x200);
	} else {
		log_printf(1, "******* ERROR: extracting config did not work, not enough data to copy!\n");
		return -2;
	}
	if (i)
		log_printf(1, "valid SMC config data found at offset 0x%x\n", i);
	log_printf(1, "------------------\n");
	log_printf(1, "SMC config info:\n");
	log_printf(1, "------------------\n");
	showSmcConfig(e->data);
	log_printf(1, "---------------------\n");
	if (patchSmcConfig(e->data)) {
		log_printf(1, "SMC patched info:\n");
		log_printf(1, "------------------\n");
		showSmcConfig(e->data);
		log_printf(1, "---------------------\n");
	}
	return 0;
notfound: __attribute__((hot));
notfound2: __attribute__((hot));
	log_printf(0, "******* ERROR: unable to find SMC config data!\n");
	return 2;
}

/* the build's kernel version is the highest of its bootloaders' */
void raiseKernel(uint16_t magic, uint16_t build, uint16_t qfe)
{
	uint32_t k = 0x20000000 | build << 8;

	if (k > xb.kernel)
		xb.kernel = k;
}

__attribute__((optimize("no-early-inlining")))
int checkBl(uint8_t *bl, uint32_t size, int type, uint32_t crc)
{
	uint32_t blsize, c;
	int m, dead;

	/* hints (none emit code): the original copies the epilogue into the
	   size-error block, which needs that edge >= 10% of entry, and not into
	   the crc failure one, which needs it below. The hot label and cb_hint
	   (on the other edge) take the size error from 1.7% to 19%, the crc
	   expects (build.sh's probability 98) keep `bad` under 10%, and the "D"
	   pin loads type before the first call as the original does. The
	   SC/SD `crc == -1` expects send more frequency to `bad` by branch
	   (crc32 path), so it is aligned as a loop head like the original
	   (.p2align 4,,10: branch freq > 4 x the B case's fallthru). */
	__asm__("" : : "D"(type));
	/* emits the crc error's literal first, as the original's .rdata */
	__asm__("" :: "i"("\n\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\n"));
	blsize = getBeU32(bl + 12);
	if (blsize > size) {
		size_err: __attribute__((hot));
		log_printf(0, "\n\n***** ERROR: BL size (0x%x) is bigger than the file (0x%x) read in!\n", blsize, size);
		return -3;
	}
	cb_hint(&dead);
	m = bl[0];
	__asm__("" :: "a"(m));
	if ((m & 0x43) != 0x43)
		goto magic;
	switch (type) {
	case 5:
	case 6:
	case 11:
	case 17:
		if (bl[1] != 'B')
			goto magic;
		memset(bl + 0x10, 0, 0x30);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 7:
	case 18:
		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 8:
	case 19:
		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		break;
	case 9:
	case 15:
	case 20:
		if (bl[1] != 'F')
			goto magic;
		memset(bl + 0x20, 0, 0x210);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		raiseKernel(getBeU16(bl), getBeU16(bl + 20), getBeU16(bl + 22));
		break;
	case 10:
	case 16:
	case 21:
		if (bl[1] != 'G')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 12:
		if (bl[1] != 'C')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		if (__builtin_expect(crc == 0xffffffff, 0))
			break;
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 13:
		if (bl[1] != 'D')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		if (__builtin_expect(crc == 0xffffffff, 0))
			break;
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	case 14:
		if (bl[1] != 'E')
			goto magic;
		memset(bl + 0x10, 0, 0x10);
		c = crc32(bl, blsize);
		raiseKernel(getBeU16(bl), getBeU16(bl + 2), getBeU16(bl + 4));
		if (crc == 0xffffffff)
			break;
		c = crc32(bl, blsize);
		if (__builtin_expect(crc != c, 0))
			goto bad;
		break;
	default:
		c = 0;
		goto bad;
	}
	return 0;
bad:
	log_printf(0, "\n\n***** ERROR: BL crc check failed! calculated: %08x expected: %08x\n", c, crc);
	return -2;
magic:
	log_printf(0, "\n\n***** ERROR: BL magic check %c%c for type %d failed!\n", bl[0], bl[1], type);
	return -1;
}

int verifyBlSigs(void)
{
	int ok = 1, sb, sd;
	struct fileent *e;
	uint32_t i;
	const uint8_t *salt;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		switch (e->type) {
		case 5:
		case 11:
		case 17:
			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl))
					log_printf(0, "\n***** ERROR: %s failed signature check!\n", e->name);
				else
					log_printf(1, "%s signature is good\n", e->name);
			} else
				log_printf(1, "could not check signature of %s, 1BL RSA key not present!\n", e->name);
			break;
		case 12:
		case 13:
			sb = findFile(11);
			if (sb) {
				salt = e->type == 12 ? xb.files[sb].data + 904 : xb.files[sb].data + 914;
				if (blVerifySig(e->data, e->size, xb.files[sb].data + 616, salt))
					log_printf(1, "%s signature is good\n", e->name);
				else if (xb.prvKey) {
					if (!memcmp(xb.prvKey, xb.files[sb].data + 616, 0x110)) {
						log_printf(0, "%s failed signature check, attempting to resign\n", e->name);
						if (!blSignU32(e->data, e->size, xb.files[sb].data + 616, xb.prvKey, salt)) {
							log_printf(0, "\n***** ERROR: failed to resign %s!\n", e->name);
							ok = 0;
						} else
							log_printf(1, "%s resigned successfully!\n", e->name);
					} else
						log_printf(0, "\n***** ERROR: %s failed signature check, RSA key provided does not match the pub key in SB!\n", e->name);
				} else
					log_printf(0, "\n***** ERROR: %s failed signature check, RSA key not available for resigning!\n", e->name);
			} else
				log_printf(1, "could not locate SB data to check %s!\n", e->name);
			break;
		case 14:
			sd = findFile(13);
			if (sd) {
				if (!blCheckHashU32(e->data, e->size, xb.files[sd].data + 588)) {
					if (xb.prvKey) {
						sb = findFile(11);
						if (!memcmp(xb.prvKey, xb.files[sb].data + 616, 0x110)) {
							log_printf(0, "%s failed hash check, attempting to correct SE and resign\n", e->name);
							if (!blHashAndSign(e->data, e->size, xb.files[sd].data, xb.files[sd].size,
									   xb.files[sd].data + 588, xb.files[sb].data + 616, xb.prvKey))
								log_printf(0, "\n***** ERROR: failed to resign SE to correct %s hash!\n", e->name);
							else
								log_printf(1, "SE resigned successfully to correct %s hash!\n", e->name);
						} else
							log_printf(0, "\n***** ERROR: %s failed hash check, RSA key provided does not match the pub key in SD!\n", e->name);
					} else
						log_printf(0, "\n***** ERROR: %s failed hash check!\n", e->name);
				} else
					log_printf(1, "%s hash from SE is good\n", e->name);
			} else
				log_printf(1, "\n***** ERROR: could not locate SD data to check %s!\n", e->name);
			break;
		}
	}
	return ok;
}

/* the 0x60-byte bootloader (type 24) from the base dir, else the default */
static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e) || e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		{
		uint8_t *p = e->data;

		__asm__("" : "+r"(p));
		e->size = 0x60;
		memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);
		}
	}
	return 0;
}

/* load the input file e (xb.files[i]) by its type */
static void loadBl(struct fileent *e, uint32_t i, uint32_t *pr)
{
	int type;

	type = e->type;
	switch (type) {
	case 5: case 7: case 8: case 9: case 10: case 11: case 12: case 13:
	case 14: case 15: case 16: case 17: case 18: case 19: case 20: case 21:
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (*pr) {
			if (type == 9) {
				if (!suGetCF(&e->data, &e->size))
					break;
			} else if (__builtin_expect(type == 10, 0)) {
				if (!suGetCG(&e->data, &e->size))
					break;
				goto chk;
			} else
				break;
		}
		if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
			/* an SE where the CF goes */
			e->type = type = 14;
			xb.cfLdv = 0;
			xb.f01c = 1;
		}
	chk:
		*pr = checkBl(e->data, e->size, type, e->crc);
		if (*pr)
			break;
		if (type == 5 || type == 17 || type == 11) {
			if (xb.pub1bl) {
				if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\n***** ERROR: loaded %s, but signature check failed!\n", e->name);
					*pr = -1;
				} else if (type)
					log_printf(1, "loaded %s, signature check passed!\n", e->name);
			} else
				log_printf(1, "loaded %s, could not check signature rsa key not present!\n", e->name);
		}
		/* the expect leaves vrp1's signature-failed copy of this test a
		   >5 edge (else its setFlashBuild copy has frequency 0 and final
		   aligns the type-11 block after it); the hot label keeps the SE
		   copy's <=5 edge the likely one (jbe) */
		if (xb.type <= 5) {
		t5le: __attribute__((hot));
			if (__builtin_expect(*pr != 0, 0))
				goto fail;
			break;
		}
		if (type == 14)
			setFlashBuild(getBeU16(xb.files[i].data + 2));
		break;
	case 6:
		if (!xb.cbb)
			break;
		*pr = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (!*pr) {
			uint32_t r6 = checkBl(e->data, e->size, 6, e->crc);

			__asm__("" : "+r"(r6));
			*pr = r6;
		}
		break;
	case 24:
		if (xb.type == 2 || xb.glitch2mfg)
			*pr = loadBl60(e);
		if (xb.type == 4 || xb.type == 5)
			*pr = loadBl60(e);
		break;
	case 1:
		if (!loadBinFile(e))
			break;
		log_printf(1, "could not read %s%s, using built in payload (0x%x bytes)\n", xb.binDir, e->name, 0x200);
		e->data = malloc(0x200);
		if (!e->data) {
			*pr = 1;
			break;
		}
		e->size = 0x200;
		memcpy(e->data, defPayload, 0x200);
		break;
	case 22:
		if (!loadBinFile(e))
			break;
		log_printf(1, "could not read %s%s, using built in core (0x%x bytes)\n", xb.binDir, e->name, 0xd40);
		e->data = malloc(0xd40);
		if (!e->data) {
			*pr = 1;
			break;
		}
		e->size = 0xd40;
		memcpy(e->data, defCore, 0xd40);
		break;
	case 25:
		if (xb.type == 1 || xb.type > 5)
			break;
		if (!loadBaseFile(e->name, e))
			break;
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\n");
		if (!loadBinFile(e))
			break;
		log_printf(1, "xell not found in firmware /bin folder, checking base path\n");
		*pr = loadLocalFile(e);
		break;
	case 3:
		if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
		    !loadBaseFile("keyvault.bin", &xb.files[xb.nFlashFiles]) ||
		    !(*pr = loadBaseFile("KV_dec.bin", &xb.files[xb.nFlashFiles]))) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
		} else if (xb.kv.data) {
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (e->data)
				free(e->data);
			e->data = xb.kv.data;
			e->size = xb.kv.size;
			xb.kv.data = NULL;
			xb.kv.size = 0;
			*pr = 0;
		}
		break;
	case 4:
		if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
		    !loadBaseFile("keyvault_alt.bin", &xb.files[xb.nFlashFiles]) ||
		    !(*pr = loadBaseFile("KV_alt_dec.bin", &xb.files[xb.nFlashFiles]))) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
		} else if (xb.kvAlt.data) {
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (e->data)
				free(e->data);
			e->data = xb.kvAlt.data;
			e->size = xb.kvAlt.size;
			xb.kvAlt.data = NULL;
			xb.kvAlt.size = 0;
			*pr = 0;
		}
		break;
	case 23:
		if (xb.type == 1)
			break;
		*pr = loadBinFile(e);
		if (*pr)
			break;
		if (e->size & 3) {
		badsize: __attribute__((hot));
			log_printf(1, "\n\n***** ERROR: patch size 0x%x is not a multiple of 4!\n", e->size);
			goto fail;
		}
		appendAddonPatches(e);
		break;
	case 27:
		if (__builtin_expect(type == 27, 1) && loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
		    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
		    (*pr = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
			if (!xb.smcConfig.data)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
			xb.smcConfig.data = NULL;
			xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
			xb.smcConfig.size = 0;
			*pr = 0;
		}
		{
			uint8_t *d = xb.files[xb.nFlashFiles].data;

			__asm__("" : "+a"(d));
			if (d)
				*pr = extractSmcConfig(e, d, xb.files[xb.nFlashFiles].size);
		}
		break;
	case 2:
		*pr = loadBaseFile(e->name, &xb.files[xb.nFlashFiles]);
		if (!*pr) {
			if (e->data)
				free(e->data);
			e->data = xb.files[xb.nFlashFiles].data;
			e->size = xb.files[xb.nFlashFiles].size;
			xb.files[xb.nFlashFiles].data = NULL;
			xb.files[xb.nFlashFiles].size = 0;
		} else {
			if (!xb.smc.data)
				break;
			log_printf(1, "reading %s%s failed, using %s from nand dump\n", xb.baseDir, e->name, e->name);
			if (e->data)
				free(e->data);
			e->data = xb.smc.data;
			e->size = xb.smc.size;
			xb.smc.data = NULL;
			xb.smc.size = 0;
			*pr = 0;
		}
		e->offset = smcSetLoad(e->size);
		if (!e->offset)
			goto fail;
		break;
	default:
		log_printf(1, "####### unhandled bl load %d %s\n", type, e->name);
		/* never taken, but the edge lasts until dom2 resolves
		   __builtin_constant_p: an entry into vrp1's shared checkBl
		   copy whose type isn't a constant, so dom2's jump threads don't
		   scale the type == 11 test's frequency down to 0 (the original
		   places it by a frequency of ~25). The pointer compares set its
		   weight (wip/README.md, build.c, eleventh pass) */
		if ((char *)__builtin_constant_p(i) == (char *)1 && (char *)__builtin_constant_p(type) == (char *)1) {
			type = (type & 1) + 18;
			goto chk;
		}
		break;
	}
	return;
	/* one -1 block for the patch size, SMC and (xb.type <= 5) signature
	   failures: the asm keeps it a block of its own (else the -1 is appended
	   to the size log, which crossjump can't then share) */
fail:
	__asm__ __volatile__("");
	*pr = -1;
}

int loadBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	uint32_t r;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc)
			loadBl(e, i, &r);
		if (r) {
			log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

static inline __attribute__((always_inline)) uint32_t loadConsoleBl(struct fileent *e)
{
	uint32_t r = 0;
	int type;

	type = e->type;
	switch (type) {
	case 5: case 6: case 7: case 8: case 11: case 12: case 13: case 14:
	case 17: case 18: case 19:
		log_printf(1, "skipping %s%s as it is in glitch bootloader dump\n", xb.baseDir, e->name);
		break;
	case 9: case 10: case 15: case 16: case 20: case 21:
		r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
		if (r) {
			if (__builtin_expect(type == 9, 0)) {
				if (suGetCF(&e->data, &e->size))
					r = 0;
			} else if (type == 10) {
				if (suGetCG(&e->data, &e->size))
					r = 0;
			}
			if (r)
				break;
		}
		r = checkBl(e->data, e->size, type, e->crc);
		break;
	case 24:
		if (!xb.glitch2mfg || (!loadBaseFile(e->name, e) && e->size == 0x60))
			break;
		e->data = malloc(0x60);
		if (!e->data) {
			r = 1;
			break;
		}
		{
			uint8_t *p = e->data;

			/* p's points-to unknown: the size store may alias the
			   copy, so sched2 keeps it before the rep movsd setup */
			__asm__("" : "+r"(p));
			e->size = 0x60;
			memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);
		}
		break;
	case 25:
		if (xb.type == 1 || xb.type > 5)
			break;
		if (!loadBaseFile(e->name, e))
			break;
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\n");
		if (!loadBinFile(e))
			break;
		log_printf(1, "xell not found in firmware /bin folder, checking base path\n");
		r = loadLocalFile(e);
		break;
	case 3:
		if (xb.kv.data) {
			log_printf(1, "using keyvault data from console\n");
			if (e->data)
				free(e->data);
			e->data = xb.kv.data;
			e->size = xb.kv.size;
			xb.kv.data = NULL;
			xb.kv.size = 0;
		} else {
			log_printf(0, "\n***** ERROR!: acquiring keyvault data failed!\n");
			r = -1;
		}
		break;
	case 4:
		if (xb.kvAlt.data) {
			log_printf(1, "using keyvault alt data from console\n");
			if (e->data)
				free(e->data);
			e->data = xb.kvAlt.data;
			e->size = xb.kvAlt.size;
			xb.kvAlt.data = NULL;
			xb.kvAlt.size = 0;
		} else {
			log_printf(0, "\n***** ERROR!: acquiring keyvault data failed!\n");
			r = -1;
		}
		break;
	case 23:
		r = loadBinFile(e);
		if (r)
			break;
		if (e->size & 3) {
			log_printf(1, "\n\n***** ERROR: patch size 0x%x is not a multiple of 4!\n", e->size);
			r = -1;
			break;
		}
		appendAddonPatches(e);
		break;
	case 27:
		if (xb.smcConfig.data) {
			log_printf(1, "using smc configuration from console\n");
			if (xb.files[xb.nFlashFiles].data)
				free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
			xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
			xb.smcConfig.data = NULL;
			xb.smcConfig.size = 0;
			r = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
		} else {
			log_printf(0, "\n***** ERROR!: acquiring smc configuration data failed!\n");
			r = -1;
		}
		break;
	case 2:
		/* always false (VRP drops it): makes the smc error a bit colder
		   than the config one, so its trace comes after it */
		if (__builtin_expect(type != 2, 0))
			break;
		if (xb.smc.data) {
			log_printf(1, "using smc binary from console\n");
			if (e->data)
				free(e->data);
			e->data = xb.smc.data;
			e->size = xb.smc.size;
			xb.smc.data = NULL;
			xb.smc.size = 0;
			e->offset = smcSetLoad(e->size);
			if (!e->offset)
				r = -1;
		} else {
			log_printf(0, "\n***** ERROR!: acquiring smc binary data failed!\n");
			r = -1;
		}
		break;
	default:
		log_printf(1, "####### unhandled bl load %d %s\n", type, e->name);
		break;
	}
	return r;
}

int loadConsoleBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	uint32_t r;

	/* the cold label gives the shrink-wrapped return 0 frequency 0, so
	   bb-reorder lays it out last */
	if ((uint32_t)xb.nFiles <= 1)
		goto none;
	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		if (strnicmp(e->name, "none", 4) || e->crc)
			r = loadConsoleBl(e);
		else
			r = 0;
		if (r) {
			log_printf(0, "\n\n**** could not read %s (%i) ****\n\n", e->name, r);
			return -1;
		}
	}
	return 0;
none: __attribute__((cold));
	return 0;
}

/* the header bytes freeboot/xell read: UART speed, power-on reasons */
void patchHeaderOpts(void)
{
	uint8_t opts = 0;

	xb.hdr[0x4b] = 1;
	if (xb.bootFlags & 9) {
		log_printf(1, "\tPatching header for slower demon/cygnos UART speed\n");
		opts = 1;
	}
	if (xb.type == 2) {
		opts |= xb.bootFlags & 7;
		if (xb.bootFlags & 8)
			opts |= 1;
		if (xb.dualButton == xb.xellButton || xb.dualButton == xb.xellAltButton)
			xb.dualButton = 0;
	} else
		xb.dualButton = 0;
	xb.hdr[0x4c] = xb.dualButton;
	xb.hdr[0x4d] = opts;
	log_printf(1, "\tPatching header for xell power reason\n");
	if (xb.xellButton == xb.xellAltButton)
		xb.xellAltButton = 0;
	xb.hdr[0x4f] = xb.xellButton;
	if (xb.xellAltButton)
		log_printf(1, "\tPatching header for xell alt power reason\n");
	xb.hdr[0x4e] = xb.xellAltButton;
}

int blmodMissing(struct fileent *e)
{
	return loadBaseFile("blmod.bin", e) != 0;
}

/* XeCryptRotSumSha, showing the sums */
void rotSumSha(const uint8_t *a, uint32_t alen, const uint8_t *b, uint32_t blen, uint8_t *out, uint32_t outlen)
{
	uint8_t sum[32];
	XECRYPT_SHA_STATE sha;
	uint32_t i;

	for (i = 0; i < 32; i++)
		sum[i] = 0;
	/* TODO(prototype cast): xecrypt.h's inputs aren't const */
	XeCryptRotSum(sum, (uint8_t *)a, alen >> 3);
	log_printf(1, "sum1:");
	display_buffer_hex(sum, 32, 1);
	XeCryptRotSum(sum, (uint8_t *)b, blen >> 3);
	log_printf(1, "sum2:");
	display_buffer_hex(sum, 32, 1);
	XeCryptShaInit(&sha);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, (uint8_t *)a, alen);
	XeCryptShaUpdate(&sha, (uint8_t *)b, blen);
	for (i = 0; i < 32; i++)
		sum[i] = ~sum[i];
	log_printf(1, "sum3:");
	display_buffer_hex(sum, 32, 1);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaUpdate(&sha, sum, 32);
	XeCryptShaFinal(&sha, out, outlen);
	log_printf(1, "fin :");
	display_buffer_hex(out, outlen, 1);
}

int countBits(uint8_t v)
{
	int i, n = 0;

	for (i = 0; i < 8; i++) {
		if (v & 1)
			n++;
		v >>= 1;
	}
	return n;
}

int patchBlsResign(void)
{
	int sb = findFile(11), cd = findFile(7), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, t;
	int n = 0, ok = 0;

	log_printf(1, "Patching BLs...");
	off = 0;
	while (off < p->size) {
		if (n != 2) {
			addr = getBeU32(d + off);
			t = off + 4;
			if (addr != 0xffffffff) {
				len = getBeU32(d + t) * 4;
				off += 8;
				if (n) {
					if (addr + len > xb.files[cd].size) {
						xb.files[cd].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cd].size, xb.files[cd].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cd].data[addr + i] = d[off + i];
				}
				off += len;
			} else {
				n++;
				off = t;
			}
		} else {
			for (i = 0; i < p->size - off; i++)
				p->data[i] = p->data[off + i];
			p->size -= off;
			off = p->size;
		}
	}
	log_printf(1, "Done!\n");
	if (sb) {
		log_printf(1, "Checking patched CD signature...");
		if (!blVerifySig(xb.files[cd].data, xb.files[cd].size, xb.files[sb].data + 616, xb.files[sb].data + 914)) {
			if (xb.prvKey) {
				if (!memcmp(xb.prvKey, xb.files[sb].data + 616, 0x110)) {
					log_printf(0, "%s failed signature check, attempting to resign\n", xb.files[cd].name);
					if (!blSignU32(xb.files[cd].data, xb.files[cd].size, xb.files[sb].data + 616, xb.prvKey, xb.files[sb].data + 914))
						log_printf(0, "\n***** ERROR: failed to resign %s!\n", xb.files[cd].name);
					else {
						log_printf(1, "%s resigned successfully!\n", xb.files[cd].name);
						ok = 1;
					}
				} else
					log_printf(0, "\n***** ERROR: %s failed signature check, RSA key provided does not match the pub key in SB!\n", xb.files[cd].name);
			} else
				log_printf(0, "\n***** ERROR: %s failed signature check, RSA key not available for resigning!\n", xb.files[cd].name);
		} else {
			log_printf(1, "%s signature is good\n", xb.files[cd].name);
			ok = 1;
		}
		if (ok)
			log_printf(1, "Done!\n");
	} else
		log_printf(1, "could not locate SB data to check %s!\n", xb.files[cd].name);
	return ok;
}

__attribute__((optimize("no-early-inlining")))
void patchBlsBlmod(const void *blmod, int size)
{
	int cd = findFile(7), cbb = findFile(6), pt = findFile(23);
	struct fileent *p = &xb.files[pt];
	uint8_t *d = p->data;
	uint32_t off, addr, len, i, max, end, t;
	int n = 0;

	log_printf(1, "Patching BLs...");
	off = 0;
	while (off < p->size) {
		if (n != 2) {
			addr = getBeU32(d + off);
			t = off + 4;
			if (addr != 0xffffffff) {
				len = getBeU32(d + t) * 4;
				off += 8;
				if (!n) {
					if (addr + len > xb.files[cbb].size) {
						xb.files[cbb].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cbb].size, xb.files[cbb].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cbb].data[addr + i] = d[off + i];
				} else {
					if (addr + len > xb.files[cd].size) {
						xb.files[cd].size = (addr + len + 15) & ~15;
						setBeU32(xb.files[cd].size, xb.files[cd].data + 12);
					}
					for (i = 0; i < len; i++)
						xb.files[cd].data[addr + i] = d[off + i];
				}
				off += len;
			} else {
				n++;
				off = t;
			}
		} else {
			for (i = 0; i < p->size - off; i++)
				p->data[i] = p->data[off + i];
			p->size -= off;
			off = p->size;
		}
	}
	if (blmod && size) {
		log_printf(1, "Done!\n");
		if (!xb.cbb)
			cbb = cd;
		max = xb.cbb ? 0xc000 : 0x10000;
		off = getBeU32(xb.files[cbb].data + 12);
		end = (off + size + 15) & ~15;
		if (end > max) {
			size -= end - max;
			log_printf(0, "***** WARNING: blmod.bin is 0x%x bytes too large, truncating to 0x%x bytes!\n", end - max, max - off);
		}
		log_printf(1, "Adding 0x%x bytes blmod.bin data to %s...", size, xb.cbb ? "CBB" : "CD");
		memcpy(xb.files[cbb].data + off, blmod, size);
		end = (off + size + 15) & ~15;
		i = end - xb.files[cbb].size;
		xb.hdr[0x49] = i >> 8;
		xb.hdr[0x4a] = i;
		xb.files[cbb].size = end;
		setBeU32(end, xb.files[cbb].data + 12);
	}
	log_printf(1, "Done!\n");
}

void fixupPatchSet(void)
{
	struct fileent *e = &xb.files[findFile(23)];
	uint8_t *p = e->data;
	uint32_t off, i, v, t;
	int n = 0;

	log_printf(1, "Fixing up patch set...");
	off = 0;
	while (off < e->size) {
		if (n == 2) {
			for (i = 0; i < e->size - off; i++)
				e->data[i] = e->data[off + i];
			e->size -= off;
			off = e->size;
		} else {
			v = getBeU32(p + off);
			t = off + 4;
			if (v != 0xffffffff)
				off += getBeU32(p + t) * 4 + 8;
			else {
				n++;
				off = t;
			}
		}
	}
	log_printf(1, "Done!\n");
}

void addBlsToImage(void)
{
	struct fileent *e;
	int ecc = imgBigBlock() ? 0xf1f1 : 0x1ffb;
	uint32_t i;
	int type, j, off = 0;

	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		type = e->type;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		if (xb.type == 2) {
			if (type == 14) {
				off += e->size;
				continue;
			}
			if (type == 21) {
				j = findFile(20);
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
					   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
				imgAddInt(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
			} else if (type == 10) {
				j = findFile(9);
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
					   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
				imgAddInt(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
			} else {
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
					   e->name, off, e->size, off + e->size);
				imgAddInt(off, e->data, e->size, 0, ecc, 1);
			}
			off += e->size;
			continue;
		}
		if (type == 9)
			off = imgCfOffset();
		else if (type == 23) {
			off = imgCfOffset() + imgCfSize();
			if (xb.glitch2mfg)
				off += 0x60;
			else if (xb.type == 4 || xb.type == 5)
				off += 0x60;
			else
				off += 0x10;
		}
		if (xb.type == 1 && (type == 23 || type == 25)) {
			log_printf(1, "retail image, skipping %s\n", e->name);
			continue;
		} else if (xb.type > 5) {
			if (type == 23 || type == 25) {
				log_printf(1, "devkit/testkit image, skipping %s\n", e->name);
				continue;
			}
		} else if (type == 25 && __builtin_expect(type != 24, 1) && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\n");
			continue;
		}
		if (type != 10 && type != 16 && type != 24)
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
				   e->name, off, e->size, off + e->size);
		if (type == 10) {
			j = findFile(9);
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAddInt(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 16) {
			j = findFile(15);
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAddInt(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 6) {
			if (xb.cbb)
				imgAddInt(off, e->data, e->size, 0, ecc, 1);
		} else if (type == 24) {
			if (xb.glitch2mfg || xb.type == 4 || xb.type == 5) {
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
					   e->name, off, e->size, off + e->size);
				imgAddInt(off, e->data, e->size, 0, ecc, 1);
			}
		} else
			imgAddInt(off, e->data, e->size, 0, ecc, 1);
		off += e->size;
	}
	if (xb.f01c) {
		j = findFile(14);
		log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
			   xb.files[j].name, off, xb.files[j].size, off + xb.files[j].size);
		imgAddInt(off, xb.files[j].data, xb.files[j].size, 0, ecc, 1);
	}
}

/* the bootloader types an update (xeBuild's -u) replaces */
int isUpdateBl(int type)
{
	return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;
}

void addUpdateBls(void)
{
	struct fileent *e;
	int ecc = imgBigBlock() ? 0xf1f1 : 0x1ffb;
	uint32_t i;
	int type, j, off = 0;

	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		type = e->type;
		if (!isUpdateBl(type))
			continue;
		if (e->offset != 0xffffffff)
			off = e->offset;
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		if (type == 9)
			off = imgCfOffset();
		else if (type == 23) {
			off = imgCfOffset() + imgCfSize();
			if (xb.glitch2mfg)
				off += 0x60;
			else
				off += 0x10;
		}
		if (type == 25 && e->offset < imgSize()) {
			log_printf(0, "***** WARNING: skipping xell, there doesn't appear to be enough room!\n");
			continue;
		}
		if (type != 10 && type != 16 && type != 24)
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
				   e->name, off, e->size, off + e->size);
		if (type == 10) {
			j = findFile(9);
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAddInt(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 16) {
			j = findFile(15);
			log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x, rest in fs)\n",
				   e->name, off, e->size, off + e->size - xb.files[j].fsSize);
			imgAddInt(off, e->data, e->size - xb.files[j].fsSize, 0, ecc, 1);
		} else if (type == 24) {
			if (xb.glitch2mfg || xb.type == 4 || xb.type == 5) {
				log_printf(1, "adding %s at raw offset 0x%08x len 0x%x (end 0x%x)\n",
					   e->name, off, e->size, off + e->size);
				imgAddInt(off, e->data, e->size, 0, ecc, 1);
			}
		} else
			imgAddInt(off, e->data, e->size, 0, ecc, 1);
		off += e->size;
	}
}

int logPowerButton(int reason, const char *use)
{
	switch (reason) {
	case 0x11:
		log_printf(1, "    - console power button is being used to %s \n", use);
		break;
	case 0x12:
		log_printf(1, "    - console DVD eject button is being used to %s \n", use);
		break;
	case 0x20:
		log_printf(1, "    - IR remote power button is being used to %s \n", use);
		break;
	case 0x22:
		log_printf(1, "    - IR remote guide/X button is being used to %s \n", use);
		break;
	case 0x24:
		log_printf(1, "    - IR remote windows button is being used to %s \n", use);
		break;
	case 0x41:
		log_printf(1, "    - KIOSK debug pin is being used to %s \n", use);
		break;
	case 0x55:
		log_printf(1, "    - wireless controller powering on console is being used to %s \n", use);
		break;
	case 0x59:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear top usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (INVALID FOR FATS!!) is being used to %s \n", use);
		break;
	case 0x58:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear middle usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (INVALID FOR FATS!!) is being used to %s \n", use);
		break;
	case 0x5a:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (rear bottom usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (rear usb port) is being used to %s \n", use);
		break;
	case 0x56:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (front left usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (front top usb port) is being used to %s \n", use);
		break;
	case 0x57:
		if ((xb.flags & 7) > 4)
			log_printf(1, "wired controller (front right usb port) is being used to %s \n", use);
		else
			log_printf(1, "wired controller (front bottom usb port) is being used to %s \n", use);
		break;
	default:
		return 1;
	}
	return 0;
}

/* freeboot.bin: the kernel version string, boot options and buttons */
void patchFreeboot(uint8_t *buf, int len)
{
	uint32_t opts = xb.bootFlags & 0xf;
	char pat[] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
	uint32_t hold[4];	/* the hold address instructions; [2..3]: 9199's */
	uint32_t *q;
	char *p;

	hold[0] = 0x80;
	hold[1] = 0x78300001;
	log_printf(1, "patching freeboot.bin with with kernel version string '%s'\n", xb.kernelStr);
	log_printf(1, "Boot options set:\n");
	if (opts & 9) {
		log_printf(1, "    - Set debug UART speed to cygnos/demon compatible\n");
		opts = (opts & 6) | 1;
	}
	if (!(opts & 4)) {
		if (opts & 2)
			log_printf(1, "    - Tray has to be fully ejected for Xell to start (old nodvd method)\n");
		else
			log_printf(1, "    - When powered on, if tray is not fully closed Xell starts\n");
	} else {
		if (logPowerButton(xb.xellButton, "start xell")) {
			log_printf(1, "    - UKNOWN POWER REASON, using eject button\n");
			xb.xellButton = 0x12;
		}
		if (xb.xellAltButton == xb.xellButton)
			xb.xellAltButton = 0;
		if (logPowerButton(xb.xellAltButton, "alternately start xell")) {
			log_printf(1, "    - alternate xell button disabled\n");
			xb.xellAltButton = 0;
		}
	}
	if (xb.dualButton == xb.xellButton || xb.dualButton == xb.xellAltButton ||
	    logPowerButton(xb.dualButton, "dual boot"))
		xb.dualButton = 0;
	p = (char *)findInst(buf, len, (uint8_t *)pat, 32);
	if (p) {
		log_printf(2, "org version %s\n", p);
		strncpy(p, xb.kernelStr, 32);
		log_printf(2, "fin version %s\n", p);
	} else
		log_printf(0, "**** ERROR PATCHING FREEBOOT.BIN for kernel version string!\n");
	if (!strncmp(xb.kernelStr, "9199", 4)) {
		hold[2] = 0x80;
		hold[3] = 0xf8ff1f00;
		log_printf(1, "9199 ini string detected, patching to old hold address\n");
		q = (uint32_t *)findInst(buf, len, (uint8_t *)hold, 8);
		if (q)
			memcpy(q, hold + 2, 8);
	}
}

/* payload.bin's `li r4, reps` (copy loop count in words) */
void patchPayloadSize(uint8_t *buf, int len, int size)
{
	int pat = 0xffff8038;	/* li r4, (any) */
	uint8_t *p;
	uint32_t reps = (size + 3) >> 2;

	log_printf(1, "patching payload.bin to load size 0x%x (0x%x reps)\n", size, reps);
	p = findInst(buf, len, (uint8_t *)&pat, 4);
	if (!p)
		return;
	log_printf(2, "org li %r4, %02x%02x\n", p[2], p[3]);
	p[3] = reps;
	p[2] = reps >> 8;
	log_printf(2, "fin li %r4, %02x%02x\n", p[2], p[3]);
}

static int findFileN(int type)
{
	int i, n = xb.nFiles;

	for (i = 0; i < n; i++)
		if (xb.files[i].type == type)
			return i;
	return 0;
}

int encodeBls(uint8_t *salt, int ldv)
{
	struct fileent *e;
	uint32_t i;
	int type, zero, j;

	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		type = e->type;
		if (xb.type == 2) {
			log_printf(1, "encoding %s size 0x%x (JTAG)\n", e->name, e->size);
			switch (type) {
			case 1:
				if (!memcmp(e->data, defPayload, 0x200))
					patchPayloadSize(e->data, e->size, xb.files[findFile(22)].size);
				break;
			case 2:
				if (smcPrepare(e->data, salt, e->size))
					return 1;
				break;
			case 3:
				kvPrepare(e, 0);
				break;
			case 5:
				j = findFile(24);
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), xb.files[j].data, xb.f01c);
				cbaEncrypt(salt, e->data, e->key, e->size, 0);
				break;
			case 7:
				j = findFile(5);
				cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 9:
				j = findFile(10);
				cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
				break;
			case 10:
				j = findFileN(9);
				cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 17:
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				cbaEncrypt2(salt, e->data, e->key, e->size, 1);
				break;
			case 18:
				j = findFile(17);
				cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 19:
				j = findFile(18);
				ceEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 20:
				j = findFile(21);
				ldv += cfEncrypt(e, xb.files[j].size, ldv, 1, imgCfSize());
				break;
			case 21:
				j = findFile(20);
				cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 22:
				if (!memcmp(e->data, defCore, 0xd40))
					patchFreeboot(e->data, e->size);
				else if (xb.bootFlags)
					log_printf(0, "\n******* WARNING: CYGNOS, DEMON and NODVD command line options are ignored due to external freeboot.bin!\n\n");
				break;
			}
		} else if (xb.type > 3) {
			if (type != 24)
				log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			switch (type) {
			case 2:
				if (smcPrepare(e->data, salt, e->size))
					return 1;
				break;
			case 3:
				kvPrepare(e, 0);
				break;
			case 4:
				kvPrepare(e, 1);
				break;
			case 7:
				j = findFile(12);
				cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 8:
				j = findFile(7);
				ceEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 9:
				j = findFile(10);
				cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
				break;
			case 10:
				j = findFile(9);
				cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 11:
				if (xb.type == 4 || xb.type == 5) {
					j = findFile(24);
					if ((xb.flags & 7) > 4)
						showExpectedFuses(0x3000000, getBeU16(e->data + 2), NULL, xb.f01c);
					else
						showExpectedFuses(0x1000000, getBeU16(e->data + 2), NULL, xb.f01c);
					log_printf(1, "zeropairing SB\n");
					setFuseCpuKey(xb.files[j].data);
					cbaEncryptZero(e->data, e->key, e->size);
					break;
				}
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				if (checkZeros(xb.cpuKey, 16)) {
					log_printf(1, "CPU key is all zeros, zeropairing SB\n");
					xb.cfLdv = 0;
					cbaEncryptZero(e->data, e->key, e->size);
				} else
					cbaEncrypt(salt, e->data, e->key, e->size, 0);
				break;
			case 12:
				cdEncryptZero(e->data, e->key, e->size);
				break;
			case 13:
				j = findFile(12);
				cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 14:
				j = findFileN(13);
				ceEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 15:
				j = findFileN(16);
				cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
				break;
			case 16:
				j = findFile(15);
				cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 23:
			case 24:
			case 25:
				break;
			default:
				log_printf(1, "****** Unhandled BL typ %d ******\n", type);
				break;
			}
		} else {
			if (type != 24 || xb.glitch2mfg)
				log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			switch (type) {
			case 2:
				if (smcPrepare(e->data, salt, e->size))
					return 1;
				break;
			case 3:
				kvPrepare(e, 0);
				break;
			case 5:
				if (xb.cbb) {
					cbaEncrypt(salt, e->data, e->key, e->size, 1);
					break;
				}
				showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				if (xb.type != 1)
					cbaEncryptZero(e->data, e->key, e->size);
				else
					cbaEncrypt(salt, e->data, e->key, e->size, 0);
				break;
			case 6:
				if (!xb.cbb)
					break;
				zero = checkZeros(xb.cpuKey, 16);
				j = findFile(24);
				if (xb.glitch2mfg)
					showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), xb.files[j].data, xb.f01c);
				else
					showExpectedFuses(getBeU32(e->data + 944), getBeU16(e->data + 2), NULL, xb.f01c);
				if (zero) {
					log_printf(1, "CPU key is all zeros, zeropairing CB_B\n");
					xb.cfLdv = 0;
				}
				j = findFile(5);
				cbbEncrypt(salt, e->data, xb.files[j].key, xb.files[j].data, e->key, e->size, zero);
				break;
			case 7:
				if (xb.cbb) {
					j = findFile(6);
					cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
				} else {
					j = findFile(5);
					if (xb.type != 1)
						cdEncrypt(e->data, xb.files[j].key, e->key, e->size);
					else
						cdEncryptCpu(e->data, xb.files[j].key, e->key, e->size);
				}
				break;
			case 8:
				j = findFile(7);
				ceEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			case 9:
				j = findFile(10);
				cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
				break;
			case 10:
				j = findFile(9);
				cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
				break;
			}
		}
	}
	if (xb.f01c) {
		/* the SE that replaced the CF follows the CD */
		e = &xb.files[findFile(14)];
		j = findFile(7);
		log_printf(1, "re-encoding %s size 0x%x\n", e->name, e->size);
		ceEncrypt(e->data, xb.files[j].key, e->key, e->size);
	}
	return 0;
}

/* encodeBls for an update image: only the CF and CG */
int encodeUpdateBls(int unused, int ldv)
{
	struct fileent *e;
	uint32_t i;
	int j;

	for (i = 1; i < (uint32_t)xb.nFlashFiles; i++) {
		e = &xb.files[i];
		if (!strnicmp(e->name, "none", 4) && !e->crc)
			continue;
		switch (e->type) {
		case 9:
			log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			j = findFile(10);
			cfEncrypt(e, xb.files[j].size, ldv, 0, imgCfSize());
			break;
		case 10:
			log_printf(1, "encoding %s size 0x%x\n", e->name, e->size);
			j = findFile(9);
			cgEncrypt(e->data, xb.files[j].key, e->key, e->size);
			break;
		}
	}
	return 0;
}

uint32_t calcBlAreaSize(void)
{
	uint32_t size, xs, x;

	if (xb.type == 2) {
		x = findFile(5);
		size = findFileOffset(5) + xb.files[x].size;
		x = findFile(7);
		size += xb.files[x].size;
		if (xb.f01c) {
			x = findFile(14);
			size += xb.files[x].size;
		}
	} else if (xb.type > 5) {
		x = findFile(11);
		size = findFileOffset(11) + xb.files[x].size;
		x = findFile(12);
		size += xb.files[x].size;
		x = findFile(13);
		size += xb.files[x].size;
		x = findFile(14);
		/* the sum so far in ebx (esi up to the 13 lookup), as in the
		   original: IRA otherwise keeps it in esi */
		__asm__("" : "+b"(size));
		size += xb.files[x].size;
		setPatchSlot(size);
		size += 2 * imgCfSize();
	} else {
		size = findFileOffset(5) + findFileSize(5);
		size += findFileSize(6);
		size += findFileSize(7);
		size += findFileSize(8);
		if (xb.type != 1) {
			x = findFile(25);
			if (xb.files[x].offset > size) {
				xs = xb.files[x].size;
				if (xs > 0x40000)
					log_printf(0, "***** WARNING: xell is unexpectedly larger than 256KiB!!\n");
				else
					xs = 0x40000;
				size = xb.files[x].offset + xs;
			}
		}
		size = (size + 0xffff) & ~0xffff;
		setPatchSlot(size);
		size += 2 * imgCfSize();
	}
	if (size & 0x3fff)
		size = (size + 0x3fff) & ~0x3fff;
	return size;
}

/* no blmod.bin: the console's, if any */
static void patchConsoleBlmod(void)
{
	if (!xb.consoleBlmod.data || !xb.consoleBlmod.size) {
		patchBlsBlmod(NULL, 0);
		return;
	}
	patchBlsBlmod(xb.consoleBlmod.data, xb.consoleBlmod.size);
	free(xb.consoleBlmod.data);
}

int buildFlash(void)
{
	uint8_t salt[16];
	uint32_t ts;
	FILETIME ft;
	const char *name, *base;
	uint32_t area, off, raw, save, a, b, k, crc, len, end;
	int fuse, blocks, r, cf, cg, region, i;
	uint16_t t;
	char last;

	memset(salt, 0, sizeof(salt));
	fuse = 1;
	if (xb.type != 2) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == 4 || xb.type == 5, 0))
			fuse = 1;
	}
	if (!xb.fromConsole) {
		log_printf(1, "Writing initial header to flash image\n");
		writeInitialHeader();
	} else {
		log_printf(1, "\n------ Copying bootloader image to flash image ------ \n");
		r = checkBootImage(1);
		if (r) {
			log_printf(0, "******* ERROR: bootloaders retrieved from console are inconsistent, cannot proceed!\n\n");
			return r;
		}
	}
	suLoadDir(xb.dataDir);
	log_printf(1, "\n------ Loading bootloaders and required security files ------\n");
	if (xb.fromConsole)
		r = loadConsoleBlFiles();
	else
		r = loadBlFiles();
	if (r) {
		log_printf(0, "******* ERROR: critical bootloader files are missing, cannot proceed!\n\n");
		return r;
	}
	if (!xb.fromConsole && !verifyBlSigs())
		return 1;
	log_printf(1, "done!\n");
	blocks = fsStartBlock();
	area = calcBlAreaSize();
	if (!blocks)
		blocks = area >> 14;
	else
		area = blocks << 14;
	if (xb.type == 3) {
		log_printf(1, "\n------ Patching BLs and modifying patches ------\n");
		if (xb.fromConsole)
			fixupPatchSet();
		else {
			struct fileent f;

			memset(&f, 0, sizeof(f));
			if (!loadBaseFile("blmod.bin", &f)) {
				patchBlsBlmod(f.data, f.size);
				free(f.data);
			} else
				patchConsoleBlmod();
		}
	} else if (xb.type == 4 || xb.type == 5) {
		log_printf(1, "\n------ Patching BLs and modifying patches ------\n");
		if (!patchBlsResign())
			return 1;
	}
	if (!xb.fromConsole && !(xb.type == 1 || xb.type > 5)) {
		log_printf(1, "\n------ Patching boot reasons and options into flash header ------\n");
		patchHeaderOpts();
	}
	log_printf(1, "\n------ Encrypting and finalizing bootloaders ------\n");
	keysInit(xb.randomKeys);
	if (fuse) {
		struct fileent *e = &xb.files[findFile(24)];
		setFuseCpuKey(e->data);
		if (xb.type != 2)
			e->offset = imgCfOffset() + imgCfSize();
	}
	if (!xb.fromConsole) {
		if (encodeBls(salt, blocks))
			return -4;
	} else if (encodeUpdateBls((int)salt, blocks))
		return -4;
	if (fuse)
		showFuses(1, "\nVirtual Fuses set to:", xb.files[findFile(24)].data);
	log_printf(1, "done!\n\n------ Adding bootloaders to flash image ------\n");
	if (!xb.fromConsole)
		addBlsToImage();
	else
		addUpdateBls();
	if (!fsStartBlock()) {
		log_printf(1, "Fixing up FS table...");
		fixupFsTable(area);
		imgSetSize(area);
		log_printf(1, "done!\n");
	}
	if (fsStartBlock())
		imgSetSize(fsStartBlock() << 14);

	/* the CG's patch slot overflow goes in the filesystem */
	if (xb.type != 2) {
		if (xb.files[findFile(9)].fsSize) {
			off = imgSize();
			cf = findFile(9);
			cg = findFile(10);
			log_printf(1, "Writing zeropair CG patch slot overflow data to sysupdate.xexp1\n");
			log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
			makeTimestamp((uint8_t *)&ts, NULL);
			imgAddFile("sysupdate.xexp1", xb.files[cg].data + xb.files[cf].fsOffset, &ts, xb.files[cf].fsSize);
			log_printf(1, "done!\n");
		}
	} else {
		off = imgSize();
		if (xb.files[findFile(20)].fsSize) {
			cf = findFile(20);
			cg = findFile(21);
			log_printf(1, "Writing CG patch slot overflow data to sysupdate.xexp1\n");
			log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
			makeTimestamp((uint8_t *)&ts, NULL);
			imgAddFile("sysupdate.xexp1", xb.files[cg].data + xb.files[cf].fsOffset, &ts, xb.files[cf].fsSize);
			log_printf(1, "done!\n");
		}
		if (xb.files[findFile(9)].fsSize) {
			cf = findFile(9);
			cg = findFile(10);
			log_printf(1, "Writing target CG patch slot overflow data to sysupdate.xexp2\n");
			log_printf(1, "\tat raw offset 0x%x len 0x%08x (end: 0x%08x)...", off, xb.files[cf].fsSize, off + xb.files[cf].fsSize);
			makeTimestamp((uint8_t *)&ts, NULL);
			imgAddFile("sysupdate.xexp2", xb.files[cg].data + xb.files[cf].fsOffset, &ts, xb.files[cf].fsSize);
			log_printf(1, "done!\n");
		}
	}

	log_printf(1, "\n------ adding %d firmware files ------\n", xb.nFirmware);
	for (i = 0; i < xb.nFirmware; i++) {
		struct fileent f;

		strcpy(f.name, xb.firmware[i]);
		last = f.name[strlen(f.name) - 1];
		if (!strnicmp("sysupdate.xexp", f.name, 14)) {
			log_printf(1, "\n******* WARNING: firmware file %s ignored, 'sysupdate.xexp' is a reserved name!\n\n", f.name);
			continue;
		}
		if (!xb.firmwareCrc[i])
			r = loadInputFile(f.name, &xb.files[xb.nFlashFiles], 0, 0, (uint8_t *)&ts, 0, 1, 0);
		else {
			/* a patch (.xexp): the target's comes as .xexp1, a JTAG's as .xexp2 */
			if (last == 'p') {
				if (xb.type == 2)
					strcat(xb.firmware[i], "2");
				else
					strcat(xb.firmware[i], "1");
			}
			r = loadInputFile(f.name, &xb.files[xb.nFlashFiles], 0, xb.firmwareCrc[i], (uint8_t *)&ts, 1, 1, 1);
			if (r && last == 'p') {
				strcat(f.name, "1");
				r = loadInputFile(f.name, &xb.files[xb.nFlashFiles], 0, xb.firmwareCrc[i], (uint8_t *)&ts, 0, 1, 1);
				if (r) {
					f.name[strlen(f.name) - 1] = '2';
					r = loadInputFile(f.name, &xb.files[xb.nFlashFiles], 0, xb.firmwareCrc[i], (uint8_t *)&ts, 0, 1, 1);
				}
			}
		}
		if (!r) {
			base = strrchr(xb.firmware[i], '/');
			if (!base)
				base = strrchr(xb.firmware[i], '\\');
			if (base)
				base++;
			else
				base = xb.firmware[i];
			off = imgSize();
			len = xb.files[xb.nFlashFiles].size;
			log_printf(1, "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n", base, off, len, off + len);
			imgAddFile(base, xb.files[xb.nFlashFiles].data, &ts, len);
		} else if (!xb.firmwareCrc[i])
			log_printf(1, "***** could not read file '%s', skipping *****\n", xb.firmware[i]);
		else {
			log_printf(0, "***** could not read file '%s' *****\n", xb.firmware[i]);
			log_printf(0, "\n******* ERROR: critical firmware file missing, cannot proceed!\n\n");
			return r;
		}
	}

	log_printf(1, "\n------ adding %d security files ------\n", xb.nFlashFiles2);
	for (k = 0; k < xb.nFlashFiles2; k++) {
		int found = 1;

		memset(&xb.files[xb.nFlashFiles], 0, sizeof(struct fileent));
		setBeU32(0, (uint8_t *)&ts);
		if (k)
			log_printf(1, "\n");
		name = xb.flashFiles[k];
		log_printf(1, "<- Processing %s ->\n", name);
		if (loadBaseFileMeta(name, &xb.files[xb.nFlashFiles], (uint8_t *)&ts)) {
			found = 0;
			if (!(xb.bootFlags & 0x1000000)) {
				if (xb.files[xb.nFlashFiles].data)
					free(xb.files[xb.nFlashFiles].data);
				if (suGetFile(name, &xb.files[xb.nFlashFiles].data, &xb.files[xb.nFlashFiles].size)) {
					log_printf(1, "\tcould not read %s, using data from SUPD...\n", name);
					found = 1;
				}
			}
			if (!found) {
				if (xb.flashBuf[k]) {
					if (xb.files[xb.nFlashFiles].data)
						free(xb.files[xb.nFlashFiles].data);
					xb.files[xb.nFlashFiles].data = xb.flashBuf[k];
					xb.files[xb.nFlashFiles].size = xb.flashSize[k];
					log_printf(1, "\tcould not read %s, using data from previous parse...\n", name);
					found = 1;
				} else if (!strcmp(name, "secdata.bin") || !strcmp(name, "extended.bin")) {
					xb.files[xb.nFlashFiles].size = 0;
					found = 1;
				}
			}
		}
		if (found) {
			if (!getBeU32((uint8_t *)&ts))
				makeTimestamp((uint8_t *)&ts, &ft);
			else
				timestampToFileTime((uint16_t *)&ts, &ft);
			if (!strcmp(name, "secdata.bin"))
				secdataPrepare(&xb.files[xb.nFlashFiles], (uint8_t *)&ft);
			else if (!strcmp(name, "extended.bin"))
				extendedPrepare(&xb.files[xb.nFlashFiles]);
			else if (!strcmp(name, "dae.bin"))
				daeEncrypt(xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size, (uint8_t *)&ft);
			else if (!strcmp(name, "crl.bin"))
				crlEncrypt(xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size, (uint8_t *)&ft);
			else if (!strcmp(name, "fcrt.bin"))
				fcrtEncrypt(xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
			else if (!strcmp(name, "odd.bin")) {
				if (xb.flashTime[k])
					setBeU32(xb.flashTime[k], (uint8_t *)&ts);
			} else
				log_printf(0, "******* WARNING: writing %s%s as-is to NAND, if .meta was not included it may be invalid!\n", xb.baseDir, name);
			imgAddFileAs(name, xb.files[xb.nFlashFiles].data, &ts, xb.files[xb.nFlashFiles].size);
		} else if (!strcmp(name, "fcrt.bin")) {
			region = kvGetGameRegion();
			if (region) {
				log_printf(0, "\n\n***** ERROR: %s not found, keyvault has this file flagged as required but it's being skipped *****\n", name);
				if (xb.type != 1 && xb.type <= 5) {
					if (region == 1)
						log_printf(0, "             note - on hacked images a nofcrt patch should allow the drive and machine to function\n");
					else {
						log_printf(0, "             note - on hacked images a nofcrt patch WILL NOT allow the drive to function\n");
						log_printf(0, "             but should allow the machine to boot normally\n");
					}
				}
			} else
				log_printf(1, "\t%s not found and not required by keyvault, skipped\n", name);
		} else
			log_printf(0, "***** WARNING: %s not found, skipping *****\n", name);
		if (xb.files[xb.nFlashFiles].data) {
			free(xb.files[xb.nFlashFiles].data);
			xb.files[xb.nFlashFiles].data = NULL;
		}
	}

	log_printf(1, "\n------ checking for Mobile*.dat ------\n");
	for (k = 0; k < 11; k++) {
		struct fileent f;

		switch (k) {
		case 9:
			strcpy(f.name, "Statistics.settings");
			raw = statisticsOffset(xb.bigBlock, xb.type > 5, (xb.flags & 0x10000000) != 0, NULL, NULL);
			break;
		case 10:
			strcpy(f.name, "Manufacturing.data");
			raw = manufacturingOffset(xb.bigBlock, xb.type > 5, (xb.flags & 0x10000000) != 0, NULL, NULL);
			break;
		default:
			strcpy(f.name, "MobileA.dat");
			f.name[6] = 'B' + k;
			raw = 0;
		}
		if (!loadBaseFile(f.name, &xb.files[xb.nFlashFiles])) {
			log_printf(1, "%s found, adding from file\n", f.name, xb.files[xb.nFlashFiles].size, '1' + k);
			if (raw) {
				save = imgSize();
				imgAddRawVoid(f.name, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size, raw);
				imgSetSize(save);
			} else {
				t = imgAddMobile(xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size, '1' + k);
				if (t && k <= 8) {
					setBeU16(t, (uint8_t *)&xb.mobileTab[k].type);
					setBeU16(xb.files[xb.nFlashFiles].size >= 0x4000 ? 0 : xb.files[xb.nFlashFiles].size, (uint8_t *)&xb.mobileTab[k].size);
				}
			}
		} else if (xb.mobile[k].data && xb.mobile[k].size) {
			log_printf(1, "%s found, adding from previous parse\n", f.name);
			if (raw) {
				save = imgSize();
				imgAddRawVoid(f.name, xb.mobile[k].data, xb.mobile[k].size, raw);
				imgSetSize(save);
			} else {
				t = imgAddMobile(xb.mobile[k].data, xb.mobile[k].size, '1' + k);
				if (t && k <= 8) {
					setBeU16(t, (uint8_t *)&xb.mobileTab[k].type);
					setBeU16(xb.mobile[k].size > 0x3fff ? 0 : xb.mobile[k].size, (uint8_t *)&xb.mobileTab[k].size);
				}
			}
		}
	}
	a = imgSizeAligned();
	b = imgSizeAligned();
	log_printf(1, "\n------ adding smc_config.bin ------\n");
	{
		struct fileent *e = &xb.files[findFile(27)];
		addSmcConfig(e->data, e->size);
	}
	log_printf(1, "\n------ cleaning up image ------\n");
	log_printf(1, "Fixing up empty FS block entries...");
	fixupEmptyFsBlocks(a);
	log_printf(1, "done!\nWriting FS table to image ");
	writeFsTable(b);
	log_printf(1, "done!\n");
	if (xb.flags & 0x10000000) {
		/* MMC: two anchor blocks */
		xb.anchorNum = 1;
		shaHeader(xb.anchor);
		copyAnchorBlock(1);
		xb.anchorNum = 2;
		shaHeader(xb.anchor);
		copyAnchorBlock(2);
	}
	for (k = 0; k < 19; k++) {
		if (xb.files[k].data && xb.files[k].size)
			free(xb.files[k].data);
		xb.files[k].size = 0;
	}
	if (xb.nRawPatches) {
		struct fileent f;

		log_printf(1, "\n------ adding [rawpatch] data ------\n");
		f.data = NULL;
		for (k = 0; k < xb.nRawPatches; k++) {
			r = loadInputFile(xb.rawPatch[k].name, &f, 0, 0, (uint8_t *)&ts, 0, 0, 0);
			if (!r) {
				off = xb.rawPatch[k].offset;
				end = off + f.size;
				if (end <= xb.userSize) {
					memcpy(xb.hdr + off, f.data, f.size);
					log_printf(1, "[rawpatch] (%d): '%s' copied to offset 0x%x len: 0x%x (end: 0x%x) successfully!\n\n",
						   k + 1, xb.rawPatch[k].name, off, f.size, end);
					free(f.data);
					f.data = NULL;
				} else {
					log_printf(1, "[rawpatch] (%d): '%s' copied to offset 0x%x (len: 0x%x) would exceed user size 0x%x!\n\n",
						   k + 1, xb.rawPatch[k].name, off, f.size, xb.userSize);
					free(f.data);
					return -1;
				}
			} else {
				log_printf(0, "***** ERROR: could not load [rawpatch] file '%s'!!\n", xb.rawPatch[k].name);
				return r;
			}
		}
		log_printf(1, "done!\n");
	}
	log_printf(1, "\n------ finalizing image ------\n");
	return finalizeImage();
}
