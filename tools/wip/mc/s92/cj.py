import sys
# cj.py base off n [style]  -> conjunction of n bcp tests base+off..
b,o,n=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); st=sys.argv[4] if len(sys.argv)>4 else 'c'
if st=='c': print(' && '.join('(char *)__builtin_constant_p(%s + %d) == (char *)1'%(b,o+k) for k in range(n)))
else: print(' && '.join('__builtin_constant_p(%s + %d)'%(b,o+k) for k in range(n)))
