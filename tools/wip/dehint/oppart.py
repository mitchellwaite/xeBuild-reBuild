"""parseButtonPart as a plain static cold helper: where its definition goes decides its
FDE's place in .eh_frame (the reference has it second, after baseFileExists' split).
python oppart.py [base.c]   (base: src/options.c with the hand-written part)"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

HDR = '''__attribute__((cold, section(".text.startup"), regparm(1)))
int parseButtonPart(const char *s) __asm__("_parseButton.part.0");
__attribute__((regparm(1))) int parseButtonPart(const char *s)
'''
ATTRS = {
    'cold': '__attribute__((cold)) static int parseButtonPart(const char *s)\n',
    'static_cold2': 'static __attribute__((cold)) int parseButtonPart(const char *s)\n',
}


def ehrel(o):
    t = subprocess.run([optlib.bdlib.OBJDUMP, '-r', '-j', '.eh_frame', o], capture_output=True, text=True).stdout
    return [l.split()[-1].replace('.text.unlikely', '.text.startup') for l in t.split('\n') if 'DISP32' in l]


REFEH = ehrel(optlib.REF)


def try_text(t, tag):
    ok, o, d = optlib.compile_src(t)
    if not ok:
        print(tag, 'COMPILE ERROR', o[:200])
        return
    idn, tot, per, notes = optlib.report(o)
    eh = ehrel(o)
    print('%-28s eh %s  %s' % (tag, 'SAME' if eh == REFEH else eh[:4], '%d %s' % (tot, per)), flush=True)
    optlib.cleanup(d)


def main():
    b = optlib.read_src(sys.argv[1] if len(sys.argv) > 1 else optlib.SRC)
    i = b.find('/* parseButton after its first four names')
    j = b.find('int baseFileExists(')
    k = b.find(HDR)
    body_end = b.find('\n}\n', k) + 3
    body = b[k + len(HDR):body_end]
    rest = b[:i] + b[body_end:].lstrip('\n')
    anchors = ['int baseFileExists(', '/* name or name.txt', 'int iniConsoleType(', 'int setConsoleType(',
               '/* a boolean option from a perbox', 'int optIniInt(', 'static int parseButtonX(', 'int parseButton(const']
    for an, a in ATTRS.items():
        for anc in anchors:
            p = rest.find(anc)
            if p < 0:
                continue
            fn = a + body + '\n'
            # parseButtonX/parseButton call it: they need a prototype when it comes later
            pre = 'static int parseButtonPart(const char *s);\n\n'
            t = rest[:p] + fn + rest[p:]
            first_use = min(x for x in (t.find('parseButtonPart(s)'),) if x >= 0)
            if t.find(a) > first_use:
                t = t[:i] + pre + t[i:]
            try_text(t, an + '@' + anc[:18])


main()
