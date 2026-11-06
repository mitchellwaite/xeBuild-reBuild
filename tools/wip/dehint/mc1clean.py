"""mode_client attempt 1: tidy a rendered mc1.py state and check each step stays identical.

python tools/wip/dehint/mc1clean.py in.c out.c
Steps (each kept only if the object stays IDENTICAL vs build/mc/reference.o):
  tramp   dead asm-goto trampolines (rkN:/faN: not in the label list, orkN:/ofaN: nothing reaches)
  labels  plain labels nothing jumps to, one at a time (AT(x) and `x:` forms)"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc1lib


def ident(text):
    s = mc1lib.score_text(text)
    return bool(s.get('identical')), mc1lib.fmt(s)[:120]


def used_labels(text):
    body = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    used = set(re.findall(r'goto (\w+);', body))
    for m in re.finditer(r'(?:JMP\(|: ?: ?)([\w, ]+)\);', body):
        used |= {x.strip() for x in m.group(1).split(',')}
    return used


def tramp(text):
    m = re.search(r'__asm__ goto \("" :::: ([\w, ]+)\); goto rkn0;', text)
    if m:
        labs = {x.strip() for x in m.group(1).split(',')}
        text = re.sub(r'rk(\d+): goto ork\1; ', lambda k: k.group(0) if 'rk' + k.group(1) in labs else '', text)
    m = re.search(r'__asm__ goto \("" :::: ([\w, ]+)\); fkA2:', text)
    if m:
        labs = {x.strip() for x in m.group(1).split(',')}
        text = re.sub(r'fa(\d+): goto ofa\1; ', lambda k: k.group(0) if 'fa' + k.group(1) in labs else '', text)
    for _ in range(3):
        used = used_labels(text)
        text = re.sub(r'(ork|ofa)(\d+): goto \w+; ?', lambda k: k.group(0) if k.group(1) + k.group(2) in used else '', text)
    return text


def label_sites(text):
    """(start, end, name) of each removable label definition"""
    out = []
    bad = [(m.start(), m.end()) for m in re.finditer(r'/\*.*?\*/|#define[^\n]*', text, re.S)]
    def skip(a):
        return any(x <= a < y for x, y in bad)
    for m in re.finditer(r'AT\((\w+)\) ?', text):
        if skip(m.start()):
            continue
        out.append((m.start(), m.end(), m.group(1)))
    for m in re.finditer(r'(?<![\w:"%\'])([A-Za-z_]\w*): ?;? ?(?=[\w{(]|\n|$)', text):
        n = m.group(1)
        if skip(m.start()):
            continue
        if n in ('default', 'case', 'public', 'http') or re.match(r'\s*case\b', text[m.start() - 6:m.start()]):
            continue
        line = text[text.rfind('\n', 0, m.start()) + 1:m.start()]
        if '"' in line and line.count('"') % 2:
            continue
        out.append((m.start(), m.end(), n))
    return out


def main():
    src, dst = sys.argv[1], sys.argv[2]
    text = mc1lib.read_src(src)
    ok, r = ident(text)
    print('base', r)
    assert ok
    t2 = tramp(text)
    ok, r = ident(t2)
    print('tramp', r)
    if ok:
        text = t2
    changed = True
    while changed:
        changed = False
        used = used_labels(text)
        for a, b, n in sorted(label_sites(text), reverse=True):
            if n in used:
                continue
            t2 = text[:a] + text[b:]
            if '__attribute__((cold))' in text[b:b + 30]:
                continue
            ok, r = ident(t2)
            print('label', n, r)
            if ok:
                text = t2
                changed = True
                break
    open(dst, 'w', newline='\n').write(text)


if __name__ == '__main__':
    main()
