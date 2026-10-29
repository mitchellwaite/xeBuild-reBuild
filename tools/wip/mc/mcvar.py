"""Compile a mode_client variant and score its round-4 trace order against the original's.
python mcvar.py <variant.c> [gcc flags]   (env: FNCMP=1 also runs fncmp)
Prints: inv=<inversions> pre=<matching prefix> [fncmp=<lines>] and the order as signatures."""
import os, re, subprocess, sys, shutil, hashlib
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
BIN = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'wip'))
S = os.path.dirname(os.path.abspath(__file__))
# the original's round-4 order, as signatures (see sigs())
WANT = ['strnicmp:-ip', 'log:cannot send avatar d', 'log:cannot send xbox com', 'usage:2', 'strnicmp:-r', 'log:Block 0x%x is outsid',
        'log:Failed to erase bloc', 'strnicmp:-w', 'usage:4:cx', 'usage:3:cx', 'strnicmp:-e', 'log:Invalid arguments sp', 'clientPatches:0',
        'clientInfo:0', 'usage:5:cx', 'usage:5:dx', 'usage:3:dx', 'usage:3:ax', 'usage:5:ax', 'strnicmp:-c', 'strnicmp:-i',
        'strnicmp:-p', 'strnicmp:-v', 'usage:1']

def section(txt, fn):
    s = txt.index(';; Function %s ' % fn)
    e = txt.find('\n;; Function ', s + 1)
    return txt[s:e if e > 0 else len(txt)]

def sigs(cbody, asm):
    strs, cur = {}, None
    for l in asm.split('\n'):
        m = re.match(r'^(LC\d+):', l)
        if m: cur = m.group(1); continue
        m = re.match(r'^\s*\.(?:ascii|string)\s+"(.*)"', l)
        if m and cur: strs.setdefault(cur, m.group(1).replace('\\12', '').replace('\\0', '').replace('\\n', '').replace('*', '').replace(' ERROR: ', '')); cur = None
    out, cur, blk = {}, None, {}
    chunks = re.split(r'(?m)^(?=\((?:insn|call_insn|jump_insn|note|code_label|barrier|debug_insn))', cbody)
    for ch in chunks:
        m = re.search(r'\[bb (\d+)\] NOTE_INSN_BASIC_BLOCK', ch)
        if m: cur = int(m.group(1)); blk[cur] = {'call': [], 'str': [], 'const': [], 'idx': []}; continue
        if cur is None or not ch.startswith(('(insn', '(call_insn', '(jump_insn')): continue
        m = re.search(r'\(call \(mem:QI \(symbol_ref:SI \("(\w+)"\)', ch)
        if m: blk[cur]['call'].append(m.group(1))
        for m in re.finditer(r'\(symbol_ref(?:/\w)?:SI \("\*?(LC\d+)"\)', ch): blk[cur]['str'].append(strs.get(m.group(1), m.group(1)))
        m = re.search(r'\(set \(mem:SI (?:\(reg/f:SI 7 sp\)|\(plus:SI \(reg/f:SI 7 sp\)\s*\(const_int \d+ \[0x[0-9a-f]+\]\)\))\s*\[[^\]]*\]\)\s*\(const_int (-?\d+) ', ch, re.S)
        if m: blk[cur]['const'].append(m.group(1))
        m = re.search(r'\(mult:SI \(reg(?:/\w)*:SI \d+ (\w+)', ch)
        if m: blk[cur]['idx'].append(m.group(1))
    for b, d in blk.items():
        if 'client_usage' in d['call']:
            code = [c for c in d['const'] if c != '0']
            s = 'usage:' + (code[0] if code else '0') + (':' + d['idx'][0] if d['idx'] and code and code[0] in ('3', '4', '5') else '')
        elif 'strnicmp' in d['call'] and d['str']:
            s = 'strnicmp:' + d['str'][0][:3]
        elif 'log_printf' in d['call'] and d['str'] and d['str'][0].startswith(('cannot', 'Block', 'Failed', 'Invalid arg', 'invalid mode')):
            s = 'log:' + d['str'][0][:20]
        elif d['call'] in (['clientPatches'], ['clientInfo']) and '0' in d['const'] and not d['str']:
            s = d['call'][0] + ':0'
        else:
            s = None
        out[b] = s
    return out

def order(bbro):
    o = []
    r4 = bbro[bbro.index('STC - round 4'):]
    for m in re.finditer(r'^Getting bb (\d+)\n(Basic block \1 was visited)?', r4, re.M):
        if m.group(2): o.append(int(m.group(1)))
    return o

def score(o):
    pos = {s: i for i, s in enumerate(WANT)}
    pre = 0
    for a, b in zip(o, WANT):
        if a != b: break
        pre += 1
    inv = sum(1 for i in range(len(o)) for j in range(i + 1, len(o)) if pos[o[i]] > pos[o[j]])
    return inv, pre

def run(src, flags, fncmp=False, fn='mode_client'):
    d = os.path.join(S, 'var', hashlib.md5((src + ' '.join(flags)).encode()).hexdigest()[:10])
    os.makedirs(d, exist_ok=True)
    shutil.copy(src, os.path.join(d, 'v.c'))
    env = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get('PATH', ''))
    r = subprocess.run([os.path.join(BIN, 'gcc.exe'), '-S', '-masm=intel', '-fno-asynchronous-unwind-tables'] + flags +
                       ['-fdump-rtl-bbro-details', '-fdump-rtl-compgotos-blocks', 'v.c', '-o', 'v.s'], cwd=d, env=env, capture_output=True, text=True)
    if r.returncode:
        return None, r.stderr
    bbro = section(open(os.path.join(d, 'v.c.274r.bbro')).read(), fn)
    cg = section(open(os.path.join(d, 'v.c.267r.compgotos')).read(), fn)
    sg = sigs(cg, open(os.path.join(d, 'v.s')).read())
    o = [sg.get(b) for b in order(bbro)]
    o = [s for s in o if s in WANT]
    res = {'inv': score(o)[0], 'pre': score(o)[1], 'order': o, 'dir': d, 'missing': [w for w in WANT if w not in o]}
    if fncmp:
        rr = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 're', 'fncmp.py'), src, fn] + flags, cwd=ROOT, env=dict(os.environ, FNCMP_LITERALS='1'), capture_output=True, text=True)
        out = rr.stdout + rr.stderr
        res['fncmp'] = 0 if 'MATCH' in out else len([l for l in out.splitlines() if re.match(r'^[-+](?![-+])', l)])
    return res, ''

if __name__ == '__main__':
    src = sys.argv[1]
    flags = sys.argv[2:] or ['-O3', '--param', 'builtin-expect-probability=50']
    res, err = run(src, flags, fncmp=bool(os.environ.get('FNCMP')))
    if res is None: sys.exit(err)
    print('inv=%d pre=%d%s missing=%s' % (res['inv'], res['pre'], ' fncmp=%d' % res['fncmp'] if 'fncmp' in res else '', res['missing']))
    print(' '.join(res['order']))
