"""keysdaegrid.py [pins] : daeEncrypt shape sweep without expects or the cold label.

Axes: loop form, header test form, how the bad header leaves, the ladder's success
arms, declaration order.  'pins' keeps the two asm pins so the layout and hint
questions can be looked at apart from allocation."""
import itertools, sys
from multiprocessing.pool import ThreadPool
import keyslib as K
from keysfn import replace_fn

LH = r'log_printf(0, "\n******* ERROR: dae segment does not have the expected header!\n");'
TRY1 = r'log_printf(1, "dae appears encrypted, attempting to decrypt with CPU key...");'
OK = r'log_printf(1, "success!\n");'
TRY2 = r'log_printf(1, "failed! Attempting to decrypt with alternate key...\n");'
FAILM = r'log_printf(0, "failed!\n******* ERROR: dae hash incorrect, could not verify decrypted dae!\n");'
SC = 'shaCheck(dae, len, 12, 20, 336, NULL)'
ONE = 'daeEncryptOne(dae, len, date);'

# the decrypt ladder; every form ends with the segment encrypted or given up
LADDER = {
    'L0': f'''if (!{SC}) {{
if (!n) {TRY1}
memcpy(dae, orig + off, len);
daeDecrypt(dae, len, 1);
if ({SC}) {{ {OK} {ONE} n++; goto next; }}
if (!n) {TRY2}
memcpy(dae, orig + off, len);
daeDecrypt(dae, len, 0);
if ({SC}) {{ if (!n) {OK} }} else {{
if (!n) {FAILM}
n = 0; off = size + 1; goto next; }}
}}
{ONE} n++;''',
    'L1': f'''if (!{SC}) {{
if (!n) {TRY1}
memcpy(dae, orig + off, len);
daeDecrypt(dae, len, 1);
if ({SC}) {OK}
else {{
if (!n) {TRY2}
memcpy(dae, orig + off, len);
daeDecrypt(dae, len, 0);
if ({SC}) {{ if (!n) {OK} }} else {{
if (!n) {FAILM}
n = 0; off = size + 1; goto next; }}
}} }}
{ONE} n++;''',
    'L2': f'''if ({SC}) {{ {ONE} n++; }}
else {{
if (!n) {TRY1}
memcpy(dae, orig + off, len);
daeDecrypt(dae, len, 1);
if ({SC}) {{ {OK} {ONE} n++; }}
else {{
if (!n) {TRY2}
memcpy(dae, orig + off, len);
daeDecrypt(dae, len, 0);
if ({SC}) {{ if (!n) {OK} {ONE} n++; }} else {{
if (!n) {FAILM}
n = 0; off = size + 1; }}
}} }}''',
}
LEN = 'len = (uint16_t)((buf[off + 4] << 8) + buf[off + 5]);'
HDR = {
    'H0': lambda g: f"if (buf[off] == 'D' && buf[off + 1] == 'A' && buf[off + 2] == 'E' && buf[off + 3] == 'P') {{ {g} }} else {{ {LH} BRK }}",
    'H1': lambda g: f"if (buf[off] != 'D' || buf[off + 1] != 'A' || buf[off + 2] != 'E' || buf[off + 3] != 'P') {{ {LH} BRK }}\n{g}",
    'H2': lambda g: f"if (buf[off] != 'D' || buf[off + 1] != 'A' || buf[off + 2] != 'E' || buf[off + 3] != 'P') {{ {LH} BRK }} else {{ {g} }}",
    'H3': lambda g: f"if (buf[off] == 'D') {{ if (buf[off + 1] == 'A') {{ if (buf[off + 2] == 'E') {{ if (buf[off + 3] == 'P') {{ {g} goto next; }} }} }} }}\n{LH} BRK",
    'H4': lambda g: f"if (dae[0] == 'D' && dae[1] == 'A' && dae[2] == 'E' && dae[3] == 'P') {{ {g} }} else {{ {LH} BRK }}",
    'H5': lambda g: f"if (buf[off] == 'D' && buf[off + 1] == 'A' && buf[off + 2] == 'E' && buf[off + 3] == 'P') {{ {g} }} else {{ {LH} BRK }}".replace("buf[off] == 'D'", "*dae == 'D'"),
}
BRK = {'B0': 'break;', 'B1': 'off = size; len = 0;', 'B2': 'goto done;'}
LOOP = {
    'W0': lambda b: f'if (size) do {{ {b}\nnext:\noff += len;\n}} while (off < size);',
    'W1': lambda b: f'while (off < size) {{ {b}\nnext:\noff += len;\n}}',
    'W2': lambda b: f'for (; off < size; off += len) {{ {b}\nnext:\n;\n}}',
    'W3': lambda b: f'if (size) {{ while (off < size) {{ {b}\nnext:\noff += len;\n}} }}',
    'W4': lambda b: f'while (1) {{ if (off >= size) break; {b}\nnext:\noff += len;\n}}',
    'W5': lambda b: f'for (;;) {{ if (off < size) {{ {b} }} else break;\nnext:\noff += len;\n}}',
    'W6': lambda b: f'do {{ if (off >= size) break; {b}\nnext:\noff += len;\n}} while (1);',
    'W7': lambda b: f'if (size > 0) {{ for (; off < size; off += len) {{ {b}\nnext:\n;\n}} }}',
    'W8': lambda b: f'do {{ if (off < size) {{ {b}\nnext:\noff += len;\n}} }} while (off < size);',
}
LW = r'log_printf(0, "\n******* WARNING: dae data appears to be crypted with a different key or damaged! Skipping encryption.\n");'
END = {
    'E0': f'if (n != 2) {{ {LW} }}\nfree(orig);',
    'E1': f'if (n == 2) {{ free(orig); return; }}\n{LW}\nfree(orig);',
    'E2': f'if (n == 2) free(orig);\nelse {{ {LW} free(orig); }}',
    'E3': f'if (n != 2) {{ {LW} free(orig); return; }}\nfree(orig);',
    'E4': f'if (n != 2) {{ {LW} free(orig); }} else free(orig);',
    'E5': f'if (n == 2) {{ }} else {LW}\nfree(orig);',
    'E6': f'free(orig);\nif (n != 2) {{ {LW} }}',
    'E7': f'if (n != 2) {{ {LW} }}\nfree(orig);\nreturn;',
    'E8': f'{{ int ok = 0; if (n == 2) ok = 1; if (!ok) {{ {LW} }} }}\nfree(orig);',
    'E9': f'{{ int ok = 1; if (n != 2) ok = 0; if (!ok) {{ {LW} }} }}\nfree(orig);',
    'Ea': f'{{ int bad = n != 2; if (bad) {{ {LW} }} }}\nfree(orig);',
    'Eb': f'if (n > 2 || n < 2) {{ {LW} }}\nfree(orig);',
    'Ec': f'if (n == 2) goto out;\n{LW}\nout:\nfree(orig);',
    'Ed': f'if (n != 2) {{ {LW} goto out; }}\nout:\nfree(orig);',
    'Ee': f'switch (n) {{ case 2: break; default: {LW} }}\nfree(orig);',
    'Ef': f'if ((n ^ 2) != 0) {{ {LW} }}\nfree(orig);',
    'Eg': f'if (n != 2) goto warn;\nout:\nfree(orig);\nreturn;\nwarn:\n{LW}\ngoto out;',
    'Eh': f'if (n == 2) {{\nout:\nfree(orig);\nreturn;\n}}\n{LW}\ngoto out;',
    'Ei': f'if (n != 2) goto warn;\nfree(orig);\nreturn;\nwarn:\n{LW}\nfree(orig);',
    'Ej': f'if (n == 2) {{ free(orig); return; }}\n{LW}\nfree(orig);\nreturn;',
    'Ek': f'if (n != 2) {{ {LW} }}\nif (orig) free(orig);',
    'El': f'if (n != 2) {{ {LW} }}\nif (orig != NULL) free(orig);',
    'Em': f'if (n == 2) {{ }} else {LW}\nif (orig) free(orig);',
}


