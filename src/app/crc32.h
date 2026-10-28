/* crc32.h: crc32.c's functions that other objects use */
#ifndef CRC32_H
#define CRC32_H

#include "xebuild.h"

unsigned int crc32(const unsigned char *buf, unsigned int len);

#endif
