import re, sys, difflib
# sig.py origs.txt ours.txt : compact block-content sequence diff (cold block order)
M = {'406330': 'CU', '41fe10': 'GetInfo', '420840': 'Reboot', '41fa40': 'Disc',
     '406c60': 'Keys', '406740': 'Info', '407320': 'Patches'}
REN = {'_client_usage': '_CU', '_netGetInfo': '_GetInfo', '_netReboot': '_Reboot',
       '_netDisconnect': '_Disc', '_clientKeys': '_Keys', '_clientInfo': '_Info',
       '_clientPatches': '_Patches'}


def sig(f, orig):
    out = []
    for l in open(f):
        if orig:
            l = re.sub(r'FUN_([0-9a-f]+)', lambda m: '_' + M.get(m.group(1), m.group(1)), l)
        for k, v in REN.items():
            l = l.replace(k, v)
        m = re.search(r'"([^"]*)', l)
        if m and ('ERROR' in l or '"-' in l):
            t = m.group(1).split('ERROR: ')[-1][:16].replace('\\0', '')
            out.append(('E:' if 'ERROR' in l else '') + t)
            continue
        m = re.search(r'call\s+_(CU|GetInfo|Reboot|Disc|Keys|Info|Patches)\b', l)
        if m:
            out.append(m.group(1))
        if re.search(r'\bret\b', l):
            out.append('RET')
    return out


a = sig(sys.argv[1], True)
b = sig(sys.argv[2], False)
for x in difflib.ndiff(a, b):
    if x[0] != '?':
        print(x)
