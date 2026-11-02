import os
P=os.environ.get('TP','fk'); W=[x for x in os.environ.get('TW','10').split(',')]
G=os.environ.get('TG','b')  # b: bcp goto ; a: bcp asm goto
DEP=int(os.environ.get('TD','1'))
def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {')
    f=s.index('fkbo: {',i)
    if P=='fk': s=s[:f]+'dsp: '+s[f:]
    elif P=='sw': j=s.index('switch (mode) {',i); s=s[:j]+'dsp: '+s[j:]
    else: g=s.index('cinfo = netGetInfo();',f); s=s[:g]+'dsp: '+s[g:]
    j=s.index('switch (mode) {',i)
    for n,c in enumerate(W):
        lab='case %s:'%c if c!='d' else 'default:'
        k=s.index(lab,j); b=k+len(lab)
        cond=' && '.join('__builtin_constant_p(mode + %d)'%(1700+20*n+q) for q in range(DEP))
        ins='if (%s) goto dsp; '%cond if G=='b' else 'if (%s) __asm__ goto ("" :::: dsp); '%cond
        s=s[:b]+ins+s[b:]
    return s
