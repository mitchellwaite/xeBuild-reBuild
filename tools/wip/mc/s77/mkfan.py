import sys
# mkfan.py PREFIX N TARGETS... -> asm goto fan with N dilution labels merging into fallthrough
p=sys.argv[1]; n=int(sys.argv[2]); t=sys.argv[3:]
labs=t+[f'{p}{i}' for i in range(n)]
s='{ __asm__ goto ("" :::: '+', '.join(labs)+'); goto '+p+'N; '+' '.join(f'{p}{i}: goto {p}o{i};' for i in range(n))+' } '+' '.join(f'{p}o{i}: goto {p}N;' for i in range(n))+f' {p}N: ;'
print(s)
