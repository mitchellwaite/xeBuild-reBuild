"""fl9j.py: natural spellings of the one-pop-fewer index in bl's log, err or copy lines, at T1,T2,T3.  Axis bl=<form>; also pre, ff from fl6lib."""
import os, sys
os.environ.setdefault('FLA', 'a9')
import fllib as L, fl6lib as F, fl8lib as G

LOG = 'log_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, xb.files[blOrder[i]].name, xb.files[blOrder[i]].crc);'
ERR = 'log_printf(0, "\\n******* ERROR: crc data for file \'%s\' in ini is incorrect size!\\n", xb.files[blOrder[i]].name);'
CPY = 'strncpy(xb.files[blOrder[i]].name, (char *)p, len);'
assert LOG in G.S0 and ERR in G.S0 and CPY in G.S0


def rep(old, new):
    return lambda s: F.secsub(s, 'bl', old, new)


def loc(ty, name='file'):
    return rep(LOG, '%s %s = blOrder[i];\n\n\t\t\tlog_printf(1, "found (%%d) \'%%s\' crc: 0x%%08x\\n", i + 1, xb.files[%s].name, xb.files[%s].crc);' % (ty, name, name, name))


def inblock(ty):
    """a block around the log line, the local inside"""
    return rep(LOG, '{\n\t\t\t\t%s file = blOrder[i];\n\n\t\t\t\tlog_printf(1, "found (%%d) \'%%s\' crc: 0x%%08x\\n", i + 1, xb.files[file].name, xb.files[file].crc);\n\t\t\t}' % ty)


def top(ty):
    """declared with the function's locals"""
    def f(s):
        s = F.secsub(s, 'bl', LOG, 'file = blOrder[i];\n\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, xb.files[file].name, xb.files[file].crc);')
        return L.sub(s, "\tchar label[50];\n", "\t%s file;\n\tchar label[50];\n" % ty)
    return f


def entp(line, fmt):
    return rep(line, fmt)


FORMS = {
    'none': lambda s: s,
    'u32': loc('uint32_t'),
    'uns': loc('unsigned int'),
    'ulong': loc('unsigned long'),
    'sizet': loc('size_t'),
    'blk': inblock('uint32_t'),
    'top': top('uint32_t'),
    'topsz': top('size_t'),
    'e': rep(LOG, 'e = &xb.files[blOrder[i]];\n\t\t\tlog_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, e->name, e->crc);'),
    'cast': rep(LOG, 'log_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, xb.files[(uint32_t)blOrder[i]].name, xb.files[(uint32_t)blOrder[i]].crc);'),
    'nameonly': rep(LOG, 'log_printf(1, "found (%d) \'%s\' crc: 0x%08x\\n", i + 1, xb.files[(uint32_t)blOrder[i]].name, xb.files[blOrder[i]].crc);'),
    'errloc': rep(ERR, '{\n\t\t\t\t\t\tuint32_t file = blOrder[i];\n\n\t\t\t\t\t\tlog_printf(0, "\\n******* ERROR: crc data for file \'%s\' in ini is incorrect size!\\n", xb.files[file].name);\n\t\t\t\t\t}'),
    'cpyloc': rep(CPY, 'file = blOrder[i];\n\t\t\tstrncpy(xb.files[file].name, (char *)p, len);'),
}


def efix(k, s):
    if k == 'e':
        s = L.sub(s, "\tchar label[50];\n", "\tstruct fileent *e;\n\tchar label[50];\n")
    if k == 'cpyloc':
        s = L.sub(s, "\tchar label[50];\n", "\tuint32_t file;\n\tchar label[50];\n")
    return s


G.E['bl'] = {k: (lambda k, fn: lambda s: efix(k, fn(s)))(k, fn) for k, fn in FORMS.items()}
G.E['pre'] = F.E['pre']
G.E['ff'] = F.E['ff']

if __name__ == '__main__':
    V = {}
    for k in FORMS:
        for x in ['', 'pre=in', 'ff=none', 'pre=in,ff=none']:
            lb = 'T1,T2,T3|bl=%s%s' % (k, ',' + x if x else '')
            V[lb] = G.state(lb)
    rs = G.run(V, 'j', 60)
