def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {'); j=s.index('switch (mode) {',i)
    k=s.index('case 12:',j); b=s.index('break;',k)
    return s[:j]+'dsp: '+s[j:b]+'__asm__ goto ("" :::: dsp); '+s[b:]
