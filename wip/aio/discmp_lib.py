import os, re, sys
import subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 're'))
import fncmp


def norm_gcc(l):
    n = fncmp.norm([l])
    return n[0] if n else ''


def orig_stream():
    lines = subprocess.run(['git', 'show', '56e988e:src/app/options.s'], capture_output=True, text=True, check=True).stdout.split('\n')
    s = lines.index('_applyIniOptions:')
    out, lab = [], None
    for l in lines[s + 1:]:
        if l.startswith('#@C') or l.startswith('.section') or re.match(r'^_\w+:', l):
            break
        m = re.match(r'^L_([0-9a-f]+):', l.strip())
        if m:
            lab = int(m.group(1), 16); continue
        if re.search(r'\.byte|\bnop\b|mov ESI,ESI', l):
            continue
        n = fncmp.norm([l])
        if n:
            out.append((None, lab, n[0]))
            lab = None
    return out
