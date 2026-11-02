exec(open('lp.py').read()); mod=mk(['case %d'%k for k in (1,2,3,4,5,7,8,9,10,11,12)]+['default'],g='if (1'+''.join(' && __builtin_constant_p(argc + %d)'%(800+k) for k in range(2))+') goto dsp; ')
