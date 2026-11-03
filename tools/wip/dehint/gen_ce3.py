"""ceDecrypt: the alloc test split in two so the surviving edge keeps the first test's prediction
(the hinted build's `if (buf) asm` did that): a flag set by one if and tested by the next, or a first guard around memcpy."""
import importlib.util, os
spec = importlib.util.spec_from_file_location('gen_ce1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ce1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FN = 'ceDecrypt'
ind = g.ind
BODY_REST = g.BODY.split('\n', 1)[1]
class _T:
    def __mod__(self, c):
        return 'if (' + c + ') {\n' + ind(g.BODY) + '} else\n\t' + g.ALLOC + '\n'


TEST2 = _T()
LEN = 'len = BL_SIZE(bl);\nbuf = calloc(len, 1);\n'


def wrap(decl, inner):
    return g.HEAD + ind('if (bl && hmacKey) {\n' + ind("if (BL_MAGIC(bl, 'E')) {\n" + ind(decl + '\n' + inner) + '} else\n\t' + g.MAGICLOG + '\n') + '} else\n\t' + g.NULLLOG + '\nreturn 0;\n') + '}\n'


D = 'uint8_t *buf;\nuint32_t len;\nuint8_t key[16];\n'
SH = {
    'set_if': (D + 'int ok = 0;\n', LEN + 'if (buf)\n\tok = 1;\n' + TEST2 % 'ok'),
    'set_if_bool': (D + 'BOOL ok = 0;\n', LEN + 'if (buf)\n\tok = 1;\n' + TEST2 % 'ok'),
    'clr_if': (D + 'int ok = 1;\n', LEN + 'if (!buf)\n\tok = 0;\n' + TEST2 % 'ok'),
    'else_set': (D + 'int ok;\n', LEN + 'if (buf)\n\tok = 1;\nelse\n\tok = 0;\n' + TEST2 % 'ok'),
    'init_ne': (D + 'int ok;\n', LEN + 'ok = buf != 0;\n' + TEST2 % 'ok'),
    'memcpy_guard': (D, LEN + 'if (buf)\n\tmemcpy(buf, bl, len);\nif (buf) {\n' + ind(BODY_REST) + '} else\n\t' + g.ALLOC + '\n'),
}


def variants():
    for k, (d, i) in SH.items():
        yield (k, wrap(d, i))
