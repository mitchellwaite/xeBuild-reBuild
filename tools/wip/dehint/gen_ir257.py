"""Attempt 21: getImageKv's own form taken further: the load inline as Kv has it (no loadSmc), an `ok` result as Kv keeps,
and addr and size filled through pointers by a helper, each on gen_ir254's best addr and size forms.  No flags."""
import itertools, multiprocessing, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ir17lib import put, score, diff, LOG0, L38, L30, NOTSANE, LIM
from gen_ir254 import Z, S

LOAD = '''xb.smc.data = malloc(size);
 if (xb.smc.data) {
  xb.smc.size = size;
  memcpy(xb.smc.data, xb.dump + addr, size);
  log_printf(1, "decrypting SMC at address 0x%x of size 0x%x\\n", addr, size);
  if (unscramble(xb.smc.data, xb.smc.size)) {
   log_printf(1, "SMC decrypted OK, will use if no external smc.bin is provided\\n");
   setSmcKey(xb.smc.data);
  } else {
   log_printf(1, "SMC did not decrypt, discarding it\\n");
   free(xb.smc.data);
   xb.smc.data = 0;
   xb.smc.size = 0;
  }
 } else
  log_printf(1, "Wasn't able to alloc 0x%x bytes memory for SMC bin, not using...\\n", size);
'''
H = {
    # locals as today
    'loc': ('', 'struct flashhdr *h = (struct flashhdr *)xb.dump;\n int addr = SWAP32(h->smcBootAddr);\n int size = SWAP32(h->smcBootSize);\n'),
    # a helper fills both through pointers
    'ptr': ('static void smcArea(int *addr, int *size)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n *addr = SWAP32(h->smcBootAddr);\n *size = SWAP32(h->smcBootSize);\n}\n',
            'int addr, size;\n smcArea(&addr, &size);\n'),
    # helpers returning each value
    'ret': ('static int smcAddr(void)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n return SWAP32(h->smcBootAddr);\n}\nstatic int smcSize(void)\n{\n struct flashhdr *h = (struct flashhdr *)xb.dump;\n return SWAP32(h->smcBootSize);\n}\n',
            'int addr = smcAddr();\n int size = smcSize();\n'),
}
C = {
    'inl': f'if (addr < {LIM}) {{ {LOAD} }} else {NOTSANE}',
    'inlr': f'if (addr >= {LIM}) {{ {NOTSANE} return; }} {LOAD}',
    'hlp': f'if (addr < {LIM}) loadSmc(addr, size); else {NOTSANE}',
    # the load's success reported to a flag, as Kv's ok; the flag has no further use
    'okf': f'int ok = 0; if (addr < {LIM}) {{ loadSmc(addr, size); ok = 1; }} else {NOTSANE} (void)ok;',
}


def text(h, z, s, c):
    pre, d = H[h]
    return f'''{pre}void getImageSmc(void)
{{
 {d} {Z[z]}
 {S[s]}
 {C[c]}
}}'''


def one(k):
    return ('.'.join(k), score(put(text(*k))))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(diff(put(text(*sys.argv[1].split('.')))))
        sys.exit()
    keys = list(itertools.product(H, ['nestu', 'or', 'kv', 'share'], ['and', 'and30'], C))
    with multiprocessing.Pool(4) as p:
        res = p.map(one, keys, 4)
    res = [x for x in res if x[1][0] != 'E']
    res.sort(key=lambda x: (x[1][1], x[1][0]))
    for k, r in res[:14]:
        print(k, r[0], r[1], r[3])
    print(len(res), 'of', len(keys))
