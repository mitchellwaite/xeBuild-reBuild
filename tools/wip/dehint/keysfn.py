"""keysfn.py: helpers to replace one function of src/keys.c with a text template.

python keysfn.py <fn> <template file> [out.c]: replace fn, compile, print the score;
the replaced file goes to out.c (default build/keys/v/<fn>.c)."""
import difflib, os, re, sys
import keyslib as K

ORDER = re.compile(r'^(?:void|int|uint32_t|uint16_t|short|static int|inline short) \w+\(', re.M)
NOPURE = 'uint32_t getBeU32(const uint8_t *p) __attribute__((pure));\n'


def replace_fn(base, name, text):
    m = re.search(r'^[a-z].* \*?%s\(.*\)\n\{' % re.escape(name), base, re.M)
    if not m:
        raise SystemExit('no fn ' + name)
    # the function ends at the first line that is exactly a closing brace
    e = base.index('\n}\n', m.end()) + 3
    while e < len(base) and base[e] == '\n':
        e += 1
    return base[:m.start()] + text + base[e:]


if __name__ == '__main__':
    fn, tpl = sys.argv[1:3]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(K.OUT, fn + '.c')
    base = K.base()
    if os.environ.get('NOPURE'):
        base = base.replace(NOPURE, '')
    s = replace_fn(base, fn, open(tpl, newline='').read())
    open(out, 'w', newline='\n').write(s)
    fl = os.environ.get('KEYSFLAGS')
    o = K.compile(s, fl.split() if fl else None, 'fn_' + fn)
    print('MATCH' if K.same(o) else 'differ', K.fndiff(o))
    if os.environ.get('DIFF'):
        for ln in difflib.unified_diff(K.dis(K.REF)['_' + fn], K.dis(o)['_' + fn], lineterm='', n=1):
            print(ln)
