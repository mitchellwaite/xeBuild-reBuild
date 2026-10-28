"""bbins.py DUMP BB... : compact insn patterns of mode_client blocks in a post-reload RTL dump"""
import sys,re
t=open(sys.argv[1]).read()
i=t.find(';; Function mode_client');j=t.find(';; Function',i+5);s=t[i:j if j>0 else None]
parts=re.split(r'\(note \d+ \d+ \d+ (\d+) \[bb \d+\] NOTE_INSN_BASIC_BLOCK\)',s)
blk={}
for k in range(1,len(parts),2): blk[parts[k]]=parts[k+1]
def compact(b):
    out=[]
    for x in re.findall(r'\n\((?:insn|jump_insn|call_insn)[^\n]*(?:\n [^\n]*)*',b):
        x=re.sub(r'C:\\S+','',x); x=re.sub(r'\(expr_list:REG_\w+.*','',x,flags=re.S)
        out.append(' '.join(x.split())[:200])
    return out
for b in sys.argv[2:]:
    print('=== bb',b)
    for l in compact(blk.get(b,'')): print('  ',l)
