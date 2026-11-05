"""getImageSmc: P(addr == 0x800) must be under 23.5% (call + opcode gives 13.7%): only the 3800 arm may be a guarded block with a call first.  Forms where the 3000 arm's first block holds a test or has two predecessors, no unreachable."""
FOCUS = ['_getImageSmc']
BASE = 'tools/wip/dehint/drafts/image_read_attempt6.c'
src = open(BASE, newline='').read().replace('\r\n', '\n')
i = src.index('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc')
j = src.index('void getImageKv(void)')
OLD = src[i:j]
LL = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);\n addr = 0x1000;\n'
S38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);\n'
S30 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);\n'
A38 = 'size = 0x3800; ' + S38
A30 = 'size = 0x3000; ' + S30
REST = OLD[OLD.index('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {'):]
REST = REST[:REST.index('	return;\nbad:')]
H = '''{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
%s
'''
A3 = '__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) '
PIN = '__asm__("" : "+D"(addr));'
Z = {'vh': f'if (!addr) {{ {LL} }} else {{ vhot: __attribute__((hot)); }}\n', 'v0': f'if (!addr) {{ {LL} }}\n'}
BL = {'bh': 'bhot: __attribute__((hot));\n', 'b0': ''}
T = 'unsigned t = addr;\n if (t != 0x1000) { if (t != 0x800) goto bad; }\nbback:\n'
SH = 'shot: __attribute__((hot));\n'
C = '(size != 0x3000 && size != 0x3800)'
ARMS = {
 # reference: the plain arm, for scale
 'eq': f'if {C} {{ {SH} if (addr == 0x800) {{ {A38} }} else {{ {A30} }} }} else {{ {PIN} }}',
 # the flag
 'flag': f'int fix = {C}; if (fix && addr == 0x800) {{ {SH} {A38} }} else if (fix) {{ {SH} {A30} }} else {{ {PIN} }}',
 'flag2': f'int fix = {C}; if (fix) {{ {SH} if (addr == 0x800) {{ {A38} }} else {{ {A30} }} }} else {{ {PIN} }}',
 'flag3': f'int fix = {C}; if (fix && addr == 0x800) {{ {A38} }} else if (fix) {{ {SH} {A30} }} else {{ {PIN} }}',
 # 3800 first with the condition repeated
 'rep': f'if ({C} && addr == 0x800) {{ {SH} {A38} }} else if {C} {{ {SH} {A30} }} else {{ {PIN} }}',
 'rep2': f'if ({C} && addr == 0x800) {{ {A38} }} else if {C} {{ {SH} {A30} }} else {{ {PIN} }}',
 # 3000 first by a second size test in the arm
 's30': f'if {C} {{ {SH} if (addr == 0x800) {{ {A38} }} else if (size != 0x3000) {{ {A30} }} }} else {{ {PIN} }}',
 's30b': f'if {C} {{ {SH} if (addr == 0x800) {{ {A38} }} else if (size != 0x3800) {{ {A30} }} }} else {{ {PIN} }}',
 'nz': f'if {C} {{ {SH} if (addr == 0x800) {{ {A38} }} else if (addr) {{ {A30} }} }} else {{ {PIN} }}',
 # early out of the 3800 arm
 'gd': f'if {C} {{ {SH} if (addr == 0x800) {{ {A38} goto done; }} {A30} }} else {{ {PIN} }} done:\n',
 # a real second predecessor of the 3000 block
 'tw': f'if {C} {{ {SH} if (addr != 0x800) goto s30; {A38} }} else {{ {PIN} }} goto done; s30: {A30} done:\n',
 # tests on size after picking a new value
 'ns': f'int fixed = addr == 0x800 ? 0x3800 : 0x3000; if {C} {{ {SH} size = fixed; if (size == 0x3800) {{ {S38} }} else {{ {S30} }} }} else {{ {PIN} }}',
 'ns2': f'if {C} {{ {SH} size = addr == 0x800 ? 0x3800 : 0x3000; if (size == 0x3800) {{ {S38} }} else {{ {S30} }} }} else {{ {PIN} }}',
 'ns3': f'if {C} {{ {SH} size = 0x3000; if (addr == 0x800) size = 0x3800; if (size == 0x3800) {{ {S38} }} else {{ {S30} }} }} else {{ {PIN} }}',
 'ns4': f'if {C} {{ {SH} if (addr == 0x800) size = 0x3800; else size = 0x3000; if (size != 0x3000) {{ {S38} }} else {{ {S30} }} }} else {{ {PIN} }}',
}
AX = []
for kz, z in Z.items():
    for kb, bl in BL.items():
        for ka, a in ARMS.items():
            tail = f'return;\nbad:\n{bl}{LL}goto bback;\n}}\n\n'
            AX.append(('.'.join((kz, kb, ka)), [(OLD, A3 + 'void getImageSmc(void)\n' + (H % '') + z + T + a + '\n' + REST + tail)]))
AXES = [AX]
