# finalizeImage: `<= 0`, calcPageEcc written out, the re-reads, const on q only
I4 = '\t\t\t'
X = '(b * 32 + p) * 512'
Y = '(b * 32 + p) * 16'
T = I4 + 'if (pageErased(h + %s, q + %s) <= 0) {\n' % (X, Y)
ARM = (I4 + '\tuint32_t val;\n\n'
       + I4 + '\ts = xb.spare + %s;\n' % Y
       + I4 + '\tval = calcEcd(h + %s, s);\n' % X
       + I4 + '\ts[12] = (s[12] & 0x3f) + (val << 6);\n'
       + I4 + '\ts[13] = val >> 2;\n'
       + I4 + '\ts[14] = val >> 10;\n'
       + I4 + '\ts[15] = val >> 18;\n')
RR = I4 + '\tq = xb.spare;\n' + I4 + '\th = xb.hdr;\n'
FROM = '\t\t\t\tconst uint8_t *from[2] = { h + %s, q + %s };\n' % (X, Y)
DQ = I4 + 'const uint8_t *q = xb.spare;\n' + I4 + 'uint8_t *h = xb.hdr;\n'
V = [
    ('base', []),
    ('not', [(T, I4 + 'if (!pageErased(h + %s, q + %s)) {\n' % (X, Y))]),
    ('eq0', [(T, I4 + 'if (pageErased(h + %s, q + %s) == 0) {\n' % (X, Y))]),
    ('lt1', [(T, I4 + 'if (pageErased(h + %s, q + %s) < 1) {\n' % (X, Y))]),
    ('ne1', [(T, I4 + 'if (pageErased(h + %s, q + %s) != 1) {\n' % (X, Y))]),
    ('call', [(ARM, I4 + '\tcalcPageEcc(h + %s, xb.spare + %s);\n' % (X, Y))]),
    ('callnot', [(T, I4 + 'if (!pageErased(h + %s, q + %s)) {\n' % (X, Y)), (ARM, I4 + '\tcalcPageEcc(h + %s, xb.spare + %s);\n' % (X, Y))]),
    ('norr', [(RR, '')]),
    ('noq', [(RR, I4 + '\th = xb.hdr;\n')]),
    ('noh', [(RR, I4 + '\tq = xb.spare;\n')]),
    ('hq', [(RR, I4 + '\th = xb.hdr;\n' + I4 + '\tq = xb.spare;\n')]),
    # the copy reads xb.hdr and xb.spare itself, no re-reads
    ('direct', [(RR, ''), (FROM, '\t\t\t\tconst uint8_t *from[2] = { xb.hdr + %s, xb.spare + %s };\n' % (X, Y))]),
    ('directq', [(RR, I4 + '\th = xb.hdr;\n'), (FROM, '\t\t\t\tconst uint8_t *from[2] = { h + %s, xb.spare + %s };\n' % (X, Y))]),
    ('directh', [(RR, I4 + '\tq = xb.spare;\n'), (FROM, '\t\t\t\tconst uint8_t *from[2] = { xb.hdr + %s, q + %s };\n' % (X, Y))]),
    ('qnc', [(DQ, I4 + 'uint8_t *q = xb.spare;\n' + I4 + 'uint8_t *h = xb.hdr;\n')]),
    # the stores through q's own pointer
    ('sq', [(DQ, I4 + 'uint8_t *q = xb.spare;\n' + I4 + 'uint8_t *h = xb.hdr;\n'), (I4 + '\ts = xb.spare + %s;\n' % Y, I4 + '\ts = q + %s;\n' % Y)]),
    ('sq2', [(I4 + '\ts = xb.spare + %s;\n' % Y, I4 + '\ts = (uint8_t *)q + %s;\n' % Y)]),
]
