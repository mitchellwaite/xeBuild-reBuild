"""Attempt 10, families 4 and 5: FD_SET/FD_ZERO's expansion, tv order; netSock's and netEmpty's declarations; log_printf's prototype."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
TV = 'tv.tv_sec = 15;\n\ttv.tv_usec = 0;\n'
FD = 'FD_ZERO(&fds);\n\tFD_SET(netSock, &fds);\n'
HEAD = TV + '\t' + FD
OLDSET = 'if (fds.fd_count < FD_SETSIZE)\n\t\tfds.fd_array[fds.fd_count++] = netSock;\n'
FDS = {
 'macro': FD,
 'hand': 'fds.fd_count = 1;\n\tfds.fd_array[0] = netSock;\n',
 'hand-rev': 'fds.fd_array[0] = netSock;\n\tfds.fd_count = 1;\n',
 'old': 'FD_ZERO(&fds);\n\t' + OLDSET,
 'memset': 'memset(&fds, 0, sizeof fds);\n\tFD_SET(netSock, &fds);\n',
 'ptr': '{ fd_set *p = &fds; FD_ZERO(p); FD_SET(netSock, p); }\n',
 'hand-loop': 'FD_ZERO(&fds);\n\t{ u_int i; for (i = 0; i < fds.fd_count; i++) if (fds.fd_array[i] == netSock) break;\n\tif (i == fds.fd_count) { fds.fd_array[i] = netSock; fds.fd_count++; } }\n',
 'sock': '{ SOCKET s = netSock; FD_ZERO(&fds); FD_SET(s, &fds); }\n',
 'helper': 'netSetFds(&fds);\n',
}
FDHELP = 'static void netSetFds(fd_set *fds)\n{\n\tFD_ZERO(fds);\n\tFD_SET(netSock, fds);\n}\n\n'
ORD = {'tvfd': lambda f: TV + '\t' + f, 'fdtv': lambda f: f + '\t' + TV}
SOCKD = 'SOCKET netSock = INVALID_SOCKET;'
EMPTY = 'static uint32_t netEmpty;'
LOGP = '#include "log.h"'
GLOBALS = {
 'base': [],
 'volsock': [(SOCKD, 'volatile SOCKET netSock = INVALID_SOCKET;')],
 'intsock': [(SOCKD, 'int netSock = INVALID_SOCKET;')],
 'volempty': [(EMPTY, 'static volatile uint32_t netEmpty;')],
 'u8empty': [(EMPTY, 'static uint8_t netEmpty[4];'), ('&netEmpty', 'netEmpty')],
 'intempty': [(EMPTY, 'static int netEmpty;')],
 'charempty': [(EMPTY, 'static char netEmpty[4];'), ('&netEmpty', 'netEmpty')],
}
PROTOS = {
 'base': [],
 'int': [(LOGP, '#define log_printf log_printf_\n#include "log.h"\n#undef log_printf\nint log_printf(unsigned int level, const char *fmt, ...);')],
 'knr': [(LOGP, '#define log_printf log_printf_\n#include "log.h"\n#undef log_printf\nvoid log_printf();')],
 'level-int': [(LOGP, '#define log_printf log_printf_\n#include "log.h"\n#undef log_printf\nvoid log_printf(int level, const char *fmt, ...);')],
 'fmt-char': [(LOGP, '#define log_printf log_printf_\n#include "log.h"\n#undef log_printf\nvoid log_printf(unsigned int level, char *fmt, ...);')],
 'attr': [(LOGP, '#define log_printf log_printf_\n#include "log.h"\n#undef log_printf\nvoid log_printf(unsigned int level, const char *fmt, ...) __attribute__((format(printf, 2, 3)));')],
 'mac-do': [(LOGP, '#include "log.h"\n#define LOGF(...) do { log_printf(0, __VA_ARGS__); } while (0)')],
}


def variants():
    for fn, f in FDS.items():
        for on, o in ORD.items():
            s = rep(FLIP, (HEAD, o(f)))
            if fn == 'helper':
                s = FDHELP + s
            yield 'fd|%s|%s' % (fn, on), s
    for gn, g in GLOBALS.items():
        s = FLIP
        repl = list(g)
        yield 'glob|' + gn, s, repl
    for pn, p in PROTOS.items():
        s = FLIP
        if pn == 'mac-do':
            s = rep(s, ('log_printf(0, "received only', 'LOGF("received only'))
        yield 'proto|' + pn, s, list(p)
