"""Attempt 9, reconstruction A: loadBlFiles as one loop, the switch in it, r a local tested after the
switch, as loadConsoleBlFiles and the Linux v1.16 build (tmp/xeBuild64) have it.  No hints at all.

Read off the Linux build: every arm only sets r; the smc, patch-size and signature failures share one
`r = -1` block; after a signature failure the code still reaches `xb.type > 5 && type == 14`, and r is
tested once after the switch.  Axes: the update fallback, the signature block's form and test order, the
tail, r's type, and how case 23's size error leaves.

Replaces src/build.c from loadBl's comment to loadConsoleBlFiles (attempt 8's text, f302f7d)."""
import itertools

FALLBACK = {
    # loadConsoleBlFiles' form
    'con': '''r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
				if (r) {
					if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
				}
				if (!r) {
SE					r = checkBl(e->data, e->size, type, e->crc);
				}
''',
    # the same with the SE test outside
    'con2': '''r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
				if (r) {
					if (type == 9) {
						if (suGetCF(&e->data, &e->size))
							r = 0;
					} else if (type == 10) {
						if (suGetCG(&e->data, &e->size))
							r = 0;
					}
				}
				if (r)
					break;
SE				r = checkBl(e->data, e->size, type, e->crc);
''',
    # flat && forms
    'and': '''r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
				if (r && type == 9 && suGetCF(&e->data, &e->size))
					r = 0;
				if (r && type == 10 && suGetCG(&e->data, &e->size))
					r = 0;
				if (r)
					break;
SE				r = checkBl(e->data, e->size, type, e->crc);
''',
}
SE = '''				if (type == 9 && e->data[0] == 'S' && e->data[1] == 'E') {
					/* an SE where the CF goes */
					e->type = type = 14;
					xb.cfLdv = 0;
					xb.seReplacesCf = 1;
				}
'''
ORDERS = {'5_17_11': 'type == 5 || type == 17 || type == 11', '17_5_11': 'type == 17 || type == 5 || type == 11'}
SIG = {
    # Linux string order: failed, passed, no-key
    'L': '''if (xb.pub1bl) {
					if (!cbVerifySig(e->data, xb.pub1bl)) {
						log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
						r = -1;
					} else
						log_printf(1, "loaded %s, signature check passed!\\n", e->name);
				} else
					log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
''',
    'N': '''if (!xb.pub1bl)
					log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
				else if (!cbVerifySig(e->data, xb.pub1bl)) {
					log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
					r = -1;
				} else
					log_printf(1, "loaded %s, signature check passed!\\n", e->name);
''',
    'P': '''if (xb.pub1bl) {
					if (cbVerifySig(e->data, xb.pub1bl))
						log_printf(1, "loaded %s, signature check passed!\\n", e->name);
					else {
						log_printf(0, "\\n***** ERROR: loaded %s, but signature check failed!\\n", e->name);
						r = -1;
					}
				} else
					log_printf(1, "loaded %s, could not check signature rsa key not present!\\n", e->name);
''',
}
TAIL = {
    'and': '''if (xb.type > BUILD_DEVGL16 && type == 14)
					setFlashBuild(getBeU16(xb.files[i].data + 2));
''',
    'nest': '''if (xb.type > BUILD_DEVGL16) {
					if (type == 14)
						setFlashBuild(getBeU16(xb.files[i].data + 2));
				}
''',
}
# the signature and tail: after checkBl, under `if (!r)` or after `if (r) break;`
GUARD = {
    'nest': 'if (!r) {\nif (ORDER) {\nSIG}\nTAIL}\n',
    'brk': 'if (r)\nbreak;\nif (ORDER) {\nSIG}\nTAIL',
}
SIZE = {
    'else': '''if (e->size & 3) {
					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					r = -1;
				} else
					appendAddonPatches(e);
''',
    'brk': '''if (e->size & 3) {
					log_printf(1, "\\n\\n***** ERROR: patch size 0x%x is not a multiple of 4!\\n", e->size);
					r = -1;
					break;
				}
				appendAddonPatches(e);
''',
}

