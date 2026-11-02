"""m.py: measure a mode_client variant source (plain compile): inv, order, fq, fncmp.
python m.py SRC.c TAG [--fncmp]  ; as module: meas(text, tag, fncmp=False)"""
import ast, os, subprocess, sys
ROOT = r'C:\Users\Win11VM\Documents\GitHub\xebuildBugFix'
D = os.path.join(ROOT, 'build', 'v', 'mc36'); PY = sys.executable
NEED = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 112, 115, 103, 55, 126, 125, 61, 33, 29, 67,
        127, 117, 130, 35, 42, 53, 77, 79]
FLAGS = ['-I' + os.path.join(ROOT, 'src'), '-O3', '-fno-toplevel-reorder', '-fno-ipa-profile', '-fno-reorder-functions',
         '--param', 'builtin-expect-probability=50']
def meas(text, tag, fncmp=False):
    p = os.path.join(D, 'v_%s.c' % tag); sd = os.path.join(D, 'slot_%s' % tag)
    open(p, 'w', newline='\n').write(text)
    r = subprocess.run([PY, os.path.join(ROOT, 'tools/wip/mc/s19/mkslot.py'), p, sd], capture_output=True, text=True)
    if r.returncode: return {'err': r.stderr[-2000:] + r.stdout[-2000:]}
    r = subprocess.run([PY, os.path.join(ROOT, 'tools/wip/mc/s18/analyze.py'), sd], capture_output=True, text=True)
    try:
        l = r.stdout.strip().splitlines()
        tok = l[2].split()[1:]
        o = [int(x) for x in tok if x.isdigit()]
        miss = [b for b in NEED if b not in o]
        if len(tok) > len(o) and len(miss) <= len(tok) - len(o): miss = []
        res = {'fq': ast.literal_eval(l[0])['fq'], 'inv0': int(l[1].split()[1]), 'inv': int(l[1].split()[1]) + 5 * len(miss), 'order': l[2], 'miss': miss, 'raw': l}
    except Exception as e:
        return {'err': 'analyze ' + repr(e) + r.stdout[-3000:] + r.stderr[-2000:]}
    if fncmp:
        r = subprocess.run([PY, os.path.join(ROOT, 'tools/re/fncmp.py'), p, 'mode_client'] + FLAGS, capture_output=True, text=True, cwd=ROOT, env=dict(os.environ, FNCMP_LITERALS='1'))
        out = r.stdout + r.stderr
        import re
        res['fncmp'] = 0 if 'MATCH' in out else len([l for l in out.splitlines() if re.match(r'^[-+](?![-+])', l)])
    return res
if __name__ == '__main__':
    r = meas(open(sys.argv[1]).read(), sys.argv[2], '--fncmp' in sys.argv)
    for k, v in r.items():
        if k not in ('fq',): print(k, v)
