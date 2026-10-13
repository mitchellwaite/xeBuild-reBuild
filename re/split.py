"""Split the whole-image source into one .s per original object file.

python re/split.py <xeBuild.exe> <build/xeBuild.lines.json> <src_dir>

Writes <src_dir>/<group>/<name>.s for every object, <src_dir>/objects.txt (link
order) and prints the data-assignment summary.  Objects that have a C source
(<src_dir>/<group>/<name>.c) get no .s; functions they share with the .s files
are named by SYMBOLS.  How the pieces are found:

  .text      exact: every gcc object has its own CIE in .eh_frame, in link
             order, and its FDEs list its functions (units.py).  Objects
             without unwind info (chkstk, import stubs) are known runtime
             matches.  .text.startup holds main (unit 10), unit 21's startup
             function and crtend's constructor, then the link script's
             ctor/dtor lists.
  .eh_frame  exact: one CIE + FDEs per object.
  .rdata$zzz exact count: one `GCC: ...` ident per gcc-compiled object (104;
             identical bytes, so which object carries which is immaterial).
  .data .rdata .bss
             inferred: split at labels into atoms, find which objects reference
             each atom (code refs, propagated through data-to-data pointers),
             then choose monotone boundaries in link order minimising atoms
             placed in an object that doesn't reference them.
  COMMON     the end of .bss is uninitialized (common) globals, which ld lays
             out in hash-table order, so it stays one file (common_bss.s).
"""
import bisect, collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from ddfix import Image
from units import units