def text(w, h, b, l, pins, e='E0'):
    g = LEN + '\n' + LADDER[l]
    body = HDR[h](g).replace('BRK', BRK[b])
    pin1 = '__asm__("" : "+b"(off));' if pins else ''
    pin2 = '__asm__("" :: "d"(off));' if pins else ''
    return f'''void daeEncrypt(uint8_t *buf, uint32_t size, uint8_t *date)
{{
	uint8_t *orig = malloc(size);
	uint8_t *dae;
	uint32_t off = 0;
	uint32_t len;
	int n = 0;
	{pin1}

	memcpy(orig, buf, size);
	{LOOP[w]("dae = buf + off; " + pin2 + chr(10) + body)}
done:
	{END[e]}
}}

'''


def main():
    pins = 'pins' in sys.argv
    b = K.base()
    jobs = list(itertools.product(['W1', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8'], ['H0', 'H2', 'H3'], BRK, ['L0'], ['E0', 'E3', 'Ec']))
    print(len(jobs), flush=True)
    slots = [[] for _ in range(4)]
    for i, j in enumerate(jobs):
        slots[i % 4].append((i % 4, j))

    def work(sl):
        out = []
        for slot, j in sl:
            o = K.compile(replace_fn(b, 'daeEncrypt', text(j[0], j[1], j[2], j[3], pins, j[4])), tag='dx%d' % slot)
            out.append((j, K.same(o), K.fndiff(o) if o else {'fail': 9999}))
        return out
    with ThreadPool(4) as p:
        res = sum(p.map(work, slots), [])
    res.sort(key=lambda r: sum(r[2].values()))
    for r in res[:25]:
        print('MATCH' if r[1] else '     ', r[0], r[2])


if __name__ == '__main__':
    main()
