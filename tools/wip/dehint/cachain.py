"""Block chain of sendAvatarData per gimple dump: python cachain.py <dumpdir> [passname...]

For each pass, prints blocks from the prepSysex success log on, in chain order, tagged by what they do.
Needs rfdump.sh's -fdump-tree-all-details -fdump-tree-all-blocks.
"""
import glob, os, re, sys

TAGS = [('Sending avatar', 'GUARD'), ('sending %03d', 'BODY'), ('sending manifest to', 'MF'), ('failed to send %s\\n", _', 'LOOPFAIL'),
        ('failed to send %s\\n", manifest.e', 'LOOPFAIL'), ('failed to send %s\\n", &manifest.path', 'MFFAIL'), ('successfully sent', 'OK'), ('netUnmount', 'OUT'),
        ('mount sysex', 'MNTFAIL'), ('createSysexDirs', 'CREATE'), ('format sysex', 'FMTFAIL')]


def main():
    d = sys.argv[1]
    passes = sys.argv[2:] or ['vrp1', 'dom2', 'ch2', 'ivopts', 'dom3', 'vrp2', 'optimized']
    for p in passes:
        fs = glob.glob(os.path.join(d, '*.' + p))
        if not fs:
            print(p, 'missing')
            continue
        t = open(fs[0]).read()
        m = re.search(r'^;; Function sendAvatarData \(', t, re.M)
        t = t[m.start():t.find('\n;; Function ', m.end())]
        i = t.rfind('\nsendAvatarData (')
        t = t[i:]
        parts = re.split(r'^;;   basic block (\d+), loop depth (\d+), count \d+, freq (\d+)', t, flags=re.M)
        out = []
        for j in range(1, len(parts), 4):
            b, ld, f, body = parts[j:j + 4]
            tag = next((n for s, n in TAGS if s in body), '')
            succ = ' '.join(re.findall(r'succ:\s+(\S+)', body) + re.findall(r'^;;\s{10,}(\d+) \[', body, re.M))
            phis = re.findall(r'# (\w+) = PHI <([^>]*)>', body)
            ph = ';'.join(x + '=<' + y + '>' for x, y in phis if x.startswith(('i_', 'i.', 'ret')))
            out.append('%s[%s]%s->%s %s' % (b, f, tag and ':' + tag, succ, ph))
        print('==', p)
        print('\n'.join(out))


main()
