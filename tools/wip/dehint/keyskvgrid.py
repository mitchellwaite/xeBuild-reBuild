"""keyskvgrid.py: kvPrepare grammar sweep with no hints (or a kept alt expect).

Axes are the polarity and nesting of each test.  Prints the best and any whole-object
match; set KEYSBASE to the draft with the rest of the object."""
import itertools, os, sys
from multiprocessing.pool import ThreadPool
import keyslib as K
from keysfn import replace_fn

LSZ = r'log_printf(0, "\n******* ERROR: %s is not the correct size! Skipping verification and encryption!\n", file);'
PRE = r'''log_printf(1, "%s appears to be decrypted already, but the hash does not match the CPU key...", file);
log_printf(0, "\n******* WARNING: could not verify pre-decrypted keyvault, please be sure your provided a valid %s!\n", file);'''
ENCMSG = r'log_printf(1, "%s appears to be encrypted, attempting to decrypt...", file);' + '\nmemcpy(buf, kv->data, kv->size);'
FAIL = r'''log_printf(1, "Failed!\n%s could not be decrypted!\n", file);
log_printf(0, "\n******* ERROR: could not decrypt %s, please be sure your provided a valid %s!\n", name, file);
memcpy(buf, kv->data, kv->size);'''
OKM = r'log_printf(1, "Success!\n");'
DEC = r'log_printf(0, "\n******* ERROR: please be sure your provided a DEcrypted %s!\n", file);'
ENC = 'kvSet(kv->data);\nkvEncrypt(kv->data, kv->size);'
ENA = 'kvEncryptAlt(kv->data, kv->size);'

V = {
    'v0': f'if (!verifyExtended(buf, 0x4000)) {{ {FAIL} }} else {OKM}',
    'v1': f'if (verifyExtended(buf, 0x4000)) {OKM}\nelse {{ {FAIL} }}',
}
Z88 = {
    'z0': lambda v: f'if (checkZeros(buf + 56, 88)) {{ {PRE} }} else {{ {ENCMSG}\n{v} }}',
    'z1': lambda v: f'if (!checkZeros(buf + 56, 88)) {{ {ENCMSG}\n{v} }} else {{ {PRE} }}',
}
H = {
    'h0': lambda z: f'if (!kvHashOk(buf, kv->size)) {{ {z} }}',
    'h1': lambda z: f'if (kvHashOk(buf, kv->size)) {{ }} else {{ {z} }}',
}
Z16 = {
    'q0': lambda h: f'if (!checkZeros(buf, 16)) {{ {h} }} else if (!checkZeros(kv->data + 88, 8)) {{ {DEC} }}',
    'q1': lambda h: f'if (checkZeros(buf, 16)) {{ if (!checkZeros(kv->data + 88, 8)) {{ {DEC} }} }} else {{ {h} }}',
    'q2': lambda h: f'if (!checkZeros(buf, 16)) {{ {h} }} else {{ if (!checkZeros(kv->data + 88, 8)) {{ {DEC} }} }}',
}
ALT = {
    'a0': f'if (!alt) {{ {ENC} }} else {{ {ENA} }}',
    'a1': f'if (alt) {{ {ENA} }} else {{ {ENC} }}',
    'a2': f'if (alt == 0) {{ {ENC} }} else {{ {ENA} }}',
    'ax': f'if (__builtin_expect(!alt, 0)) {{ {ENC} }} else {{ {ENA} }}',
    'a3': f'if (alt) {{ {ENA} free(buf); return; }}\n{ENC}',
    'a4': f'if (!alt) {{ {ENC} free(buf); return; }}\n{ENA}',
    'a5': f'if (!alt) {{ {ENC} }}\nif (alt) {{ {ENA} }}',
    'a6': f'if (alt) {{ {ENA} }}\nif (!alt) {{ {ENC} }}',
    'a7': f'if (!alt) kvSet(kv->data);\nif (alt) {{ {ENA} }} else kvEncrypt(kv->data, kv->size);',
    'a8': f'if (!alt) kvSet(kv->data);\nif (!alt) kvEncrypt(kv->data, kv->size);\nelse {{ {ENA} }}',
    'a9': f'if (!alt) kvSet(kv->data);\nif (alt) {{ {ENA} }}\nif (!alt) kvEncrypt(kv->data, kv->size);',
    'aa': f'if (!alt) {{ {ENC} }}\nelse if (alt) {{ {ENA} }}',
}
SIZE = {
    's0': lambda r: f'if (kv->size != 0x4000) {{ {LSZ} return; }}\n{r}',
    's1': lambda r: f'if (kv->size != 0x4000) {{ {LSZ} }} else {{ {r} }}',
    's2': lambda r: f'if (kv->size == 0x4000) {{ {r} }} else {{ {LSZ} }}',
    's3': lambda r: f'if (kv->size == 0x4000) {{ {r} return; }}\n{LSZ}',
}
FIX = {
    'f0': '''if (kv->size == 0x3ff0) {
nbuf = malloc(0x4000); memset(nbuf, 0, 16); memcpy(nbuf + 16, kv->data, 0x3ff0);
free(kv->data); kv->data = nbuf; kv->size = 0x4000; }
''',
}


def text(s, f, q, h, z, v, a):
    inner = Z16[q](H[h](Z88[z](V[v])))
    rest = f'buf = malloc(0x4000);\nmemcpy(buf, kv->data, 0x4000);\n{inner}\nmemcpy(kv->data, buf, kv->size);\n{ALT[a]}\nfree(buf);'
    return f'''void kvPrepare(struct fileent *kv, int alt)
{{
	const char *file = "kv.bin", *name = "kv";
	uint8_t *buf, *nbuf;

	if (alt) {{
		file = "kv_alt.bin";
		name = "alt kv";
	}}
{FIX[f]}{SIZE[s](rest)}
}}

'''


def main():
    b = K.base()
    jobs = list(itertools.product(SIZE, FIX, ['q0', 'q1'], ['h0'], Z88, V, ALT))
    print(len(jobs), flush=True)
    slots = [[] for _ in range(4)]
    for i, j in enumerate(jobs):
        slots[i % 4].append((i % 4, j))

    def work(sl):
        out = []
        for slot, j in sl:
            o = K.compile(replace_fn(b, 'kvPrepare', text(*j)), tag='kg%d' % slot)
            out.append((j, K.same(o), K.fndiff(o) if o else {'fail': 9999}))
        return out
    with ThreadPool(4) as p:
        res = sum(p.map(work, slots), [])
    res.sort(key=lambda r: sum(r[2].values()))
    for r in res[:30]:
        print('MATCH' if r[1] else '     ', r[0], r[2])
    print('-- best without ax')
    for r in [r for r in res if r[0][6] != 'ax'][:15]:
        print('MATCH' if r[1] else '     ', r[0], r[2])


if __name__ == '__main__':
    main()
