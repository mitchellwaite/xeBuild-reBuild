"""checkHeader: the SysUpdateAddr test without the empty asm."""
FOCUS = ['_checkHeader']
OLD = '''	if (size < SWAP32(hdr.sysUpdateAddr))
		goto badSysUpdate;
	__asm__("");
	if (SWAP32(hdr.cfOffset) > SWAP32(hdr.sysUpdateAddr)) {
badSysUpdate:
		log_printf(0, "******* ERROR loading '%s', flash header SysUpdateAddr is malformed\\n", name);
		return 0;
	}
'''
M = '''log_printf(0, "******* ERROR loading '%s', flash header SysUpdateAddr is malformed\\n", name);
		return 0;
'''
SU = 'SWAP32(hdr.sysUpdateAddr)'
CF = 'SWAP32(hdr.cfOffset)'
SH = {
    'or': f'if (size < {SU} || {CF} > {SU}) {{\n{M}}}\n',
    'rev': f'if ({CF} > {SU} || size < {SU}) {{\n{M}}}\n',
    'rev2': f'if ({SU} < {CF} || size < {SU}) {{\n{M}}}\n',
    'rev3': f'if ({SU} < {CF} || {SU} > size) {{\n{M}}}\n',
    'or2': f'if ({SU} > size || {SU} < {CF}) {{\n{M}}}\n',
    'and': f'if (size >= {SU} && {CF} <= {SU}) {{\n}} else {{\n{M}}}\n',
    'and2': f'if ({CF} <= {SU} && size >= {SU}) {{\n}} else {{\n{M}}}\n',
    'two': f'if (size < {SU}) {{\n{M}}}\nif ({CF} > {SU}) {{\n{M}}}\n',
    'two2': f'if ({CF} > {SU}) {{\n{M}}}\nif (size < {SU}) {{\n{M}}}\n',
    'nest': f'if (size >= {SU}) {{\nif ({CF} > {SU}) {{\n{M}}}\n}} else {{\n{M}}}\n',
    'nest2': f'if (size < {SU}) {{\n{M}}} else if ({CF} > {SU}) {{\n{M}}}\n',
    'var': f'{{\nuint32_t su = {SU};\nif (size < su || {CF} > su) {{\n{M}}}\n}}\n',
    'var2': f'{{\nuint32_t su = {SU};\nif ({CF} > su || size < su) {{\n{M}}}\n}}\n',
    'var3': f'{{\nuint32_t su = {SU};\nuint32_t cf = {CF};\nif (size < su || cf > su) {{\n{M}}}\n}}\n',
    'var4': f'{{\nuint32_t cf = {CF};\nuint32_t su = {SU};\nif (size < su || cf > su) {{\n{M}}}\n}}\n',
    'var5': f'{{\nuint32_t cf = {CF};\nuint32_t su = {SU};\nif (cf > su || size < su) {{\n{M}}}\n}}\n',
    'll': f'if (size < (long long){SU} || {CF} > {SU}) {{\n{M}}}\n',
}
AXES = [[(k, [(OLD, v)]) for k, v in SH.items()]]
