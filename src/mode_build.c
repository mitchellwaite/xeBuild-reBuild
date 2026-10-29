/* mode_build: the default build mode, its usage and switches (-t/-c/-d/-b/-p) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define XB_PATCHES		/* xb.patches (xebuild.h) */
#include "xebuild.h"
#include "filelist_ini.h"
#include "fileutil.h"
#include "image_read.h"
#include "image_write.h"
#include "keys.h"
#include "log.h"
#include "main.h"
#include "mode_build.h"
#include "options.h"

void build_usage(void)
{
	log_printf(0, separator);
	log_printf(0, "Usage    :\n   %s [mode] -t <type> [<switch> [<switch>...]] <out.bin>\n\n", "xeBuild");
	log_printf(0, "Example  :\n   %s -t retail -c trinity -d files -b 0102...0f -p 0102...0f out.bin\n", "xeBuild");
	log_printf(0, "\nSwitches:\n");
	log_printf(0, "   -t <type>: retail, jtag, glitch, glitch2, glitch2m, devkit (defaults to retail)\n");
	log_printf(0, "   -p <key> : 32 character CPU hex key (override, can be elsewhere)\n");
	log_printf(0, "   -b <key> : 32 character 1BL hex key (override, can be elsewhere)\n");
	log_printf(0, "   -c <con> : console type\n");
	log_printf(0, "   -d <dir> : per build files directory\n");
	log_printf(0, "   -f <dir> : use different data dir and file lists\n");
	log_printf(0, "   -s <file>: outputs SHA-1 of final image to <file>, if <file> is not provided an auto generated name is used\n");
	log_printf(0, "   -o <opt> : set %s options\n", "xeBuild");
	log_printf(0, "   -a <name>: append patches\n");
	log_printf(0, "   -i <ext> : adds _<ext> into firmware ini and patches file names\n");
	log_printf(0, "   -r <ext> : adds _<ext> into ini bl section name and patches file names\n");
	log_printf(0, "   -8 <pat> : adds raw patch to NAND just before finalizing\n");
	log_printf(0, "   -v       : shows more info during build process\n");
	log_printf(0, "   -noenter : suppresses prompt for enter key when finished\n");
	log_printf(0, "   -?       : shows this info\n\n");
	log_printf(0, "legend:\n");
	log_printf(0, "[mode]      : build, extract");
	log_printf(0, ", client, update");
	log_printf(0, " - defaults to build if not present\n");
	log_printf(0, "<con>       = xenon, zephyr, falcon, jasper, jaspersb, jasper256,\n");
	log_printf(0, "              jasper512, jasperbb, jasperbigffs, trinity, trinitybb, trinitybigffs\n");
	log_printf(0, "              corona, corona4g, winchester, winchester4g\n");
	log_printf(0, "<dir>       = path, absolute or relative, to a directory - do not terminate with /\n");
	log_printf(0, "<key>       = 128 bit key in hexadecimal representation\n");
	log_printf(0, "<name>      = name.bin contents will be appended to hv/kernel patches\n\n");
	log_printf(0, "<out.bin>   = optional, overrides auto built output image name\n");
	log_printf(0, "<ext>       = using this option would cause the builder to look for _glitch_<ext>.ini instead of _glitch.ini\n");
	log_printf(0, "              and patches_jasper_<ext>.bin instead of patches_jasper.bin\n");
	log_printf(0, "<opt> various options can be specified on the command line, see perbox sample ini for descriptions\n");
	log_printf(0, "      listed below, ALL are available to all image types\n");
	log_printf(0, "      the others can be specified but are only used for that specific image type\n");
	log_printf(0, "ALL         = nomobile noremap noecdremap nosecurity nosusecurity nandmu smcnocheck cputemp=\n");
	log_printf(0, "ALL         = gputemp= edramtemp= overcputemp= overgputemp= overedramtemp= cpufan= gpufan=\n");
	log_printf(0, "ALL         = avregion= gameregion= dvdregion= macid= cfldv=\n");
	log_printf(0, "JTAG/GLITCH = smcnoeject smcnoblink cygnos demon xellbutton= xellbutton2= dvdkey=\n");
	log_printf(0, "JTAG only   = nodvd olddvd dualboot=\n");
	log_printf(0, "GLITCH only = patchsmc\n");
	log_printf(0, "      options noted above with an = are expected to be followed with a value\n");
	log_printf(0, "      specifying one of the options without an = is the same as setting TRUE in the ini\n");
	log_printf(0, "         any value assigned to it will be ignored.\n");
	log_printf(0, "      note that command line options take precedence over any values set in perbox ini\n");
	log_printf(0, "      and that only values preceded with 0x will be interpreted as hex, MAC is the only exception\n");
	log_printf(0, "      example: -o macid=00:22:48:F1:01:02;gameregion=0x00FF;nomobile\n");
	log_printf(0, "      example: -o macid=00:22:48:F1:01:02 -o gameregion=0x00FF -o nomobile\n");
	log_printf(0, "      example: -o macid=002248F10102 -o gameregion=255 -o nomobile\n");
	log_printf(0, "<pat>       = optional, <pat> consists of filename.ext,offset\n");
	log_printf(0, "      patches NAND image with file contents just before combining spare and finalizing ecc\n");
	log_printf(0, "      offset is the raw offset without spare data\n");
	log_printf(0, "      file will load based from the -f directory, or absolute path if drive letter is found\n");
	log_printf(0, "      add 0x to offset to specify hexadecimal, otherwise it will be read as decimal\n");
	log_printf(0, "      example: -8 myfile.bin,0x12345\n");
	log_printf(0, "      example: -8 myfile.bin,0x12345;myotherfile.bin,0x54321\n");
	log_printf(0, separator);
	if (promptEnter) {
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	exit(1);
}

int loadKeyFile(char *key, const char *dir, const char *name)
{
	char path[1024] = "\0";
	FILE *f;
	size_t n;

	if (dir)
		strcpy(path, dir);
	strcat(path, name);
	f = fopen(path, "rb");
	if (f) {
		log_printf(1, "loading %s from %s\n", name, path);
		n = fread(key, 32, 1, f);
		fclose(f);
		if (n == 1) {
			key[32] = 0;
			return 1;
		}
	}
	return 0;
}

void loadPubKey(const char *desc, const char *file, void **out, uint32_t size, uint32_t sum, int quiet)
{
	char path[1024] = "./";
	size_t len;
	uint32_t s;

	strcat(path, file);
	if (!FileExists(path)) {
		strcpy(path, "./common/");
		strcat(path, file);
	}
	*out = FileToBuffer(path, &len);
	if (*out) {
		if (len == size) {
			s = sumBytes(*out, size);
			if (s == sum) {
				log_printf(1, "loaded %s from file %s\n", desc, path);
				return;
			}
			log_printf(1, "loaded %s from file %s but sum 0x%x is not expected sum of 0x%x, discarding\n", desc, path, s, sum);
		}
		free(*out);
		*out = 0;
	} else if (!quiet)
		log_printf(1, "%s (%s) not available, signature checks will not be performed\n", desc, file);
}

void loadPubKeys(void)
{
	loadPubKey("1BL RSA pub key", "1BL_pub.bin", &xb.pub1bl, 272, 0x79c7, 0);
	loadPubKey("PIRS RSA pub key", "PIRS_pub.bin", &xb.pubPirs, 272, 0x80d0, 0);
	loadPubKey("MASTER RSA pub key", "MAST_pub.bin", &xb.masterPub, 272, 0x843c, 0);
	loadPubKey("SC/SD RSA priv key", "SB_priv.bin", &xb.prvKey, 912, 0x1ca16, 1);
}

int mode_build(int argc, char **argv)
{
	char name[1024] = {0};
	char ini[1024] = "./data/";
	char cpuKey[40] = {0};
	char key1bl[40] = {0};
	int i;
	int have = 0;
	char *v;
	int ret;

	xb.nRawPatches = 0;
	for (i = 0; i < argc; i++) {
		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2)) {
			build_usage();
		} else if (!strnicmp(argv[i], "-noenter", 8)) {
			log_printf(1, "<enter> key on completion suppressed\n");
			promptEnter = 0;
		} else if (!strnicmp(argv[i], "-norandom", 9)) {
			log_printf(1, "disabling random nonces\n");
			xb.randomKeys = 0;
		} else if (!strnicmp(argv[i], "-t", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -t on command line but no argument provided!\n");
				build_usage();
			}
			if (!strnicmp(argv[i], "retail", 6)) {
				log_printf(0, "building retail image\n");
				xb.type = BUILD_RETAIL;
			} else if (!strnicmp(argv[i], "jtag", 4)) {
				log_printf(0, "building jtag image\n");
				xb.type = BUILD_JTAG;
			} else if (!strnicmp(argv[i], "glitch2m", 8)) {
				log_printf(0, "building glitch2 mfg image\n");
				xb.glitch2mfg = 1;
				xb.glitch2 = 1;
				xb.type = BUILD_GLITCH;
			} else if (!strnicmp(argv[i], "glitch2", 7)) {
				log_printf(0, "building glitch2 image\n");
				xb.glitch2 = 1;
				xb.type = BUILD_GLITCH;
			} else if (!strnicmp(argv[i], "glitch", 6)) {
				log_printf(0, "building glitch image\n");
				xb.type = BUILD_GLITCH;
			} else if (!strnicmp(argv[i], "devkit16", 8)) {
				log_printf(0, "building devkit16 image\n");
				xb.type = BUILD_DEVKIT16;
			} else if (!strnicmp(argv[i], "devkit", 6)) {
				log_printf(0, "building devkit image\n");
				xb.type = BUILD_DEVKIT;
			} else if (!strnicmp(argv[i], "testkit16", 9)) {
				log_printf(0, "building testkit16 image\n");
				xb.type = BUILD_TESTKIT16;
			} else if (!strnicmp(argv[i], "testkit", 7)) {
				log_printf(0, "building testkit image\n");
				xb.type = BUILD_TESTKIT;
			} else if (!strnicmp(argv[i], "devgl16", 7)) {
				log_printf(0, "building devgl16 image\n");
				xb.type = BUILD_DEVGL16;
			} else if (!strnicmp(argv[i], "devgl", 5)) {
				log_printf(0, "building devgl image\n");
				xb.type = BUILD_DEVGL;
			} else {
				log_printf(0, "\n\n***** ERROR: option flag -t on command line followed by unknown argument '%s'!\n", argv[i]);
				build_usage();
			}
		} else if (!strnicmp(argv[i], "-c", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: console type flag -c on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			if (!setConsoleType(argv[i])) {
				log_printf(0, "ERROR: invalid command line, console type %s unknown!\n", argv[i]);
				build_usage();
			}
		} else if (!strnicmp(argv[i], "-o", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -o on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			if (!parseCmdOptions(argv[i])) {
				log_printf(0, "\n\n***** ERROR: option flag -o on command line with invalid arguments!\n", argv[i]);
				build_usage();
			}
		} else if (!strnicmp(argv[i], "-8", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -8 on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			if (!parseRawPatches(argv[i])) {
				log_printf(0, "\n\n***** ERROR: option flag -8 on command line with invalid arguments!\n", argv[i]);
				build_usage();
			}
		} else if (!strnicmp(argv[i], "-s", 2)) {
			xb.sha1Write = 1;
			if (argv[++i] && i != argc && argv[i][0] != '-') {
				strcpy(xb.sha1File, argv[i]);
				log_printf(1, "outputting SHA-1 hash of final image to custom file %s\n", argv[i]);
			} else
				log_printf(1, "outputting SHA-1 hash of final image to auto file\n");
		} else if (!strnicmp(argv[i], "-a", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -a on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			if (xb.numPatches < 16) {
				strcpy(xb.patches[xb.numPatches], argv[i]);
				strcat(xb.patches[xb.numPatches], ".bin");
				xb.numPatches++;
			} else
				log_printf(0, "***** WARNING: exceeded total number of optional patches with -a %s!\n", argv[i]);
		} else if (!strnicmp(argv[i], "-r", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: option flag -r on command line but no argument provided!\n");
				build_usage();
			}
			if (xb.blSuffix[0])
				log_printf(0, "***** WARNING: option flag -r %s on command line replacing previous setting of -r %s!\n", argv[i], xb.blSuffix + 1);
			sprintf(xb.blSuffix, "_%s", argv[i]);
		} else if (!strnicmp(argv[i], "-p", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: CPU key flag -p on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			log_printf(1, "CPU key overridden from command line, not looking for cpukey.txt\n");
			if (strlen(argv[i]) != 32) {
				log_printf(0, "ERROR: invalid command line, CPU key incorrect size!\n");
				build_usage();
			}
			if (!setCpuKeyStr(argv[i]))
				build_usage();
			have |= 1;
			strcpy(cpuKey, argv[i]);
		} else if (!strnicmp(argv[i], "-b", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: 1BL key flag -b on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			log_printf(1, "1BL key overridden from command line, not looking for 1blkey.txt\n");
			if (strlen(argv[i]) != 32) {
				log_printf(0, "ERROR: invalid command line, 1BL key incorrect size!\n");
				build_usage();
			}
			if (!checkKeys(argv[i]))
				build_usage();
			have |= 2;
			strcpy(key1bl, argv[i]);
		} else if (!strnicmp(argv[i], "-v", 2)) {
			log_verbose_flag(argv[i][2]);
		} else if (!strnicmp(argv[i], "-d", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: per build directory flag -d on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			strcpy(xb.baseDir, argv[i]);
			strcat(xb.baseDir, "/");
			log_printf(1, "per build directory overridden from command line to '%s'\n", xb.baseDir);
			have |= 4;
		} else if (!strnicmp(argv[i], "-f", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: data directory flag -f on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			sprintf(ini, "%s/", argv[i]);
			log_printf(1, "data directory overridden from command line to '%s'\n", ini);
			sprintf(xb.dataDir, "%s/", argv[i]);
			sprintf(xb.binDir, "%s/bin/", argv[i]);
			have |= 8;
		} else if (!strnicmp(argv[i], "-i", 2)) {
			if (!argv[++i] || i == argc || argv[i][0] == '-') {
				log_printf(0, "\n\n***** ERROR: data directory flag -i on command line but no argument provided!\n", argv[i]);
				build_usage();
			}
			strcpy(xb.suffix, "_");
			strcat(xb.suffix, argv[i]);
			log_printf(1, "suffix '%s' added from command line to ini and patches filenames\n", xb.suffix);
		} else if (!name[0]) {
			log_printf(1, "file name overridden from command line to '%s'\n", argv[i]);
			strcpy(name, argv[i]);
		} else
			log_printf(0, "WARNING: command line has excess parameters without switches!\n");
	}

	if (!xb.type) {
		log_printf(0, "*****WARNING: image type not provided, defaulting to build a retail image\n");
		xb.type = BUILD_RETAIL;
	}
	if (!(have & 4)) {
		have |= 4;
		log_printf(0, "*****WARNING: you did not specify per build directory! Using %s\n", xb.dataDir);
		strcpy(xb.baseDir, xb.dataDir);
	}
	loadUserIni();
	if (xb.iniSize)
		log_printf(1, "User options.ini loaded, 0x%x bytes in memory\n", xb.iniSize);
	if (!(xb.flags & CONSOLE_MASK) && !iniConsoleType() && !setConsoleType(getIniValue("type"))) {
		log_printf(0, "ERROR: you need to specify console type!\n");
		build_usage();
	}
	if (!(have & 1)) {
		if (loadKeyFile(cpuKey, xb.baseDir, "cpukey.txt") && setCpuKeyStr(cpuKey))
			have |= 1;
		if (!(have & 1) && (v = getIniValue("cpukey")) != 0) {
			log_printf(1, "setting cpukey from ini: 0x%s\n", v);
			if (!setCpuKeyStr(v)) {
				log_printf(0, "ERROR: you need to specify CPU key!\n");
				build_usage();
			}
			memcpy(cpuKey, v, strlen(v));
			have |= 1;
		}
	}
	if (!(have & 2)) {
		if (loadKeyFile(key1bl, 0, "1blkey.txt") && checkKeys(key1bl))
			have |= 2;
		if (!(have & 2) && (v = getIniValue("1blkey")) != 0) {
			log_printf(1, "setting 1blkey from ini: 0x%s\n", v);
			if (!checkKeys(v)) {
				log_printf(0, "ERROR: you need to specify 1BL key!\n");
				build_usage();
			}
			memcpy(key1bl, v, strlen(v));
			have |= 2;
		}
	}

	if (xb.type == BUILD_RETAIL)
		strcat(ini, "_retail");
	else if (xb.type == BUILD_JTAG)
		strcat(ini, "_jtag");
	else if (xb.type == BUILD_GLITCH) {
		if (xb.glitch2mfg)
			strcat(ini, "_glitch2m");
		else if (xb.glitch2)
			strcat(ini, "_glitch2");
		else
			strcat(ini, "_glitch");
	} else if (xb.type == BUILD_DEVKIT)
		strcat(ini, "_devkit");
	else if (xb.type == BUILD_DEVKIT16)
		strcat(ini, "_devkit16");
	else if (xb.type == BUILD_TESTKIT)
		strcat(ini, "_testkit");
	else if (xb.type == BUILD_TESTKIT16)
		strcat(ini, "_testkit16");
	else if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
		strcat(ini, "_devgl");
	strcat(ini, xb.suffix);
	strcat(ini, ".ini");
	applyIniOptions();
	loadAddons();
	if (!parseIni(ini)) {
		ret = 3;
		goto out;
	}

	if (name[0]) {
		strcpy(xb.outName, name);
		log_printf(1, "output name overridden to: %s\n\n", xb.outName);
	} else
		log_printf(1, "auto image name used: %s\n\n", xb.outName);
	log_set_name(xb.outName);
	if ((xb.type == BUILD_DEVKIT || xb.type == BUILD_TESTKIT) && (xb.flags & NAND_BIG_BLOCK)) {
		if (!(xb.flags & NAND_BIG_FFS)) {
			log_printf(1, "building jasper devkit/testkit image requires bigffs, forcing option enable\n");
			xb.flags |= NAND_BIG_FFS;
		}
	}
	loadPubKeys();
	loadDump(0);
	ret = buildImage();
	if (!ret) {
		ret = writeImage(xb.outName);
		if (!ret) {
			log_printf(0, separator);
			log_printf(0, "%s image built, info:\n", xb.outName);
		} else {
			log_printf(0, "\n\n***** ERROR: %i writing to file %s\n\n", ret, xb.outName);
			ret = 2;
		}
	} else {
		log_printf(0, "\n\n***** FATAL BUILD ERROR: %i unable to complete NAND image\n\n", ret);
		ret = 3;
	}
out:
	buildCleanup();
	return ret;
}
