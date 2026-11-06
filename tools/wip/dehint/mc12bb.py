"""mode_client attempt 12: bbro traces of mode_client with each block named by the calls it
makes (first RTL listing of the bbro dump, the numbering the trace lines use).

python tools/wip/dehint/mc12bb.py A.c TAG [-r LO-HI]   (compiles plain -O3 into build/mc4/TAG)
Prints the traces (bb[freq]{calls}), the bbro keys of named blocks and the final order."""
import os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1lib


def dump(src, tag):
    d = os.path.join(bdlib.R, 'build', 'mc4', tag)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'mode_client.c'), 'w', newline='\n').write('#line 1 "mode_client.c"\n' + mc1lib.read_src(src))
    subprocess.run([bdlib.GCC, '-c', '-O3', '-fdump-rtl-bbro-details', '-I' + os.path.join(bdlib.R, 'src'),
                    'mode_client.c', '-o', 'o.o'], cwd=d, capture_output=True)
    p = [f for f in os.listdir(d) if f.endswith('bbro')][0]
    t = open(os.path.join(d, p)).read()
    t = t[t.index(';; Function mode_client '):]
    m = re.search(r'\n;; Function ', t[10:])
    return t[:m.start() + 10] if m else t


SHORT = {'log_printf': 'L', 'strnicmp': 'S', 'client_usage': 'U'}


def names(t):
    """bb -> call names, from the first insn listing after the trace dump."""
    k = t.index('Final order:')
    body = t[k:]
    calls = {}
    seen = set()
    for m in re.finditer(r'\(call_insn(?:/\w)? (\d+) \d+ \d+ (\d+) .*?symbol_ref:SI \("(\w+)"\)', body):
        uid, bb, fn = m.groups()
        if uid in seen:
            continue
        seen.add(uid)
        calls.setdefault(int(bb), []).append(SHORT.get(fn, fn))
    return calls


def main():
    a = sys.argv[1:]
    t = dump(a[0], a[1])
    open(os.path.join(bdlib.R, 'build', 'mc4', a[1], 'mc.bb'), 'w', newline='\n').write(t)
    # call map from the RTL that precedes "Final order"? use the listing before reordering
    pre = t[:t.index('STC - round 1')]
    calls = {}
    for m in re.finditer(r'\(call_insn(?:/\w)? (\d+) \d+ \d+ (\d+) .*?symbol_ref:SI \("(\w+)"\)', t):
        uid, bb, fn = m.groups()
        calls.setdefault(int(bb), [])
        if fn not in calls[int(bb)]:
            calls[int(bb)].append(SHORT.get(fn, fn))
        if 'Final order' in t[:m.start()][-1:]:
            break
    # restrict to the first listing: uid -> bb of first occurrence
    first = {}
    for m in re.finditer(r'\(call_insn(?:/\w)? (\d+) \d+ \d+ (\d+) .*?symbol_ref:SI \("(\w+)"\)', t):
        uid, bb, fn = m.groups()
        if uid not in first:
            first[uid] = (int(bb), SHORT.get(fn, fn))
    calls = {}
    for uid, (bb, fn) in first.items():
        calls.setdefault(bb, []).append(fn)
    def nm(bb):
        c = calls.get(bb)
        return '%d{%s}' % (bb, ','.join(c)) if c else str(bb)
    for m in re.finditer(r'Trace (\d+) \(round (\d)\):(.*)', t):
        items = re.findall(r'(\d+) \[(\d+)\]', m.group(3))
        print('T%s r%s: ' % (m.group(1), m.group(2)) + ' '.join('%s[%s]' % (nm(int(b)), f) for b, f in items))
    fo = re.search(r'Final order:\n(.*)', t).group(1).split()
    print('FINAL:', ' '.join(nm(int(b)) for b in fo if int(b) in calls))


if __name__ == '__main__':
    main()
