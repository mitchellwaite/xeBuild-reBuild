# cfg.py DIR : parse DIR/mc.cprop_hardreg (blocks) + DIR/mc.bbro -> trace-time CFG with content
import re, sys, json
def parse(d):
    L = open(d + '/mc.cprop_hardreg').read().split('\n')
    B = {}; cur = None
    for l in L:
        m = re.match(r';; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', l)
        if m:
            cur = int(m.group(1)); B[cur] = dict(f=int(m.group(2)), pred=[], succ=[], n=0, jmp=0, call=[], sym=[], ln=[], ci=[]); mode = None; continue
        if cur is None: continue
        m = re.match(r';;  (pred|succ):(.*)', l)
        if m: mode = m.group(1); l = ';;    ' + m.group(2)
        m = re.match(r';;\s+(\d+|ENTRY|EXIT) \[([\d.]+)%\]\s*(\(([^)]*)\))?', l)
        if m and mode:
            B[cur][mode].append((m.group(1), float(m.group(2)), m.group(4) or '')); continue
        if l.startswith(';;'): mode = None
        b = B[cur]
        if re.match(r'\((insn|call_insn|jump_insn)', l): b['n'] += 1
        if l.startswith('(jump_insn'): b['jmp'] += 1
        for s in re.findall(r'symbol_ref[^(]*\("([^"]+)"', l):
            if s not in b['sym']: b['sym'].append(s)
        m = re.search(r'\.c":(\d+)|\.c:(\d+)', l)
        if m:
            x = int(m.group(1) or m.group(2))
            if x not in b['ln']: b['ln'].append(x)
        for c in re.findall(r'const_int (-?\d+)', l):
            if c not in b['ci'] and abs(int(c)) < 100000: b['ci'].append(c)
    T = open(d + '/mc.bbro').read()
    dele = set(int(x) for x in re.findall(r'deleting block (\d+)', T.split('Trace 1 (round')[0]))
    tr = {}
    for m in re.finditer(r'Trace (\d+) \(round (\d)\):(.*)', T):
        for i, b in enumerate(re.findall(r'(\d+) \[', m.group(3))): tr[int(b)] = (int(m.group(1)), int(m.group(2)), i)
    return B, dele, tr
if __name__ == '__main__':
    B, dele, tr = parse(sys.argv[1])
    live = [b for b in B if b not in dele]
    print('blocks', len(B), 'deleted', len(dele), 'live', len(live), 'in traces', len(tr))
    for b in sorted(B):
        x = B[b]; t = tr.get(b)
        print(b, 'DEL' if b in dele else '', 'f', x['f'], 'n', x['n'], 'T%dr%d' % t[:2] if t else '-', 'L' + ','.join(map(str, x['ln'][:3])), ' '.join(x['sym'][:3]),
              'p:' + ','.join(p[0] for p in x['pred']), 's:' + ','.join(s[0] for s in x['succ']))
