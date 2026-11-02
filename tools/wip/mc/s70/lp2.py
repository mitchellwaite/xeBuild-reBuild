exec(open('lp.py').read())
def mkw(w):  # w: case->multiplicity
    def mod(s):
        import re
        i=s.index('if (NO_MODE_ARG(mode, arg)) {'); j=s.index('switch (mode) {',i)
        head=s[:j]+'dsp: '+s[j:j]; t=s[j:]
        t=re.sub(r'(case \d+|default):\n\t+',lambda m:m.group(0)+'__asm__ goto ("" :::: dsp); '*w.get(m.group(1),0),t,count=13)
        return head+t
    return mod
