"""python tools/wip/dehint/bdanchors.py <file.c> <fn>: fn's block order in build/bd/reference.o against the draft,
read off its anchors (calls by name, .rdata string offsets, ret) and diffed as sequences.  A moved block shows as
a -/+ pair; registers and jumps are ignored.  Attempt 9 (loadBl's whole-function reconstructions)."""
import difflib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib


def text(o, fn):
    t = subprocess.run([bdlib.OBJDUMP, '-d', '-r', '-M', 'intel', '--no-show-raw-insn', o],
                       capture_output=True, text=True).stdout
    out, p = [], False
    for l in t.split('\n'):
        m = re.match(r'^[0-9a-f]+ <(.+)>:$', l)
        if m:
            p = m.group(1) == '_' + fn
            continue
        if p:
            out.append(l)
    return out


def anchors(lines):
    out = []
    for i, l in enumerate(lines):
        m = re.search(r'DISP32\s+(\S+)', l)
        if m:
            out.append(m.group(1))
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) else ''
        if 'dir32\t.rdata' in nxt:
            m = re.search(r'(0x[0-9a-f]+)\s*$', l.strip()) or re.search(r'(0x[0-9a-f]+)', l)
            if m:
                out.append('s' + m.group(1))
        if re.search(r'\bret\b', l):
            out.append('RET')
        m = re.search(r'call\s+\S+ <_(\w+)>', l)
        if m and m.group(1) != sys.argv[2]:
            out.append(m.group(1))
    return out


def main():
    ok, o, d = bdlib.compile_src(bdlib.read_src(sys.argv[1]))
    if not ok:
        print(o)
        return
    a = anchors(text(bdlib.REF, sys.argv[2]))
    b = anchors(text(o, sys.argv[2]))
    bdlib.cleanup(d)
    for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if t == 'equal':
            print('  ', ' '.join(a[i1:i2]))
        else:
            if i2 > i1:
                print('- ', ' '.join(a[i1:i2]))
            if j2 > j1:
                print('+ ', ' '.join(b[j1:j2]))


if __name__ == '__main__':
    main()
