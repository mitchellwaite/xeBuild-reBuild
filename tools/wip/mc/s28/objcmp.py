"""objcmp.py VARIANT.c [extra gcc flags] : compile like build.sh's plain mode_client compile
(#line "mode_client.c", -O3 -fno-toplevel-reorder -fno-ipa-profile -fno-reorder-functions
--param builtin-expect-probability=50) to an object and compare it with build/obj/mode_client.o:
per-function .text (objdump, addresses stripped) and the other sections' bytes."""
import os, re, subprocess, sys, difflib
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
TC = os.path.join(ROOT, 'tools', 'toolchain-4745', 'mingw32', 'bin')
FL = ['-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions', '--param', 'builtin-expect-probability=50']
env = dict(os.environ, PATH=TC + os.pathsep + os.environ['PATH'])


def build(src, out, extra):
    txt = '#line 1 "mode_client.c"\n' + open(src).read()
    p = subprocess.run([os.path.join(TC, 'gcc.exe'), '-c'] + FL + extra + ['-I' + os.path.join(ROOT, 'src'), '-x', 'c', '-', '-o', out],
                       input=txt, text=True, capture_output=True, env=env)
    if p.returncode: sys.exit(p.stderr)


def funcs(o):
    d = subprocess.run([os.path.join(TC, 'objdump.exe'), '-d', '-r', '-M', 'intel', o], capture_output=True, text=True, env=env).stdout
    fs, cur = {}, None
    for l in d.splitlines():
        m = re.match(r'^[0-9a-f]+ <(\S+)>:', l)
        if m: cur = m.group(1); fs[cur] = []; continue
        if cur and re.match(r'^\s+[0-9a-f]+:', l):
            t = l.split('\t')
            body = '\t'.join(t[2:]) if len(t) > 2 else t[-1]
            body = re.sub(r'\b[0-9a-f]+ <', '<', body)
            body = re.sub(r'<[^>]*\+0x[0-9a-f]+>', '<L>', body)
            fs[cur].append(body.strip() + ' | ' + t[1].strip() if len(t) > 2 else 'RELOC ' + l.strip().split(None, 1)[1])
    return fs


def sections(o):
    d = subprocess.run([os.path.join(TC, 'objdump.exe'), '-s', o], capture_output=True, text=True, env=env).stdout
    out, cur = {}, None
    for l in d.splitlines():
        m = re.match(r'^Contents of section (\S+):', l)
        if m: cur = m.group(1); out[cur] = []; continue
        if cur and l.startswith(' '): out[cur].append(l[:43])
    return out


if __name__ == '__main__':
    src = sys.argv[1]
    o = os.path.join(ROOT, 'build', 'v', 'mc28', 'objcmp.o')
    build(src, o, sys.argv[2:])
    ref = os.path.join(ROOT, 'build', 'obj', 'mode_client.o')
    a, b = funcs(ref), funcs(o)
    for f in a:
        if f not in b: print('missing', f); continue
        if a[f] != b[f]:
            n = sum(1 for l in difflib.unified_diff(a[f], b[f], lineterm='', n=0) if l[:1] in '+-' and l[:2] not in ('++', '--'))
            print('DIFF %-24s %d lines' % (f, n))
        else:
            print('ok   %s' % f)
    sa, sb = sections(ref), sections(o)
    for s in sa:
        if s == '.text': continue
        print(('ok   ' if sa[s] == sb.get(s) else 'DIFF ') + 'section ' + s)
