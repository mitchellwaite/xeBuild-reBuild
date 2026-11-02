import os
P=os.environ.get('TP','gi'); C=os.environ.get('TC','12')
def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {')
    f=s.index('fkbo: {',i)
    if P=='fk': s=s[:f]+'dsp: '+s[f:]
    else:
        g=s.index('cinfo = netGetInfo();',f)
        if P=='gi': s=s[:g]+'dsp: '+s[g:]
        else:
            h=s.index('\n',g)+1; h=s.index('\t',h); h+=len(s[h:])-len(s[h:].lstrip('\t'))
            if P=='l2': h=s.index('\n',h)+1; h+=len(s[h:])-len(s[h:].lstrip('\t'))
            s=s[:h]+'dsp: '+s[h:]
    j=s.index('switch (mode) {',i); k=s.index('case %s:'%C,j) if C!='default' else s.index('default:',j); b=s.index('break;',k)
    return s[:b]+'__asm__ goto ("" :::: dsp); '+s[b:]
