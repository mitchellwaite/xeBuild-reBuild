import sys
# bc.py BASE K -> bcp conjunct chain of K terms
b,k=int(sys.argv[1]),int(sys.argv[2])
print(' && '.join('__builtin_constant_p(mode + %d)'%(b+50000*i) for i in range(k)))
