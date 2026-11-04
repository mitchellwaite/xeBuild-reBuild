"""python tools/wip/dehint/iw19hs.py <file.c> [flags]: finalizeImage's ECD loop at IRA. Every pseudo loaded from xb.hdr (56) or xb.spare (48) anywhere in the function, its RTL reference count, every copy between pseudos of those two groups, and the l0 costs. Reads -fdump-rtl-ira-all via iw9ira.py's route; scratch build/iw/a19/hs."""
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
path, flags = sys.argv[1], sys.argv[2:]
d = os.path.join(iwlib.BUILD, 'a19', 'hs'); os.makedirs(d, exist_ok=True)
for f in glob.glob(os.path.join(d, 'a.c*')): os.remove(f)
open(os.path.join(d, 'a.c'), 'w', newline='\n').write(open(path, newline='').read().replace('\r\n', '\n'))
subprocess.run([iwlib.GCC, '-c', '-O3'] + flags + ['-I' + os.path.join(iwlib.R, 'src'), '-fdump-rtl-ira-all', 'a.c', '-o', 'a.o'], cwd=d, check=True)
t = open(glob.glob(os.path.join(d, 'a.c.*ira'))[0], errors='replace').read()
b = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', t, re.S | re.M).group(0)
open(os.path.join(d, 'fi.ira'), 'w', newline='\n').write(b)
# the insn stream only (after the allocation dump): last occurrence of the first insn
i = b.rfind('\n(note ', 0, b.find('\n(insn ', len(b) // 2)) if False else 0
ins = re.findall(r'^\((?:insn|jump_insn|call_insn)[^\n]*\n(?:[ \t]+[^\n]*\n)*', b, re.M)
for name, off in (('spare', 48), ('hdr', 56)):
    ps = set(re.findall(r'\(set \(reg[^ ]*:SI (\d+)[^)]*\)\s*\(mem/f/c:SI \(const:SI \(plus:SI \(symbol_ref:SI \("xb"\)[^\n]*\n\s*\(const_int %d ' % off, b))
    print(name, 'loaded into', sorted(ps, key=int))
    for p in sorted(ps, key=int):
        n = sum(len(re.findall(r'reg[^ ]*:SI %s[ )]' % p, x)) for x in ins)
        cost = re.findall(r'a\d+\(r%s,l\d+\) costs: GENERAL_REGS:\S+ MEM:\S+' % p, b)
        print('  r%s refs(text)=%d' % (p, n), ' '.join(c.split(' costs: ')[0] + ' ' + c.split('MEM:')[1] for c in cost))
for l in re.findall(r'Popping a\d+\(r\d+,l0\)  -- [^\n]*', b)[:0]:
    print(l)
