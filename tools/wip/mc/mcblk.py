"""Block order of mode_client: original (src/mode_client.s) vs a gcc -S intel file.
python mcblk.py <gcc.s> [fn]
Each block: label, calls, string refs (first 20 chars), usage codes."""
import re, sys, os, difflib
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
args=[a for a in sys.argv[1:] if not a.startswith('-')]
fn = args[1] if len(args) > 1 else 'mode_client'

def strings(lines, labre, strre):
    out, cur = {}, None
    for l in lines:
        m = re.match(labre, l.strip())
        if m:
            cur = m.group(1); continue
        m = re.match(strre, l.strip())
        if m and cur:
            out.setdefault(cur, m.group(1).replace('\12', '\n').replace('\n','|').replace('\0', '').replace('\\"','"')[:20])
    return out

def blocks(lines, fnlab, labre, strs, isend):
    s = next(i for i, l in enumerate(lines) if l.strip().startswith(fnlab + ':'))
    res, cur, lab = [], [], fnlab
    for l in lines[s + 1:]:
        l = l.strip()
        if re.match(r'^_\w+:', l) or l.startswith('#@C') or l.startswith('.def') or isend(l):
            break
        m = re.match(labre, l)
        if m:
            if cur: res.append((lab, cur))
            cur, lab = [], m.group(1)
            continue
        if not l or l.startswith('.'):
            continue
        w = l.split()
        op = w[0].lower()
        if op == 'call':
            cur.append('call ' + w[1].lstrip('_').lower())
        elif op.startswith('j'):
            cur.append(op)
            if op == 'jmp':
                res.append((lab, cur)); cur, lab = [], '-'
        elif op == 'ret':
            cur.append('ret'); res.append((lab, cur)); cur, lab = [], '-'
        else:
            for m in re.finditer(r'(L_[0-9a-f]+|_mc_[0-9a-f]+|LC\d+)', l):
                t = m.group(1)
                if t in strs:
                    cur.append('"%s"' % strs[t])
            m = re.match(r'mov\s+dword\s+ptr\s+\[esp(?:\+\d+)?\],\s*(\d+)$', l, re.I)
            if m and m.group(1) not in ('0',):
                cur.append('#' + m.group(1))
    if cur: res.append((lab, cur))
    return res

orig = open(os.path.join(ROOT, 'src', 'mode_client.s')).read().split('\n')
ostr = strings(orig, r'^(L_[0-9a-f]+|_mc_[0-9a-f]+):', r'^\.(?:string|ascii)\s+"(.*)"')
ob = blocks(orig, '_' + fn, r'^(L_[0-9a-f]+):', ostr, lambda l: False)
mine = open(args[0]).read().split('\n')
mstr = strings(mine, r'^(LC\d+):', r'^\.(?:string|ascii)\s+"(.*)"')
mb = blocks(mine, '_' + fn, r'^(L\d+):', mstr, lambda l: l.startswith('.globl') or l.startswith('.ident'))
if '-v' in sys.argv:
    for name, b in (('ORIG', ob), ('MINE', mb)):
        print('==', name)
        for lab, c in b:
            print('%-10s %s' % (lab, ' '.join(c)))
else:
    for l in difflib.unified_diff([' '.join(c) for _, c in ob], [' '.join(c) for _, c in mb], 'original', sys.argv[1], lineterm='', n=100):
        print(l)
