"""cfDecrypt: key scoped in a block, with a return from inside it.  tree-eh then copies
key's clobber into both arms, so the block between the checkZeros test and the join isn't empty."""
import itertools

CALL = 'checkZeros(cf + 496, 32)'
WORK = """XeCryptHmacSha(xb.key1bl, 16, cf + 32, 16, 0, 0, 0, 0, key, 16);
XeCryptRc4(key, 16, cf + 48, len - 48);
"""
TESTS = {
    'ifret': (WORK + 'if (' + CALL + ')\n\treturn 1;\n', ''),
    'okret': (WORK + 'ok = ' + CALL + ';\nif (ok)\n\treturn 1;\n', 'int ok;\n'),
    'oksc': (WORK + 'int ok = ' + CALL + ';\nif (ok)\n\treturn 1;\n', ''),
    'neret': (WORK + 'if (' + CALL + ' != 0)\n\treturn 1;\n', ''),
    'retexpr': (WORK + 'return ' + CALL + ' != 0;\n', ''),
    'rettern': (WORK + 'return ' + CALL + ' ? 1 : 0;\n', ''),
    'retelse': (WORK + 'if (' + CALL + ')\n\treturn 1;\nelse\n\treturn 0;\n', ''),
}


def ind(s, n):
    return ''.join('\t' * n + l + '\n' for l in s.split('\n') if l)


def variants():
    for (tn, (t, d)), scope, lend in itertools.product(TESTS.items(), ['inner', 'outer'], ['fn', 'outer']):
        decl = ''
        if lend == 'fn':
            decl += 'uint32_t len;\n'
        decl += d
        s = 'int cfDecrypt(uint8_t *cf, uint32_t size)\n{\n' + ind(decl, 1) + ('\n' if decl else '')
        s += "\tif (BL_MAGIC(cf, 'F')) {\n"
        if scope == 'outer':
            s += '\t\tuint8_t key[16];\n'
        if lend == 'outer':
            s += '\t\tuint32_t len;\n'
        if scope == 'outer' or lend == 'outer':
            s += '\n'
        s += '\t\tlen = BL_SIZE(cf);\n\t\tif (len <= size) {\n'
        if scope == 'inner':
            s += '\t\t\tuint8_t key[16];\n\n'
        s += ind(t, 3) + '\t\t}\n\t}\n'
        s += '\treturn 0;\n}\n'
        yield '%s|%s|%s' % (tn, scope, lend), s
