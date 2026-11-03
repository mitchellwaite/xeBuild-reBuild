"""ceDecrypt: the brief's remaining axes, in product: head spelling, hash test's form, key's block, len/buf's block."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('gen_ce1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ce1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FN = 'ceDecrypt'
ind = g.ind
CRYPT_L = g.BODY.splitlines(True)[:3]
CRYPT = ''.join(CRYPT_L)
OK = 'log_printf(1, "%c%c hash check OK! Decryption successful!\\n", buf[0], buf[1]);\n'
ERR = 'log_printf(0, "***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\\n", buf[0], buf[1]);\nfree(buf);\n'
WARN = 'log_printf(0, "***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\\n", buf[0]);\n'
SET = 'if (outLen)\n\t*outLen = len;\n'

HASH = {
    'nest': 'if (hash) {\n\tif (blCheckHash(buf, len, hash)) {\n' + ind(OK + SET + 'return buf;\n', 2) + '\t}\n' + ind(ERR) + '} else {\n' + ind(WARN + SET + 'return buf;\n') + '}\n',
    'nest_else': 'if (hash) {\n\tif (blCheckHash(buf, len, hash)) {\n' + ind(OK + SET + 'return buf;\n', 2) + '\t} else {\n' + ind(ERR, 2) + '\t}\n} else {\n' + ind(WARN + SET + 'return buf;\n') + '}\n',
    'ret0': 'if (hash) {\n\tif (blCheckHash(buf, len, hash)) {\n' + ind(OK + SET + 'return buf;\n', 2) + '\t}\n' + ind(ERR + 'return 0;\n') + '} else {\n' + ind(WARN + SET + 'return buf;\n') + '}\n',
    'and': 'if (hash && blCheckHash(buf, len, hash)) {\n' + ind(OK + SET + 'return buf;\n') + '}\nif (hash) {\n' + ind(ERR) + '} else {\n' + ind(WARN + SET + 'return buf;\n') + '}\n',
    'flag': 'int ok = 1;\n\nif (hash) {\n\tok = blCheckHash(buf, len, hash);\n\tif (ok)\n' + ind(OK, 2) + '\telse\n\t{\n' + ind(ERR, 2) + '\t}\n} else\n' + ind(WARN.rstrip('\n') + '\n') + 'if (ok) {\n' + ind(SET + 'return buf;\n') + '}\n',
}
HEADS = {
    'and': lambda inner, nl: 'if (bl && hmacKey) {\n' + ind(inner) + '} else\n\t' + nl + '\n',
    'ne': lambda inner, nl: 'if (bl != 0 && hmacKey != 0) {\n' + ind(inner) + '} else\n\t' + nl + '\n',
    'nest': lambda inner, nl: 'if (bl) {\n\tif (hmacKey) {\n' + ind(inner, 2) + '\t} else\n\t\t' + nl + '\n} else\n\t' + nl + '\n',
    'flag': lambda inner, nl: 'int have = bl && hmacKey;\n\nif (have) {\n' + ind(inner) + '} else\n\t' + nl + '\n',
}
KD = 'uint8_t key[16];\n'
DL = 'uint8_t *buf;\nuint32_t len;\n'


def build(head, hsh, kscope, lscope):
    arm = CRYPT + HASH[hsh]
    if kscope == 'crypt':
        # key in a block of its own around the crypto
        arm = '{\n\t' + KD + '\n' + ind(CRYPT) + '}\n' + HASH[hsh]
    elif kscope == 'buf':
        arm = KD + '\n' + arm
    body = 'len = BL_SIZE(bl);\nbuf = calloc(len, 1);\nif (buf) {\n' + ind(arm) + '} else\n\t' + g.ALLOC + '\n'
    if lscope == 'magic' and kscope == 'magic':
        body = DL + KD + '\n' + body
    elif lscope == 'magic':
        body = DL + '\n' + body
    elif kscope == 'magic':
        body = KD + '\n' + body
    inner = "if (BL_MAGIC(bl, 'E')) {\n" + ind(body) + '} else\n\t' + g.MAGICLOG + '\n'
    if kscope == 'head':
        inner = KD + '\n' + inner
    if lscope == 'head':
        inner = DL + '\n' + inner
    fn = HEADS[head](inner, g.NULLLOG) + 'return 0;\n'
    top = ''
    if kscope == 'fn':
        top += KD
    if lscope == 'fn':
        top += DL
    if top:
        fn = top + '\n' + fn
    return g.HEAD + ind(fn) + '}\n'


def variants():
    for h, s, k, l in itertools.product(HEADS, HASH, ('magic', 'head', 'fn', 'buf', 'crypt'), ('magic', 'head', 'fn')):
        yield ('head=%s hash=%s key=%s len=%s' % (h, s, k, l), build(h, s, k, l))
