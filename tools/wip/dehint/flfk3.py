"""flfk3.py: getter shapes per getter over findKey tail forms (no unreachable, no pin).
Prints each getter's best forms."""
import itertools, re, sys
import fllib as L
import flfk2 as K

s = L.base()
HEADEND = s.index('#define FIND')
PIN = '	__asm__("" :: "b"(val));\n'

BOOL = {
 'orig': '''{ int off; char *val; if (xb.iniSize == 0) return def; off = FIND; if (off == -1) return def; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return 1; if (strnicmp(val, "false", 5) == 0) return 0; return def; }''',
 'nestall': '''{ int off; char *val; if (xb.iniSize != 0) { off = FIND; if (off != -1) { val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return 1; if (strnicmp(val, "false", 5) == 0) return 0; } } return def; }''',
 'noval': '''{ int off; if (xb.iniSize == 0) return def; off = FIND; if (off == -1) return def;
 if (strnicmp((char *)&xb.iniBuf[off], "true", 4) == 0) return 1; if (strnicmp((char *)&xb.iniBuf[off], "false", 5) == 0) return 0; return def; }''',
 'plus': '''{ int off; char *val; if (xb.iniSize == 0) return def; off = FIND; if (off == -1) return def; val = (char *)xb.iniBuf + off;
 if (strnicmp(val, "true", 4) == 0) return 1; if (strnicmp(val, "false", 5) == 0) return 0; return def; }''',
 'ret': '''{ int off; char *val; long ret = def; if (xb.iniSize == 0) return ret; off = FIND; if (off == -1) return ret; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) ret = 1; else if (strnicmp(val, "false", 5) == 0) ret = 0; return ret; }''',
 'ret2': '''{ int off; char *val; long ret = def; if (xb.iniSize != 0) { off = FIND; if (off != -1) { val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) ret = 1; else if (strnicmp(val, "false", 5) == 0) ret = 0; } } return ret; }''',
 'else': '''{ int off; char *val; if (xb.iniSize == 0) return def; off = FIND; if (off == -1) return def; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return 1; else if (strnicmp(val, "false", 5) == 0) return 0; else return def; }''',
 'loc': '''{ if (xb.iniSize == 0) return def; { int off = FIND; if (off == -1) return def; { char *val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return 1; if (strnicmp(val, "false", 5) == 0) return 0; return def; } } }''',
 'neq': '''{ int off; char *val; if (xb.iniSize == 0) return def; off = FIND; if (off == -1) return def; val = (char *)&xb.iniBuf[off];
 if (!strnicmp(val, "true", 4)) return 1; if (!strnicmp(val, "false", 5)) return 0; return def; }''',
 'lt': '''{ int off; char *val; if (xb.iniSize == 0) return def; off = FIND; if (off < 0) return def; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return 1; if (strnicmp(val, "false", 5) == 0) return 0; return def; }''',
}
INV = {
 'orig': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return NULL; if (strnicmp(val, "false", 5) != 0) return val; return NULL; }''',
 'ret': '''{ int off; char *val, *ret = NULL; if (xb.iniSize == 0) return ret; off = FIND; if (off == -1) return ret; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) != 0 && strnicmp(val, "false", 5) != 0) ret = val; return ret; }''',
 'nest': '''{ int off; char *val; if (xb.iniSize != 0) { off = FIND; if (off != -1) { val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) != 0) { if (strnicmp(val, "false", 5) != 0) return val; } } } return NULL; }''',
 'and': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) != 0 && strnicmp(val, "false", 5) != 0) return val; return NULL; }''',
 'n1': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) != 0) { if (strnicmp(val, "false", 5) != 0) return val; } return NULL; }''',
 'n2': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return NULL; if (strnicmp(val, "false", 5) == 0) return NULL; return val; }''',
 'n3': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0 || strnicmp(val, "false", 5) == 0) return NULL; return val; }''',
 'n4': '''{ int off; char *val = NULL; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) val = NULL; else if (strnicmp(val, "false", 5) == 0) val = NULL; return val; }''',
 'n5': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) val = NULL; else if (strnicmp(val, "false", 5) == 0) val = NULL; return val; }''',
 'n6': '''{ int off; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL;
 if (strnicmp((char *)&xb.iniBuf[off], "true", 4) == 0) return NULL; if (strnicmp((char *)&xb.iniBuf[off], "false", 5) != 0) return (char *)&xb.iniBuf[off]; return NULL; }''',
 'n7': '''{ int off; char *val; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; val = (char *)xb.iniBuf + off;
 if (strnicmp(val, "true", 4) == 0) return NULL; if (strnicmp(val, "false", 5) != 0) return val; return NULL; }''',
 'n8': '''{ int off; if (xb.iniSize == 0) return NULL; off = FIND; if (off == -1) return NULL; { char *val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return NULL; if (strnicmp(val, "false", 5) != 0) return val; return NULL; } }''',
 'n9': '''{ int off; char *val; if (xb.iniSize != 0) { off = FIND; if (off != -1) { val = (char *)&xb.iniBuf[off];
 if (strnicmp(val, "true", 4) == 0) return NULL; if (strnicmp(val, "false", 5) != 0) return val; } } return NULL; }''',
}


def repl(src, sig, body):
    i = src.index(sig)
    j = src.index('\n}\n', i) + 3
    return src[:i] + sig + '\n' + body + '\n' + src[j:]


if __name__ == '__main__':
    V = {}
    for chk in ['nest', 'eq0']:
        base = K.fk('buf', 'keyfirst', 'set', 'p', chk, 'for')
        base = base.replace(PIN, '')
        for n, b in BOOL.items():
            V['B_%s_%s' % (chk, n)] = repl(base, 'long getIniBool(const char *key, int def)', b)
        for n, b in INV.items():
            V['I_%s_%s' % (chk, n)] = repl(base, 'char *iniBoolInvalid(const char *key)', b)
    rs = L.sweep(V, prefix='fk3', show=0)
    for n, (sc, st, fd, sd) in rs:
        fn = 'getIniBool' if n[0] == 'B' else 'iniBoolInvalid'
        print(n, fd.get(fn, 0), {k: v for k, v in fd.items() if k != fn and k != 'iniU32Invalid' and k != 'getIniU32'})
