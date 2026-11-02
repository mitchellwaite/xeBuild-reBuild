import os
D=int(os.environ.get('DD','3')); SITE=os.environ.get('SITE','v'); VAR=os.environ.get('VAR','i')
def cond(d,o): return ' && '.join('__builtin_constant_p(%s + %d)'%(VAR,o+k) for k in range(d))
def mod(s):
    a='switch (mode) {\n			case 1:'; assert s.count(a)==1
    s=s.replace(a,'dsp: '+a)
    g='if (%s) goto dsp; '%cond(D,1500)
    if SITE=='v':
        a='			log_verbose_flag(argv[i][2]);\n'; assert s.count(a)==1
        s=s.replace(a,'			{ log_verbose_flag(argv[i][2]); '+g+'}\n')
    elif SITE=='top':
        a='	for (i = 0; i < argc; i++) {\n'; assert s.count(a)==1
        s=s.replace(a,a+g+'\n')
    elif SITE=='pre':
        a='	for (i = 0; i < argc; i++) {\n'; assert s.count(a)==1
        s=s.replace(a,g+'\n'+a)
    elif SITE=='post':
        a='	if (NO_MODE_ARG(mode, arg)) {\n'; assert s.count(a)==1
        s=s.replace(a,'	'+g+'\n'+a)
    elif SITE=='back':
        a='			}\n		} else\n			goto fail;\n	}\n	dtg:'; assert s.count(a)==1
        s=s.replace(a,'			}\n			'+g+'\n		} else\n			goto fail;\n	}\n	dtg:')
    elif SITE=='lx':
        a='	for (i = 0; i < argc; i++) {\n'; assert s.count(a)==1
        s=s.replace(a,a+g.replace('dsp','lxp')+'\n')
        a='	if (NO_MODE_ARG(mode, arg)) {\n'; assert s.count(a)==1
        s=s.replace(a,'	lxp: '+a)
    elif SITE=='ndl':
        a='	ndl: netDisconnect();\n'; s=s.replace(a,a+'	'+g+'\n')
    elif SITE=='fkN':
        a='fkN: ;\n'; s=s.replace(a,a+g)
    return s
