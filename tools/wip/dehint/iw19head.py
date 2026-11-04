"""python tools/wip/dehint/iw19head.py <file.c>...: finalizeImage's ECD page head frequency at IRA (the block where the pseudo holding xb.hdr is used, highest frequency), which must be >= 350 for REG_FREQ 35 (attempt 9's (A)), plus the lines against the reference."""
import glob, os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import iwlib
def head(text):
    d = tempfile.mkdtemp(dir=iwlib.BUILD, prefix='hd')
    ok, o, d = iwlib.compile_src(text, [], workdir=d, extra=['-fdump-rtl-ira-all'])
    try:
        if not ok:
            return None, {'compile': o[:300]}
        idn, tot, per, notes = iwlib.report(o)
        r = {'identical': idn, 'total': tot, 'per': per, 'notes': notes}
        t = open(glob.glob(os.path.join(d, '*.ira'))[0], errors='replace').read()
        b = re.search(r'^;; Function finalizeImage \(.*?(?=^;; Function |\Z)', t, re.S | re.M).group(0)
        pp = re.findall(r'\(set \(reg[^ ]*:SI (\d+)[^)]*\)\s*\(mem/f/c:SI \(const:SI \(plus:SI \(symbol_ref:SI \("xb"\)[^\n]*\n\s*\(const_int 56 ', b)
        best = 0
        parts = re.split(r'^;; basic block (\d+), loop depth (\d+), count 0, freq (\d+)', b, flags=re.M)
        for i in range(1, len(parts) - 3, 4):
            f = int(parts[i + 2]); body = parts[i + 3]
            if any(re.search(r'\(plus:SI[^\n]*\(reg[^ ]*:SI %s ' % p, body) or re.search(r'\n\s+\(reg[^ ]*:SI %s [^\n]*\)\)\)? ' % p, body) for p in pp) and f > best:
                best = f
        return best, r
    finally:
        iwlib.cleanup(d)
if __name__ == '__main__':
    for p in sys.argv[1:]:
        h, r = head(open(p, newline='').read().replace('\r\n', '\n'))
        print(p, 'head', h, iwlib.fmt(r)[:100])
