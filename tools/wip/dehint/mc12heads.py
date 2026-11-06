"""mode_client attempt 12: profile_estimate frequencies of the case-region blocks (by the
function they call or a label they hold) for several sources side by side.

python tools/wip/dehint/mc12heads.py A.c [B.c ...] [-k clientBinPatch,clientPatches,...]"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mc9freq

KEYS = ['netDumpNand', 'clientWrite', 'clientKeys', 'sendAvatarData', 'sendCompatData', 'clientPatches',
        'clientReadBlocks', 'clientWriteBlocks', 'netEraseBlock', 'clientBinPatch', 'clientInfo',
        'myatoh32', 'netDisconnect', 'netReboot', 'client_usage']


def heads(src, tag):
    rows = mc9freq.dump(src, tag)
    out = {}
    for bb, fr, labs, calls, first in rows:
        for k in KEYS:
            if k in calls.split():
                out.setdefault(k, []).append(fr)
    return out


def main():
    a = sys.argv[1:]
    global KEYS
    if '-k' in a:
        KEYS = a[a.index('-k') + 1].split(',')
        a = a[:a.index('-k')] + a[a.index('-k') + 2:]
    res = [heads(s, 'h12_%d' % n) for n, s in enumerate(a)]
    for k in KEYS:
        print('%-18s' % k, ' | '.join(str(r.get(k, [])) for r in res))


if __name__ == '__main__':
    main()
