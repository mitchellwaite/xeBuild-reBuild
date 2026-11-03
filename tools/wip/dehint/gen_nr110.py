"""Attempt 12: the transfer loop ends by assignment on its failure paths (sendAvatarData's `i = count`), no dead test.
Axes: which failure paths assign (s/r/both), stop assignment, failure marker tested after the loop, form of the post-loop test, loop form, body form."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nrflip import *
A = FLIP.index('\t\tbuf = calloc(size, 1);')
B = FLIP.index('\t*len = 0;\n\treturn (uint8_t *)&netEmpty;')
HEAD, FOOT = FLIP[:A], FLIP[B:]
E = '(uint8_t *)&netEmpty'
FREE = 'if (buf != ' + E + ')\n free(buf);\n'
LOGS = 'log_printf(0, "timeout waiting for data, error %d\\n", WSAGetLastError());\n'
NLOGR = 'if (verbose)\n putchar(\'\\n\');\nlog_printf(0, "could not receive data on socket, error %d\\n", WSAGetLastError());\n'
PRINT = 'if (verbose)\n printf("received 0x%08x of 0x%08x\\r", got, size);\n'
TAILCORE = ('if (verbose)\n putchar(\'\\n\');\nif (got == size) {\n*len = size;\nreturn buf;\n}\nif (verbose)\n putchar(\'\\n\');\n'
            'log_printf(0, "received only %x of %x bytes! fail\\n", got, size);\n' + FREE + 'return NULL;\n')
SEL = 'r = select(0, &fds, NULL, NULL, &tv);\nif (r == SOCKET_ERROR || r == 0) {\n'
RECV = 'r = recv(netSock, (char *)buf + got, size - got, 0);\nif (r == SOCKET_ERROR) {\n'
STOPS = {'got=size': 'got = size;', 'got=size+1': 'got = size + 1;', 'size=got': 'size = got;', 'size=0': 'size = 0;'}
MARKS = {
    'buf': ('', 'buf = NULL;', 'buf = NULL;', '!buf'),
    'ok': ('int ok = 1;', 'ok = 0;', 'ok = 0;', '!ok'),
    'r': ('', 'r = SOCKET_ERROR;', '', 'r == SOCKET_ERROR'),
}
LOOPS = ['while', 'do']
BODIES = ['else', 'cont']
POSTS = ['ret', 'if', 'single']


def tail(post, test, mark):
    if post == 'ret':
        return 'if (' + test + ')\n return NULL;\n' + TAILCORE
    if post == 'if':
        return 'if (' + {'!buf': 'buf', '!ok': 'ok', 'r == SOCKET_ERROR': 'r != SOCKET_ERROR'}[test] + ') {\n' + TAILCORE + '}\nreturn NULL;\n'
    # single return of buf: only with the buf marker
    return ('if (buf) {\nif (verbose)\n putchar(\'\\n\');\nif (got == size)\n*len = size;\nelse {\nif (verbose)\n putchar(\'\\n\');\n'
            'log_printf(0, "received only %x of %x bytes! fail\\n", got, size);\n' + FREE + 'buf = NULL;\n}\n}\nreturn buf;\n')


def build(which, stop, mark, post, loop, body, cond=None):
    decl, ms, mr, test = MARKS[mark]
    a_s = FREE + (ms + '\n' + stop + '\n' if 's' in which else 'return NULL;\n')
    a_r = FREE + (mr + '\n' + stop + '\n' if 'r' in which else 'return NULL;\n')
    cond = cond or 'got < size'
    if body == 'else':
        inner = SEL + LOGS + a_s + '} else {\n' + RECV + NLOGR + a_r + '} else {\ngot += r;\n' + PRINT + '}\n}\n'
    else:
        inner = (SEL + LOGS + a_s + ('continue;\n' if 's' in which else '') + '}\n' + RECV + NLOGR + a_r + ('continue;\n' if 'r' in which else '') +
                 '}\ngot += r;\n' + PRINT)
    if loop == 'while':
        lp = 'got = 0;\nwhile (' + cond + ') {\n' + inner + '}\n'
    else:
        lp = 'got = 0;\nif (size > 0) do {\n' + inner + '} while (' + cond + ');\n'
    h = HEAD.replace('uint8_t *buf;', 'uint8_t *buf;\n' + decl) if decl else HEAD
    return (h + 'buf = calloc(size, 1);\nif (verbose)\n printf("waiting for 0x%x bytes\\n", size);\n' + lp + tail(post, test, mark) + '}\n' + FOOT)


def variants():
    for loop in LOOPS:
        for body in BODIES:
            for which in ('s', 'r', 'sr'):
                for sn, stop in STOPS.items():
                    for mn in MARKS:
                        for post in POSTS:
                            if post == 'single' and mn != 'buf':
                                continue
                            yield '|'.join((loop, body, which, sn, mn, post)), build(which, stop, mn, post, loop, body)
    # stop through the loop's own condition: the marker is the only assignment
    for loop in LOOPS:
        for body in BODIES:
            for which in ('s', 'r', 'sr'):
                for mn, conds in (('buf', ('got < size && buf', 'buf && got < size')), ('ok', ('got < size && ok', 'ok && got < size')),
                                  ('r', ('got < size && r != SOCKET_ERROR', 'r != SOCKET_ERROR && got < size'))):
                    for c in conds:
                        for post in POSTS:
                            if post == 'single' and mn != 'buf':
                                continue
                            yield '|'.join((loop, body, which, 'cond:' + c, mn, post)), build(which, '', mn, post, loop, body, c)
