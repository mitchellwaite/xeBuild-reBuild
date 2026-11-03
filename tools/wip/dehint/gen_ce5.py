"""ceDecrypt: gotos move PRED_GOTO onto edges (up through postdominated blocks), a block going straight to the return
takes the early-return prediction. The alloc edge needs odds x 1.04..1.57. Cleanup-style gotos, in string order."""
import importlib.util, itertools, os
spec = importlib.util.spec_from_file_location('gen_ce1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_ce1.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
FN = 'ceDecrypt'
ind = g.ind
CRYPT = ''.join(g.BODY.splitlines(True)[:3])
OK = 'log_printf(1, "%c%c hash check OK! Decryption successful!\\n", buf[0], buf[1]);\n'
ERR = 'log_printf(0, "***** ERROR: %c%c hash check invalid, corrupted or decryption failed!\\n", buf[0], buf[1]);\nfree(buf);\n'
WARN = 'log_printf(0, "***** WARNING: could not check %cE signature, 1BL RSA key not loaded!\\n", buf[0]);\n'
SET = 'if (outLen)\n\t*outLen = len;\n'

GOOD = {
    'ret': ('return buf;\n', ''),                 # each good arm returns
    'gotodone': ('goto done;\n', 'done:\nreturn buf;\n'),   # each good arm jumps to a shared return
    'setgoto': ('goto done;\n', 'done:\nreturn buf;\n'),
}
FREE = {
    'fall': '',
    'ret0': 'return 0;\n',
    'gotofail': 'goto fail;\n',
}
ALLOCF = {
    'fall': '',
    'ret0': 'return 0;\n',
    'gotofail': 'goto fail;\n',
}
ENDARM = {'none': '', 'gotofail': 'goto fail;\n'}


def variants():
    for gn, fn_, an, ea, kscope, lab in itertools.product(GOOD, FREE, ALLOCF, ENDARM, ('magic', 'fn'), ('outer', 'inner')):
        gret, gtail = GOOD[gn]
        if gn == 'setgoto':
            armok, armwarn = OK + gret.replace('goto done', 'goto setlen'), WARN + gret.replace('goto done', 'goto setlen')
            gt = 'setlen:\n' + SET + 'return buf;\n'
        else:
            armok, armwarn = OK + SET + gret, WARN + SET + gret
            gt = gtail
        hashpart = 'if (hash) {\n\tif (blCheckHash(buf, len, hash)) {\n' + ind(armok, 2) + '\t}\n' + ind(ERR + FREE[fn_]) + '} else {\n' + ind(armwarn) + '}\n'
        body = CRYPT + hashpart + ENDARM[ea]
        if gt:
            # the shared return sits after the failure tail, jumped to
            body += 'goto fail;\n' if ea == 'none' and not FREE[fn_] else ''
            body += gt
        inner = 'len = BL_SIZE(bl);\nbuf = calloc(len, 1);\nif (buf) {\n' + ind(body) + '} else {\n' + ind(g.ALLOC + '\n' + ALLOCF[an]) + '}\n'
        if lab == 'inner' and ('goto fail' in inner):
            inner += 'fail:\n;\n'
        decl = 'uint8_t *buf;\nuint32_t len;\n'
        kd = 'uint8_t key[16];\n'
        block = ind((decl + kd if kscope == 'magic' else decl) + '\n' + inner)
        fn = (kd + '\n' if kscope == 'fn' else '') + 'if (bl && hmacKey) {\n' + ind("if (BL_MAGIC(bl, 'E')) {\n" + block + '} else\n\t' + g.MAGICLOG + '\n') + '} else\n\t' + g.NULLLOG + '\n'
        if lab == 'outer' and 'goto fail' in fn:
            fn += 'fail:\n'
        elif lab == 'outer':
            continue
        fn += 'return 0;\n'
        yield ('good=%s free=%s alloc=%s end=%s key=%s lab=%s' % (gn, fn_, an, ea, kscope, lab), g.HEAD + ind(fn) + '}\n')