# unit index (CIE order) -> (path, evidence)
NAMES = {
    0: ('runtime/crt2', 'mingw-w64 crt2.o, byte match'),
    1: ('runtime/crtbegin', 'gcc crtbegin.o, byte match'),
    2: ('app/bootloaders', 'CB/CF/CD/CE decryption, pairing, FCRT, bootloader signature checks'),
    3: ('app/mode_update', '"Usage: %s update", bad block handling'),
    4: ('app/stfs', 'container header/content/manifest hash checks, STFS file listing'),
    5: ('app/mode_client', '"Usage: %s client", network read/write of NAND'),
    6: ('app/filelist_ini', '"parsing ini at", file list ini labels'),
    7: ('app/timeutil', 'gmtime/mktime/rand, date arithmetic constants'),
    8: ('app/smc', 'SMC checksum, type detection, reset-limit/eject/blink patches'),
    9: ('app/sysupdate', 'system update container, xboxupd.bin extraction'),
    10: ('app/main', 'main (.text.startup), signal handlers, mode dispatch'),
    11: ('app/mode_extract', '"Usage: %s extract"'),
    12: ('app/xboxrom', 'XBOX_ROM_B/4/3 names'),
    13: ('app/image_write', 'flash layout (CB/CE/SMC/Mobile*.dat), writing image to disk'),
    14: ('app/keyvault', 'keyvault hash check, DVD key, console serial/date formatting'),
    15: ('app/image_read', 'parsing an existing NAND image: sectors, pairing, LDV, smc.bin'),
    16: ('app/mode_ini', '"Usage: %s ini"'),
    17: ('app/mode_build', 'default build mode usage and switches (-t/-c/-d/-b/-p)'),
    18: ('app/keys', 'CPU/1BL key setup, SMC/keyvault/CRL input decryption, pairing init'),
    19: ('app/net', 'winsock: beacon, send/recv'),
    20: ('app/fileutil', 'file read/write/dump helpers, mkdir; called by almost every unit'),
    21: ('app/options', 'console types (xenon...corona), command line options; startup fn'),
    22: ('app/build', 'image build: reading inputs with crc32 checks, patches, payloads'),
    23: ('app/consoleinfo', 'options/launch ini writing, console info response parsing'),
    24: ('app/console_hdd', 'manifest + avatar/kinect data to console HDD, remote dirs'),
    25: ('app/log', 'build.log, verbose levels; called by every app unit'),
    26: ('app/crc32', 'table-driven crc32'),
    27: ('crypto/xecrypt', 'XeCrypt-style API: SHA/HMAC (0x36/0x5c pads), RC4, DES, AES, RSA'),
    28: ('crypto/xecrypt_bn', 'big-endian qword bignum helpers, Montgomery inverse'),
    29: ('crypto/aes_modes', 'Gladman AES: ECB/CBC over the block functions'),
    30: ('crypto/aestab', 'Gladman AES: aes_init() returning 0 (static tables)'),
    31: ('crypto/aescrypt', 'Gladman AES: block encrypt/decrypt'),
    32: ('crypto/aeskey', 'Gladman AES: key schedules for 128/192/256'),
    33: ('bigdigits/mpSubtract', 'assert path .../XeCrypt/bign/mpSubtract.c'),
    34: ('crypto/rsa', 'RSA key generation, PKCS#1 v1.5/OAEP/PSS'),
    35: ('bigdigits/mpMultiply', 'assert path .../XeCrypt/bign/mpMultiply.c'),
    36: ('bigdigits/mpShortMod', 'remainder of mpShortDiv'),
    37: ('bigdigits/mpModExp', 'square-and-multiply over mpModMult'),
    38: ('bigdigits/mpSetZero', 'memset digits'),
    39: ('bigdigits/mpShortDiv', 'divide by one digit'),
    40: ('crypto/base64', 'base64 alphabet, encode/decode'),
    41: ('crypto/hash', 'hash-id size table, SHA-1 one-shot wrappers'),
    42: ('bigdigits/mpModInv', 'extended Euclid'),
    43: ('bigdigits/mpModulo', 'mpDivide keeping the remainder'),
    44: ('bigdigits/mpShortSub', 'subtract one digit with borrow'),
    45: ('bigdigits/mpSizeof', 'count significant digits'),
    46: ('bigdigits/mpCompare', 'compare from the top digit'),
    47: ('crypto/memwipe', 'memset wrapper + two empty functions'),
    48: ('bigdigits/mpSetDigit', 'set low digit, zero the rest'),
    49: ('bigdigits/mpIsPrime', 'small-prime sieve + Rabin-Miller'),
    50: ('bigdigits/mpIsZero', 'all digits zero'),
    51: ('bigdigits/mpShiftLeft', 'multi-digit shift left'),
    52: ('bigdigits/spMultiply', '32x32->64 multiply via 16-bit halves'),
    53: ('bigdigits/mpAdd', 'assert path .../XeCrypt/bign/mpAdd.c'),
    54: ('bigdigits/mpModMult', 'mpMultiply then mpModulo'),
    55: ('bigdigits/mpUtil', 'digit alloc/free, hex print, random fill, string conversion'),
    56: ('bigdigits/mpShortAdd', 'add one digit with carry'),
    57: ('crypto/rc4_enc', 'RC4 stream (OpenSSL RC4())'),
    58: ('crypto/rc4_skey', 'RC4 key setup; RC4_options() "rc4(idx,int)"'),
    59: ('crypto/sha1dgst', 'SHA-1 init/block/update/final'),
    60: ('crypto/md5_dgst', 'MD5 init/block/update/final'),
    61: ('crypto/des', 'DES/3DES key schedule and block functions'),
    62: ('bigdigits/mpSetEqual', 'copy digits'),
    63: ('bigdigits/mpShiftRight', 'multi-digit shift right'),
    64: ('bigdigits/mpDivide', 'long division (quotient, remainder)'),
    65: ('bigdigits/spDivide', '64/32 digit division'),
    66: ('bigdigits/mpShortCmp', 'compare with one digit'),
    67: ('bigdigits/spPseudoRand', 'rand()-based random digit'),
    68: ('runtime/libmingw32/atonexit', 'byte match'),
    69: ('runtime/libmingw32/gccmain', 'byte match'),
    70: ('runtime/libmingw32/charmax', 'byte match; calls __lconv_init'),
    71: ('runtime/libmingw32/dllargv', '`return 0` (_setargv); 16-byte match is ambiguous'),
    72: ('runtime/libmingw32/gs_support', 'byte match'),
    73: ('runtime/libmingw32/tlssup', 'byte match'),
    74: ('runtime/libmingw32/merr', 'byte match'),
    75: ('runtime/libmingw32/CRT_fp10', 'byte match (_fpreset)'),
    76: ('runtime/libmingw32/mingw_helpers', 'byte match'),
    77: ('runtime/libmingw32/pseudo-reloc', 'byte match'),
    78: ('runtime/libmingw32/crt_handler', 'byte match'),
    79: ('runtime/libmingw32/tlsthrd', 'byte match'),
    80: ('runtime/libmingw32/pesect', 'byte match'),
    81: ('runtime/libgcc/_divdi3', 'byte match'),
    82: ('runtime/libgcc/_moddi3', 'byte match'),
    83: ('runtime/libgcc/_udivdi3', 'byte match'),
    84: ('runtime/libgcc/_umoddi3', 'byte match'),
    85: ('runtime/libmingwex/difftime32', 'byte match'),
    86: ('runtime/libmingwex/dirent', 'byte match'),
    87: ('runtime/libmingwex/wassert', 'byte match (_assert)'),
    88: ('runtime/libmingwex/_stat', 'byte match'),
    89: ('runtime/libmingwex/fseeko64', 'byte match'),
    90: ('runtime/libmingwex/ftello64', 'byte match'),
    91: ('runtime/ms_vsnprintf', '__ms_vsnprintf jump'),
    92: ('runtime/libmingwex/invalid_parameter_handler', 'get/set (xchg) of one global'),
    93: ('runtime/crtend', 'gcc crtend.o: register_frame_ctor, .jcr, eh_frame terminator'),
}
# Real names for functions shared with C sources (src/<obj>.c): gcc objects
# define and call these names, so the .s files must use them too.  Address ->
# symbol (with the leading underscore of i386 PE).
SYMBOLS = {
    # BigDigits (src/bigdigits/*.c); names from the library
    0x43e550: '_mpSubtract', 0x440e20: '_mpMultiply', 0x440f80: '_mpShortMod',
    0x440fc0: '_mpModExp', 0x4410e0: '_mpSetZero', 0x441110: '_mpShortDiv',
    0x441540: '_mpModInv', 0x441710: '_mpModulo', 0x441780: '_mpShortSub',
    0x4417d0: '_mpSizeof', 0x441800: '_mpCompare', 0x4418a0: '_mpSetDigit',
    0x441be0: '_mpIsPrime', 0x441c80: '_mpRabinMiller', 0x441f00: '_mpIsZero',
    0x441f40: '_mpShiftLeft', 0x442050: '_spMultiply', 0x4420b0: '_mpAdd',
    0x442130: '_mpModMult', 0x4425d0: '_mpShortAdd', 0x446200: '_mpSetEqual',
    0x446230: '_mpShiftRight', 0x446360: '_mpDivide', 0x446830: '_spDivide',
    0x446a40: '_mpShortCmp', 0x446a90: '_spPseudoRand',
    # runtime functions the C code calls
    0x448760: '__assert',       # libmingwex wassert.o
    0x449050: '__time32',       # import stub, msvcrt `time`
    0x449090: '_srand', 0x4490c0: '_rand', 0x4490f0: '_memset',  # import stubs
}
CHKSTK = (0x447c00,'runtime/libgcc/_chkstk_ms', 'byte match; assembly, no unwind info')
STUBS = (0x449038, 'runtime/import_stubs', 'dlltool `jmp [__imp_x]` stubs, no unwind info')
STARTUP = 0x4492c0          # .text.startup begins (main)
LISTS = (0x4497a0, 0x4497b4, 'runtime/ctor_dtor_lists', '__CTOR_LIST__/__DTOR_LIST__ from the link script')
NOCODE = ('runtime/no_code_objects', '10 gcc objects without code (idents only; data merged into neighbours)')
COMMON = (0x479e84, 'common_bss', 'COMMON globals, laid out by ld in hash order')
WHOLE = {'.idata': ('runtime/idata', 'import tables (ld builds these from import libraries)'),
         '.CRT': ('runtime/crt_tls_sections', '.CRT initializer tables and .tls directory'),
         '.tls': ('runtime/crt_tls_sections', None),
         '.rsrc': ('runtime/manifest', 'default application manifest resource')}

