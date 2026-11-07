"""Attempt 14: find basic blocks that reach bb-reorder with no code (only labels, notes and
USE/CLOBBER insns, or an asm with an empty template), in every app object compiled
with its build.sh flags (or in one source given on the command line).

python tools/wip/dehint/op14scan.py [obj|path.c ...]   (default: every non-crypto object)
Dumps go to build/op/a14scan/<name>/.  For each empty block: function, bb, freq, preds,
succs, source lines of its neighbours, and whether bbro's trace dump names it."""
import os, re, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TC = os.path.join(R, 'tools', 'toolchain-4745', 'mingw32', 'bin')
GCC = os.path.join(TC, 'gcc.exe')
OUT = os.path.join(R, 'build', 'op', 'a14scan')
APP = ('bootloaders mode_update stfs mode_client filelist_ini timeutil smc sysupdate main '
       'mode_extract xboxrom image_write keyvault image_read mode_ini mode_build keys net '
       'fileutil options build consoleinfo console_hdd log crc32').split()


def flags(name):
    if name == 'options':
        return ['-O3', '--param', 'builtin-expect-probability=83']
    return ['-O3']


def compile_dump(src, name, fl=None, extra=()):
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if '.c.' in f:
            os.remove(os.path.join(d, f))
    a = os.path.join(d, 'a.c')
    with open(src, encoding='latin-1') as f:
        t = f.read()
    with open(a, 'w', newline='\n', encoding='latin-1') as f:
        f.write(t)
    env = dict(os.environ)
    env['PATH'] = TC + os.pathsep + env['PATH']
    cmd = [GCC, '-S'] + (fl or flags(name)) + list(extra) + [
        '-I', os.path.join(R, 'src'), '-I', os.path.dirname(os.path.abspath(src)),
        '-I', os.path.join(R, 'src', 'crypto'), 'a.c', '-o', 'o.s',
        '-fdump-rtl-cprop_hardreg-blocks-details', '-fdump-rtl-bbro-details']
    p = subprocess.run(cmd, cwd=d, env=env, capture_output=True, text=True)
    if p.returncode:
        print(p.stderr)
        raise SystemExit('compile failed: ' + name)
    return d


def funcs(text):
    parts = re.split(r'^;; Function (\S+)', text, flags=re.M)
    for i in range(1, len(parts), 2):
        yield parts[i], parts[i + 1]


BBH = re.compile(r'^;; basic block (\d+), loop depth \d+, count \d+, freq (\d+)', re.M)


def blocks(body):
    """bb -> dict(freq, preds, succs, insns, lines)"""
    out = {}
    hs = list(BBH.finditer(body))
    for k, m in enumerate(hs):
        end = hs[k + 1].start() if k + 1 < len(hs) else len(body)
        chunk = body[m.start():end]
        b = int(m.group(1))
        pm = re.search(r';;  pred:(.*?)\n(?=;; bb|;; lr|\(|;;  succ)', chunk, re.S)
        sm = re.search(r';;  succ:(.*?)\n(?=;; lr|;; live|\(|$)', chunk, re.S)
        preds = re.findall(r'(\d+|ENTRY) \[', pm.group(1)) if pm else []
        succs = re.findall(r'(\d+|EXIT) \[', sm.group(1)) if sm else []
        ins = []
        for im in re.finditer(r'^\((insn|jump_insn|call_insn|debug_insn)\b(.*?)(?=^\(|^;;|\Z)', chunk, re.M | re.S):
            kind, rest = im.group(1), im.group(2)
            if kind == 'debug_insn':
                continue
            pat = re.search(r'\((\w+)', rest[rest.find('(', 1):] if False else rest)
            m2 = re.search(r'^\s*\d+ \d+ \d+ \d+ \((\w+)', rest)
            code = m2.group(1) if m2 else '?'
            empty_asm = 'asm_operands' in rest and '("")' in rest
            ins.append((kind, code, empty_asm))
        lines = [int(x) for x in re.findall(r'a\.c:(\d+)', chunk)]
        out[b] = dict(freq=int(m.group(2)), preds=preds, succs=succs, ins=ins, lines=lines)
    return out


def is_empty(bl):
    for kind, code, ea in bl['ins']:
        if kind == 'insn' and code in ('use', 'clobber'):
            continue
        if ea and kind == 'jump_insn':
            continue
        if kind == 'insn' and ea:
            continue
        return False
    return True


def scan(d, name, src_lines):
    pre = open(os.path.join(d, [f for f in os.listdir(d) if f.endswith('r.cprop_hardreg')][0]),
               encoding='latin-1').read()
    bb = open(os.path.join(d, [f for f in os.listdir(d) if f.endswith('r.bbro')][0]),
              encoding='latin-1').read()
    bbf = dict(funcs(bb))
    found = 0
    for fn, body in funcs(pre):
        bls = blocks(body)
        tr = bbf.get(fn, '')
        for b, bl in sorted(bls.items()):
            if not is_empty(bl):
                continue
            # skip entry-ish empty blocks with no info
            kinds = ','.join('%s:%s%s' % (k, c, '*' if e else '') for k, c, e in bl['ins']) or '-'
            in_trace = bool(re.search(r'\b(?:Getting|bb) %d\b' % b, tr))
            neigh = []
            for p in bl['preds']:
                if p.isdigit() and int(p) in bls and bls[int(p)]['lines']:
                    l = bls[int(p)]['lines'][-1]
                    neigh.append('p%s@%d' % (p, l))
            print('%-14s %-28s bb %3d freq %5d preds %-14s succs %-10s ins %-24s %s %s' % (
                name, fn, b, bl['freq'], ','.join(bl['preds']), ','.join(bl['succs']) or '(none)',
                kinds, 'T' if in_trace else '-', ' '.join(neigh)))
            for p in bl['preds']:
                if p.isdigit() and int(p) in bls and bls[int(p)]['lines']:
                    l = bls[int(p)]['lines'][-1]
                    if 0 < l <= len(src_lines):
                        print('      %d: %s' % (l, src_lines[l - 1].strip()[:100]))
            found += 1
    return found


def main():
    args = sys.argv[1:] or APP
    for a in args:
        if a.endswith('.c'):
            src, name = a, 'x_' + os.path.basename(a)[:-2]
        else:
            src, name = os.path.join(R, 'src', a + '.c'), a
        d = compile_dump(src, name)
        sl = open(os.path.join(d, 'a.c'), encoding='latin-1').read().split('\n')
        scan(d, name, sl)


if __name__ == '__main__':
    main()
