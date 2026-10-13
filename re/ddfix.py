"""Make ddisasm's GNU-syntax output re-assemble to the exe's original encodings.

python re/ddfix.py <xeBuild.exe> <xeBuild.dbg.s> <out.s> [path/to/as.exe]

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
"""
import re, struct, subprocess, sys, os, tempfile

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
        self.secs = []
        for i in range(nsec):
            o = pe + 24 + opt + 40 * i
            name = self.d[o:o + 8].rstrip(b'\0').decode()
            vsz, va, rsz, raw = struct.unpack_from('<IIII', self.d, o + 8)
            self.secs.append((name, self.base + va, vsz, raw, rsz))

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


def main():
    exe, dbg, out = sys.argv[1:4]
    as_exe = os.path.abspath(sys.argv[4] if len(sys.argv) > 4 else os.path.join(
        os.path.dirname(__file__), '..', 'tools', 'toolchain-4745', 'mingw32', 'bin', 'as.exe'))
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
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