BODY = '''int loadBlFiles(void)
{
	struct fileent *e;
	uint32_t i;
	RTYPE r;

	for (i = 1; i < (uint32_t)xb.nFiles; i++) {
		e = &xb.files[i];
		r = 0;
		if (strnicmp(e->name, "none", 4) || e->crc) {
			int type = e->type;

			switch (type) {
			case 5: case 7: case 8: case 9: case 10: case 11: case 12: case 13:
			case 14: case 15: case 16: case 17: case 18: case 19: case 20: case 21:
				FALLBACK
				GUARD
				break;
			case 6:
				if (!xb.cbb)
					break;
				r = loadInputFile(e->name, e, 1, 0, NULL, 0, 0, 1);
				if (!r)
					r = checkBl(e->data, e->size, 6, e->crc);
				break;
			case 24:
				if (xb.type == BUILD_JTAG || xb.glitch2mfg) {
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
					r = 0;
					if (loadBaseFile(e->name, e))
						r = defaultBl60(e);
					else if (e->size != 0x60)
						r = defaultBl60(e);
				}
				break;
			case 1:
				if (!loadBinFile(e))
					break;
				log_printf(1, "could not read %s%s, using built in payload (0x%x bytes)\\n", xb.binDir, e->name, 0x200);
				e->data = malloc(0x200);
				if (!e->data) {
					r = 1;
					break;
				}
				e->size = 0x200;
				memcpy(e->data, defPayload, 0x200);
				break;
			case 22:
				if (!loadBinFile(e))
					break;
				log_printf(1, "could not read %s%s, using built in core (0x%x bytes)\\n", xb.binDir, e->name, 0xd40);
				e->data = malloc(0xd40);
				if (!e->data) {
					r = 1;
					break;
				}
				e->size = 0xd40;
				memcpy(e->data, defCore, 0xd40);
				break;
			case 25:
				if (xb.type == BUILD_RETAIL || xb.type > BUILD_DEVGL16)
					break;
				if (!loadBaseFile(e->name, e))
					break;
				log_printf(1, "xell not found in perbuild directory, checking firmware /bin folder\\n");
				if (!loadBinFile(e))
					break;
				log_printf(1, "xell not found in firmware /bin folder, checking base path\\n");
				r = loadLocalFile(e);
				break;
			case 3:
				if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
				    !loadBaseFile("keyvault.bin", &xb.files[xb.nFlashFiles]) ||
				    !(r = loadBaseFile("KV_dec.bin", &xb.files[xb.nFlashFiles]))) {
					if (e->data)
						free(e->data);
					e->data = xb.files[xb.nFlashFiles].data;
					e->size = xb.files[xb.nFlashFiles].size;
					xb.files[xb.nFlashFiles].data = NULL;
					xb.files[xb.nFlashFiles].size = 0;
				} else if (xb.kv.data) {
					log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
					if (e->data)
						free(e->data);
					e->data = xb.kv.data;
					e->size = xb.kv.size;
					xb.kv.data = NULL;
					xb.kv.size = 0;
					r = 0;
				}
				break;
			case 4:
				if (!loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) ||
				    !loadBaseFile("keyvault_alt.bin", &xb.files[xb.nFlashFiles]) ||
				    !(r = loadBaseFile("KV_alt_dec.bin", &xb.files[xb.nFlashFiles]))) {
					if (e->data)
						free(e->data);
					e->data = xb.files[xb.nFlashFiles].data;
					e->size = xb.files[xb.nFlashFiles].size;
					xb.files[xb.nFlashFiles].data = NULL;
					xb.files[xb.nFlashFiles].size = 0;
				} else if (xb.kvAlt.data) {
					log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
					if (e->data)
						free(e->data);
					e->data = xb.kvAlt.data;
					e->size = xb.kvAlt.size;
					xb.kvAlt.data = NULL;
					xb.kvAlt.size = 0;
					r = 0;
				}
				break;
			case 23:
				if (xb.type == BUILD_RETAIL)
					break;
				r = loadBinFile(e);
				if (r)
					break;
				SIZE
				break;
			case 27:
				if (loadBaseFile(e->name, &xb.files[xb.nFlashFiles]) &&
				    loadBaseFile("config.bin", &xb.files[xb.nFlashFiles]) &&
				    (r = loadBaseFile("config_raw.bin", &xb.files[xb.nFlashFiles]))) {
					if (!xb.smcConfig.data)
						break;
					log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
					if (xb.files[xb.nFlashFiles].data)
						free(xb.files[xb.nFlashFiles].data);
					xb.files[xb.nFlashFiles].data = xb.smcConfig.data;
					xb.smcConfig.data = NULL;
					xb.files[xb.nFlashFiles].size = xb.smcConfig.size;
					xb.smcConfig.size = 0;
					r = 0;
				}
				if (xb.files[xb.nFlashFiles].data)
					r = extractSmcConfig(e, xb.files[xb.nFlashFiles].data, xb.files[xb.nFlashFiles].size);
				break;
			case 2:
				r = loadBaseFile(e->name, &xb.files[xb.nFlashFiles]);
				if (!r) {
					if (e->data)
						free(e->data);
					e->data = xb.files[xb.nFlashFiles].data;
					e->size = xb.files[xb.nFlashFiles].size;
					xb.files[xb.nFlashFiles].data = NULL;
					xb.files[xb.nFlashFiles].size = 0;
				} else {
					if (!xb.smc.data)
						break;
					log_printf(1, "reading %s%s failed, using %s from nand dump\\n", xb.baseDir, e->name, e->name);
					if (e->data)
						free(e->data);
					e->data = xb.smc.data;
					e->size = xb.smc.size;
					xb.smc.data = NULL;
					xb.smc.size = 0;
					r = 0;
				}
				e->offset = smcSetLoad(e->size);
				if (!e->offset)
					r = -1;
				break;
			default:
				log_printf(1, "####### unhandled bl load %d %s\\n", type, e->name);
				break;
			}
		}
		if (r) {
			log_printf(0, "\\n\\n**** could not read %s (%i) ****\\n\\n", e->name, r);
			return -1;
		}
	}
	return 0;
}

'''


def make(base, fb, order, sig, tail, guard, size, rtype):
    i = base.index('/* load the input file e (xb.files[i]) by its type */')
    j = base.index('int loadConsoleBlFiles(void)')
    g = GUARD[guard].replace('ORDER', ORDERS[order]).replace('SIG', SIG[sig]).replace('TAIL', TAIL[tail])
    f = FALLBACK[fb].replace('SE', SE)
    body = BODY.replace('FALLBACK', f).replace('GUARD', g).replace('SIZE', SIZE[size]).replace('RTYPE', rtype)
    return base[:i] + body + base[j:]


AXES = dict(fb=list(FALLBACK), order=list(ORDERS), sig=list(SIG), tail=list(TAIL), guard=list(GUARD),
            size=list(SIZE), rtype=['uint32_t', 'int'])


def CASES(base):
    out = []
    keys = list(AXES)
    for combo in itertools.product(*[AXES[k] for k in keys]):
        kw = dict(zip(keys, combo))
        out.append((' '.join(combo), lambda b, kw=kw: make(b, **kw)))
    return out


FOCUS = ['_loadBlFiles']
