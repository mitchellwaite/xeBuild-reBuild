/* mode_client: `xeBuild client`, single commands against a console over the network */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "xebuild.h"
#include "console_hdd.h"
#include "consoleinfo.h"
#include "fileutil.h"
#include "image_write.h"
#include "log.h"
#include "main.h"
#include "mode_client.h"
#include "net.h"

/* client_usage's errors (ERR_NONE: -? asked for the usage) */
#define ERR_NONE 0
#define ERR_UNKNOWN 1			/* an unknown option */
#define ERR_NO_COMMAND 2
#define ERR_NO_ARG 3
#define ERR_ARGS 4			/* too few arguments */
#define ERR_TWICE 5			/* a second command */

/* the console's hack type, for -p's patches */
#define PATCHES_JTAG 1
#define PATCHES_GLITCH 2		/* glitch and glitch2 */
#define PATCHES_GLITCH2M 3

/* mode_client's commands */
#define CMD_READ 1			/* -r */
#define CMD_WRITE 2			/* -w */
#define CMD_KEYS 3			/* -keys */
#define CMD_AVATAR 4			/* -e */
#define CMD_COMPAT 5			/* -c */
#define CMD_NONE 6			/* -s or -reboot alone */
#define CMD_PATCHES 7			/* -p */
#define CMD_READ_BLOCKS 8		/* -rb */
#define CMD_WRITE_BLOCKS 9		/* -wb */
#define CMD_ERASE_BLOCK 10		/* -eb */
#define CMD_BIN_PATCH 11		/* -bp */
#define CMD_INFO 12			/* -i */

static struct consoleinfo *cinfo;

