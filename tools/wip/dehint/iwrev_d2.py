# finalizeImage: fewer locals / re-reads
import os
exec(open(os.path.join(os.path.dirname(__file__), 'iwrev_d.py')).read())
FX = '\t\t\t\tconst uint8_t *from[2] = { xb.hdr + %s, q + %s };\n' % (X, Y)
FXX = '\t\t\t\tconst uint8_t *from[2] = { xb.hdr + %s, xb.spare + %s };\n' % (X, Y)
FH = '\t\t\t\tconst uint8_t *from[2] = { h + %s, xb.spare + %s };\n' % (X, Y)
TH = I4 + 'if (pageErased(xb.hdr + %s, q + %s) <= 0) {\n' % (X, Y)
CH = I4 + '\tval = calcEcd(h + %s, s);\n' % X
CX = I4 + '\tval = calcEcd(xb.hdr + %s, s);\n' % X
V = [
    ('directh', [(RR, I4 + '\tq = xb.spare;\n'), (FROM, FX)]),
    ('dh_swap', [(DQ, I4 + 'uint8_t *h = xb.hdr;\n' + I4 + 'const uint8_t *q = xb.spare;\n'), (RR, I4 + '\tq = xb.spare;\n'), (FROM, FX)]),
    # no h: xb.hdr wherever the page's data is used
    ('noh_all', [(DQ, I4 + 'const uint8_t *q = xb.spare;\n'), (T, TH), (CH, CX), (RR, I4 + '\tq = xb.spare;\n'), (FROM, FX)]),
    # no q: xb.spare wherever the spare is used, h re-read
    ('noq_all', [(DQ, I4 + 'uint8_t *h = xb.hdr;\n'), (T, I4 + 'if (pageErased(h + %s, xb.spare + %s) <= 0) {\n' % (X, Y)), (RR, I4 + '\th = xb.hdr;\n'), (FROM, FH)]),
    # no locals at all
    ('none', [(DQ, ''), (T, I4 + 'if (pageErased(xb.hdr + %s, xb.spare + %s) <= 0) {\n' % (X, Y)), (CH, CX), (RR, ''), (FROM, FXX)]),
    # the spare pointer of the page as a local, re-read after the stores
    ('sp', [(DQ, I4 + 'const uint8_t *q = xb.spare + %s;\n' % Y + I4 + 'uint8_t *h = xb.hdr;\n'),
            (T, I4 + 'if (pageErased(h + %s, q) <= 0) {\n' % X),
            (RR, I4 + '\tq = xb.spare + %s;\n' % Y + I4 + '\th = xb.hdr;\n'),
            (FROM, '\t\t\t\tconst uint8_t *from[2] = { h + %s, q };\n' % X)]),
]
