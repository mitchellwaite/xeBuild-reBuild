"""Attempt 9: scoping axes. hn (select/recv failure: early return or nested else), hdr scope, fds/tv scope, size head, tail (returns or fall-out to a final return NULL), select spelling, loop form.
NR80_LOOP=do also runs the do > 0 form; NR80_SIDE=1 the side-effect select."""
import itertools, os
BS = chr(92)
NLS = "if (verbose)\n\tputchar('" + BS + "n');\n"
FREE = 'if (buf != (uint8_t *)&netEmpty)\n\tfree(buf);\n'
SEL1 = 'r = select(0, &fds, NULL, NULL, &tv);\n'
TEST = 'r == SOCKET_ERROR || r == 0'
LOG1 = 'log_printf(0, "timeout waiting for data, %d' + BS + 'n", WSAGetLastError());\n'
LOG2 = 'log_printf(0, "unable to fetch first 4 bytes, %d' + BS + 'n", WSAGetLastError());\n'
ZERO = '*len = 0;\nreturn (uint8_t *)&netEmpty;\n'
INIT = 'tv.tv_sec = 15;\ntv.tv_usec = 0;\nFD_ZERO(&fds);\nFD_SET(netSock, &fds);\n*len = 0;\n'
HDR = 'uint8_t hdr[4];\n'
FT = 'fd_set fds;\nstruct timeval tv;\n'
LOCALS = 'uint8_t *buf;\nint size, got, r;\n'


def loop(sel, form):
    if sel == 'side':
        s = 'if ((r = select(0, &fds, NULL, NULL, &tv)) == SOCKET_ERROR || r == 0) {\n'
    else:
        s = SEL1 + 'if (' + TEST + ') {\n'
    body = s + 'log_printf(0, "timeout waiting for data, error %d' + BS + 'n", WSAGetLastError());\n' + FREE + 'return NULL;\n}\n'
    body += 'r = recv(netSock, (char *)buf + got, size - got, 0);\nif (r == SOCKET_ERROR) {\n' + NLS
    body += 'log_printf(0, "could not receive data on socket, error %d' + BS + 'n",\nWSAGetLastError());\n' + FREE + 'return NULL;\n}\n'
    body += 'got += r;\nif (verbose)\n\tprintf("received 0x%08x of 0x%08x' + BS + 'r", got, size);\n'
    if form == 'while':
        return 'while (got < size) {\n' + body + '}\n'
    return 'if (size > 0)\ndo {\n' + body + '} while (got < size);\n'


def ta(sel, form):
    return 'buf = calloc(size, 1);\nif (verbose)\n\tprintf("waiting for 0x%x bytes' + BS + 'n", size);\ngot = 0;\n' + loop(sel, form)


LOG = 'log_printf(0, "received only %x of %x bytes! fail' + BS + 'n", got, size);\n'


def tb(tail):
    nl = NLS
    if tail == 'ret':
        return nl + 'if (got == size) {\n*len = size;\nreturn buf;\n}\n' + nl + LOG + FREE + 'return NULL;\n'
    if tail == 'fall':
        return nl + 'if (got == size) {\n*len = size;\nreturn buf;\n}\n' + nl + LOG + FREE
    if tail == 'ne':
        return nl + 'if (got != size) {\n' + nl + LOG + FREE + 'return NULL;\n}\n*len = size;\nreturn buf;\n'
    if tail == 'var':  # one return value carried in buf
        return nl + 'if (got == size) {\n*len = size;\nreturn buf;\n}\n' + nl + LOG + FREE + 'buf = NULL;\nreturn buf;\n'


def after_size(ss, T, sized=True):
    """the code after size is known; T may fall out."""
    if ss == 'flip':
        return 'if (size == -1)\nreturn NULL;\nif (size) {\n' + T + '}\n' + ZERO
    if ss == 'old':
        return 'if (size == -1)\nreturn NULL;\nif (size == 0) {\n' + ZERO + '}\n' + T
    if ss == 'else':
        return 'if (size == -1)\nreturn NULL;\nif (size) {\n' + T + '} else {\n' + ZERO + '}\n'
    if ss == 'nest':  # size != -1 wraps both
        return 'if (size != -1) {\nif (size) {\n' + T + '} else {\n' + ZERO + '}\n}\n'


