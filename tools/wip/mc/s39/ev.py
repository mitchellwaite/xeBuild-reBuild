"""ev.py: evaluate a variant (edits [+ bcp injections]) with the TRUE original order
(compat 115 before avatar 112, see s18 NOTES), 'x1' = the case head an asm goto took over."""
import os, sys, re, hashlib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m, voc
WANT = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132, 49, 115, 112, 103, 55, 126, 125, 61, 33, 29, 67,
        127, 117, 130, 35, 42, 53, 77, 79, 73, 81, 86, 91, 93]
POS = {b: i for i, b in enumerate(WANT)}
CASES = [129, 107, 109, 110, 113, 108, 119, 120, 121, 128, 116, 132]


def score_order(tok):
    o = [int(x) for x in tok if x.isdigit()]
    miss = [b for b in WANT if b not in o]
    xs = [i for i, x in enumerate(tok) if not x.isdigit()]
    cm = [b for b in miss if b in CASES]
    if xs and len(cm) == len(xs):
        tok = list(tok)
        for i, b in zip(xs, cm): tok[i] = str(b)
        o = [int(x) for x in tok if x.isdigit()]
        miss = [b for b in WANT if b not in o]
    o = [b for b in o if b in POS]
    inv = sum(1 for a in range(len(o)) for b in range(a + 1, len(o)) if POS[o[a]] > POS[o[b]])
    return inv, miss, o


def ev(text, tag, fncmp=True):
    r = m.meas(text, tag, fncmp=fncmp)
    if 'err' in r: return None
    tok = r['order'].split()[1:]
    inv, miss, o = score_order(tok)
    r['tinv'] = inv; r['tmiss'] = miss; r['o'] = o
    r['score'] = inv + 5 * len(miss)
    return r


if __name__ == '__main__':
    edits = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []
    r = ev(voc.make(edits), sys.argv[2] if len(sys.argv) > 2 else 'ev')
    print('score', r['score'], 'inv', r['tinv'], 'miss', r['tmiss'], 'fncmp', r.get('fncmp'))
    print(' '.join(map(str, r['o'])))
    print(r['raw'][3])
