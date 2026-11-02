# bbs.py DUMP b1 b2.. : source lines/syms per block; trace bb numbers are mapped through the
# first "Reordered sequence" table (index -> orig bb) to the renumbered RTL after it.
import re,sys
t=open(sys.argv[1]).read()
i=t.find('Reordered sequence:')
j=t.find('basic blocks,',i)
mp={}
for m in re.finditer(r'^\s*(\d+) bb (\d+)\s',t[i:j],re.M): mp[int(m.group(2))]=int(m.group(1))
s=t[j:]
for b in map(int,sys.argv[2:]):
    c=mp.get(b)
    m=re.search(r'\(note \d+ \d+ \d+ %s \[bb %s\] NOTE_INSN_BASIC_BLOCK\)(.*?)(?=\n;; bb \d+ artificial_defs|\Z)'%(c,c),s,re.S)
    if not m: print(b,'?');continue
    x=m.group(1)
    print(b,'->',c,'lines',sorted(set(re.findall(r'\.c:(\d+)',x))),'syms',list(dict.fromkeys(re.findall(r'symbol_ref[^"]*"([^"]+)"',x)))[:3], 'asmgoto' if 'asm_operands' in x else '', 'probs',re.findall(r'REG_BR_PROB (\d+)',x))
