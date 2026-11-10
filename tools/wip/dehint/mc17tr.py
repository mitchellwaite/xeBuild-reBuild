#!/usr/bin/env python3
"""mode_client attempt 17: bbro's traces of mode_client with the blocks named by what they
reach (strings, callees), from a dump made by `mc17.py -d` / `mc17lib.py -d TAG`.

python tools/wip/dehint/mc17tr.py TAG [-r N] [-k] [-f]
  -r N  only round N's traces
  -k    the heap events (keys) too
  -f    the final order, one block per line, with frequency and preds/succs"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
import mc17lib as L


def fn_part(t, fn='mode_client'):
    t = t[t.index(';; Function %s ' % fn):]
    m = re.search(r'\n;; Function ', t[10:])
    return t[:m.start() + 10] if m else t


def lcs(d):
    """*LCn -> text, from an -S compile of the dump's source"""
    s = os.path.join(d, 'o.s')
    if not os.path.exists(s):
        subprocess.run([bdlib.GCC, '-S', '-O3', '-I' + os.path.join(L.R, 'src'), 'mode_client.c', '-o', 'o.s'],
                       cwd=d, capture_output=True)
    out = {}
    cur = None
    for l in open(s, encoding='latin1'):
        m = re.match(r'^(LC\d+):', l)
        if m:
            cur = m.group(1)
            continue
        m = re.match(r'^\s+\.ascii "(.*)"$', l)
        if m and cur:
            out.setdefault(cur, '')
            out[cur] += m.group(1)
        elif not l.startswith('\t.ascii'):
            cur = None
    return {k: v.replace('\\12', ' ').replace('\\0', '').strip() for k, v in out.items()}


def blocks(d):
    """{bb: dict(freq, name, preds, succs)} from the bbro dump's final RTL (printed with
    the blocks renumbered in layout order; `Reordered sequence` maps them back)"""
    f = [x for x in os.listdir(d) if x.endswith('r.bbro')][0]
    t = fn_part(open(os.path.join(d, f), encoding='latin1').read())
    lc = lcs(d)
    # bbro prints the sequence twice: after the reorder (old numbers) and after the
    # jump fixups (the first sequence's positions, plus compensation blocks)
    seqs = []
    for s in t.split('Reordered sequence:\n')[1:]:
        q = {}
        for l in s.split('\n'):
            m = re.match(r'^ (\d+) (?:bb (\d+)|duplicate of (\d+)|compensation)\s+\[(\d+)\]', l)
            if not m:
                break
            q[int(m.group(1))] = (int(m.group(2)) if m.group(2) else
                                  'dup%s' % m.group(3) if m.group(3) else 'comp%s' % m.group(1))
        seqs.append(q)
    new2old = seqs[0]
    for q in seqs[1:]:
        new2old = {k: (new2old.get(v, v) if isinstance(v, int) else v) for k, v in q.items()}
    out = {}
    body = t[t.index('\n;; basic block 2,'):]
    parts = re.split(r'\n;; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', body)
    for k in range(1, len(parts), 3):
        nb, fr, txt = int(parts[k]), int(parts[k + 1]), parts[k + 2]
        toks = []
        for m in re.finditer(r'\(symbol_ref[^ ]* \("\*?(\w+)"\)', txt):
            n = m.group(1)
            if n in lc:
                toks.append('"%s"' % lc[n][:26])
            elif n.startswith('LC'):
                toks.append(n)
            else:
                toks.append(n + '()')
        if 'client_usage()' in toks:
            m = re.search(r'\(set \(mem:SI \(reg/f:SI 7 sp\)[^\n]*\n\s+\(const_int (\d+)', txt)
            toks = ['usage(%s)' % (m.group(1) if m else '?')]
        m = re.search(r'\(set \(mem/c:SI \(plus:SI \(reg/f:SI 7 sp\)\s+\(const_int 40 [^\n]*\n\s+\(const_int (\d+)', txt)
        if m:
            toks.append('mode=%s' % m.group(1))
        pr = re.search(r';;  pred:(.*?)\n;; bb', txt, re.S)
        su = re.search(r';;  succ:(.*?)\n\n', txt, re.S)

        def edges(s):
            return [(str(new2old.get(int(x), x)) if x.isdigit() else x, p)
                    for x, p in re.findall(r'(\w+) \[([\d.]+)%\]', s.group(1))] if s else []
        out[new2old.get(nb, nb)] = {'freq': fr, 'name': ' '.join(toks) or '-', 'preds': edges(pr),
                                    'succs': edges(su), 'new': nb}
    return out, t


def main():
    a = sys.argv[1:]
    d = os.path.join(L.BUILD, 'd_' + a[0])
    bl, t = blocks(d)
    rnd = int(a[a.index('-r') + 1]) if '-r' in a else None
    if '-f' in a:
        for b in sorted(bl, key=lambda b: bl[b]['new']):
            x = bl[b]
            print('%5s [%5s] %-58s <- %s  -> %s' % (b, x['freq'], x['name'][:58],
                                                   ' '.join('%s:%s' % e for e in x['preds']),
                                                   ' '.join('%s:%s' % e for e in x['succs'])))
        return
    if '-k' in a:
        for l in t.split('\n'):
            if re.match(r'^(STC - round|\s+Possible start|Changing key|Getting bb|Connection|Duplicat|Rotating|Basic block \d+ was visited)', l):
                m = re.search(r'(?:bb |round: |Getting bb )(\d+)', l) or re.search(r': (\d+) \(key', l)
                nm = bl.get(int(m.group(1)), {}).get('name', '') if m else ''
                print(l.rstrip(), '   ', nm[:50])
        return
    for m in re.finditer(r'Trace (\d+) \(round (\d)\):(.*)', t):
        if rnd and int(m.group(2)) != rnd:
            continue
        bs = re.findall(r'(\d+) \[(\d+)\]', m.group(3))
        print('T%-3s r%s' % (m.group(1), m.group(2)),
              ' | '.join('%s[%s] %s' % (b, f, bl.get(int(b), {}).get('name', '?')[:44]) for b, f in bs))
    for l in t.split('\n'):
        if l.startswith('Connection:'):
            print(l)


if __name__ == '__main__':
    main()
