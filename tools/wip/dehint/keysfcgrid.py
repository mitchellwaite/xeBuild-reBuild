"""keysfcgrid.py: fcrtEncrypt grammar sweep, no expect, optionally no pure.

Size, offset and hash tests each take several forms (early return, else chain,
success first, with or without trailing return in each arm); locals can be scoped.
Prints the best combinations and any whole-object match."""
import itertools, sys
from multiprocessing.pool import ThreadPool
import keyslib as K
from keysfc import LS, LO, LV, SHA, AES, GET, MC, VF
from keysfn import replace_fn, NOPURE

SIZE = {
    's0r': lambda r: f'if (size != 0x4000) {{ {LS} return; }}\n{r}',
    's1': lambda r: f'if (size != 0x4000) {LS}\nelse {{ {r} }}',
    's1r': lambda r: f'if (size != 0x4000) {{ {LS} return; }} else {{ {r} }}',
    's2': lambda r: f'if (size == 0x4000) {{ {r} }} else {LS}',
    's2r': lambda r: f'if (size == 0x4000) {{ {r} return; }} else {LS}',
    's3': lambda r: f'if (size == 0x4000) {{ {r} return; }}\n{LS}',
}
OFF = {
    'o0r': lambda r: f'if (off >= 0x4000) {{ {LO} return; }}\n{r}',
    'o1': lambda r: f'if (off >= 0x4000) {LO}\nelse {{ {r} }}',
    'o1r': lambda r: f'if (off >= 0x4000) {{ {LO} return; }} else {{ {r} }}',
    'o2': lambda r: f'if (off < 0x4000) {{ {r} }} else {LO}',
    'o2r': lambda r: f'if (off < 0x4000) {{ {r} return; }} else {LO}',
    'o3': lambda r: f'if (off < 0x4000) {{ {r} return; }}\n{LO}',
}
HASH = {
    'h0r': f'if ({MC} && {VF} != 1) {{ {LV} return; }}\n{AES}',
    'h1': f'if ({MC} && {VF} != 1) {LV}\nelse {{ {AES} }}',
    'h1r': f'if ({MC} && {VF} != 1) {{ {LV} return; }} else {{ {AES} }}',
    'h2': f'if (!{MC} || {VF} == 1) {{ {AES} }} else {LV}',
    'h2r': f'if (!{MC} || {VF} == 1) {{ {AES} return; }} else {LV}',
    'h2s': f'if (!{MC} || {VF} == 1) {{ {AES} return; }}\n{LV}',
    'h2e': f'if ({MC} == 0 || {VF} == 1) {{ {AES} }} else {LV}',
    'h3r': f'if ({MC}) {{ if ({VF} != 1) {{ {LV} return; }} }}\n{AES}',
    'h3': f'if ({MC}) {{ if ({VF} != 1) {LV} else {{ {AES} }} }} else {{ {AES} }}',
    'h3b': f'if ({MC} == 0) {{ {AES} }} else if ({VF} == 1) {{ {AES} }} else {LV}',
    'h4': f'if ({MC} == 0 || {VF} == 1) {{ {AES} return; }}\n{LV}',
    'h5': f'if ({MC}) {{ if ({VF} == 1) goto enc; {LV} return; }}\nenc:\n{AES}',
    'h6': f'{{ int r = 1; if ({MC}) r = {VF}; if (r == 1) {{ {AES} }} else {LV} }}',
    'h6n': f'{{ int r = 1; if ({MC}) r = {VF}; if (r != 1) {LV} else {{ {AES} }} }}',
    'h6r': f'{{ int r = 1; if ({MC}) r = {VF}; if (r != 1) {{ {LV} return; }} {AES} }}',
    'h7': f'{{ int r = {MC} == 0; if (!r) r = {VF} == 1; if (r) {{ {AES} }} else {LV} }}',
    'h7r': f'{{ int r = {MC} == 0; if (!r) r = {VF} == 1; if (!r) {{ {LV} return; }} {AES} }}',
}


def text(sn, on, hn):
    body = SIZE[sn](GET + '\n' + OFF[on](SHA + '\n' + HASH[hn]))
    return f"""void fcrtEncrypt(uint8_t *fcrt, uint32_t size)
{{
	uint8_t iv[16];
	uint8_t hash[20];
	uint32_t off;
	XECRYPT_AES_STATE aes;

	memcpy(iv, fcrt + 256, 16);
{body}
}}

"""


def main():
    res = []
    bases = {'nopure': K.base().replace(NOPURE, ''), 'pure': K.base()}
    jobs = [(bn, s, o, h) for bn in bases for s in SIZE for o in OFF for h in HASH]
    print(len(jobs), 'jobs', flush=True)

    def one(a):
        i, (bn, s, o, h) = a
        src = replace_fn(bases[bn], 'fcrtEncrypt', text(s, o, h))
        ob = K.compile(src, tag='fg%d' % (i % 8))
        return (bn, s, o, h), K.same(ob), K.fndiff(ob) if ob else {'fail': 9999}
    # one tag per worker slot: map chunks so slots don't collide
    slots = [[] for _ in range(4)]
    for i, j in enumerate(jobs):
        slots[i % 4].append((i % 4, j))

    def work(sl):
        return [one(x) for x in sl]
    with ThreadPool(4) as p:
        for r in p.map(work, slots):
            res += r
    res.sort(key=lambda r: sum(r[2].values()))
    for r in res[:40]:
        print('MATCH' if r[1] else '     ', r[0], r[2])


if __name__ == '__main__':
    main()