# output section in the object file: (directive, alignment cap)
OUT = {'.text': ('.text', 16), '.text.startup': ('.section .text.startup,"xr"', 16),
       '.ctors_dtors': ('.section .ctors_dtors,"dxr"', 4), '.data': ('.data', 32),
       '.jcr': ('.section .jcr,"dw"', 4), '.rdata': ('.section .rdata,"dr"', 32),
       '.rdata$zzz': ('.section .rdata$zzz,"dr"', 4), '.eh_frame': ('.section .eh_frame,"dr"', 4),
       '.bss': ('.bss', 32), '.idata': ('.section .idata,"dw"', 4), '.CRT': ('.section .CRT,"dw"', 4),
       '.tls': ('.section .tls,"dw"', 4), '.rsrc': ('.section .rsrc,"dw"', 4)}

SECDIR = re.compile(r'^(?:\.section\s+([^\s,]+)\s*,.*|(\.text|\.data|\.bss))$')
LABEL = re.compile(r'^([A-Za-z_.$][\w.$@]*):\s*$')
SYM = re.compile(r'(?<![\w.$])((?:FUN|L)_[0-9a-f]+(?:_END)?|[A-Za-z_][\w@]*)')
REFADDR = re.compile(r'(?<![\w.$])(?:FUN|L)_([0-9a-f]+)')
ZERO = re.compile(r'^(\s*)\.zero\s+(\d+)\s*$')
IDENT = 44


