"""quick test: error-variable shapes for image_read's getImageSmc, no hints.
run from the repo root: python <this> [name] (name prints the diff)"""
import itertools, os, subprocess, sys, re

R = os.getcwd()
LIB = os.path.join(R, 'tools', 'wip', 'dehint', 'irlib.py')
src = open(os.path.join(R, 'src', 'image_read.c'), newline='').read()
a = src.index('/* What stands for hints')
b = src.index('void getImageKv(void)')

HEAD = '''void getImageSmc(void)
{
	struct flashhdr *h = (struct flashhdr *)xb.dump;
	int addr = SWAP32(h->smcBootAddr);
	int size = SWAP32(h->smcBootSize);
	int fix = 0;

'''
ZLOG = 'log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);'
ADDR = {
 'two': '''	if (!addr) {
		%s
		addr = 0x1000;
	}
	if (addr != 0x1000 && addr != 0x800) {
		%s
		addr = 0x1000;
	}
''' % (ZLOG, ZLOG),
 'elif': '''	if (!addr) {
		%s
		addr = 0x1000;
	} else if (addr != 0x1000 && addr != 0x800) {
		%s
		addr = 0x1000;
	}
''' % (ZLOG, ZLOG),
 'one': '''	if (addr != 0x1000 && addr != 0x800) {
		%s
		addr = 0x1000;
	}
''' % ZLOG,
}
L3 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3000\\n", size);'
L38 = 'log_printf(1, "smc.bin should not be 0x%x bytes, using 0x3800\\n", size);'
SIZE = {
 'nest': '''	if (size != 0x3000 && size != 0x3800) {
		if (addr == 0x800) {
			size = 0x3800;
			%s
		} else {
			size = 0x3000;
			%s
		}
	}
''' % (L38, L3),
 'fixvar': '''	if (size != 0x3000 && size != 0x3800)
		fix = addr == 0x800 ? 0x3800 : 0x3000;
	if (fix) {
		size = fix;
		if (fix == 0x3800)
			%s
		else
			%s
	}
''' % (L38, L3),
 'fixvar2': '''	if (size != 0x3000 && size != 0x3800) {
		fix = 1;
		size = addr == 0x800 ? 0x3800 : 0x3000;
	}
	if (fix) {
		if (size == 0x3800)
			%s
		else
			%s
	}
''' % (L38, L3),
}
SANE = 'log_printf(1, "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\\n", addr, size);'
CHECK = {
 'if': '''	if ((unsigned)addr < 528 * xb.dumpPages)
		loadSmc(addr, size);
	else
		%s
}

''' % SANE,
 'ok': '''	fix = (unsigned)addr < 528 * xb.dumpPages;
	if (!fix) {
		%s
		return;
	}
	loadSmc(addr, size);
}

''' % SANE,
}

def text(k):
    x, s, c = k.split('.')
    return src[:a] + HEAD + ADDR[x] + SIZE[s] + CHECK[c] + src[b:]

names = ['.'.join(t) for t in itertools.product(ADDR, SIZE, CHECK)]
if len(sys.argv) > 1:
    names = sys.argv[1:]
tmp = os.path.join(R, 'build', 'ir', 'irq.c')
for n in names:
    open(tmp, 'w', newline='\n').write(text(n))
    args = [sys.executable, LIB, tmp] + (['-v', 'getImageSmc'] if len(sys.argv) > 1 else [])
    r = subprocess.run(args, capture_output=True, text=True)
    out = r.stdout.strip() or r.stderr.strip()
    print(n, '|', out if len(sys.argv) > 1 else out.splitlines()[0][:150])
