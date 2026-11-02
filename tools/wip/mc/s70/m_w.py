import os,re
P=os.environ.get('TP','gi'); W=dict((k,int(v)) for k,v in (x.split('=') for x in os.environ.get('TW','12=1').split(',')))
POS=os.environ.get('TPOS','tail')
def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {')
    f=s.index('fkbo: {',i)
    if P=='fk': s=s[:f]+'dsp: '+s[f:]
    else:
        g=s.index('cinfo = netGetInfo();',f); s=s[:g]+'dsp: '+s[g:]
    j=s.index('switch (mode) {',i)
    for c,n in W.items():
        lab='case %s:'%c if c!='d' else 'default:'
        k=s.index(lab,j)
        if POS=='tail': b=s.index('break;',k)
        else: b=k+len(lab)
        s=s[:b]+'__asm__ goto ("" :::: dsp); '*n+s[b:]
    return s
