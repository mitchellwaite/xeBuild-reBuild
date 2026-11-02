def mod(s):
    i=s.index('if (NO_MODE_ARG(mode, arg)) {')
    j=s.index('switch (mode) {',i)
    s=s[:j]+'dsp: '+s[j:]
    g=' '.join(['if (__builtin_constant_p(argc + %d))'%(700+k) for k in range(2)])
    g='{ if (1'+''.join([' && __builtin_constant_p(argc + %d)'%(700+k) for k in range(2)])+') goto dsp; }'
    site='rokf'
    if site=='u2': s=s.replace('{ AT(u2) client_usage(2, NULL); }','{ AT(u2) '+g+' client_usage(2, NULL); }',1)
    elif site=='fail': s=s[:i]+s[i:].replace('} else\n\t\t\t\tgoto fail;','} else {'+g+' goto fail; }',1)
    else: s=s.replace('cinfo = netGetInfo(); if (__builtin_constant_p(mode + 620)) goto ndl;','cinfo = netGetInfo(); '+g+' if (__builtin_constant_p(mode + 620)) goto ndl;',1)
    return s
