import os
exec(open(os.path.join(os.path.dirname(os.path.abspath('m_w.py')),'m_w.py')).read())
_m=mod; A=os.environ.get('TA','r')
def mod(s):
    s=_m(s)
    if 'r' in A: s=s.replace('__asm__ goto ("" :::: c1, hdd4,','__asm__ goto ("" :::: dsp, c1, hdd4,',1)
    if 'f' in A: s=s.replace('__asm__ goto ("" :::: i1, p1,','__asm__ goto ("" :::: dsp, i1, p1,',1)
    return s
