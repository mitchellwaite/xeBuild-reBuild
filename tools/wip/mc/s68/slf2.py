def mk(g):
    def mod(s):
        i=s.index('if (NO_MODE_ARG(mode, arg)) {'); j=s.index('switch (mode) {',i)
        return s[:j]+'dsp: '+g+' '+s[j:]
    return mod
