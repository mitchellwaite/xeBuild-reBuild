"""Make ddisasm's GNU-syntax output re-assemble to the exe's original encodings.

python tools/re/ddfix.py <xeBuild.exe> <xeBuild.dbg.s> <build/xeBuild.s> [path/to/as.exe]

as.exe defaults to the binutils 2.27 in tools/toolchain-4745.

Input is `gtirb-pprinter --format raw --syntax intel --keep-all --listing-mode debug`
output, where every emitted line is prefixed with its original address.  We strip
those prefixes, assemble with a listing, and wherever gas picked a different
length than the original (shortened padding `lea`s, relaxed jumps), pin the
original encoding:
  * lines with no symbol operand become `.byte` of the original bytes;
  * direct jmp/jcc/call to a label keep the label: opcode bytes + `.long L-.-4`
    (or `.byte L-.-1` for short forms).
Lines without symbol operands must also match byte for byte (e.g. ddisasm prints
the 2-byte `66 90` padding as two `nop`s).  Repeats until nothing changes.

Also writes <out>.lines.json (lines + original addresses) for tools/re/split.py, and
prepares the single-file source for linking with tools/re/single.ld (see prepare_link).
"""
import collections, json, re, struct, subprocess, sys, os, tempfile

ADDR = re.compile(r'^\s+([0-9a-f]+):\s*(.*)$')
SYMREF = re.compile(r'(?<![\w.$])(FUN_[0-9a-f]+|\.L_[0-9a-f]+|[A-Za-z_.$][\w.$@]*)')
REGS = set('''eax ebx ecx edx esi edi esp ebp ax bx cx dx si di sp bp al ah bl bh cl ch dl dh
cs ds es fs gs ss st byte word dword qword tbyte xmmword ptr offset short near far
mm0 mm1 mm2 mm3 mm4 mm5 mm6 mm7 xmm0 xmm1 xmm2 xmm3 xmm4 xmm5 xmm6 xmm7 eiz'''.split())
JCC = {'jo': 0x0, 'jno': 0x1, 'jb': 0x2, 'jc': 0x2, 'jnae': 0x2, 'jae': 0x3, 'jnb': 0x3, 'jnc': 0x3,
       'je': 0x4, 'jz': 0x4, 'jne': 0x5, 'jnz': 0x5, 'jbe': 0x6, 'jna': 0x6, 'ja': 0x7, 'jnbe': 0x7,
       'js': 0x8, 'jns': 0x9, 'jp': 0xa, 'jpe': 0xa, 'jnp': 0xb, 'jpo': 0xb, 'jl': 0xc, 'jnge': 0xc,
       'jge': 0xd, 'jnl': 0xd, 'jle': 0xe, 'jng': 0xe, 'jg': 0xf, 'jnle': 0xf}


class Image:
    def __init__(self, path):
        self.d = open(path, 'rb').read()
        pe = struct.unpack_from('<I', self.d, 0x3c)[0]
        nsec = struct.unpack_from('<H', self.d, pe + 6)[0]
        opt = struct.unpack_from('<H', self.d, pe + 20)[0]
        self.base = struct.unpack_from('<I', self.d, pe + 24 + 28)[0]
        self.secs, self.flags = [], {}
        for i in range(nsec):
            o = pe + 24 + opt + 40 * i
            name = self.d[o:o + 8].rstrip(b'\0').decode()
            vsz, va, rsz, raw = struct.unpack_from('<IIII', self.d, o + 8)
            self.secs.append((name, self.base + va, vsz, raw, rsz))
            self.flags[name] = struct.unpack_from('<I', self.d, o + 36)[0]
        self.dirs = [struct.unpack_from('<II', self.d, pe + 24 + 96 + 8 * i) for i in range(16)]

    def align(self, name):
        """Section alignment recorded in the header (ld writes it into images too)."""
        return 1 << ((self.flags[name] >> 20 & 0xf) - 1)

    def offset(self, rva):
        va = self.base + rva
        for _, sva, vsz, raw, rsz in self.secs:
            if sva <= va < sva + max(vsz, rsz):
                return raw + va - sva
        raise ValueError(hex(va))

    def sec(self, name):
        return next(s for s in self.secs if s[0] == name)

    def read(self, va, n):
        for name, sva, vsz, raw, rsz in self.secs:
            if sva <= va and va + n <= sva + max(vsz, rsz):
                off = va - sva
                b = self.d[raw + off: raw + min(off + n, rsz)]
                return b + b'\0' * (n - len(b))
        raise ValueError(hex(va))