def lowbit(x):
    return x & -x if x else 1 << 30


def main():
    exe, lj, outdir = sys.argv[1:4]
    img = Image(exe)
    d = json.load(open(lj))
    L = [re.sub(r'(?<![\w.$])\.L_', 'L_', l) for l in d['lines']]
    A = d['addr']
    sec = {n: (va, va + max(vsz, rsz) if n == '.bss' else va + vsz) for n, va, vsz, _, rsz in img.secs}
    sec['.bss'] = (sec['.bss'][0], img.sec('.bss')[1] + img.sec('.bss')[2])
    us = units(img)

    # ---- lines: section and position (labels sit at the next addressed line)
    cur, secof = None, []
    for l in L:
        m = SECDIR.match(l.strip())
        if m:
            s = m.group(1) or m.group(2)
            cur = '.eh_fram' if s == '.eh_frame' else s
        secof.append(cur)
    pos = [None] * len(L)
    nxt = None
    for i in range(len(L) - 1, -1, -1):
        if SECDIR.match(L[i].strip()) or secof[i] is None:
            nxt = None
            continue
        if A[i] is not None:
            nxt = A[i]
        pos[i] = A[i] if A[i] is not None else (nxt if nxt is not None else sec[secof[i]][1])

    # ---- link order and fixed pieces: (section, lo, hi, file, out_section)
    order, info = [], {}
    def add(path, why):
        if path not in info:
            order.append(path)
            info[path] = why
    pieces = []
    text_starts = {}
    for i, (cie, fdes) in enumerate(us):
        path, why = NAMES[i]
        if i == 81:
            add(CHKSTK[1], CHKSTK[2])
            text_starts[CHKSTK[0]] = CHKSTK[1]
        if i == 92:
            add(STUBS[1], STUBS[2])
            text_starts[STUBS[0]] = STUBS[1]
        add(path, why)
        normal = [a for a, _ in fdes if a < STARTUP]
        if normal:
            text_starts[min(normal)] = path
    add(LISTS[2], LISTS[3])
    add(NOCODE[0], NOCODE[1])
    add(COMMON[1], COMMON[2])
    for s, (p, why) in WHOLE.items():
        add(p, why or info.get(p))
    ts = sorted(text_starts)
    for k, a in enumerate(ts):
        pieces.append(('.text', a, ts[k + 1] if k + 1 < len(ts) else STARTUP, text_starts[a], '.text'))
    startup = sorted((a, NAMES[i][0]) for i, (_, f) in enumerate(us) for a, _ in f if a >= STARTUP)
    for k, (a, p) in enumerate(startup):
        pieces.append(('.text', a, startup[k + 1][0] if k + 1 < len(startup) else LISTS[0], p, '.text.startup'))
    pieces.append(('.text', LISTS[0], LISTS[1], LISTS[2], '.ctors_dtors'))
    # eh_frame: one piece per CIE; crtend's starts with the 4-byte zero terminator
    ehs = []
    for i, (cie, _) in enumerate(us):
        lo = cie - 4 if i == 93 and img.read(cie - 4, 4) == b'\0' * 4 else cie
        ehs.append((lo, NAMES[i][0]))
    for k, (lo, p) in enumerate(ehs):
        pieces.append(('.eh_fram', lo, ehs[k + 1][0] if k + 1 < len(ehs) else sec['.eh_fram'][1], p, '.eh_frame'))
    # idents: one per gcc object in link order, the remainder to NOCODE
    rlo, rhi = sec['.rdata']
    nid = (rhi - rlo) // IDENT
    id0 = rhi - IDENT * 104
    gcc_objs = [NAMES[i][0] for i in range(len(us))]
    for k in range(104):
        p = gcc_objs[k] if k < len(gcc_objs) else NOCODE[0]
        pieces.append(('.rdata', id0 + IDENT * k, id0 + IDENT * (k + 1), p, '.rdata$zzz'))
    jcr = sec['.data'][1] - 4
    pieces.append(('.data', jcr, sec['.data'][1], NAMES[93][0], '.jcr'))
    pieces.append(('.bss', COMMON[0], sec['.bss'][1], COMMON[1], '.bss'))
    for s, (p, _) in WHOLE.items():
        pieces.append((s, sec[s][0], sec[s][1], p, s))

    # ---- inferred pieces for .data/.rdata/.bss
    owner_text = []
    for s, lo, hi, p, o in pieces:
        if s == '.text':
            owner_text.append((lo, hi, p))
    owner_text.sort()
    tlos = [x[0] for x in owner_text]
    def text_owner(a):
        k = bisect.bisect_right(tlos, a) - 1
        return owner_text[k][2] if k >= 0 and a < owner_text[k][1] else None

    regions = {'.data': (sec['.data'][0], jcr), '.rdata': (rlo, id0), '.bss': (sec['.bss'][0], COMMON[0])}
    labels_at = collections.defaultdict(set)
    for i, l in enumerate(L):
        if LABEL.match(l.strip()) and secof[i] in regions:
            labels_at[secof[i]].add(pos[i])
    # refs: target address -> set of files (code) / set of source addresses (data)
    code_refs = collections.defaultdict(set)
    data_refs = collections.defaultdict(set)
    for i, l in enumerate(L):
        if pos[i] is None:
            continue
        code = l.split('#')[0]
        for m in REFADDR.finditer(code):
            t = int(m.group(1), 16)
            if secof[i] == '.text':
                o = text_owner(pos[i])
                if o:
                    code_refs[t].add(o)
            elif secof[i] in regions:
                data_refs[t].add(pos[i])
    participants = [p for p in order if p not in (LISTS[2], NOCODE[0], COMMON[1]) and p not in
                    {v[0] for v in WHOLE.values()} and p != STUBS[1] and p != CHKSTK[1]]
    pidx = {p: k for k, p in enumerate(participants)}
    # atoms of all three regions, with the files referencing them
    atoms = {}
    for s, (lo, hi) in regions.items():
        # gas pads every section to a multiple of 4, so objects start 4-aligned
        cuts = sorted({lo} | {a for a in labels_at[s] if lo < a < hi and a % 4 == 0})
        atoms[s] = list(zip(cuts, cuts[1:] + [hi]))
    flat = sorted((a0, a1, s) for s, al in atoms.items() for a0, a1 in al)
    fstarts = [a for a, _, _ in flat]
    def atom_of(v):
        k = bisect.bisect_right(fstarts, v) - 1
        return k if k >= 0 and v < flat[k][1] else None
    refset = [set() for _ in flat]
    for t, fs in code_refs.items():
        k = atom_of(t)
        if k is not None:
            refset[k] |= fs
    for _ in range(6):  # propagate through data-to-data pointers, any direction
        changed = False
        for t, srcs in data_refs.items():
            k = atom_of(t)
            if k is None:
                continue
            for a in srcs:
                j = atom_of(a)
                if j is not None and not refset[j] <= refset[k]:
                    refset[k] |= refset[j]
                    changed = True
        if not changed:
            break
    summary = {}
    for s, al in atoms.items():
        rsets = [refset[atom_of(a0)] for a0, _ in al]
        # DP: monotone assignment in link order, cost 1 per atom placed in a file
        # that doesn't reference it.  Ties switch files as late as possible, so
        # alignment padding stays with the object before it.
        m = len(participants)
        cost_prev = [0] * m
        back = []
        for k, (a0, a1) in enumerate(al):
            rs = {pidx[p] for p in rsets[k] if p in pidx}
            best, bj, row, ch = None, -1, [0] * m, [0] * m
            for j in range(m):
                stay = cost_prev[j]
                if bj >= 0 and best <= stay:
                    base, src = best, bj
                else:
                    base, src = stay, j
                row[j] = base + (0 if not rs or j in rs else 1)
                ch[j] = src
                if best is None or cost_prev[j] < best:
                    best, bj = cost_prev[j], j
            back.append(ch)
            cost_prev = row
        atoms_s = al
        refset_s = rsets
        j = min(range(m), key=lambda x: (cost_prev[x], x))
        assign = [0] * len(atoms_s)
        for k in range(len(atoms_s) - 1, -1, -1):
            assign[k] = j
            j = back[k][j]
        runs = []
        for k, (a0, a1) in enumerate(atoms_s):
            p = participants[assign[k]]
            if runs and runs[-1][2] == p:
                runs[-1][1] = a1
            else:
                runs.append([a0, a1, p])
        for a0, a1, p in runs:
            pieces.append((s, a0, a1, p, s))
        bad = sum(1 for k in range(len(atoms_s)) if refset_s[k] and participants[assign[k]] not in refset_s[k])
        summary[s] = (len(atoms_s), len(runs), bad)

    # ---- distribute lines to pieces
    by_sec = collections.defaultdict(list)
    for pc in pieces:
        by_sec[pc[0]].append(pc)
    for s in by_sec:
        by_sec[s].sort(key=lambda x: x[1])
    files = collections.defaultdict(lambda: collections.defaultdict(list))  # file -> outsec -> [(lo,hi,lines)]
    piece_lines = {pc: [] for pc in pieces}
    for i, l in enumerate(L):
        s = secof[i]
        st = l.strip()
        if s is None or SECDIR.match(st) or re.match(r'^\.align\s', st) or st.startswith('#') or not st \
                or st == '.intel_syntax noprefix' or st.startswith('.set __ImageBase'):
            continue  # __ImageBase comes from the link script instead
        lst = by_sec[s]
        k = bisect.bisect_right([x[1] for x in lst], pos[i]) - 1
        if k < 0:
            sys.exit('line %d %r at %x before first piece of %s' % (i, st, pos[i], s))
        pc = lst[k]
        if pos[i] >= pc[2] and not (pos[i] == pc[2] == sec[s][1]):
            sys.exit('line %d %r at %x not in a piece of %s' % (i, st, pos[i], s))
        z = ZERO.match(l)
        if z and A[i] is not None and A[i] + int(z.group(2)) > pc[2]:
            # .zero straddling a piece boundary: split it
            a, n = A[i], int(z.group(2))
            for pc2 in lst[k:]:
                take = min(a + n, pc2[2]) - max(a, pc2[1])
                if take > 0:
                    piece_lines[pc2].append('%s.zero %d' % (z.group(1), take))
                if pc2[2] >= a + n:
                    break
            continue
        piece_lines[pc].append(l)

    # ---- real names (after the address-based analysis above)
    rename = re.compile(r'(?<![\w.$])FUN_(%s)(?![\w$])' % '|'.join('%x' % a for a in SYMBOLS))
    for pc, ls in piece_lines.items():
        piece_lines[pc] = [rename.sub(lambda m: SYMBOLS[int(m.group(1), 16)], l) for l in ls]

    # ---- globals: labels referenced from another file
    defined = {}
    used = collections.defaultdict(set)
    for pc, ls in piece_lines.items():
        for l in ls:
            m = LABEL.match(l.strip())
            if m:
                defined[m.group(1)] = pc[3]
            for t in SYM.findall(l.split('#')[0]):
                used[pc[3]].add(t)
    need_global = collections.defaultdict(set)
    for f, syms in used.items():
        for t in syms:
            if t in defined and defined[t] != f:
                need_global[defined[t]].add(t)

    # ---- write
    secname = {'.eh_fram': '.eh_frame'}
    written = []
    for f in order:
        mine = [pc for pc in pieces if pc[3] == f and piece_lines[pc]]
        if not mine:
            continue
        if os.path.exists(os.path.join(outdir, f + '.c')):
            written.append(f)   # rebuilt from C source; keep it in the link order
            continue
        out =['# %s.s -- %s' % (f, info[f]), '#', '# original placement:']
        for pc in sorted(mine, key=lambda x: (x[0], x[1])):
            out.append('#   %-14s %08x-%08x' % (pc[4], pc[1], pc[2]))
        out += ['', '.intel_syntax noprefix']
        globs = sorted(need_global.get(f, ()))
        for g in globs:
            out.append('.globl ' + g)
        for pc in sorted(mine, key=lambda x: (list(OUT).index(x[4]), x[1])):
            directive, cap = OUT[pc[4]]
            al = min(cap, lowbit(pc[1]), lowbit(pc[2]))
            out += ['', directive, '.p2align %d' % (al.bit_length() - 1)]
            out += piece_lines[pc]
        path = os.path.join(outdir, f + '.s')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
        written.append(f)
    open(os.path.join(outdir, 'objects.txt'), 'w', newline='\n').write(
        '# link order (one object per line), generated by re/split.py\n' + '\n'.join(written) + '\n')
    for s, (na, nr, bad) in summary.items():
        print('%-6s %5d atoms -> %3d pieces, %d atoms outside their referencing object' % (s, na, nr, bad))
    print('%d files' % len(written))


if __name__ == '__main__':
    main()
