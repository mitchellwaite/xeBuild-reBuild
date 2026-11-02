"""lab.py INJ-JSON TAG SPEC...: s19 injections + hot/cold label attributes (PRED_HOT/COLD_LABEL,
no new edge). SPEC = name:hot|cold, names: hdd4 hdd5 (the HDD log calls), s4 s5 (send calls)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ext, table, search
PAT = {'hdd4': (r'AT(hdd4) log_printf(0, "\n\n***** ERROR: cannot send avatar', r'!\n");'),
       'hdd5': (r'AT(hdd5) log_printf(0, "\n\n***** ERROR: cannot send xbox', r'!\n");'),
       's4': ('sendAvatarData(arg, cinfo->kernel);', None),
       's5': ('sendCompatData(arg);', None),
       'reb': ('netReboot(reboot);', None),
       'u2': ('client_usage(2, NULL);', None)}
# case heads: label before the first statement after 'case N:' (switch -> case edge)
for n in range(1, 13):
    PAT['c%d' % n] = ('\t\t\tcase %d:\n\t\t\t\t' % n, '')
PAT['cdef'] = ('\t\t\tdefault:\n\t\t\t\t', '')
# option chain: label at the start of the then-branch of `else if (!strnicmp(argv[i], "-x", n)) {`
import re as _re
for _m in _re.finditer(r'strnicmp\(argv\[i\], "(-\w+)", \d+\)\)\)? \{\n', search.SRC):
    PAT['o' + _m.group(1)[1:]] = (_m.group(0), '')
_make = search.make
RAW = {'ent': ('\tlog_set_name("client");\n', '\tif (argc <= 0) { zc: __attribute__((%s)); }\n'),
       'ent2': ('\tlog_set_name("client");\n', '\tif (argc <= 0) { zc: __attribute__((%s)); client_usage(2, NULL); }\n')}
def make(inj, specs=()):
    s = _make(inj)
    for sp in specs:
        nm, kind = sp.split(':')
        if nm in RAW:
            a, t = RAW[nm]; i = s.index(a) + len(a); s = s[:i] + t % kind + s[i:]; continue
        a, endpat = PAT[nm]
        i = s.index(a)
        if endpat == '':
            j = i + len(a)
            s = s[:j] + 'hl_%s: __attribute__((%s)); ' % (nm, kind) + s[j:]
        elif endpat:
            j = s.index(endpat, i) + len(endpat)
            s = s[:i] + '{ hl_%s: __attribute__((%s)); %s }' % (nm, kind, s[i:j]) + s[j:]
        else:
            j = i + len(a)
            s = s[:i] + '{ hl_%s: __attribute__((%s)); %s }' % (nm, kind, s[i:j]) + s[j:]
    return s
if __name__ == '__main__':
    inj = [tuple(x) for x in json.loads(sys.argv[1])]
    specs = sys.argv[3:]
    search.make = lambda i: make(i, specs)
    r = table.meas(inj, sys.argv[2])
    if r is None: print('fail'); sys.exit()
    print(r['inv'], r['needmiss']); print(r['order'])
    print({k: r['fq'][k] for k in (103, 110, 111, 112, 113, 114, 115, 55) if k in r['fq']})
