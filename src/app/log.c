/* log.c: console verbosity and build.log */

#include <stdarg.h>
#include <stdio.h>
#include <string.h>

#define LOG_FILE "build.log"

static unsigned int verbose_level;
static int log_disabled;
static char log_name[1024];

void log_set_verbose(int level)
{
	unsigned int v = level & 3;

	if (level < 0) {
		log_disabled = 1;
		return;
	}
	if (v == 3)
		v = 2;
	verbose_level = v;
}

void log_verbose_flag(char c)
{
	/* '\0' has its own copy of the level-1 body: gcc merges them, but the
	 * original block order only comes out this way */
	switch (c) {
	case '\0':
		verbose_level = 1;
		puts("verbose set to level 1");
		break;
	case ' ':
	case '1':
		verbose_level = 1;
		puts("verbose set to level 1");
		break;
	case '2':
		verbose_level = 2;
		puts("verbose set to level 2");
		break;
	case '0':
		break;
	default:
		puts("verbose flag is invalid or default, ignoring");
		break;
	}
}

unsigned int log_get_verbose(void)
{
	return verbose_level;
}

void log_set_name(const char *name)
{
	if (name) {
		strcpy(log_name, name);
		strcat(log_name, ".log");
		remove(log_name);
	}
}

void log_printf(unsigned int level, const char *fmt, ...)
{
	char buf[512];
	va_list ap;
	FILE *f;

	va_start(ap, fmt);
	vsnprintf(buf, sizeof(buf), fmt, ap);
	va_end(ap);
	if (verbose_level >= level)
		printf(buf);
	if (level <= 2 && !log_disabled) {
		f = fopen(LOG_FILE, "a");
		if (f) {
			fprintf(f, buf);
			fclose(f);
		}
	}
}

void log_init(void)
{
	FILE *f = fopen(LOG_FILE, "wb");
	if (f) {
		fclose(f);
		return;
	}
	printf("could not initialize temp log file at '%s', logging disabled!\n", LOG_FILE);
	log_disabled = 1;
}

void log_finish(void)
{
	FILE *f;

	if (log_disabled)
		return;
	log_disabled = 1;
	if (log_name[0]) {
		f = fopen(LOG_FILE, "rb");
		if (f) {
			fclose(f);
			rename(LOG_FILE, log_name);
		}
	}
}
