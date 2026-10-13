"""Recover the original object files (translation units) of xeBuild.exe.

Every object compiled by gcc contributes one CIE followed by its FDEs to
.eh_frame, in link order, so CIE boundaries give the objects and their
functions.  `units(img)` returns them; run directly to print a profile of each
(functions, imports called, strings referenced) for naming:

python re/units.py <xeBuild.exe> <xeBuild.dbg.s>
"""
import bisect, collections, os, re, struct, sys

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image, strip, imports, symbolize

REF = re.compile(r'(?<![\w.$])(?:FUN|\.L)_([0-9a-f]+)')


def units(img):
    """[(cie_va, [(func_va, length), ...]), ...] in link order."""
    _, eh, ehsz, _, _ = img.sec('.eh_fram')
    out, off = [], 0
    while off < ehsz:
        ln, cid = struct.unpack('<II', img.read(eh + off, 8))
        if not ln:
            off += 4
            continue
        if cid == 0:
            out.append((eh + off, []))
        else:
            f = eh + off + 8
            pc, n = struct.unpack('<II', img.read(f, 8))
            out[-1][1].append(((f + pc) & 0xffffffff, n))
        off += 4 + ln
    return out


def listing(img, dbg):
    """{va: source text} for every addressed line, after symbolize()."""
    lines, addr = strip(dbg)
    symbolize(lines, addr, img)
    text = {}
    for l, a in zip(lines, addr):
        if a is not None and a not in text:
            text[a] = l.strip()
    return text


def main():
    img = Image(sys.argv[1])
    text = listing(img, sys.argv[2])
    starts = sorted(text)
    imp = set(imports(img).values())
    us = units(img)
    _, rd, rdsz, _, _ = img.sec('.rdata')
    _, dt, dtsz, _, _ = img.sec('.data')

    def string_at(va):
        s = text.get(va, '')
        m = re.match(r'\.(?:string|ascii)\s+"(.*)"$', s)
        return m.group(1) if m else None

    # import thunks: `jmp DWORD PTR [name]`
    thunk = {}
    for a, s in text.items():
        m = re.match(r'jmp DWORD PTR \[([A-Za-z_][\w@]*)\]$', s)
        if m and m.group(1) in imp:
            thunk[a] = m.group(1)
    owner = {fa: i for i, (_, fdes) in enumerate(us) for fa, _ in fdes}
    calls_into = collections.defaultdict(set)
    profile = []

    for i, (cie, fdes) in enumerate(us):
        funcs = sorted(fdes)
        imps, strs, data, consts = collections.Counter(), [], set(), collections.Counter()
        for fa, n in funcs:
            k = bisect.bisect_left(starts, fa)
            while k < len(starts) and starts[k] < fa + n:
                src = text[starts[k]].split('#')[0]
                for t in re.findall(r'[A-Za-z_][\w@]*', src):
                    if t in imp:
                        imps[t] += 1
                for m in REF.finditer(src):
                    v = int(m.group(1), 16)
                    s = string_at(v)
                    if v in thunk:
                        imps[thunk[v]] += 1
                    elif v in owner and owner[v] != i:
                        calls_into[i].add(owner[v])
                    elif s is not None and s not in strs:
                        strs.append(s)
                    elif rd <= v < rd + rdsz or dt <= v < dt + dtsz:
                        data.add(v)
                if not src.startswith('.'):
                    for c in re.findall(r'(?<![\w.+\-\[])(-?\d{6,})(?![\w\]])', src):
                        consts['%#x' % (int(c) & 0xffffffff)] += 1
                k += 1
        profile.append((i, cie, funcs, imps, strs, data, consts))
    called_by = collections.defaultdict(set)
    for i, cs in calls_into.items():
        for j in cs:
            called_by[j].add(i)

    for i, cie, funcs, imps, strs, data, consts in profile:
        print('=== unit %d  cie %x  %d funcs  %x-%x' % (
            i, cie, len(funcs), funcs[0][0], funcs[-1][0] + funcs[-1][1]) if funcs else '=== unit %d (no fdes)' % i)
        if imps:
            print('  imports:', ' '.join(sorted(imps)))
        if calls_into[i] or called_by[i]:
            print('  calls units: %s   called by: %s' % (sorted(calls_into[i]), sorted(called_by[i])))
        if consts:
            print('  consts:', ' '.join(c for c, _ in consts.most_common(8)))
        if data:
            print('  data refs: %d' % len(data))
        for s in strs[:8]:
            print('  "%s"' % s[:90])
        if len(strs) > 8:
            print('  ... %d more strings' % (len(strs) - 8))


if __name__ == '__main__':
    main()
