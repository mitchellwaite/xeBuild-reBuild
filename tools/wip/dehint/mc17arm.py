#!/usr/bin/env python3
"""mode_client attempt 17: the option arms one by one.  For each variant, every arm's
instructions (from its strnicmp to the jump back to the latch, jump targets dropped)
against the reference's, so a change in one arm's code shows apart from layout changes.

python tools/wip/dehint/mc17arm.py [-s ARM] VARIANT ..
  prints, per variant, the arms that differ (lines) and the usage blocks (code, register);
  -s ARM also prints that arm's instructions next to the reference's."""
import difflib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib
import mc17
import mc17lib as L


def arms(o):
    """({option: [insn]}, [usage block text]) of _mode_client"""
    t = subprocess.run([bdlib.OBJDUMP, '-d', '-r', '--no-show-raw-insn', o], capture_output=True, text=True).stdout
    b = L.section(o, '.rdata')

    def lit(off):
        e = b.find(b'\0', off)
        return b[off:e].decode('latin1')
    ins = []
    cur = False
    for l in t.split('\n'):
        m = re.match(r'^([0-9a-f]+) <(.+)>:$', l)
        if m:
            cur = m.group(2) == '_mode_client'
            continue
        if not cur:
            continue
        m = re.match(r'^\s*([0-9a-f]+):\s+(\S.*)$', l)
        if not m:
            continue
        s = m.group(2).strip()
        if re.match(r'^(dir32|DISP32)\s', s):
            ins[-1] = ins[-1] + ' ' + s.split()[-1]
        else:
            ins.append(s)
    out, use = {}, []
    name = None
    for k, s in enumerate(ins):
        m = re.match(r'^movl\s+\$0x([0-9a-f]+),0x4\(%esp\) \.rdata$', s)
        if m and k + 3 < len(ins) and any('_strnicmp' in x for x in ins[k:k + 5]):
            x = lit(int(m.group(1), 16))
            if x.startswith('-') or x in ('help', '/?'):
                name = x
                out[name] = []
        if name is not None:
            out[name].append(re.sub(r'^(j\w+)\s+[0-9a-f]+ <.*$', r'\1', re.sub(r'^call\s+[0-9a-f]+ <_mode_client.*> (\S+)$', r'call \1', s)))
            if re.match(r'^jmp\s', s) or s.endswith('<_client_usage>'):
                name = None
        if s.endswith('<_client_usage>'):
            use.append(' | '.join(x for x in ins[k - 3:k] if 'esp' in x or 'ebx' in x))
    return out, use


_ref = arms(L.REF)


def compare(text):
    ok, o, d = L.compile_src(text)
    try:
        if not ok:
            return None, o
        a, use = arms(o)
        diff = {}
        for n, x in _ref[0].items():
            y = a.get(n, [])
            if x != y:
                sm = difflib.SequenceMatcher(None, x, y, autojunk=False)
                diff[n] = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal')
        return (a, use, diff), None
    finally:
        L.cleanup(d)


if __name__ == '__main__':
    args = sys.argv[1:]
    show = None
    if '-s' in args:
        k = args.index('-s'); show = args[k + 1]; del args[k:k + 2]
    for v in args:
        r, err = compare(mc17.text_of(v))
        if err:
            print(v, 'COMPILE', err.strip().split('\n')[-1][:120])
            continue
        a, use, diff = r
        print('%s\n  arms: %s\n  usage blocks: %d (reference %d)%s' % (
            v, ' '.join('%s:%d' % kv for kv in diff.items()) or 'all equal', len(use), len(_ref[1]),
            '' if sorted(use) == sorted(_ref[1]) else '  differ'))
        if show:
            for l in difflib.unified_diff(_ref[0].get(show, []), a.get(show, []), 'ref', 'new', n=30, lineterm=''):
                print('   ', l)
