"""image_read's tricks as named source edits.  Importable; also a CLI:

python tools/wip/dehint/irtricks.py singles          every trick removed alone
python tools/wip/dehint/irtricks.py pairs [names..]  every pair (of names, default all)
python tools/wip/dehint/irtricks.py greedy           greedy descent from the full source
python tools/wip/dehint/irtricks.py show a,b,c [-o out.c] : score that combination, optional output
Base text: src/image_read.c, or IRBASE=<file>.  Names whose text isn't in the base are skipped."""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import irlib

T = {
    # --- getImageSmc
    'opt_smc': [('__attribute__((optimize("no-if-conversion", "no-if-conversion2", "no-tree-tail-merge"))) void getImageSmc', 'void getImageSmc')],
    'lit_smc': [('''	/* code-free: emits the zero/bad arms' string (at the end) first, as the original */
	__asm__("" : : "i"("smc.bin should not be at 0x%x, trying 0x1000\\n"));
''', '')],
    'lab_vhot': [('''	} else {
		vhot: __attribute__((hot));
	}
''', '''	}
''')],
    'lab_shot': [('''		shot: __attribute__((hot));
''', '')],
    'unr_smc': [('''			if (!h)
				__builtin_unreachable();
''', '')],
    'pin_addr': [('''	} else
		__asm__("" : "+D"(addr));
''', '''	}
''')],
    'exp_smc': [('if (__builtin_expect(addr < 528 * xb.dumpPages, 0)) {', 'if (addr < 528 * xb.dumpPages) {')],
    'lab_bhot': [('''		bhot: __attribute__((hot));
''', '')],
    # keeps the blocks, only spells them after a return
    'if0_smc': [('''	if (0) {
zero:
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
		goto zback;
bad:
''', '''	return;
zero:
		log_printf(1, "smc.bin should not be at 0x%x, trying 0x1000\\n", addr);
		addr = 0x1000;
		goto zback;
bad:
'''), ('''		addr = 0x1000;
		goto bback;
	}
}
''', '''		addr = 0x1000;
		goto bback;
}
''')],
    # --- loadFlashFile
    'noinline': [('int loadFlashFile(int i, uint32_t block) __attribute__((noinline));', 'int loadFlashFile(int i, uint32_t block);')],
    # --- fsGetFile
    'pin_v': [('''	/* code-free hint: fsValid (reused for return 1) in esi, name in edi */
	__asm__("" : : "S"(v));
''', '')],
    # --- findAnchor
    'lit_anchor': [('''		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
''', '')],
    'bar_anchor': [('''		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
''', '')],
    'exp_ok0': [('if (__builtin_expect(ok0, 1) && (', 'if (ok0 && (')],
    'exp_nok1': [('(__builtin_expect(!ok1, 1) || v0 >= v1)', '(!ok1 || v0 >= v1)')],
    'exp_ok1': [('if (__builtin_expect(ok1, 1)) {', 'if (ok1) {')],
    # --- scanMobiles
    'exp_scan': [('''			/* lays the advance block after the found path's stores */
			if (__builtin_expect(len & 0x8000, 1)) {''', '''			if (len & 0x8000) {''')],
    # --- checkBlock
    'pin_t': [('''				/* opaque int copy: the <= 0x29 test stays an int
				   compare and isn't merged with the zero test */
				__asm__("" : "+d"(t));
''', '')],
    # --- remapBadBlocks
    'unr_remap': [('''			if (!xb.numBad)	/* i < numBad: drops the inlined loop's guard */
				__builtin_unreachable();
''', '')],
    # --- copyMmcImage
    'opt_mmc': [('__attribute__((optimize("no-if-conversion"))) uint32_t copyMmcImage', 'uint32_t copyMmcImage')],
    # --- addRemapP
    'pin_cb': [('''	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));
''', '')],
    # --- parseDump
    'pin_b2': [('''			__asm__("" : "+r"(b2));
''', '')],
    'unr_p1': [('''			if (blk >= blocks)
				__builtin_unreachable();
			log_printf(1, "ECD''', '''			log_printf(1, "ECD''')],
    'bar_p': [('''			__asm__("");
			dst = blk;
''', '''			dst = blk;
''')],
    'lab_rem': [('''rem: __attribute__((hot));
''', '')],
    'unr_p2': [('''		if (blk >= blocks)
			__builtin_unreachable();
		if (dst != blk &&''', '''		if (dst != blk &&''')],
    # --- detectController
    'pin_found': [('''		if (n > 1)
			__asm__("" : "+a"(found));
''', '')],
    'pin_lo': [('''					/* code-free: lo stays live over both tests: the
					   first sum takes hi's register (ebp), lo2 edx */
					__asm__("" : : "a"(lo));
''', '')],
    'pin_lo2': [('''					__asm__("" : : "d"(lo2));
''', '')],
    # --- checkHeader
    'bar_hdr': [('''	__asm__("");
	if (SWAP32(hdr.cfOffset)''', '''	if (SWAP32(hdr.cfOffset)''')],
    # --- loadDump
    'lab_mmc': [('''mmcbad: __attribute__((hot));
''', '')],
}


def base():
    p = os.environ.get('IRBASE', irlib.SRC)
    return open(p, newline='').read().replace('\r\n', '\n')


def apply(text, names):
    for n in names:
        for a, b in T[n]:
            if a not in text:
                continue  # already gone from this base
            text = text.replace(a, b)
    return text


def run(names, text=None):
    t = apply(text if text is not None else base(), list(names))
    return irlib.score_text(t, [])


ALL = [n for n in T if all(a in base() for a, b in T[n])]


def many(combos, text=None, workers=4):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda c: (c, run(c, text)), combos))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'singles':
        missing = [n for n in T if n not in ALL]
        if missing:
            print('not in base:', missing)
        for c, r in many([(n,) for n in ALL]):
            print(','.join(c), irlib.fmt(r), flush=True)
    elif cmd == 'pairs':
        names = sys.argv[2:] or ALL
        res = many(list(itertools.combinations(names, 2)))
        res.sort(key=lambda x: x[1].get('total', 1e9))
        for c, r in res:
            print(','.join(c), irlib.fmt(r))
    elif cmd == 'show':
        names = sys.argv[2].split(',') if sys.argv[2] != '-' else []
        r = run(names)
        print(irlib.fmt(r))
        if '-o' in sys.argv:
            open(sys.argv[sys.argv.index('-o') + 1], 'w', newline='\n').write(apply(base(), names))
    elif cmd == 'greedy':
        cur = []
        best = run(cur)
        print('start', irlib.fmt(best), flush=True)
        while True:
            res = many([cur + [n] for n in ALL if n not in cur])
            res.sort(key=lambda x: x[1].get('total', 1e9))
            c, r = res[0]
            print(','.join(c), irlib.fmt(r), flush=True)
            for c2, r2 in res[1:4]:
                print('   ', c2[-1], r2.get('total'), flush=True)
            if len(c) >= len(ALL):
                break
            cur = list(c)
