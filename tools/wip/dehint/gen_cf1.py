"""cfDecrypt: where the result is normalised to 0/1, against where the fail paths join."""
import itertools

BODY = """XeCryptHmacSha(xb.key1bl, 16, cf + 32, 16, 0, 0, 0, 0, key, 16);
XeCryptRc4(key, 16, cf + 48, len - 48);
"""
CALL = 'checkZeros(cf + 496, 32)'


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.split('\n') if l)


def fn(decl, body):
    return 'int cfDecrypt(uint8_t *cf, uint32_t size)\n{\n' + ind(decl, 1) + '\n' + body + '}\n'


# the test: nested or joined
def head(kind, inner):
    if kind == 'nest':
        return ('\tif (BL_MAGIC(cf, \'F\')) {\n\t\tlen = BL_SIZE(cf);\n\t\tif (len <= size) {\n' + ind(inner, 3)
                + '\t\t}\n\t}\n')
    if kind == 'guard':
        return ('\tif (!BL_MAGIC(cf, \'F\'))\n\t\treturn 0;\n\tlen = BL_SIZE(cf);\n\tif (len > size)\n\t\treturn 0;\n' + ind(inner, 1))
    if kind == 'nestret':
        return ('\tif (BL_MAGIC(cf, \'F\')) {\n\t\tlen = BL_SIZE(cf);\n\t\tif (len > size)\n\t\t\treturn 0;\n' + ind(inner, 2)
                + '\t}\n')
    if kind == 'and':
        return ("\tlen = BL_SIZE(cf);\n\tif (BL_MAGIC(cf, 'F') && len <= size) {\n" + ind(inner, 2) + '\t}\n')
    raise ValueError(kind)


TAILS = {
    'ne': 'return ok != 0;\n',
    'tern': 'return ok ? 1 : 0;\n',
    'not2': 'return !!ok;\n',
    'ifret': 'if (ok)\n\treturn 1;\nreturn 0;\n',
    'ifset': 'if (ok)\n\tok = 1;\nreturn ok;\n',
    'ifelse': 'if (ok)\n\tok = 1;\nelse\n\tok = 0;\nreturn ok;\n',
    'negret': 'if (!ok)\n\treturn 0;\nreturn 1;\n',
    'ret2': 'ret = 0;\nif (ok)\n\tret = 1;\nreturn ret;\n',
    'ret3': 'ret = ok != 0;\nreturn ret;\n',
    'ret4': 'if (ok)\n\tret = 1;\nelse\n\tret = 0;\nreturn ret;\n',
    'ret5': 'if (ok)\n\tret = 1;\nelse\n\tret = ok;\nreturn ret;\n',
    'ret6': 'ret = ok;\nif (ret)\n\tret = 1;\nreturn ret;\n',
}
OKS = {'int': 'int ok = 0;\n', 'u32': 'uint32_t ok = 0;\n', 'u8': 'uint8_t ok = 0;\n', 'long': 'long ok = 0;\n'}


def variants():
    for h, (tn, t), (on, o) in itertools.product(['nest', 'guard', 'nestret', 'and'], TAILS.items(), OKS.items()):
        decl = 'uint32_t len;\nuint8_t key[16];\n' + o
        if 'ret' in t and tn.startswith('ret'):
            decl += 'int ret;\n'
        if h == 'guard' or h == 'nestret':
            # guards: the join is only the check itself
            pass
        src = fn(decl, head(h, BODY + 'ok = ' + CALL + ';\n') + ind(t, 1))
        yield '%s|%s|%s' % (h, tn, on), src
