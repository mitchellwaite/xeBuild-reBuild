/* mode_extract: `xeBuild extract`, loads a NAND dump and lists its files */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void log_set_name(const char *name);
void log_printf(int level, const char *fmt, ...);
void log_verbose_flag(unsigned char c);
void log_finish(void);

int loadDump(const char *path);
void listFlashFiles(void);
void checkBootImage(int arg);

extern char separator[];
extern int promptEnter;
extern char flashFiles[][22];
extern int buildMode;
extern int g479f4c, g47a080;

void extract_usage(int err, const char *opt)
{
	switch (err) {
	case 3:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line but no argument provided!\n", opt);
		break;
	case 4:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n", opt);
		break;
	case 5:
		log_printf(0, "\n\n***** ERROR: option flag %s on command line but option was already set!\n", opt);
		break;
	case 1:
		log_printf(0, "\n\n***** ERROR: unknown option '%s' provided on command line!\n", opt);
		break;
	case 2:
		log_printf(0, "\n\n***** ERROR: not enough info provided to carry out command!\n");
		break;
	}
	log_printf(0, separator);
	log_printf(0, "Usage   :\n   %s extract <switch> <input NAND image>\n\n", "xeBuild");
	log_printf(0, "Examples:\n");
	log_printf(0, "   %s extract -v nanddump.bin\n", "xeBuild");
	log_printf(0, "\nSwitches:\n");
	log_printf(0, "   -noenter : suppresses prompt for enter key when finished\n");
	log_printf(0, "   -v       : shows more info during extract process\n");
	log_printf(0, "   -?       : shows this help\n\n");
	log_printf(0, "legend:\n");
	log_printf(0, "<dir>       = path, absolute or relative, to a directory - do not terminate with /\n");
	log_printf(0, separator);
	log_finish();
	if (promptEnter) {
		log_printf(0, "\npress <enter> to quit...\n");
		fgetc(stdin);
	}
	exit(1);
}

int mode_extract(int argc, char **argv)
{
	int i;
	char *dump = NULL;

	log_set_name("extract");
	log_printf(0, "***** NOTE: Most errors/warnings will be due to the fact extract mode does not process 1BL and CPU keys! *****\n\n");
	for (i = 0; i < argc; i++) {
		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) ||
		    !strnicmp(argv[i], "/?", 2))
			extract_usage(0, NULL);
		if (argv[i][0] == '-') {
			if (!strnicmp(argv[i], "-noenter", 8)) {
				log_printf(0, "<enter> key on completion suppressed\n");
				promptEnter = 0;
			} else if (!strnicmp(argv[i], "-v", 2))
				log_verbose_flag(argv[i][2]);
		} else if (argv[i][0] == '\0')
			extract_usage(1, argv[i]);
		else if (dump != NULL)
			extract_usage(5, argv[i]);
		else
			dump = argv[i];
	}
	if (dump == NULL)
		extract_usage(2, NULL);
	strcpy(flashFiles[0], "crl.bin");
	strcpy(flashFiles[1], "dae.bin");
	strcpy(flashFiles[2], "extended.bin");
	strcpy(flashFiles[3], "fcrt.bin");
	strcpy(flashFiles[4], "secdata.bin");
	buildMode = 5;
	if (!loadDump(dump)) {
		log_printf(0, "Loading dump failed!\n");
		return -1;
	}
	log_printf(0, "Dump load success!\n\n");
	log_printf(1, separator);
	log_printf(1, "flash fs file list:\n");
	log_printf(1, separator);
	listFlashFiles();
	log_printf(1, separator);
	log_printf(1, "checking boot image (update mode test):\n");
	log_printf(1, separator);
	g47a080 = g479f4c;
	checkBootImage(0);
	return 0;
}
