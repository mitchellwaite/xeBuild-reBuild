"""fl8g.py: findKey and matchAt with the type axes.  KF dropped; parseIni as in src.  Random sample of the product.
  python fl8g.py N [seed]
Labels are the axis values joined by ,; python fl8g.py show <label> prints the diff."""
import itertools, random, sys
import fl7lib as K, fl8lib as T

AX = dict(
    form=['plain_p', 'plain_b', 'match'],
    ret=['int', 'long', 'char', 'unsigned char', 'unsigned', 'uint32_t'],
    mret=['2ret', 'ok', 'r0'],
    buf=['unsigned char *', 'const unsigned char *', 'char *', 'const char *'],
    key=['const char *', 'char *', 'const unsigned char *', 'unsigned char *'],
    mbuf=['unsigned char *', 'const unsigned char *', 'char *', 'const char *'],
    mkey=['const char *', 'char *', 'const unsigned char *'],
    ity=['int', 'long', 'unsigned', 'uint32_t', 'size_t'],
    jty=['int', 'long', 'unsigned', 'uint32_t', 'size_t'],
    lty=['int', 'long', 'unsigned', 'uint32_t', 'size_t'],
    mlty=['int', 'long', 'unsigned', 'size_t'],
    fret=['int', 'long'],
    cmp=['buf[i] == key[0]', 'key[0] == buf[i]', 'buf[i] == (unsigned char)key[0]', '(char)buf[i] == key[0]'],
    tail=['q', 'n', 'c', 'qc'],
)


def src(c):
    b, k = c['buf'], c['key']
    sub = 'buf[i + len]'
    tails = {
        'q': "\t\t\t\t%sq = &buf[i + len];\n\n\t\t\t\tif (*q != 0)\n\t\t\t\t\treturn i + len;\n" % b.replace('const ', ''),
        'n': "\t\t\t\tif (buf[i + len] != 0)\n\t\t\t\t\treturn i + len;\n",
        'c': "\t\t\t\tif (buf[i + len] == 0)\n\t\t\t\t\tcontinue;\n\t\t\t\treturn i + len;\n",
        'qc': "\t\t\t\tchar v = buf[i + len];\n\n\t\t\t\tif (v != 0)\n\t\t\t\t\treturn i + len;\n",
    }
    tl = tails[c['tail']]
    pre = ''
    if c['form'] == 'match':
        rets = {
            '2ret': "\tif (j == len)\n\t\treturn 1;\n\treturn 0;\n",
            'r0': "\tif (j != len)\n\t\treturn 0;\n\treturn 1;\n",
            'ok': None,
        }
        mr = rets[c['mret']]
        decl = "\t%s j;\n" % c['jty']
        if mr is None:
            decl += "\t%s ok = 0;\n" % c['ret']
            mr = "\tif (j == len)\n\t\tok = 1;\n\treturn ok;\n"
        pre = ("static %s matchAt(%sp, %skey, %s len)\n{\n%s\n\tfor (j = 0; j < len; j++)\n\t\tif (p[j] != key[j])\n\t\t\tj = len + 1;\n%s}\n\n"
               % (c['ret'], c['mbuf'], c['mkey'], c['mlty'], decl, mr))
        body = "\t\t\tif (matchAt(&buf[i], key, len)) {\n" + tl + "\t\t\t}\n"
        d = "\t%s i;\n\t%s len;\n" % (c['ity'], c['lty'])
    else:
        ps = {'plain_p': "\t\t\tp = &buf[i];\n\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (p[j] != key[j])\n\t\t\t\t\tj = len + 1;\n",
              'plain_b': "\t\t\tfor (j = 0; j < len; j++)\n\t\t\t\tif (buf[i + j] != key[j])\n\t\t\t\t\tj = len + 1;\n"}
        body = ps[c['form']] + "\t\t\tif (j == len) {\n" + tl + "\t\t\t}\n"
        d = "\t%s i;\n\t%s j;\n\t%s len;\n" % (c['ity'], c['jty'], c['lty'])
        if c['form'] == 'plain_p':
            d += "\t%sp;\n" % b
    fn = ("/* getters' own helper (not memFindStr) */\n" + pre + "static %s findKey(unsigned char *buf0, %skey)\n{\n%s\t%sbuf = buf0;\n\n\tlen = strlen(key);\n" % (c['fret'], k, d, b)
          if 0 else
          "/* getters' own helper (not memFindStr) */\n" + pre + "static %s findKey(%sbuf, %skey)\n{\n%s\tlen = strlen((const char *)key);\n" % (c['fret'], b, k, d))
    fn += "\tfor (i = 0; i < xb.iniSize - len; i++) {\n\t\tif (%s) {\n%s\t\t}\n\t}\n\treturn -1;\n}\n" % (c['cmp'], body)
    return K.fk(fn)


BASE = dict(form='match', ret='int', mret='2ret', buf='unsigned char *', key='const char *', mbuf='unsigned char *', mkey='const char *',
            ity='int', jty='int', lty='int', mlty='int', fret='int', cmp='buf[i] == key[0]', tail='q')


def lab(c):
    return ','.join(str(AX[k].index(c[k])) for k in AX)


def unlab(s):
    return {k: AX[k][int(x)] for k, x in zip(AX, s.split(','))}


def singles():
    V = {}
    for form in AX['form']:
        for k in AX:
            for v in AX[k]:
                c = dict(BASE, form=form)
                c[k] = v
                V[lab(c)] = src(c)
    return V


def sample(n):
    V = {}
    while len(V) < n:
        c = dict(BASE)
        p = random.choice([.15, .3, .5])
        for k in AX:
            if random.random() < p:
                c[k] = random.choice(AX[k])
        V[lab(c)] = src(c)
    return V


def nice(lb):
    c = unlab(lb)
    return {k: v for k, v in c.items() if BASE[k] != v}


if __name__ == '__main__':
    if sys.argv[1] == 'show':
        K.diff(src(unlab(sys.argv[2])))
    elif sys.argv[1] == 'single':
        rs = T.run(singles(), 'g_single', 0)
        for r in rs[:40]:
            print(r[0], r[1], nice(r[3]))
    else:
        random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
        rs = T.run(sample(int(sys.argv[1])), 'g', 0)
        for r in rs[:30]:
            print(r[0], r[1], nice(r[3]))
