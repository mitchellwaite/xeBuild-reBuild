"""Attempt 6: print ipa-cp's evaluations for imgAdd's values (who gets cloned, and how far from the threshold).

python tools/wip/dehint/iw6cp.py <file.c> [-a]     -a: all the "evaluation" lines, not only the first param's"""
import glob, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib


def cp_dump(path):
    text = open(path, newline='').read().replace('\r\n', '\n')
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='t')
    ok, o, d = iwlib.compile_src(text, [], workdir=d, extra=['-fdump-ipa-cp-details'])
    if not ok:
        print(o)
        sys.exit(1)
    fs = glob.glob(os.path.join(d, '*cp*'))
    out = open(fs[0], errors='replace').read() if fs else ''
    iwlib.cleanup(d)
    return out


if __name__ == '__main__':
    t = cp_dump(sys.argv[1])
    open(os.path.join(iwlib.BUILD, 'a6_cp.txt'), 'w').write(t)
    for l in t.split('\n'):
        if re.search(r'Estimating effects for imgAdd|time_benefit|good_cloning_opportunity|size: \d+, time|Creating a specialized node|evaluation:|- estimates for value', l):
            print(l[:170])
