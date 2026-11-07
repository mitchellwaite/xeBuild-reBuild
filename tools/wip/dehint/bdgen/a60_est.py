"""Attempt 60: code-neutral (or nearly) edits that change inline-size estimates, IPA inline order,
block numbering or SSA numbering, on src as of 862bda0c, crossed with each remaining hint off.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a60_est.py [-f label] [-o ..]"""

ANCHOR = '/* load the input files by their type; the arms only set r, which is\n'
MM1 = ('\t\t\t\tmemmove(e->data, defPayload, 0x200);\n', '\t\t\t\tmemcpy(e->data, defPayload, 0x200);\n')
MM22 = ('\t\t\t\tmemmove(e->data, defCore, 0xd40);\n', '\t\t\t\tmemcpy(e->data, defCore, 0xd40);\n')
SALT = [('\tuint8_t salt[16];\n', '\tuint8_t salt[16] = {0};\n'), ('\tmemset(salt, 0, sizeof(salt));\n', '')]
FST = [('\t\t\tstruct fileent f;\n\n\t\t\tmemset(&f, 0, sizeof(f));\n', '\t\t\tstruct fileent f = {0};\n\n')]
PCB_OLD = '''			} else
				patchConsoleBlmod();
'''
PCB_NEW = '''			} else if (!xb.consoleBlmod.data || !xb.consoleBlmod.size)
				patchBlsBlmod(NULL, 0);
			else {
				patchBlsBlmod(xb.consoleBlmod.data, xb.consoleBlmod.size);
				free(xb.consoleBlmod.data);
			}
'''
PCB_FN = '''/* no blmod.bin: the console's, if any */
static void patchConsoleBlmod(void)
{
	if (!xb.consoleBlmod.data || !xb.consoleBlmod.size) {
		patchBlsBlmod(NULL, 0);
		return;
	}
	patchBlsBlmod(xb.consoleBlmod.data, xb.consoleBlmod.size);
	free(xb.consoleBlmod.data);
}

'''
PCB_FN2 = '''/* no blmod.bin: the console's, if any */
static void patchConsoleBlmod(void)
{
	if (xb.consoleBlmod.data && xb.consoleBlmod.size) {
		patchBlsBlmod(xb.consoleBlmod.data, xb.consoleBlmod.size);
		free(xb.consoleBlmod.data);
	} else
		patchBlsBlmod(NULL, 0);
}

'''

NAND_FN = '''/* take a file's data (from the nand dump or the console) in place of e's */
static void useNandData(struct fileent *e, struct netfile *f)
{
	if (e->data)
		free(e->data);
	e->data = f->data;
	e->size = f->size;
	f->data = NULL;
	f->size = 0;
}

'''


def nand_old(ind, f):
    t = '\t' * ind
    return (t + 'if (e->data)\n' + t + '\tfree(e->data);\n' + t + 'e->data = xb.%s.data;\n' % f + t +
            'e->size = xb.%s.size;\n' % f + t + 'xb.%s.data = NULL;\n' % f + t + 'xb.%s.size = 0;\n' % f)


def nand(fields):
    ed = [(ANCHOR, NAND_FN + ANCHOR)]
    for f in fields:
        ed.append((nand_old(5, f), '\t\t\t\t\tuseNandData(e, &xb.%s);\n' % f, 2))
    return ed


LOG = 'log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);\n'
NR_OLD = '\t\tif (r) {\n\t\t\t' + LOG + '\t\t\treturn -1;\n\t\t}\n'
NR_FN = ('/* the error both loaders end on */\nstatic int notRead(struct fileent *e, uint32_t r)\n{\n\t' + LOG +
         '\treturn -1;\n}\n\n')
NR_FNV = '/* the error both loaders end on */\nstatic void notRead(struct fileent *e, uint32_t r)\n{\n\t' + LOG + '}\n\n'

SMC = '''				e->offset = smcSetLoad(e->size);
				if (e->offset)
					break;
				/* one -1 block for the patch size, SMC and (xb.type <=
				   BUILD_DEVGL16) signature failures: the asm keeps it a block
				   of its own (else the -1 is appended to the size log, which
				   crossjump can't then share) */
			fail:
				__asm__ __volatile__("");
				r = -1;
				break;
'''
SMCIF = '''				e->offset = smcSetLoad(e->size);
				if (!e->offset) {
			fail:
				__asm__ __volatile__("");
					r = -1;
				}
				break;
'''
DEF = '''				log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
				break;
			}
'''
SMCEND = [(SMC, '''				e->offset = smcSetLoad(e->size);
				if (!e->offset)
					goto fail;
				break;
'''), (DEF, DEF.replace('\t\t\t}\n', '\t\t\tfail:\n\t\t\t\t__asm__ __volatile__("");\n\t\t\t\tr = -1;\n\t\t\t\tbreak;\n\t\t\t}\n'))]

