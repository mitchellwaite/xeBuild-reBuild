import os
def mk(d,var='argc',base=700,where='self'):
    def mod(s):
        i=s.index('if (NO_MODE_ARG(mode, arg)) {'); j=s.index('switch (mode) {',i)
        g='if (1'+''.join([' && __builtin_constant_p(%s + %d)'%(var,base+k) for k in range(d)])+') goto dsp; '
        return s[:j]+'dsp: '+g+s[j:]
    return mod
