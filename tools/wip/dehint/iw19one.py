import sys
sys.path.insert(0,'tools/wip/dehint')
import iwlib
t=open('build/iw/a19/d_blockdecl_h.c',newline='\n').read()
E={'q uint8_t':[('const uint8_t *q = xb.spare;','uint8_t *q = xb.spare;'),('calcEcd(h','calcEcd(h')],
 'h const':[('uint8_t *h = xb.hdr;','const uint8_t *h = xb.hdr;'),('val = calcEcd(h +','val = calcEcd(xb.hdr +')],
 'no q reread':[('\t\t\t\tq = xb.spare;\n','')],
 'no h reread':[('\t\t\t\th = xb.hdr;\n','')],
 'neither reread':[('\t\t\t\tq = xb.spare;\n\t\t\t\th = xb.hdr;\n','')],
 'h then q top':[('const uint8_t *q = xb.spare;\n\t\t\tuint8_t *h = xb.hdr;','uint8_t *h = xb.hdr;\n\t\t\tconst uint8_t *q = xb.spare;')],
 'reread h then q':[('\t\t\t\tq = xb.spare;\n\t\t\t\th = xb.hdr;\n','\t\t\t\th = xb.hdr;\n\t\t\t\tq = xb.spare;\n')],
 '!pageErased':[(') <= 0) {\n\t\t\t\tuint32_t val;',') == 0) {\n\t\t\t\tuint32_t val;')],
 'calcPageEcc call':[('\t\t\t\tuint32_t val;\n\n\t\t\t\ts = xb.spare + (b * 32 + p) * 16;\n\t\t\t\tval = calcEcd(h + (b * 32 + p) * 512, s);\n\t\t\t\ts[12] = (s[12] & 0x3f) + (val << 6);\n\t\t\t\ts[13] = val >> 2;\n\t\t\t\ts[14] = val >> 10;\n\t\t\t\ts[15] = val >> 18;\n','\t\t\t\tcalcPageEcc(h + (b * 32 + p) * 512, xb.spare + (b * 32 + p) * 16);\n')],
}
for k,ed in E.items():
    x=t
    for a,b in ed:
        assert a in x,a
        x=x.replace(a,b)
    print(k,'|',iwlib.fmt(iwlib.score_text(x,[]))[:80],flush=True)
