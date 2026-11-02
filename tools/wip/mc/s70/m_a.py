import os
P=os.environ.get('TP','fk'); W=os.environ.get('TW','t4').split(','); N=int(os.environ.get('TN','1'))
def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {')
    f=s.index('fkbo: {',i)
    if P=='fk': s=s[:f]+'dsp: '+s[f:]
    elif P=='sw': j=s.index('switch (mode) {',i); s=s[:j]+'dsp: '+s[j:]
    else: g=s.index('cinfo = netGetInfo();',f); s=s[:g]+'dsp: '+s[g:]
    j=s.index('switch (mode) {',i)
    for c in W:
        k=s.index('AT(%s) '%c,j)+len('AT(%s) '%c)
        s=s[:k]+'__asm__ goto ("" :::: dsp); '*N+s[k:]
    return s
