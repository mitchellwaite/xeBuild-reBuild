"""ceDecrypt: the magic test through a flag, so its `!= 0` test takes no opcode/call heuristic. bb5 must rise to >= 5226."""
import importlib.util, os
spec = importlib.util.spec_from_file_location('gen_ce1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ce1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FN = 'ceDecrypt'
ind = g.ind
BASE = g.ARMS['base']
OPEN = 'if (bl && hmacKey) {\n'
TAIL = '} else\n\t' + g.NULLLOG + '\nreturn 0;\n'
BLOCK = '{\n' + ind(g.DECL + BASE) + '} else\n\t' + g.MAGICLOG + '\n'


def wrap(inner):
    return g.HEAD + ind(OPEN + ind(inner) + TAIL) + '}\n'


FLAGS = {
    'init_int': "int ok = BL_MAGIC(bl, 'E');\n\nif (ok) " + BLOCK,
    'init_bool': "BOOL ok = BL_MAGIC(bl, 'E');\n\nif (ok) " + BLOCK,
    'init_u8': "uint8_t ok = BL_MAGIC(bl, 'E');\n\nif (ok) " + BLOCK,
    'set_if': "int ok = 0;\n\nif (BL_MAGIC(bl, 'E'))\n\tok = 1;\nif (ok) " + BLOCK,
    'set_if2': "int ok = 1;\n\nif (!BL_MAGIC(bl, 'E'))\n\tok = 0;\nif (ok) " + BLOCK,
    'set_two': "int ok = 0;\n\nif ((bl[0] & 0x43) == 0x43 && bl[1] == 'E')\n\tok = 1;\nif (ok) " + BLOCK,
    'set_nest': "int ok = 0;\n\nif ((bl[0] & 0x43) == 0x43) {\n\tif (bl[1] == 'E')\n\t\tok = 1;\n}\nif (ok) " + BLOCK,
    'set_second': "int ok = (bl[0] & 0x43) == 0x43;\n\nif (ok)\n\tok = bl[1] == 'E';\nif (ok) " + BLOCK,
    'half': "int ok = bl[1] == 'E';\n\nif ((bl[0] & 0x43) == 0x43 && ok) " + BLOCK,
    'half2': "int ok = (bl[0] & 0x43) == 0x43;\n\nif (ok && bl[1] == 'E') " + BLOCK,
}


def variants():
    for k, v in FLAGS.items():
        yield (k, wrap(v))
