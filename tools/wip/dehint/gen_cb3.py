"""cbDecrypt: key's scope x how the signature-failure path leaves x good arms' returns.
Keeps the failure's 0 in a clobber block shared by several failures (no uncprop), and
tries to keep the free path's 0 a direct argument of the return PHI (NULL_RETURN prediction)."""
FN = 'cbDecrypt'

HEAD = '''/* decrypted copy of a CB/SB (free it), checked against the 1BL RSA key */
uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey);
uint8_t *cbDecrypt(uint8_t *cb, uint32_t *outLen, uint8_t *outKey)
{
'''

OK = 'log_printf(1, "%cB signature OK! Decryption successful!\\n", buf[0]);'
ERR = 'log_printf(0, "***** ERROR: %cB signature invalid, corrupted or decryption failed!\\n", buf[0]);'
WARN = 'log_printf(0, "***** WARNING: could not check %cB signature, 1BL RSA key not loaded!\\n", buf[0]);'
SETLEN = 'if (outLen)\n*outLen = len;'

TAILS = {
    # sig failure sets buf = 0, one return buf (the current source)
    'zero': '''if (xb.pub1bl) {
if (cbVerifySig(buf, xb.pub1bl)) {
OK
SETLEN
} else {
ERR
free(buf);
buf = 0;
}
} else {
WARN
SETLEN
}
return buf;
''',
    # sig failure returns 0 itself
    'ret0': '''if (xb.pub1bl) {
if (cbVerifySig(buf, xb.pub1bl)) {
OK
SETLEN
} else {
ERR
free(buf);
return 0;
}
} else {
WARN
SETLEN
}
return buf;
''',
    # good arms return, sig failure falls out with the other failures
    'fall': '''if (xb.pub1bl) {
if (cbVerifySig(buf, xb.pub1bl)) {
OK
SETLEN
return buf;
}
ERR
free(buf);
} else {
WARN
SETLEN
return buf;
}
''',
    # same, a shared `done` for the good arms
    'fall2': '''if (xb.pub1bl) {
if (cbVerifySig(buf, xb.pub1bl)) {
OK
} else {
ERR
free(buf);
goto fail;
}
} else {
WARN
}
if (outLen)
*outLen = len;
return buf;
''',
    # goto a label past the scope, return buf in one place
    'goto': '''if (xb.pub1bl) {
if (cbVerifySig(buf, xb.pub1bl)) {
OK
SETLEN
} else {
ERR
free(buf);
goto fail;
}
} else {
WARN
SETLEN
}
return buf;
''',
}


def body(tail, keyat, afterlog, elsealloc):
    k = 'uint8_t key[16];\n'
    s = HEAD + 'uint8_t *buf;\nuint32_t len;\n'
    if keyat == 'fn':
        s += k
    s += '\nif (cb) {\n'
    if keyat == 'cb':
        s += k
    s += "if (BL_MAGIC(cb, 'B')) {\n"
    if keyat == 'magic':
        s += k
    s += 'len = BL_SIZE(cb);\nbuf = calloc(len, 1);\nif (buf) {\n'
    if keyat == 'buf':
        s += k
    s += '''memcpy(buf, cb, len);
XeCryptHmacSha(xb.key1bl, 16, buf + 16, 16, 0, 0, 0, 0, key, 16);
XeCryptRc4(key, 16, buf + 32, len - 32);
if (outKey)
memcpy(outKey, key, 16);
'''
    s += TAILS[tail].replace('SETLEN', SETLEN).replace('OK', OK).replace('ERR', ERR).replace('WARN', WARN)
    alloc = 'log_printf(0, "***** WARNING: Unable to allocate 0x%x bytes for %c%c!\\n", cb[0], cb[1]);\n'
    if elsealloc:
        s += '} else\n' + alloc
    else:
        s += '} \n' + alloc if tail not in ('fall',) else '} else\n' + alloc
    s += '''} else
log_printf(0, "***** WARNING: CB/SB does not have valid magic!\\n");
} else
log_printf(0, "***** WARNING: CB/SB decrypt not provided with data!\\n");
'''
    if 'goto fail' in s:
        s += 'fail:\n'
    s += 'return 0;\n}\n'
    return s


def variants():
    for t in TAILS:
        for k in ('fn', 'cb', 'magic', 'buf'):
            for e in (0, 1):
                yield ('tail=%s key=%s else=%d' % (t, k, e), body(t, k, 0, e))
