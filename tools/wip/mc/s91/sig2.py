import re, sys, difflib
# sig2.py origs.txt ours.txt : call/string token diff from the last netReboot on
M = {'406330': 'CU', '41fe10': 'GetInfo', '420840': 'Reboot', '41fa40': 'Disc', '406c60': 'Keys',
     '406740': 'Info', '407320': 'Patches', '433690': 'log', '4491d0': 'strnicmp', '41fe20': 'DumpNand',
     '432e50': 'Avatar', '433440': 'Compat', '406980': 'Write', '4076b0': 'ReadBl', '407850': 'WriteBl',
     '407bf0': 'BinPatch', '421de0': 'atoh', '420320': 'Erase', '41f700': 'Connect', '4335a0': 'verbose'}
R = [('client_usage', 'CU'), ('log_printf', 'log'), ('netDumpNand', 'DumpNand'), ('sendAvatarData', 'Avatar'),
     ('sendCompatData', 'Compat'), ('clientReadBlocks', 'ReadBl'), ('clientWriteBlocks', 'WriteBl'),
     ('netGetInfo', 'GetInfo'), ('netReboot', 'Reboot'), ('netDisconnect', 'Disc'), ('myatoh32', 'atoh'),
     ('netConnect', 'Connect'), ('log_verbose_flag', 'verbose'), ('client', '')]


def toks(f, orig):
    out = []
    txt = re.sub(r'"\s*\n\s*\n', '"', open(f).read())
    for l in txt.split('\n'):
        m = re.search(r'"([^"]*)', l)
        if m and ('[ESP+4]' in l or '[esp+4]' in l):
            s = m.group(1).replace('\\12', '').replace('\\0', '').replace('*', '').replace('ERROR: ', '').strip()
            out.append('"' + s[:10])
            continue
        if orig:
            m = re.search(r'call FUN_([0-9a-f]+)', l)
            if m:
                out.append(M.get(m.group(1), m.group(1)))
        else:
            m = re.search(r'call\s+_?(\w+)', l)
            if m:
                n = m.group(1)
                for a, b in R:
                    n = n.replace(a, b)
                out.append(n)
    out = [t for t in out if t != 'log']
    i = max(i for i, t in enumerate(out) if t == 'Reboot')
    return out[i:]


a = toks(sys.argv[1], True)
b = toks(sys.argv[2], False)
for x in difflib.ndiff(a, b):
    if x[0] != '?':
        print(x)
