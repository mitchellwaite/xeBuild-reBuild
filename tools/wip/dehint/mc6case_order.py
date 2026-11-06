"""mode_client attempt 6: with the case-head feeds removed, does the source order of the case
bodies change the layout of the case blocks?  Prints, for each variant, the diff size and
the order in which the case bodies' calls appear in .text.

python tools/wip/dehint/mc6case_order.py [-n N]   (N random permutations, default 12)"""
import os, random, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdlib, mc1, mc1lib

CP = '__builtin_constant_p'
FEEDS = [
    r'if \(__builtin_constant_p\(mode \+ 1210\).*?mode = 9; ',
    r'if \(__builtin_constant_p\(mode \+ 930\)[^;]*goto t4;',
    r'if \(__builtin_constant_p\(mode \+ 3000\)[^;]*goto t5;',
    r'if \(__builtin_constant_p\(mode \+ 2400\)[^;]*goto c11;',
    r'if \(__builtin_constant_p\(mode \+ 205\)[^;]*goto c3;',
    r'if \(__builtin_constant_p\(mode \+ 153200\)\) goto c9;',
]
MARK = {'_netDumpNand': 1, '_clientWrite': 2, '_clientKeys': 3, '_sendAvatarData': 4,
        '_sendCompatData': 5, '_clientPatches': 7, '_clientReadBlocks': 8,
        '_clientWriteBlocks': 9, '_netEraseBlock': 10, '_clientBinPatch': 11,
        '_clientInfo': 12}


def strip(text):
    for f in FEEDS:
        text, n = re.subn(f, '', text, count=1)
        assert n == 1, f
    return text


def cases(text):
    i = text.index('\t\t\tcase 1:\n')
    j = text.index('\t\t\tdefault:\n')
    body = text[i:j]
    parts = re.split(r'(?=\t\t\tcase \d+:\n)', body)
    return text[:i], [p for p in parts if p], text[j:]


def order(o):
    t = subprocess.run([bdlib.OBJDUMP, '-d', '-r', '-M', 'intel', '--no-show-raw-insn', o],
                       capture_output=True, text=True).stdout
    t = t[t.index('<_mode_client>:'):]
    seq = []
    for m in re.finditer(r'(DISP32|call\s+[0-9a-f]+ <)(\s*)(_\w+)', t):
        n = MARK.get(m.group(3))
        if n and n not in seq:
            seq.append(n)
    return seq


def run(name, text):
    ok, o, d = mc1lib.compile_src(text)
    if not ok:
        print(name, 'COMPILE', o[-200:])
        return
    idn, tot, per, notes = mc1lib.report(o)
    print('%-10s %5s %s' % (name, 'OK' if idn else tot, order(o)), flush=True)
    mc1lib.cleanup(d)


def main():
    n = int(sys.argv[sys.argv.index('-n') + 1]) if '-n' in sys.argv else 12
    base = mc1lib.read_src(mc1.BASE)
    run('ref', base)
    s = strip(base)
    head, cs, tail = cases(s)
    run('nofeed', s)
    run('rev', head + ''.join(cs[::-1]) + tail)
    rnd = random.Random(6)
    for k in range(n):
        p = cs[:]
        rnd.shuffle(p)
        run('perm%d' % k, head + ''.join(p) + tail)


if __name__ == '__main__':
    main()
