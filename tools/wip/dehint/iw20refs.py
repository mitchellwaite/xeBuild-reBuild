import re,sys
d,fn=sys.argv[1],sys.argv[2]; regs=sys.argv[3:]
import glob
t=open(glob.glob(d+'/*.ira')[0],errors='replace').read()
m=re.search(r'^;; Function %s \(%s,.*?(?=^;; Function |\Z)'%(fn,fn),t,re.S|re.M).group(0)
last=m[m.rfind('\n;; basic block 2,'):]
cur=None
pat=r'\(reg(?:/[a-z]+)*:[A-Z0-9]+ (%s)\b'%'|'.join(regs)
for blk in re.split(r'(?=^(?:\(insn|\(jump_insn|\(call_insn|\(note|\(barrier|\(code_label|\(debug_insn|;; basic block ))',last,flags=re.M):
    x=re.match(r';; basic block (\d+), loop depth (\d+), count \d+, freq (\d+)',blk)
    if x: cur=x.groups(); continue
    if re.match(r'\((insn|jump_insn) ',blk):
        b=re.split(r'\(expr_list|\(nil\)|\(int_list',blk)[0]
        if re.search(pat,b): print(cur,' '.join(b.split())[:150])
