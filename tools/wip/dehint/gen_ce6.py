"""ceDecrypt: a first test of buf with an arm that holds only a PHI (no code once threaded), like the hinted `if (buf) asm`:
n = len only if buf, then used in the second test's arm."""
import importlib.util, itertools, os, re
spec = importlib.util.spec_from_file_location('gen_ce1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ce1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FN = 'ceDecrypt'
ind = g.ind
LEN = 'len = BL_SIZE(bl);\nbuf = calloc(len, 1);\n'

SETS = {
    'if0': 'uint32_t n = 0;\n\n' + LEN + 'if (buf)\n\tn = len;\n',
    'cond': 'uint32_t n;\n\n' + LEN + 'n = buf ? len : 0;\n',
    'ifelse': 'uint32_t n;\n\n' + LEN + 'if (buf)\n\tn = len;\nelse\n\tn = 0;\n',
    'clear': 'uint32_t n;\n\n' + LEN + 'n = len;\nif (!buf)\n\tn = 0;\n',
}
# which uses of len take n
USES = {
    'all': lambda b: b.replace('memcpy(buf, bl, len)', 'memcpy(buf, bl, n)').replace('len - 32', 'n - 32').replace('buf, len, hash', 'buf, n, hash').replace('*outLen = len', '*outLen = n'),
    'outlen': lambda b: b.replace('*outLen = len', '*outLen = n'),
    'copy': lambda b: b.replace('memcpy(buf, bl, len)', 'memcpy(buf, bl, n)'),
    'crypt': lambda b: b.replace('len - 32', 'n - 32'),
    'hash': lambda b: b.replace('buf, len, hash', 'buf, n, hash'),
}
TAILS = {
    'else': lambda body: 'if (buf) {\n' + ind(body) + '} else\n\t' + g.ALLOC + '\n',
    'after': lambda body: 'if (buf) {\n' + ind(body) + '\treturn 0;\n}\n' + g.ALLOC + '\n',
}
# the variable's own value through the first test: hmacKey instead of len
KEYSETS = {
    'key_if0': 'const uint8_t *k = 0;\n\n' + LEN + 'if (buf)\n\tk = hmacKey;\n',
    'key_cond': 'const uint8_t *k;\n\n' + LEN + 'k = buf ? hmacKey : 0;\n',
}


def wrap(decl, inner):
    d = 'uint8_t *buf;\nuint32_t len;\nuint8_t key[16];\n'
    return g.HEAD + ind('if (bl && hmacKey) {\n' + ind("if (BL_MAGIC(bl, 'E')) {\n" + ind(d + decl + inner) + '} else\n\t' + g.MAGICLOG + '\n') + '} else\n\t' + g.NULLLOG + '\nreturn 0;\n') + '}\n'


def split(s):
    a, b = s.split('\n\n', 1)
    return a + '\n\n', b


def variants():
    for (sn, s), (un, u), (tn, t) in itertools.product(SETS.items(), USES.items(), TAILS.items()):
        d, i = split(s)
        yield ('%s %s %s' % (sn, un, tn), wrap(d, i + t(u(g.BODY))))
    for (sn, s), (tn, t) in itertools.product(KEYSETS.items(), TAILS.items()):
        d, i = split(s)
        yield ('%s %s' % (sn, tn), wrap(d, i + t(g.BODY.replace('XeCryptHmacSha(hmacKey', 'XeCryptHmacSha(k'))))