void client_usage(int err, const char *arg)
{
	switch (err)
	{
	case ERR_NO_ARG:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line but no argument provided!\n", arg);
		break;
	case ERR_ARGS:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n", arg);
		break;
	case ERR_TWICE:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line but option was already set!\n", arg);
		break;
	case ERR_UNKNOWN:
		log_printf(0, "\n\n***** ERROR: unknown option '%s' provided on command line!\n", arg);
		break;
	case ERR_NO_COMMAND:
		log_printf(0, "\n\n***** ERROR: not enough info provided to carry out command!\n");
		break;
	}
	log_printf(0, separator);
	log_printf(0, "Usage   :\n   %s client <switch> [<option>]\n\n", "xeBuild");
	log_printf(0, "Examples:\n");
	log_printf(0, "   %s client -r nanddump.bin\n", "xeBuild");
	log_printf(0, "   %s client -w nandflash.bin -ip 192.168.2.100\n", "xeBuild");
	log_printf(0, "\nSwitches:\n");
	log_printf(0, "   -i             : connects to console and shows some info about it\n");
	log_printf(0, "*  -i <d>         : collects console information into folder <d>, usually enough for build mode\n");
	log_printf(0, "   -r <f>         : dumps system area of NAND to <f>\n");
	log_printf(0, "   -w <f>         : writes system area of NAND from <f>\n");
	log_printf(0, "   -e <d>         : format partition and send avatar/kinect data to HDD from <d>, must match running kernel\n");
	log_printf(0, "   -c <d>         : format partition and send xbox compatibility data to HDD from <d>\n");
	log_printf(0, "   -p             : will attempt to automatically update patches based on running kernel version\n");
	log_printf(0, "   -p <f>         : update patches with <f>\n");
	log_printf(0, "   -rb <f> <b> <l>: read series of blocks starting at <b> for <l>\n");
	log_printf(0, "   -wb <f> <b>    : write series of blocks starting at <b> for the number of blocks in <f>\n");
	log_printf(0, "   -eb <b>        : attempt to erase a single block, even if marked bad on console\n");
	log_printf(0, "   -bp <f> <o>    : binary patch NAND with contents of <f> to logical offset <o>\n");
	log_printf(0, "*  -keys          : will attempt to dump RSA and 1BL keys from console\n");
	log_printf(0, "   -s             : shutdown console\n");
	log_printf(0, "   -ip <add>      : force attempt to connect to addr (ie: -i 192.168.0.100)\n");
	log_printf(0, "   -noenter       : suppresses prompt for enter key when finished\n");
	log_printf(0, "   -reboot        : causes the console to hard reboot\n");
	log_printf(0, "   -v             : shows more info during client process\n");
	log_printf(0, "   -?             : shows this help\n\n");
	log_printf(0, "legend:\n");
	log_printf(0, "<add>    = without this option network will be scanned for server broadcast beacon\n");
	log_printf(0, "           If provided the correct format is an IPv4 address like 192.168.0.100\n");
	log_printf(0, "<f>      = path, absolute or relative, to a file\n");
	log_printf(0, "<d>      = path, absolute or relative, to a directory - do not terminate with /\n");
	log_printf(0, "<b>      = hexadecimal block number\n");
	log_printf(0, "<l>      = hexadecimal number of blocks\n");
	log_printf(0, "<o>      = hexadecimal logical offset (spare data not considered) in flash\n");
	log_printf(0, "notes:\n");
	log_printf(0, "* functions not fully supported with older patch versions, use with caution.\n");
	log_printf(0, "- client mode tends to operate on a single command basis, stacking commands.\n");
	log_printf(0, "  is not possible with the exception of v, noenter, ip, s and reboot.\n");
	log_printf(0, "- patch update (-p) will retain any addon patches already on the console.\n");
	log_printf(0, separator);
	log_finish();
	if (promptEnter)
	{
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	exit(1);
}

/* -i [<d>]: console info, bad blocks; with <d> also the info files and a NAND dump */
void clientInfo(const char *dir)
{
	char path[1024];
	const char *out = NULL;
	int len;
	uint8_t *bad;
	int i;

	if (dir)
	{
		log_printf(0, "creating mydata folder output at %s\n", dir);
		if (createDir(dir))
		{
			out = dir;
		}
		else
		{
			log_printf(0, "unable to dump details to %s, disabling\n", dir);
		}
	}
	parseConsoleInfo(0, out, out, NULL);
	bad = netGetBadBlocks(&len);
	if (bad && len)
	{
		log_printf(0, "Bad Block list  : ");
		for (i = len - 2; i >= 0; i -= 2)
		{
			log_printf(0, "0x%x", getBeU16(bad + i));
			if (i)
			{
				log_printf(0, ",");
			}
		}
	}
	if (out)
	{
		strcpy(path, dir);
		strcat(path, "/nanddump.bin");
		log_printf(0, "dumping console flash to %s\n", path);
		if (netDumpNand(path))
		{
			log_printf(0, "success!\n");
		}
		else
		{
			log_printf(0, "failed!\n");
		}
		return;
	}
}

/* -w <f> */
int clientWrite(const char *file)
{
	size_t len;
	uint8_t *buf;
	int ret = 0;

	netTimerStart();
	log_printf(0, "reading file %s...", file);
	buf = FileToBuffer(file, &len);
	if (buf)
	{
		log_printf(0, "success, read 0x%x bytes\n", len);
		if (getBeU16(buf) == FLASH_MAGIC)
		{
			if (cinfo->nandSize == len)
			{
				log_printf(0, "sending data to console...\n");
				ret = netSendFlash(buf, len);
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: file size should be 0x%x but its 0x%x bytes! Aborted!\n", cinfo->nandSize, len);
			}
		}
		else
		{
			log_printf(0, "\n\n***** ERROR: image magic should be 0xFF4F but its 0x%x! Aborted!\n", getBeU16(buf));
		}
		free(buf);
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: unable to read file to send\n");
	}
	return ret;
}

void clientManifest(const char *dir)
{
	int i;

	if (!loadManifest(dir, cinfo->kernel & ~0xf))
	{
		return;
	}
	for (i = 0; i < consoleManifest.count; i++)
	{
		log_printf(1, "item %03d: %08x %08x %s\n", i + 1, consoleManifest.e[i].len, consoleManifest.e[i].data, consoleManifest.e[i].path);
	}
	log_printf(1, "manifest, %08x %08x %s\n", consoleManifest.size, consoleManifest.size, consoleManifest.path);
	freeManifest();
}

int dumpKey(const char *name, const char *file, const uint8_t *key, size_t len, uint32_t sum)
{
	uint32_t want = sum;
	int ret = 0;

	log_printf(0, "checking %s (file ./%s)\n", name, file);
	if (FileExists(file))
	{
		FileToBuffer(file, &len);
	}
	if (sumBytes(key, len) == want)
	{
		log_printf(0, "dumping valid %s to file ./%s\n", name, file);
		if (len == 16)
		{
			ret = writeKeyFile("./", file, key);
		}
		else
		{
			ret = writeFileIn("./", file, key, len);
		}
	}
	if (!ret)
	{
		log_printf(0, "\n\n****** ERROR: unable to dump %s to file ./%s, key is not valid or file is inaccessible!\n", name, file);
	}
	return ret;
}

/* -keys */
void clientKeys(void)
{
	if ((uint8_t)cinfo->version > 1)
	{
		dumpKey("1BL key", "1blkey.txt", cinfo->key1bl, sizeof cinfo->key1bl, KEY1BL_SUM);
		dumpKey("1BL RSA pub key", "1BL_pub.bin", (const uint8_t *)&cinfo->pub1bl, sizeof cinfo->pub1bl, PUB1BL_SUM);
		dumpKey("PIRS RSA pub key", "PIRS_pub.bin", (const uint8_t *)&cinfo->pubPirs, sizeof cinfo->pubPirs, PUBPIRS_SUM);
		dumpKey("MASTER RSA pub key", "MAST_pub.bin", (const uint8_t *)&cinfo->pubMaster, sizeof cinfo->pubMaster, PUBMASTER_SUM);
	}
	else
	{
		log_printf(0, "\n\n****** ERROR: console patches need to be updated to support this operation!\n");
	}
}

/* patches are sections separated by 0xffffffff: JTAG has 4, glitch 3 and
   loses the first (glitch2 keeps 16 bytes of 0xff in its place) */
int checkPatches(uint8_t *buf, size_t *len, uint32_t type)
{
	uint32_t marker = PATCHES_END;
	uint8_t *p;
	size_t n, i, off;

	if (type > PATCHES_JTAG)
	{
		log_printf(0, "checking patch sections for glitch console\n");
		if (countInst(buf, *len, &marker, 4) == 3)
		{
			p = findInst(buf, *len, &marker, 4);
			if (p)
			{
				p = findInst(p + 4, *len - (p - buf), &marker, 4);
				if (p)
				{
					p += 4;
					n = *len - (p - buf);
					off = 0;
					if (type == PATCHES_GLITCH)
					{
						off = 16;
					}
					for (i = 0; i < n; i++)
					{
						buf[off + i] = p[i];
					}
					if (off)
					{
						memset(buf, 0xff, off);
					}
					*len = n + off;
					return 1;
				}
			}
		}
		else
		{
			log_printf(0, "\n\n***** ERROR: patches do not contain all segments, aborting!\n");
		}
		return 0;
	}
	n = countInst(buf, *len, &marker, 4);
	log_printf(0, "checking patch sections for JTAG console\n");
	if (n == 4)
	{
		return 1;
	}
	log_printf(0, "\n\n***** ERROR: patches do not contain all segments, counted %d - aborting!\n", n);
	return 0;
}

void updatePatches(const char *file, uint32_t type)
{
	size_t len;
	int cur;
	uint8_t *buf, *patches;
	int same;

	buf = FileToBuffer(file, &len);
	if (buf)
	{
		if (len)
		{
			log_printf(0, "loaded %s size 0x%x (%d) bytes\n", file, (int)len, (int)len);
			if (checkPatches(buf, &len, type))
			{
				log_printf(0, "retrieving patches from console...");
				patches = netGetFile("patches", &cur);
				if (patches)
				{
					log_printf(1, "success! received 0x%x (%d) bytes\n", cur, cur);
					same = 0;
					if (len == cur && !memcmp(buf, patches, len))
					{
						same = 1;
					}
					if (!same)
					{
						log_printf(0, "sending update patches to console...");
						if (netWritePatches(buf, len))
						{
							log_printf(0, "patches updated OK!\n");
						}
						else
						{
							log_printf(0, "\n\n***** ERROR: patch update failed!\n");
						}
					}
					else
					{
						log_printf(0, "patches are already up to date!\n");
					}
				}
				else
				{
					log_printf(0, "\n\n***** ERROR: failed to retrieve current patches from console!\n");
				}
			}
		}
		else
		{
			log_printf(0, "\n\n***** ERROR: %s exists but is 0 len, aborting\n", file);
		}
		free(buf);
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: could not load %s, aborting\n", file);
	}
}

/* -p [<f>] */
void clientPatches(const char *file)
{
	char path[1024];
	uint32_t type = 0;
	uint32_t bs = cinfo->bootstrap;

	if (bs & BOOTSTRAP_JTAG)
	{
		type = PATCHES_JTAG;
	}
	else if (bs & BOOTSTRAP_GLITCH2)
	{
		type = PATCHES_GLITCH;
	}
	else if (bs & BOOTSTRAP_GLITCH2M)
	{
		type = PATCHES_GLITCH2M;
	}
	else if (bs & BOOTSTRAP_GLITCH)
	{
		type = PATCHES_GLITCH;
	}
	if (type)
	{
		if (file)
		{
			strcpy(path, file);
			log_printf(0, "Updating patches from file: %s\n", path);
		}
		else
		{
			if (bs & BOOTSTRAP_JTAG)
			{
				sprintf(path, "%d/bin/patches_%s.bin", *(uint16_t *)((uint8_t *)cinfo + 5), getConsoleTypeStr((bs & BOOTSTRAP_CONSOLE_MASK) + 1));
			}
			else if (bs & BOOTSTRAP_GLITCH2)
			{
				sprintf(path, "%d/bin/patches_g2%s.bin", *(uint16_t *)((uint8_t *)cinfo + 5), getConsoleTypeStr((bs & BOOTSTRAP_CONSOLE_MASK) + 1));
			}
			else if (bs & BOOTSTRAP_GLITCH2M)
			{
				sprintf(path, "%d/bin/patches_g2m%s.bin", *(uint16_t *)((uint8_t *)cinfo + 5), getConsoleTypeStr((bs & BOOTSTRAP_CONSOLE_MASK) + 1));
			}
			else if (bs & BOOTSTRAP_GLITCH)
			{
				sprintf(path, "%d/bin/patches_fat.bin", *(uint16_t *)((uint8_t *)cinfo + 5));
			}
			log_printf(0, "Updating patches in auto mode: %s\n", path);
		}
		updatePatches(path, type);
	}
	else
	{
		log_printf(0, "\n***** ERROR: unable to determine console hack type!\n");
	}
}

/* -rb <f> <b> <l> */
void clientReadBlocks(const char *file, const char *sstart, const char *scount)
{
	uint32_t start = myatoh32(sstart, -1);
	uint32_t count = myatoh32(scount, -1);
	int len;
	uint8_t *buf;

	if (count != 0 && count != -1 && start != -1)
	{
		if (start + count <= cinfo->nandSize / cinfo->blockSize)
		{
			log_printf(0, "Reading 0x%x (%d) blocks from console starting at block 0x%x (%d)...\n", count, count, start, start);
			buf = netReadBlocks(&len, start, count);
			if (buf && len > 0)
			{
				log_printf(0, "Done!\nWriting 0x%x (%d) bytes to %s...\n", len, len, file);
				if (writeFile(file, buf, len))
				{
					log_printf(0, "Done!\n");
				}
				else
				{
					log_printf(0, "\n\n***** ERROR: Failed to write block data to file %s!\n", file);
				}
				free(buf);
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: Trying to read blocks from the console failed!\n");
			}
		}
		else
		{
			log_printf(0, "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n", cinfo->nandSize / cinfo->blockSize);
		}
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n");
	}
}

/* -wb <f> <b> */
void clientWriteBlocks(const char *file, const char *sstart)
{
	uint32_t start = myatoh32(sstart, -1);
	uint32_t n;
	size_t len;
	uint8_t *buf;

	if (start != -1)
	{
		buf = FileToBuffer(file, &len);
		if (buf && (int)len > 0)
		{
			n = len / cinfo->blockSize;
			if (!(len % cinfo->blockSize))
			{
				if (start + n <= cinfo->nandSize / cinfo->blockSize)
				{
					log_printf(0, "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n", n, n, start, start);
					if (netWriteBlocks(buf, len, start, n))
					{
						log_printf(0, "Done! Wrote 0x%x (%d) bytes to console flash!\n", (int)len, (int)len);
					}
					else
					{
						log_printf(0, "\n\n***** ERROR: Writing data to console failed!\n");
					}
				}
				else
				{
					log_printf(0, "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n", cinfo->nandSize / cinfo->blockSize);
				}
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\n", file, (int)len, cinfo->blockSize);
			}
			free(buf);
			return;
		}
		log_printf(0, "\n\n***** ERROR: Unable to read file %s!\n", file);
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n");
	}
}

/* copy data into raw NAND pages (512 data + 16 spare) at logical offset off */
void patchNand(uint8_t *buf, int off, const uint8_t *data, int len)
{
	uint8_t *spare = buf + NAND_PAGE;

	while (off >= NAND_PAGE)
	{
		buf += NAND_RAW_PAGE;
		spare += NAND_RAW_PAGE;
		off -= NAND_PAGE;
	}
	if (off)
	{
		memcpy(buf + off, data, NAND_PAGE - off);
		len -= NAND_PAGE - off;
		calcPageEcc(buf, spare);
		data += NAND_PAGE - off;
		buf += NAND_RAW_PAGE;
		spare += NAND_RAW_PAGE;
	}
	while (len >= NAND_PAGE)
	{
		memcpy(buf, data, NAND_PAGE);
		calcPageEcc(buf, spare);
		len -= NAND_PAGE;
		data += NAND_PAGE;
		spare += NAND_RAW_PAGE;
		buf += NAND_RAW_PAGE;
	}
	if (len)
	{
		memcpy(buf, data, len);
		calcPageEcc(buf, spare);
	}
}

/* -bp <f> <o> */
void clientBinPatch(const char *file, const char *soff)
{
	uint32_t size = cinfo->nandSize;
	uint32_t bs = cinfo->blockSize;
	uint32_t off, rem, start, count;
	size_t len;
	int rlen;
	const uint8_t *data;
	uint8_t *nand;

	off = myatoh32(soff, -1);
	if (cinfo->nandSize != NAND_SIZE_MMC)
	{
		size = cinfo->nandSize / NAND_RAW_BLOCK * NAND_BLOCK;
		bs = cinfo->blockSize / NAND_RAW_BLOCK * NAND_BLOCK;
	}
	if (off != -1)
	{
		log_printf(0, "file: %s start offset 0x%x\n", file, soff);
		data = FileToBuffer(file, &len);
		if (data && len)
		{
			if (off + len < size)
			{
				rem = off % bs;
				start = rem / bs;
				count = (len + rem) / bs;
				if ((len + rem) % bs)
				{
					count++;
				}
				log_printf(0, "Reading 0x%x blocks from console starting at block 0x%x (%d)...\n", count, start, start);
				nand = netReadBlocks(&rlen, start, count);
				if (nand && rlen)
				{
					log_printf(0, "Success!\nPatching in binary data...");
					if (cinfo->nandSize == NAND_SIZE_MMC)
					{
						memcpy(nand + rem, data, len);
					}
					else
					{
						patchNand(nand, rem, data, len);
					}
					log_printf(0, "Done!\n");
					log_printf(0, "Writing 0x%x blocks from console starting at block 0x%x...\n", count, start);
					if (netWriteBlocks(nand, rlen, start, count))
					{
						log_printf(0, "Success! Completed patching NAND!\n");
					}
					else
					{
						log_printf(0, "\n\n***** ERROR: Writing data to console failed!\n");
					}
				}
				else
				{
					log_printf(0, "\n\n***** ERROR: Reading data from console failed!\n");
				}
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: File %s size patched into offset 0x%x will exceed NAND system area (0x%x)!\n", file, off, size);
			}
			/* clientWriteBlocks' shape: the read error follows the data
			   block, which returns.  Written as an else, every arm reaches
			   the return block directly and the early-return heuristic
			   cools the error arms, which moves registers in the inlined
			   patchNand */
			return;
		}
		log_printf(0, "\n\n***** ERROR: Unable to read file %s!\n", file);
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n");
	}
}

/* -eb <b> */
void clientEraseBlock(const char *sblock)
{
	uint32_t block = myatoh32(sblock, -1);

	if (block != -1)
	{
		if (block < cinfo->nandSize / cinfo->blockSize)
		{
			log_printf(0, "erasing block 0x%x...", block);
			if (netEraseBlock(block, 1))
			{
				log_printf(0, "Success!\n");
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: Failed to erase block 0x%x!\n", block);
			}
		}
		else
		{
			log_printf(0, "\n\n***** ERROR: Block 0x%x is outside system area!\n", block);
		}
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n");
	}
}

/* the option's argument(s), `first` being the option's own index; dies with
   usage if one is missing or, with check, if a mode was already set.  The
   three tests are written alike: gcc merges each one's first two conditions
   and orders them itself (the count first in the first test, the pointer
   first in the others), so an edit here can swap them. */
char *getArgs(int argc, char **argv, int *pi, int mode, int check, char **arg2, char **arg3)
{
	int first = *pi;
	int i = first + 1;

	if (!argv[i] || i == argc || *argv[i] == '-')
	{
		client_usage(ERR_NO_ARG, argv[first]);
	}
	if (arg2)
	{
		i++;
		if (!argv[i] || i == argc || *argv[i] == '-')
		{
			client_usage(ERR_ARGS, argv[first]);
		}
		*arg2 = argv[i];
	}
	if (arg3)
	{
		i++;
		if (!argv[i] || i == argc || *argv[i] == '-')
		{
			client_usage(ERR_ARGS, argv[first]);
		}
		*arg3 = argv[i];
	}
	if (mode && check)
	{
		client_usage(ERR_TWICE, argv[first]);
	}
	*pi = i;
	return argv[first + 1];
}

/* bpArgs, wbArgs, oneArg and fileArg are getArgs' checks again for the
   options below, differing only in which of the pointer and the count is
   tested first: each option's arm has its own order in the binary (-bp and
   -wb mirror each other, -eb and -ip test the pointer first, -r and -w the
   count).  Written with plain locals, or with the pointer's load in the first
   test, a test keeps the order it has here, and the call gives the arm even
   odds against the next option's test.  getArgs called from these arms gives
   the same code but for those orders (gcc orders its merged tests itself),
   and is never inlined at -wb (tools/wip/dehint/notes/mode_client.md,
   attempt 17). */

/* -bp <f> <o> */
static char *bpArgs(int argc, char **argv, int *pi, int mode, char **arg2)
{
	int i = *pi;
	int j = i + 1;
	char *a = argv[j], *b;

	if (!a || j == argc || *a == '-')
	{
		client_usage(ERR_NO_ARG, argv[i]);
	}
	j++;
	b = argv[j];
	if (j == argc || !b || *b == '-')
	{
		client_usage(ERR_ARGS, argv[i]);
	}
	*arg2 = b;
	if (mode)
	{
		client_usage(ERR_TWICE, argv[i]);
	}
	*pi = j;
	return argv[i + 1];
}

/* -wb <f> <b> */
static char *wbArgs(int argc, char **argv, int *pi, int mode, char **arg2)
{
	int i = *pi;
	int j = i + 1;
	char *a = argv[j], *b;

	if (j == argc || !a || *a == '-')
	{
		client_usage(ERR_NO_ARG, argv[i]);
	}
	j++;
	b = argv[j];
	if (!b || j == argc || *b == '-')
	{
		client_usage(ERR_ARGS, argv[i]);
	}
	*arg2 = b;
	if (mode)
	{
		client_usage(ERR_TWICE, argv[i]);
	}
	*pi = j;
	return argv[i + 1];
}

/* -eb <b>; -ip <add> passes 0 for mode: it sets no command, so it may
   follow one */
static char *oneArg(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;

	if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
	{
		client_usage(ERR_NO_ARG, argv[i]);
	}
	if (mode)
	{
		client_usage(ERR_TWICE, argv[i]);
	}
	*pi = i + 1;
	return argv[i + 1];
}

/* -r <f>, -w <f> */
static char *fileArg(int argc, char **argv, int *pi, int mode)
{
	int i = *pi;
	int j = i + 1;
	char *a = argv[j];

	if (j == argc || !a || *a == '-')
	{
		client_usage(ERR_NO_ARG, argv[i]);
	}
	if (mode)
	{
		client_usage(ERR_TWICE, argv[i]);
	}
	*pi = j;
	return argv[i + 1];
}

/* The command's number is `mode`, its first argument `arg` (`dummy` where it
   has none); -s and -reboot set `reboot` instead.  One connection serves
   both: with a reboot and no command the mode is 6, the switch's empty
   case. */
int mode_client(int argc, char **argv)
{
	char dummy[] = "dummy";
	char *start = NULL, *count = NULL;
	int i = 0;
	int reboot = 0;
	char *ip = NULL;
	char *arg = NULL;
	int mode = 0;

	log_set_name("client");
	for (i = 0; i < argc; i++)
	{
		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))
		{
			client_usage(ERR_NONE, NULL);
		}
		if (!strnicmp(argv[i], "-noenter", 8))
		{
			log_printf(0, "<enter> key on completion suppressed\n");
			promptEnter = 0;
		}
		else if (!strnicmp(argv[i], "-reboot", 7))
		{
			if (reboot == NET_SHUTDOWN)
			{
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\n");
			}
			log_printf(0, "setting reboot on completion\n");
			reboot = NET_REBOOT;
		}
		else if (!strnicmp(argv[i], "-bp", 3))
		{
			arg = bpArgs(argc, argv, &i, mode, &start);
			log_printf(0, "setting binary patch file to %s, offset %s\n", arg, start);
			mode = CMD_BIN_PATCH;
		}
		else if (!strnicmp(argv[i], "-rb", 3))
		{
			arg = getArgs(argc, argv, &i, mode, 1, &start, &count);
			log_printf(0, "reading %s blocks to %s, starting block %s\n", count, arg, start);
			mode = CMD_READ_BLOCKS;
		}
		else if (!strnicmp(argv[i], "-wb", 3))
		{
			arg = wbArgs(argc, argv, &i, mode, &start);
			log_printf(0, "writing blocks from %s, starting at block %s\n", arg, start);
			mode = CMD_WRITE_BLOCKS;
		}
		else if (!strnicmp(argv[i], "-eb", 3))
		{
			arg = oneArg(argc, argv, &i, mode);
			log_printf(0, "erase block set to %s\n", arg);
			mode = CMD_ERASE_BLOCK;
		}
		else if (!strnicmp(argv[i], "-s", 2))
		{
			if (reboot == NET_REBOOT)
			{
				log_printf(0, "reboot has already been set on command line, ignoring -s\n");
			}
			else
			{
				log_printf(0, "setting shutdown on completion\n");
				reboot = NET_SHUTDOWN;
			}
		}
		else if (!strnicmp(argv[i], "-keys", 5))
		{
			mode = CMD_KEYS;
			arg = dummy;
		}
		else if (!strnicmp(argv[i], "-ip", 3))
		{
			ip = oneArg(argc, argv, &i, 0);
			log_printf(0, "setting forced IP to %s\n", ip);
		}
		else if (!strnicmp(argv[i], "-r", 2))
		{
			arg = fileArg(argc, argv, &i, mode);
			log_printf(0, "setting read filename to %s\n", arg);
			mode = CMD_READ;
		}
		else if (!strnicmp(argv[i], "-w", 2))
		{
			arg = fileArg(argc, argv, &i, mode);
			log_printf(0, "setting write filename to %s\n", arg);
			mode = CMD_WRITE;
		}
		else if (!strnicmp(argv[i], "-e", 2))
		{
			/* -e and -c test in place: with oneArg at both, a copy of it
			   stays out of line */
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
			{
				client_usage(ERR_NO_ARG, argv[i]);
			}
			if (mode)
			{
				client_usage(ERR_TWICE, argv[i]);
			}
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting avatar/kinect files base path to %s\n", arg);
			mode = CMD_AVATAR;
		}
		else if (!strnicmp(argv[i], "-c", 2))
		{
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
			{
				client_usage(ERR_NO_ARG, argv[i]);
			}
			if (mode)
			{
				client_usage(ERR_TWICE, argv[i]);
			}
			arg = argv[i + 1];
			i++;
			log_printf(0, "setting xbox compatibility files base path to %s\n", arg);
			mode = CMD_COMPAT;
		}
		else if (!strnicmp(argv[i], "-i", 2))
		{
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
			{
				arg = dummy;
			}
			else
			{
				arg = argv[i + 1];
				i++;
				log_printf(0, "info dump path set to %s\n", arg);
			}
			mode = CMD_INFO;
		}
		else if (!strnicmp(argv[i], "-p", 2))
		{
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
			{
				arg = dummy;
			}
			else
			{
				arg = argv[i + 1];
				i++;
				log_printf(0, "patch file set to %s\n", arg);
			}
			mode = CMD_PATCHES;
		}
		else if (!strnicmp(argv[i], "-v", 2))
		{
			log_verbose_flag(argv[i][2]);
		}
		else
		{
			client_usage(ERR_UNKNOWN, argv[i]);
		}
	}
	if (!mode || !arg)
	{
		if (!reboot)
		{
			client_usage(ERR_NO_COMMAND, NULL);
		}
		mode = CMD_NONE;
	}
	if (netConnect(ip))
	{
		cinfo = netGetInfo();
		switch (mode)
		{
		case CMD_READ:
			netDumpNand(arg);
			break;
		case CMD_WRITE:
			clientWrite(arg);
			break;
		case CMD_KEYS:
			clientKeys();
			break;
		case CMD_AVATAR:
			if (cinfo->hwFlags & HW_HDD)
			{
				sendAvatarData(arg, cinfo->kernel);
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n");
			}
			break;
		case CMD_COMPAT:
			if (cinfo->hwFlags & HW_HDD)
			{
				sendCompatData(arg);
			}
			else
			{
				log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n");
			}
			break;
		case CMD_NONE:
			break;
		case CMD_PATCHES:
			if (arg == dummy)
			{
				clientPatches(NULL);
			}
			else
			{
				clientPatches(arg);
			}
			break;
		case CMD_READ_BLOCKS:
			clientReadBlocks(arg, start, count);
			break;
		case CMD_WRITE_BLOCKS:
			clientWriteBlocks(arg, start);
			break;
		case CMD_ERASE_BLOCK:
			clientEraseBlock(arg);
			break;
		case CMD_BIN_PATCH:
			clientBinPatch(arg, start);
			break;
		case CMD_INFO:
			if (arg == dummy)
			{
				clientInfo(NULL);
			}
			else
			{
				clientInfo(arg);
			}
			break;
		default:
			log_printf(0, "\n\n***** ERROR: invalid mode specified, please inform author\n");
			break;
		}
		if (reboot)
		{
			netReboot(reboot);
		}
		netDisconnect();
	}
	else
	{
		log_printf(0, "\n\n***** ERROR: unable to connect to xbox server\n");
	}
	return 0;
}

/* 16 zero bytes end the original object's .rdata (global: gcc drops an unused
   static) */
const char mc_rdpad[16] = {0};
