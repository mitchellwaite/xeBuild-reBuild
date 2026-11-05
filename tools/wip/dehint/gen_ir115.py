"""getImageSmc: hint-free, addr part from gen_ir114 `a` (bad falls through, prologue's addr half right); forms of the size part
that merge the two tests and have P(bad) over 52.7."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
L = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
Z = f'if (!addr) {{ {L} }}\n'
ADDR = Z + f'uint32_t a = addr;\n if (a != 0x800) {{ if (a != 0x1000) {{ {L} }} }}\n'
ADDR2 = Z + f'{{ uint32_t a = addr;\n if (a != 0x800) {{ if (a != 0x1000) {{ {L} }} }} }}\n'
S1 = '''if (addr == 0x800) {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		} else {
			size = 0x3000;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
		}
'''
S2 = '''if (addr != 0x800) {
			size = 0x3000;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
		} else {
			size = 0x3800;
			log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);
		}
'''
S3 = '''size = addr == 0x800 ? 0x3800 : 0x3000;
		log_printf(1, addr == 0x800 ? "smc.bin should not be 0x%x bytes, using 0x3800\\n" : "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);
'''
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')] + '}\n\n'
EXK = {'ex': REST, 'e0': REST.replace('__builtin_expect(addr < 528 * xb.dumpPages, 0)', 'addr < 528 * xb.dumpPages')}
INT = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);

'''
USZ = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	uint32_t size = SWAP32(h->smcBootSize);

'''
ISZ = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int s = SWAP32(h->smcBootSize);
	uint32_t size = s;

'''
USS = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	uint32_t s = SWAP32(h->smcBootSize);
	int size = s;

'''
FORMS = {
    'int.and': (INT, 'if (size != 0x3000 && size != 0x3800) {%s}\n'),
    'uint.and': (USZ, 'if (size != 0x3000 && size != 0x3800) {%s}\n'),
    'uint.nest': (USZ, 'if (size != 0x3000) { if (size != 0x3800) {%s} }\n'),
    'isz.nest': (ISZ, 'if (size != 0x3000) { if (size != 0x3800) {%s} }\n'),
    'isz.and': (ISZ, 'if (size != 0x3000 && size != 0x3800) {%s}\n'),
    'iss.nest': (ISZ, 'if (s != 0x3000) { if (s != 0x3800) {%s} }\n'),
    'uss.nest': (USS, 'if (s != 0x3000) { if (s != 0x3800) {%s} }\n'),
    'uss.nest2': (USS, 'if (size != 0x3000) { if (size != 0x3800) {%s} }\n'),
    'int.ucast': (INT, 'if ((uint32_t)size != 0x3000) { if ((uint32_t)size != 0x3800) {%s} }\n'),
    'int.sc': (INT, 'uint32_t sz = size;\n if (sz != 0x3000) { if (sz != 0x3800) {%s} }\n'),
    'int.sc2': (INT, '{ uint32_t sz = size;\n if (sz != 0x3000) { if (sz != 0x3800) {%s} } }\n'),
}
AX = []
for k, (h, f) in FORMS.items():
    for ka, a in (('a', ADDR), ('a2', ADDR2)):
        for kb, b in (('s1', S1), ('s2', S2), ('s3', S3)):
            for ke, e in EXK.items():
                AX.append(('.'.join((k, ka, kb, ke)), [(OLD, h + a + (f % b) + e)]))
AXES = [AX]