def src(hn, hs, fs, ss, tail, sel, form):
    TA, TB = ta(sel, form), tb(tail)
    falls = tail == 'fall'
    if ss == 'flip' and falls:
        return None
    final_null = falls or ss == 'nest' or hn != 'neg'
    tailout = fs == 'tailout'
    if tailout and (ss in ('flip', 'nest') or hn != 'neg'):
        return None  # the failure paths would fall into the tail with got unset
    T = TA if tailout else TA + TB
    rest = after_size(ss, T)
    # head
    if hs == 'fn' or hs == 'blk' or hs == 'blk1':
        if hs == 'blk1':
            size1, size2 = 'size = getBeU32(hdr);\nif (size == -1)\nreturn NULL;\n', ''
            rest = rest.replace('if (size == -1)\nreturn NULL;\n', '')
            if ss == 'nest':
                return None
        else:
            size1, size2 = 'size = getBeU32(hdr);\n', ''
    recv = 'r = recv(netSock, (char *)hdr, 4, 0);\n'
    if hs == 'fn':
        if hn == 'neg':
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + 'return NULL;\n}\n' + recv + 'if (' + TEST + ') {\n' + LOG2 + 'return NULL;\n}\n' + size1 + rest
        elif hn == 'pos':
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + '} else {\n' + recv + 'if (' + TEST + ') {\n' + LOG2 + '} else {\n' + size1 + rest + '}\n}\n'
        else:  # recv only nested
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + 'return NULL;\n}\n' + recv + 'if (' + TEST + ') {\n' + LOG2 + '} else {\n' + size1 + rest + '}\n'
    elif hs in ('blk', 'blk1'):
        if hn == 'neg':
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + 'return NULL;\n}\n{\n' + HDR + recv + 'if (' + TEST + ') {\n' + LOG2 + 'return NULL;\n}\n' + size1 + '}\n' + rest
        else:
            return None
    elif hs == 'rest':  # hdr's block holds everything after the select
        if hn == 'neg':
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + 'return NULL;\n}\n{\n' + HDR + recv + 'if (' + TEST + ') {\n' + LOG2 + 'return NULL;\n}\nsize = getBeU32(hdr);\n' + rest + '}\n'
        elif hn == 'pos':
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + '} else {\n' + HDR + recv + 'if (' + TEST + ') {\n' + LOG2 + '} else {\nsize = getBeU32(hdr);\n' + rest + '}\n}\n'
        else:
            head = SEL1 + 'if (' + TEST + ') {\n' + LOG1 + 'return NULL;\n}\n' + recv.replace('r = recv', 'r = recv') + ''
            return None
    top = 'uint8_t *netRecvVerbose(int *len, uint32_t verbose)\n{\n'
    out = top + LOCALS
    if hs == 'fn':
        out = top + HDR + LOCALS
    if ss == 'flip':
        # the zero arm can leave the fds scope: move it out for fs=blk
        if fs == 'blk':
            i = head.rindex(ZERO)
            head = head[:i] + head[i + len(ZERO):]
            return out + '{\n' + FT + INIT + head + '}\n' + ZERO + ('return NULL;\n' if final_null and 0 else '') + '}\n'
        return out + FT + INIT + head + ('return NULL;\n' if final_null else '') + '}\n'
    if fs == 'blk':
        return out + '{\n' + FT + INIT + head + '}\nreturn NULL;\n}\n'
    if fs == 'tailout':
        if tail in ('ret', 'ne', 'var'):
            return out + '{\n' + FT + INIT + head + '}\n' + TB + '}\n'
        return out + '{\n' + FT + INIT + head + '}\n' + TB + 'return NULL;\n}\n'
    return out + FT + INIT + head + ('return NULL;\n' if final_null else '') + '}\n'


def variants():
    forms = ['while'] + (['do'] if os.environ.get('NR80_LOOP') == 'do' else [])
    sels = ['plain'] + (['side'] if os.environ.get('NR80_SIDE') else [])
    for k in itertools.product(('neg', 'pos', 'rpos'), ('fn', 'blk', 'blk1', 'rest'), ('fn', 'blk', 'tailout'), ('flip', 'old', 'else', 'nest'), ('ret', 'fall', 'ne', 'var'), sels, forms):
        s = src(*k)
        if s is not None:
            yield '|'.join(k), s
