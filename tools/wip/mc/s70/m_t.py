import os
P=os.environ.get('TP','nma'); C=os.environ.get('TC','12')
def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {')
    if P=='nma': s=s[:i]+'top: '+s[i:]
    elif P=='ret':
        j=s.index('dtg: if (E(reboot))'); s=s[:j]+'top: ; '+s[j:]
    j=s.index('switch (mode) {',i); k=s.index('case %s:'%C,j) if C!='default' else s.index('default:',j); b=s.index('break;',k)
    return s[:b]+'__asm__ goto ("" :::: top); '+s[b:]
