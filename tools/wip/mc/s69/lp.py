import re
def mk(cases,pre=False,g='__asm__ goto ("" :::: dsp); '):
    def mod(s):
        i=s.index('if (NO_MODE_ARG(mode, arg)) {'); j=s.index('switch (mode) {',i)
        if pre:  # label before TH chain line
            j0=s.rindex('\n',0,j)+1
            while s[j0]=='\t': j0+=1
        else: j0=j
        head=s[:j0]+'dsp: '+s[j0:j]; t=s[j:]
        def rep(m):
            c=m.group(1)
            return m.group(0)+(g if c in cases else '')
        t=re.sub(r'(case \d+|default):\n\t+',rep,t,count=13)
        return head+t
    return mod
