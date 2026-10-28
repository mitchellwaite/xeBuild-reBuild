/* log.h: log.c's functions that other objects use */
#ifndef LOG_H
#define LOG_H

#include "xebuild.h"

void log_set_verbose(int level);
void log_verbose_flag(unsigned char c);
unsigned int log_get_verbose(void);
void log_set_name(const char *name);
void log_printf(unsigned int level, const char *fmt, ...);
void log_init(void);
void log_finish(void);

#endif