def strip(dbg_path):
    """-> (lines, addr) where addr[i] is the original VA of line i or None."""
    lines, addr = [], []
    for l in open(dbg_path, encoding='utf-8'):
        l = l.rstrip('\n')
        if l.startswith('.size '):
            continue
        m = ADDR.match(l)
        if m:
            lines.append('          ' + m.group(2))
            addr.append(int(m.group(1), 16))
        else:
            lines.append(l)
            addr.append(None)
    return lines, addr


def assemble(as_exe, lines):
    """Assemble; return {1-based source line: emitted bytes as listed (relocs unresolved)}."""
    tmp = tempfile.mkdtemp()
    s, lst = os.path.join(tmp, 'x.s'), os.path.join(tmp, 'x.lst')
    open(s, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    r = subprocess.run([as_exe, '--32', '-aln=' + lst, s, '-o', os.path.join(tmp, 'x.o')],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit('as failed:\n' + r.stderr[:3000])
    out = {}
    for l in open(lst, encoding='utf-8', errors='replace'):
        m = re.match(r'^ *(\d+)(?: ([0-9a-f]{4,8}) ([0-9A-F]+)| {6,}([0-9A-F]+))?(?:[ \t]|$)', l)
        if not m:
            continue
        n = int(m.group(1))
        hx = m.group(3) or m.group(4)
        if hx:
            out[n] = out.get(n, b'') + bytes.fromhex(hx)
    return out


def symbols_in(insn):
    return [t for t in SYMREF.findall(insn.split(None, 1)[1] if ' ' in insn.strip() else '')
            if t.lower() not in REGS and not re.fullmatch(r'\d+|0x[0-9a-f]+', t.lower())]


def pin(insn, orig):
    """Return replacement text forcing the original encoding, or None."""
    body = insn.strip()
    syms = symbols_in(body)
    if not syms:
        return '          .byte ' + ','.join('0x%02x' % b for b in orig) + '   # ' + body
    m = re.fullmatch(r'(\w+)\s+([\w.$@]+)', body)
    if m and len(syms) == 1:
        op, tgt = m.group(1).lower(), m.group(2)
        if op in ('jmp', 'call') and orig[0] in (0xe9, 0xe8) and len(orig) == 5:
            return '          .byte 0x%02x; .long %s-.-4   # %s' % (orig[0], tgt, body)
        if op == 'jmp' and orig[0] == 0xeb and len(orig) == 2:
            return '          .byte 0xeb; .byte %s-.-1   # %s' % (tgt, body)
        if op in JCC and orig[0] == 0x0f and len(orig) == 6:
            return '          .byte 0x0f,0x%02x; .long %s-.-4   # %s' % (orig[1], tgt, body)
        if op in JCC and len(orig) == 2:
            return '          .byte 0x%02x; .byte %s-.-1   # %s' % (orig[0], tgt, body)
    return None


# exe section name -> (directive starting it in the source, flags of its `$zz` tail).
# .text$zz is code+data: in the original that tail is the end of the
# __CTOR_LIST__/__DTOR_LIST__ words the default link script writes into .text,
# which is why the exe's .text carries IMAGE_SCN_CNT_INITIALIZED_DATA too.
SECTIONS = {'.text': ('.text', 'dxr'), '.data': ('.data', 'dw'), '.rdata': ('.section .rdata,"dr"', None),
            '.eh_fram': ('.section .eh_frame,"dr"', None), '.bss': ('.bss', 'b'),
            '.idata': ('.section .idata,"dw"', None), '.CRT': ('.section .CRT,"dw"', None),
            '.tls': ('.section .tls,"dw"', None), '.rsrc': ('.section .rsrc,"dw"', None)}
SECDIR = re.compile(r'^(?:\.section\s+([^\s,]+)\s*,.*|(\.text|\.data|\.bss))$')
ALIGN = re.compile(r'^\s*\.align\s+(\d+)\s*$')
ZERO = re.compile(r'^(\s*)\.zero\s+(\d+)\s*$')


def imports(img):
    """{IAT slot VA: function name} from the exe's import directory."""
    d, out = img.d, {}
    o = img.offset(img.dirs[1][0])
    while True:
        oft, _, _, name, ft = struct.unpack_from('<IIIII', d, o)
        if not name:
            return out
        thunks, slot = img.offset(oft or ft), img.base + ft
        while True:
            t = struct.unpack_from('<I', d, thunks)[0]
            if not t:
                break
            if not t & 0x80000000:
                h = img.offset(t) + 2
                out[slot] = d[h:d.index(b'\0', h)].decode()
            thunks += 4
            slot += 4
        o += 20


LABELDEF = re.compile(r'^((?:FUN|\.L)_([0-9a-f]+)(?:_END)?):\s*$')
DECIMAL = re.compile(r'(?<![\w.$+\-*])(\d{7})(?![\w])')
LO, HI = 0x401000, 0x513000


class Refs:
    """Name image addresses with labels, adding `.L_<va>` labels where needed."""

    def __init__(self, lines, addr):
        self.lines, self.addr = lines, addr
        self.first = {}
        for i, a in enumerate(addr):
            if a is not None:
                self.first.setdefault(a, i)
        self.starts = sorted(self.first)
        self.names = {}  # va -> label already defined in the source
        for l in lines:
            m = LABELDEF.match(l.strip())
            if m:
                self.names.setdefault(int(m.group(2), 16), m.group(1))
        self.new = {}  # line index -> label to insert before it

    def __call__(self, va):
        if va in self.names:
            return self.names[va]
        if va in self.first:
            name = '.L_%x' % va
            self.new[self.first[va]] = name
            self.names[va] = name
            return name
        base = max(a for a in self.names if a <= va)  # mid-line: label + offset
        return '%s+%d' % (self.names[base], va - base)

    def labels(self):
        return {i: n + ':' for i, n in self.new.items()}


def replace_word(lines, addr, refs, va, text):
    """Replace the line(s) covering exactly [va, va+4) with `text`."""
    i = refs.first[va]
    j = i + 1
    while j < len(addr) and (addr[j] is None or addr[j] < va + 4):
        if addr[j] is not None:
            lines[j], addr[j] = '', None
        elif lines[j].rstrip().endswith(':') and any(a is not None and a < va + 4 for a in addr[j:j + 8]):
            sys.exit('replace_word: label %s inside the word at %x' % (lines[j].strip(), va))
        j += 1
    if j < len(addr) and addr[j] != va + 4 and addr[j] is not None:
        sys.exit('replace_word: %x does not end on a line boundary' % va)
    lines[i] = '          ' + text


def symbolize(lines, addr, img):
    """Turn addresses ddisasm left as numbers into label expressions.

    The output stays byte-identical; this is what lets code and data move:
      * .idata: descriptor/thunk RVAs -> `.rva label`
      * .rsrc: resource data entry RVAs -> `.rva label`
      * .eh_frame: FDE pc_begin (pcrel sdata4) -> `.long label - .`
      * .CRT/.tls: pointer tables, any in-image word -> `.long label`
      * instruction operands: 7-digit decimals inside the image -> label+off
    """
    refs = Refs(lines, addr)
    word = lambda va: struct.unpack('<I', img.read(va, 4))[0]
    counts = collections.Counter()

    # .idata
    _, ida, idsz, _, _ = img.sec('.idata')
    rva = lambda va, r: replace_word(lines, addr, refs, va, '.rva %s' % refs(img.base + r))
    d = img.base + img.dirs[1][0]
    while word(d + 12):
        for off in (0, 12, 16):
            if word(d + off):
                rva(d + off, word(d + off))
                counts['idata'] += 1
        for t in (word(d), word(d + 16)):
            p = img.base + t
            while word(p):
                if not word(p) & 0x80000000:
                    rva(p, word(p))
                    counts['idata'] += 1
                p += 4
        d += 20

    # .rsrc
    _, rs, _, _, _ = img.sec('.rsrc')
    def walk(off):
        n = struct.unpack('<HH', img.read(rs + off + 12, 4))
        for k in range(sum(n)):
            e = rs + off + 16 + 8 * k
            tgt = word(e + 4)
            if tgt & 0x80000000:
                walk(tgt & 0x7fffffff)
            else:
                rva(rs + tgt, word(rs + tgt))
                counts['rsrc'] += 1
    walk(0)

    # .eh_frame (every CIE here is "zR" with FDE encoding pcrel|sdata4, checked)
    _, eh, ehsz, _, _ = img.sec('.eh_fram')
    off, cies = 0, {}
    while off < ehsz:
        ln, cid = struct.unpack('<II', img.read(eh + off, 8))
        if ln == 0:  # zero terminator from one input's .eh_frame; more may follow
            off += 4
            continue
        if cid == 0:
            # version, "zR\0", code align, data align, RA reg, aug length, R encoding
            raw = img.read(eh + off + 8, ln - 4)
            aug = raw[1:raw.index(b'\0', 1)]
            if aug != b'zR' or raw[len(aug) + 6] != 0x1b:
                sys.exit('symbolize: unexpected CIE at %x' % (eh + off))
        else:
            f = eh + off + 8
            tgt = (f + word(f)) & 0xffffffff
            replace_word(lines, addr, refs, f, '.long %s - .' % refs(tgt))
            counts['eh_frame'] += 1
        off += 4 + ln

    # .CRT / .tls pointer tables
    for name in ('.CRT', '.tls'):
        _, va, vsz, _, _ = img.sec(name)
        for p in range(va, va + vsz, 4):
            i = refs.first.get(p)
            if i is not None and not re.match(r'\s*\.long\s+\S', lines[i]) and LO <= word(p) < HI:
                replace_word(lines, addr, refs, p, '.long %s' % refs(word(p)))
                counts[name] += 1

    # instruction operands still holding image addresses as numbers
    _, tva, tvsz, _, _ = img.sec('.text')
    for i, a in enumerate(addr):
        if a is None or not tva <= a < tva + tvsz or lines[i].lstrip().startswith('.'):
            continue
        code, sep, cmt = lines[i].partition('#')
        def sub(m):
            v = int(m.group(1))
            if not LO <= v < HI:
                return m.group(0)
            counts['operand'] += 1
            in_mem = code[:m.start()].rstrip().endswith('[')
            return refs(v) if in_mem else 'OFFSET ' + refs(v)
        lines[i] = DECIMAL.sub(sub, code) + sep + cmt

    for i, l in sorted(refs.labels().items(), reverse=True):
        lines.insert(i, l)
        addr.insert(i, None)
    print('symbolized: ' + ', '.join('%s %d' % kv for kv in sorted(counts.items())))


def add_link_labels(lines, addr, img):
    """Global labels the link needs: imports on their IAT slots (ddisasm leaves
    them undefined), `__IAT_start__`/`__IAT_end__` and `__tls_used` (ld fills
    the IAT and TLS data directories from them) and the entry point."""
    labels = {va: [name] for va, name in imports(img).items()}
    iat, iatsz = img.dirs[12]
    tls = img.dirs[9][0]
    for va, name in ((img.base + iat, '__IAT_start__'), (img.base + iat + iatsz, '__IAT_end__'),
                     (img.base + tls, '__tls_used')):
        labels.setdefault(va, []).append(name)
    out, oaddr = [], []
    for line, a in zip(lines, addr):
        if line.strip() == '__EntryPoint:':
            out.append('.globl __EntryPoint')
            oaddr.append(None)
        for l in labels.pop(a, []) if a is not None else []:
            out += ['.globl ' + l, l + ':']
            oaddr += [None, None]
        out.append(line)
        oaddr.append(a)
    if labels:
        sys.exit('add_link_labels: unplaced %s' % {hex(k): v for k, v in labels.items()})
    lines[:], addr[:] = out, oaddr


def prepare_link(lines, addr, img):
    """Make the single-object source link into the original image with tools/re/single.ld.

    * section directives get the exe's flags and alignment (`.eh_fram` is the
      8-char truncation of `.eh_frame`); `.align`s above that alignment are
      dropped (layout is explicit, so they were no-ops);
    * gas pads a section's size to its alignment, but the exe's sections end on
      4-byte boundaries (the original last object in each had 4-byte alignment),
      so the bytes after the last aligned boundary move to `<name>$zz`.
    """
    labels = {}
    cuts = {va + vsz - vsz % img.align(n): n for n, va, vsz, _, _ in img.secs if vsz % img.align(n)}
    out, sec_align, done, bss_tail = [], 0, set(), False
    for line, a in zip(lines, addr):
        m = SECDIR.match(line.strip())
        if bss_tail and not m and a is None and line.strip() and not line.startswith('#'):
            sys.exit('prepare_link: unexpected %r in .bss tail' % line)
        if m:
            bss_tail = False
            src = m.group(1) or m.group(2)
            cur = '.eh_fram' if src == '.eh_frame' else src
            sec_align = img.align(cur)
            out.append(SECTIONS[cur][0])
            out.append('.p2align %d' % (sec_align.bit_length() - 1))
            continue
        m = ALIGN.match(line)
        if m and int(m.group(1)) > sec_align:
            continue
        if a is not None:
            z = ZERO.match(line)
            end = a + (int(z.group(2)) if z else 1)
            cut = next((c for c in cuts if c not in done and a <= c < end), None)
            if cut is not None and (cut == a or z):
                if cut > a:  # split a .zero that straddles the cut
                    out.append('%s.zero %d' % (z.group(1), cut - a))
                    line = '%s.zero %d' % (z.group(1), end - cut)
                done.add(cut)
                if cuts[cut] == '.bss':
                    # gas gives any section but .bss itself file contents, so the
                    # tail becomes a COMMON block (as the original's likely was)
                    _, va, vsz, _, _ = img.sec('.bss')
                    out.append('.comm __bss_tail,%d,2' % (va + vsz - cut))
                    bss_tail = True
                    continue
                out.append('.section %s$zz,"%s"' % (cuts[cut], SECTIONS[cuts[cut]][1]))
                out.append('.p2align 2')
            if bss_tail:
                if not ZERO.match(line):
                    sys.exit('prepare_link: .bss tail holds more than zeros at %x' % a)
                continue
        out.append(line)
    if len(done) != len(cuts):
        sys.exit('prepare_link: unplaced cuts %s' % [hex(c) for c in cuts if c not in done])
    return out


def main():
    exe, dbg, out = sys.argv[1:4]
    as_exe = os.path.abspath(sys.argv[4] if len(sys.argv) > 4 else os.path.join(
        os.path.dirname(__file__), '..', '..', 'tools', 'toolchain-4745', 'mingw32', 'bin', 'as.exe'))
    img = Image(exe)
    lines, addr = strip(dbg)
    tname, tva, tvsz, _, _ = img.sec('.text')
    # original length of each addressed .text line = gap to the next addressed line
    idx = [i for i, a in enumerate(addr) if a is not None and tva <= a < tva + tvsz]
    olen = {}
    for k, i in enumerate(idx):
        nxt = addr[idx[k + 1]] if k + 1 < len(idx) and addr[idx[k + 1]] > addr[i] else tva + tvsz
        olen[i] = nxt - addr[i]
    pinned, unfixable = 0, {}
    for rnd in range(10):
        emitted = assemble(as_exe, lines)
        bad = []
        for i in idx:
            if i in unfixable:
                continue
            got = emitted.get(i + 1, b'')
            if len(got) != olen[i]:
                bad.append(i)
            elif not symbols_in(lines[i].split('#')[0]) and got != img.read(addr[i], olen[i]):
                bad.append(i)   # same length, different encoding (no relocs, so bytes are final)
        print('round %d: %d mismatched lines' % (rnd, len(bad)))
        if not bad:
            break
        for i in bad:
            rep = pin(lines[i], img.read(addr[i], olen[i]))
            if rep is None:
                unfixable[i] = lines[i].strip()
            else:
                lines[i] = rep
                pinned += 1
    for i, t in sorted(unfixable.items())[:40]:
        print('UNFIXED %x (orig %d bytes, gas %d): %s' % (addr[i], olen[i], len(emitted.get(i + 1, b'')), t))
    print('pinned %d lines, %d unfixable' % (pinned, len(unfixable)))
    symbolize(lines, addr, img)
    add_link_labels(lines, addr, img)
    # address-annotated lines for tools/re/split.py
    json.dump({'lines': lines, 'addr': addr}, open(os.path.splitext(out)[0] + '.lines.json', 'w'))
    lines = prepare_link(lines, addr, img)
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
