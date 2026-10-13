"""Audit ddisasm's symbolization against IDA's view of which values are addresses.

python re/audit.py <xeBuild.exe> <xeBuild.dbg.s> <ida_dump.json> [report.txt]

The rebuild is byte-exact either way; this finds what would break once code or
data moves.  Categories (report lists every entry, stdout the counts):
  missed        IDA: operand/marked data word is an address; ddisasm wrote a number
  maybe-label   unmarked data dword whose value is exactly a label/function start
  maybe         other unmarked in-image data dwords left as numbers (mostly tables)
  false         ddisasm wrote an address symbol where IDA sees a plain constant
  imagebase     __ImageBase used as a number (only matters if the base changes)
  cross-section `sym+off` whose target lies in another section
  cross-label   `sym+off` reaching past a neighbouring label (matters if data is
                reordered or split into objects, not while the layout is kept)
  raw           sections kept as bytes although they hold addresses/RVAs
"""
import json, re, sys, os, bisect, collections

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image, strip, imports, symbolize

LO, HI = 0x401000, 0x513000
LABEL = re.compile(r'(?:FUN|\.L)_([0-9a-f]+)(?:_END)?$')
ADDRSYM = re.compile(r'(?<![\w.$])(FUN_[0-9a-f]+|\.L_[0-9a-f]+(?:_END)?|__ImageBase|__EntryPoint)(?![\w.$])')
EXPR = re.compile(r'((?:FUN|\.L)_[0-9a-f]+(?:_END)?)\s*([+-]\s*\d+)?')


def main():
    exe, dbg, ida = sys.argv[1:4]
    rep = open(sys.argv[4], 'w', newline='\n') if len(sys.argv) > 4 else None
    img = Image(exe)
    imp = set(imports(img).values())
    lines, addr = strip(dbg)
    symbolize(lines, addr, img)  # audit what src/xeBuild.s says, not raw ddisasm
    secs = [(n, va, va + max(vsz, rsz)) for n, va, vsz, _, rsz in img.secs]
    sec_of = lambda a: next((n for n, lo, hi in secs if lo <= a < hi), None)
    in_img = lambda v: LO <= v < HI

    def addr_syms(src):
        code = src.split('#')[0]
        return ADDRSYM.findall(code) + [t for t in re.findall(r'[A-Za-z_][\w@]*', code) if t in imp]

    starts, text = [], {}
    for l, a in zip(lines, addr):
        if a is not None and (not starts or a != starts[-1]):
            starts.append(a)
            text[a] = l.strip()

    def line_at(p):
        i = bisect.bisect_right(starts, p) - 1
        return starts[i] if i >= 0 else None

    d = json.load(open(ida))
    labels = sorted({int(m.group(1), 16) for l in lines if l.endswith(':')
                     for m in [LABEL.match(l[:-1].strip())] if m}
                    | {int(k) for k in d['names']} | {f[0] for f in d['funcs']})
    labelset = set(labels)
    out = collections.defaultdict(list)

    # --- instruction operands: IDA address fields vs address symbols in the line
    for ea, n, fields, dis in d['insns']:
        src = text.get(ea)
        if src is None or src.startswith('.byte 0x'):
            continue
        syms = addr_syms(src)
        want = [f for f in fields if f[0] in ('rel', 'far') or
                (f[0] in ('abs', 'disp', 'imm') and in_img(f[3]))]
        row = '%x  %-44s | %s' % (ea, dis, src)
        if '__ImageBase' in src:
            out['imagebase'].append(row)
        elif len(want) > len(syms):
            out['missed'].append(row)
        elif len(syms) > len(want):
            out['false'].append(row)

    # --- data words
    for p, v, marked in d['data_offsets']:
        s = line_at(p)
        src = text.get(s, '')
        if not src.startswith('.') or (s == p and src.startswith('.long') and addr_syms(src)):
            continue  # operand bytes inside an instruction (checked above) or symbolized
        row = '%x  -> %x  %-8s | %s' % (p, v, sec_of(v) or '-', src[:60])
        if marked:
            out['missed'].append(row)
        elif in_img(v) and v in labelset:
            out['maybe-label'].append(row)
        elif in_img(v):
            out['maybe'].append(row)
    ida_data = {p for p, v, marked in d['data_offsets']}
    for a, src in text.items():
        if src.startswith('.long') and addr_syms(src) and ' - .' not in src and a not in ida_data:
            out['false'].append('%x  data | %s' % (a, src))

    # --- sym+off reaching another section or past another label
    for a, src in text.items():
        for m in EXPR.finditer(src.split('#')[0]):
            off = int(m.group(2).replace(' ', '')) if m.group(2) else 0
            if not off:
                continue
            base = int(LABEL.match(m.group(1)).group(1), 16)
            tgt = base + off
            row = '%x  %s%+d -> %x | %s' % (a, m.group(1), off, tgt, src[:70])
            if sec_of(base) != sec_of(tgt):
                out['cross-section'].append(row + '  (%s -> %s)' % (sec_of(base), sec_of(tgt)))
                continue
            i = bisect.bisect_right(labels, min(base, tgt))
            if i < len(labels) and labels[i] <= max(base, tgt) and labels[i] != base:
                out['cross-label'].append(row)

    # --- whole sections left raw
    for name in ('.idata', '.rsrc', '.eh_fram'):
        _, va, vsz, _, _ = img.sec(name)
        n = sum(1 for a, s in text.items() if va <= a < va + vsz and addr_syms(s))
        out['raw'].append('%-9s %#x bytes, %d symbolic lines' % (name, vsz, n))

    for k in ('missed', 'maybe-label', 'maybe', 'false', 'imagebase', 'cross-section', 'cross-label', 'raw'):
        print('%-14s %d' % (k, len(out[k])))
        if rep:
            rep.write('==== %s (%d)\n%s\n' % (k, len(out[k]), '\n'.join(out[k])))


if __name__ == '__main__':
    main()