XELL = '''	if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
		return 0;
	if (!loadBaseFile(e->name, e))
		return 0;
	log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
	if (!loadBinFile(e))
		return 0;
	log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
	return loadLocalFile(e);
'''
XELL_NEST = '''	if (xb.type != BUILD_RETAIL && xb.type <= BUILD_DEVGL16 && loadBaseFile(e->name, e)) {
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
		if (loadBinFile(e)) {
			log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
			return loadLocalFile(e);
		}
	}
	return 0;
'''
XELL_R = '''	int r;

	if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
		return 0;
	r = loadBaseFile(e->name, e);
	if (r) {
		log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
		r = loadBinFile(e);
		if (r) {
			log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
			r = loadLocalFile(e);
		}
	}
	return r;
'''
XELL_RANGE = XELL.replace('xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16', 'xb.type < BUILD_JTAG || xb.type > BUILD_DEVGL16')

LBF = '''	if (xb.baseDir[0]) {
		char path[0x400];

		strcpy(path, xb.baseDir);
		strcat(path, name);
		return loadFileCrc(path, e, 1, 0, 0);
	}
	return -1;
'''
LBF_EARLY = '''	char path[0x400];

	if (!xb.baseDir[0])
		return -1;
	strcpy(path, xb.baseDir);
	strcat(path, name);
	return loadFileCrc(path, e, 1, 0, 0);
'''

BL60 = '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	e->size = 0x60;
	memmove(e->data, defBl60, 0x60);
	return 0;
'''
BL60_LATE = '''	e->data = malloc(0x60);
	if (!e->data)
		return 1;
	memmove(e->data, defBl60, 0x60);
	e->size = 0x60;
	return 0;
'''
BL60_LOCAL = '''	uint8_t *p = malloc(0x60);

	e->data = p;
	if (!p)
		return 1;
	e->size = 0x60;
	memmove(p, defBl60, 0x60);
	return 0;
'''

UB_FN = '''/* a built-in copy in place of a file that couldn't be read */
static int useBuiltIn(struct fileent *e, const uint8_t *data, uint32_t size)
{
	e->data = malloc(size);
	if (!e->data)
		return 1;
	e->size = size;
	memmove(e->data, data, size);
	return 0;
}

'''


def ub_case(what, name, size):
    old = ('\t\t\t\te->data = malloc(0x%x);\n\t\t\t\tif (!e->data) {\n\t\t\t\t\tr = 1;\n\t\t\t\t\tbreak;\n\t\t\t\t}\n'
           '\t\t\t\te->size = 0x%x;\n\t\t\t\tmemmove(e->data, %s, 0x%x);\n\t\t\t\tbreak;\n') % (size, size, name, size)
    return (old, '\t\t\t\tr = useBuiltIn(e, %s, 0x%x);\n\t\t\t\tbreak;\n' % (name, size))


UB = [('/* the default 0x60-byte bootloader (type 24).', UB_FN + '/* the default 0x60-byte bootloader (type 24).'),
      ub_case('payload', 'defPayload', 0x200), ub_case('core', 'defCore', 0xd40)]
UBB = UB + [(BL60, '\treturn useBuiltIn(e, defBl60, 0x60);\n')]

V = {
    'base': [],
    'mc1': [MM1], 'mc22': [MM22], 'mc122': [MM1, MM22],
    'salt0': SALT, 'fst0': FST, 'salt_fst': SALT + FST,
    'pcb_in': [(PCB_FN, ''), (PCB_OLD, PCB_NEW)], 'pcb_fn2': [(PCB_FN, PCB_FN2)],
    'nand_ka': nand(['kv', 'kvAlt']), 'nand_kas': nand(['kv', 'kvAlt', 'smc']),
    'nr_ret': [(NR_OLD, '\t\tif (r)\n\t\t\treturn notRead(e, r);\n', 2), (ANCHOR, NR_FN + ANCHOR)],
    'nr_void': [(NR_OLD, '\t\tif (r) {\n\t\t\tnotRead(e, r);\n\t\t\treturn -1;\n\t\t}\n', 2), (ANCHOR, NR_FNV + ANCHOR)],
    'smcif': [(SMC, SMCIF)], 'smcend': SMCEND,
    'x_nest': [(XELL, XELL_NEST)], 'x_r': [(XELL, XELL_R)], 'x_range': [(XELL, XELL_RANGE)],
    'lbf_early': [(LBF, LBF_EARLY)],
    'bl60_late': [(BL60, BL60_LATE)], 'bl60_loc': [(BL60, BL60_LOCAL)],
    'ub': UB, 'ubb': UBB,
}
