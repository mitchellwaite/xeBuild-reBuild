"""Make src/app/keys.c (mixed object) from the draft wip/app/keys.c.

python wip/keysmixed.py fn1 fn2 ...   (the functions that match)

String literals passed to functions become extern names for keys.s's
strings; the data definitions become extern declarations.  Prints the
SYMBOLS entries for the strings used.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 're'))
from ddfix import Image

NAMES = {
    0x456664: 'msg_initRandom', 0x456680: 'msg_initStatic', 0x4566a4: 'msg_pairingSet',
    0x4566c4: 'str_valid', 0x4566ca: 'str_error', 0x4566d0: 'msg_weight',
    0x4566eb: 'msg_cpuKeySet', 0x4566fe: 'str_hexByte', 0x456703: 'str_newline',
    0x456708: 'msg_cpuKeyWarn', 0x45674c: 'msg_cpuKeyChars', 0x45678c: 'msg_cpuKeyLen',
    0x4567eb: 'msg_cpuKeySet2', 0x4567fe: 'msg_fuseLdv', 0x456816: 'msg_fuseCpuKey',
    0x456830: 'msg_fuseNull', 0x45685e: 'msg_1blKeySet', 0x456873: 'msg_1blSum',
    0x456890: 'msg_xexKeySet', 0x4568a5: 'msg_xexSum', 0x4568c2: 'msg_1blBad',
    0x4568e0: 'msg_1blBad2', 0x456904: 'msg_1blChars', 0x456944: 'msg_1blLen',
    0x4569a3: 'msg_1blBadStr', 0x4569c4: 'msg_1blBadStr2', 0x4569e4: 'msg_smcEncrypted',
    0x456a21: 'str_success', 0x456a2a: 'str_failed', 0x456a34: 'msg_smcBad',
    0x456a88: 'msg_smcRetail', 0x456af4: 'msg_smcCleanType', 0x456b20: 'msg_smcDevkit',
    0x456ba0: 'msg_smcClean', 0x456bc0: 'msg_smcGlitch', 0x456be4: 'msg_smcHacked',
    0x456c1c: 'msg_smcJtag', 0x456c3c: 'msg_smcNoGlitch', 0x456c9c: 'msg_smcNoJtag',
    0x456cfc: 'msg_cbencPairing', 0x456d22: 'msg_dualCb', 0x456d40: 'msg_cbb15572',
    0x456d6c: 'msg_cbbMfg', 0x456d9f: 'str_kv', 0x456da2: 'str_kvBin',
    0x456da9: 'str_altKv', 0x456db0: 'str_kvAltBin', 0x456dbc: 'msg_kvSize',
    0x456e10: 'msg_kvHash', 0x456e60: 'msg_kvPreDecrypted', 0x456ec8: 'msg_kvEncrypted',
    0x456f00: 'msg_kvDecryptFail', 0x456f24: 'msg_kvDecryptErr', 0x456f74: 'str_Success',
    0x456f80: 'msg_kvNotDecrypted', 0x456fc0: 'msg_extMissing', 0x457028: 'msg_extSize',
    0x457088: 'msg_extEncrypted', 0x4570c8: 'msg_extDecryptFail', 0x457110: 'msg_sdMissing',
    0x457178: 'msg_sdSize', 0x4571d5: 'str_successNl', 0x4571e0: 'msg_crlRetry',
    0x457200: 'str_failedNl', 0x45720c: 'msg_crlCrypted', 0x457248: 'msg_crlBad',
    0x457298: 'msg_daeBad', 0x457300: 'msg_daeEncrypted', 0x457340: 'msg_daeHeader',
    0x457380: 'msg_daeRetry', 0x4573b8: 'msg_daeHash', 0x457404: 'msg_fcrtSize',
    0x457430: 'msg_fcrtOffset', 0x45745c: 'msg_fcrtBad',
}


def cstr(s):
    """C literal body -> text"""
    return s.encode('latin1').decode('unicode_escape')


def strings():
    """keys.s's .rdata strings: text -> address"""
    lo, hi = 0x456664, 0x4574b0
    d = Image('xeBuild.exe').read(lo, hi - lo)
    out, i = {}, 0
    while i < len(d):
        if d[i]:
            j = d.index(0, i)
            out[d[i:j].decode('latin1')] = lo + i
            i = j
        i += 1
    return out


def main():
    want = sys.argv[1:]
    src = open('wip/app/keys.c').read()
    text = strings()
    head = src[:src.index('u8 secdataKey[8]')]
    data = src[src.index('u8 secdataKey[8]'):src.index('\n\n', src.index('u8 pairing[3];'))]
    data = re.sub(r'^u8 (\w+\[\d+\])(?: = \{[^}]*\})?;', r'extern u8 \1;', data, flags=re.M)
    fns = {}
    for m in re.finditer(r'\n((?:__attribute__[^\n]*\n)?(?:static )?[^\n;{}#]*?\b(\w+)\([^;{]*\)\n\{.*?\n\})\n', src, re.S):
        fns[m.group(2)] = m.group(1)
    used = {}

    def lit(m):
        s = cstr(m.group(1))
        # (and optimize-attribute flags)
        if s == 'thisisjustajunky' or s.startswith('no-'):
            return m.group(0)
        a = text[s]
        used[a] = NAMES[a]
        return NAMES[a]
    body = []
    for name in fns:
        if name in want or name in ('kvHashOk', 'smcSum'):
            body.append(re.sub(r'"((?:[^"\\]|\\.)*)"', lit, fns[name]))
    def show(s):
        c = s.encode('unicode_escape').decode('latin1').replace('"', '\\"')
        return '"%s"' % c if len(c) <= 36 else '"%s..."' % c[:36]
    ext = ['extern const char %s[];\t/* %s */' % (NAMES[a], show(s))
           for s, a in sorted(text.items(), key=lambda x: x[1]) if a in used]
    head = head.replace(
        '   for the image being built. */',
        '   for the image being built.  Mixed object: the functions here are\n'
        '   spliced into keys.s (re/splice.py), which still holds the rest and\n'
        '   the data, so strings and key buffers are extern names for the\n'
        "   .s's.  wip/app/keys.c is the whole draft. */", 1)
    out = (head + data + '\n\n/* strings in keys.s */\n' + '\n'.join(ext) + '\n\n' +
           '\n\n'.join(body) + '\n')
    open('src/app/keys.c', 'w', newline='\n').write(out)
    print(',\n'.join("0x%x: '_%s'" % (a, n) for a, n in sorted(used.items())))


main()
