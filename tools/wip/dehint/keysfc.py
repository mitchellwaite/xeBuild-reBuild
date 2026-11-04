"""keysfc.py: fcrtEncrypt source shapes without pure or expect.

Every shape is plain C and replaces the function in src/keys.c.  Reports fncmp-like
diff lines for _fcrtEncrypt and any whole-object match.  Axes: order of the size
check (early return, else chain, flag), the offset check, the hash check."""
import itertools, re, sys
from multiprocessing.pool import ThreadPool
import keyslib as K

HEAD = """void fcrtEncrypt(uint8_t *fcrt, uint32_t size)
{
	uint8_t iv[16];
	uint8_t hash[20];
	uint32_t off;
	XECRYPT_AES_STATE aes;
%s
	memcpy(iv, fcrt + 256, 16);
%s
}

"""
LS = 'log_printf(0, "****** ERROR: FCRT encrypt invalid size!\\n");'
LO = 'log_printf(1, "**** ERROR: FCRT encrypt invalid offset!\\n");'
LV = 'log_printf(0, "****** WARNING: FCRT data appears to be crypted or damaged!! Skipping encryption.\\n");'
SHA = 'XeCryptSha(fcrt + off, 0x4000 - off, NULL, 0, NULL, 0, hash, 20);'
AES = 'XeCryptAesKey(&aes, xb.cpuKey);\nXeCryptAesCbc(&aes, fcrt + off, 0x4000 - off, fcrt + off, iv, 1);'
GET = 'off = getBeU32(fcrt + 284);'
MC = 'memcmp(fcrt + 300, hash, 20)'
VF = 'verifyFcrt(fcrt, 0x4000)'

SHAPES = {}


def add(name, decl, body):
    SHAPES[name] = (decl, body)


add('base', '', f"""if (size != 0x4000) {{ {LS} return; }}
{GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
if ({MC} && {VF} != 1) {{ {LV} return; }}
{AES}""")

add('elsechain', '', f"""if (size != 0x4000) {LS}
else {{ {GET}
if (off >= 0x4000) {LO}
else {{ {SHA}
if ({MC} && {VF} != 1) {LV}
else {{ {AES} }} }} }}""")

add('elsechain2', '', f"""if (size != 0x4000) {LS}
else {{ {GET}
if (off >= 0x4000) {LO}
else {{ {SHA}
if (!{MC} || {VF} == 1) {{ {AES} }}
else {LV} }} }}""")

add('mix1', '', f"""if (size != 0x4000) {{ {LS} return; }}
{GET}
if (off >= 0x4000) {LO}
else {{ {SHA}
if ({MC} && {VF} != 1) {LV}
else {{ {AES} }} }}""")

add('mix2', '', f"""if (size != 0x4000) {LS}
else {{ {GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
if ({MC} && {VF} != 1) {{ {LV} return; }}
{AES} }}""")

add('mix3', '', f"""if (size != 0x4000) {{ {LS} return; }}
{GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
if ({MC} && {VF} != 1) {LV}
else {{ {AES} }}""")

add('flagbad', 'int bad = 0;', f"""if (size != 0x4000) {{ {LS} bad = 1; }}
if (!bad) {{ {GET}
if (off >= 0x4000) {{ {LO} bad = 1; }} }}
if (!bad) {{ {SHA}
if ({MC} && {VF} != 1) {{ {LV} bad = 1; }} }}
if (!bad) {{ {AES} }}""")

add('flagok', 'int ok = 1;', f"""if (size != 0x4000) {{ {LS} ok = 0; }}
if (ok) {{ {GET}
if (off >= 0x4000) {{ {LO} ok = 0; }} }}
if (ok) {{ {SHA}
if ({MC} && {VF} != 1) {{ {LV} ok = 0; }} }}
if (ok) {{ {AES} }}""")

add('flag_size', 'int ok = 1;', f"""if (size != 0x4000) {{ {LS} ok = 0; }}
if (ok) {{ {GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
if ({MC} && {VF} != 1) {{ {LV} return; }}
{AES} }}""")

add('flag_size2', 'int ok = 1;', f"""if (size != 0x4000) {{ {LS} ok = 0; }}
if (!ok) return;
{GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
if ({MC} && {VF} != 1) {{ {LV} return; }}
{AES}""")

add('flag_off', '', f"""if (size != 0x4000) {{ {LS} return; }}
{GET}
if (off >= 0x4000) {LO}
if (off < 0x4000) {{ {SHA}
if ({MC} && {VF} != 1) {{ {LV} return; }}
{AES} }}""")

add('off_set', '', f"""if (size != 0x4000) {{ {LS} off = 0x4000; }}
else {GET}
if (off >= 0x4000) {{ if (size == 0x4000) {LO} return; }}
{SHA}
if ({MC} && {VF} != 1) {{ {LV} return; }}
{AES}""")

add('off_zero', 'int ok = 0;', f"""if (size != 0x4000) {LS}
else {{ {GET}
if (off >= 0x4000) {LO}
else {{ {SHA}
if (!{MC} || {VF} == 1) ok = 1;
else {LV} }} }}
if (ok) {{ {AES} }}""")

add('ok_hash', 'int ok;', f"""if (size != 0x4000) {{ {LS} return; }}
{GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
ok = !{MC} || {VF} == 1;
if (!ok) {{ {LV} return; }}
{AES}""")

add('ok_hash2', 'int ok = 1;', f"""if (size != 0x4000) {{ {LS} return; }}
{GET}
if (off >= 0x4000) {{ {LO} return; }}
{SHA}
if ({MC}) {{ if ({VF} != 1) {{ {LV} ok = 0; }} }}
if (ok) {{ {AES} }}""")

add('ok_all', 'int ok = 1;', f"""if (size == 0x4000) {{ {GET}
if (off < 0x4000) {{ {SHA}
if ({MC} && {VF} != 1) ok = 0;
}} else ok = 2;
}} else ok = 3;
if (ok == 3) {LS}
else if (ok == 2) {LO}
else if (!ok) {LV}
else {{ {AES} }}""")


def fnreplace(base, text):
    i = base.index('void fcrtEncrypt(')
    j = base.index('void shaHeader(')
    return base[:i] + text + base[j:]


def run(base, shapes, tagprefix='fc', flags=None):
    items = list(shapes.items())

    def one(a):
        i, (name, (decl, body)) = a
        s = fnreplace(base, HEAD % (('\t' + decl) if decl else '', body))
        o = K.compile(s, flags, '%s%d' % (tagprefix, i))
        return name, K.same(o), (K.fndiff(o) if o else {'fail': 9999})
    with ThreadPool(4) as p:
        return p.map(one, list(enumerate(items)))


if __name__ == '__main__':
    base = K.base()
    variants = {
        'nopure': base.replace('uint32_t getBeU32(const uint8_t *p) __attribute__((pure));\n', ''),
        'pure': base,
    }
    for vn, b in variants.items():
        print('==', vn)
        for name, ok, d in sorted(run(b, SHAPES), key=lambda r: sum(r[2].values())):
            print(' ', 'MATCH' if ok else '', name, d)
