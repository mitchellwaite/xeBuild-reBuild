"""Attempt 70: exp_devgl by attempt 69's r-class initFlash helper, closing the SSA-numbering tie
(the findFile loops' compare operand order).
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a70_dev.py -p 0 -o "-" [-f label] [-k label]"""
OLD = '''	memset(salt, 0, sizeof(salt));
	fuse = 1;
	if (xb.type != BUILD_JTAG) {
		fuse = xb.glitch2mfg != 0;
		if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))
			fuse = 1;
	}
'''
DEV = 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'
ANCHOR = '/* no blmod.bin: the console\'s, if any */'
RBODY = ('\tint fuse = 1;\n\n\tmemset(salt, 0, 16);\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n'
         '\t\tif (%s)\n\t\t\treturn 1;\n\t}\n\treturn fuse != 0;\n' % DEV)
PROTO = 'static int initFlash(uint8_t *salt)'
CALL = '\tfuse = initFlash(salt);\n'


def helper(call=CALL, proto=PROTO, body=RBODY, extra=()):
    def f(t):
        if OLD not in t:
            raise ValueError('old')
        t = t.replace(OLD, call, 1)
        t = t.replace(ANCHOR, proto + '\n{\n' + body + '}\n\n' + ANCHOR, 1)
        for e in extra:
            a, b = e[0], e[1]
            if a not in t:
                raise ValueError('not found %r' % a[:60])
            t = t.replace(a, b, 1)
        return t
    return f


V = {'r': helper()}

# sweep 1: `found` (whose PHIs take the low versions ch2 hands to loop A's nFiles copy) declared elsewhere
DECLS = '''	uint32_t area, off, raw, save, a, b, k, crc, len, end;
	int fuse, blocks, r, cf, cg, region, i;
'''
FOUNDL = '\t\tint found = 1;\n\n\t\tmemset(&xb.files[xb.nFlashFiles], 0, sizeof(struct fileent));\n'
FOUNDN = '\t\tfound = 1;\n\t\tmemset(&xb.files[xb.nFlashFiles], 0, sizeof(struct fileent));\n'
INTS = ['fuse', 'blocks', 'r', 'cf', 'cg', 'region', 'i']
for pos in range(len(INTS) + 1):
    for ty in ('int', 'BOOL'):
        if ty == 'int':
            l = INTS[:pos] + ['found'] + INTS[pos:]
            d = DECLS.replace('int fuse, blocks, r, cf, cg, region, i;', 'int %s;' % ', '.join(l))
        else:
            d = DECLS.replace('int fuse, blocks, r, cf, cg, region, i;\n', 'int %s;\n\tBOOL found;\n' % ', '.join(INTS)) if pos == 0 else None
        if d is None:
            continue
        V['s1_%s_%d' % (ty, pos)] = helper(extra=[(DECLS, d), (FOUNDL, FOUNDN)])
        if pos == 0:
            V['s1src_%s' % ty] = [(DECLS, d), (FOUNDL, FOUNDN)]
V['s1_first'] = helper(extra=[(DECLS, '\tint found;\n' + DECLS), (FOUNDL, FOUNDN)])
V['s1_u32'] = helper(extra=[(DECLS, DECLS.replace('end;', 'end, found;')), (FOUNDL, FOUNDN)])
V['s1_lbool'] = helper(extra=[(FOUNDL, FOUNDL.replace('int found', 'BOOL found'))])
V['s1_lu32'] = helper(extra=[(FOUNDL, FOUNDL.replace('int found', 'uint32_t found'))])

# sweep 2 (diagnostic): return expressions that leave different numbers of VRP-made copies
RET = '\treturn fuse != 0;\n'
for k, e in {'eq1': '(fuse != 0) == 1', 'nn': '!(fuse == 0)', 'and1': 'fuse & 1', 'teq1': 'fuse == 1 ? 1 : 0',
             'gt': 'fuse > 0', 'tf': 'fuse > 0 ? fuse : 0', 'ucmp': '(unsigned)fuse != 0', 'min': 'fuse < 1 ? fuse : 1',
             'dbl': '!!(fuse != 0)', 'eq0': '(fuse == 0) == 0', 'tt': 'fuse ? fuse : 0', 'sub': '1 - (fuse == 0)'}.items():
    V['s2_' + k] = helper(body=RBODY.replace(RET, '\treturn %s;\n' % e))

# sweep 3: buildFlash's fuse type x helper return type x return expression (one fewer statement left after vrp1)
D3 = 'int fuse, blocks, r, cf, cg, region, i;'
for ct in ('int', '_Bool', 'BOOL', 'char', 'uint8_t', 'unsigned'):
    for rt in ('int', '_Bool', 'BOOL'):
        for rk, re_ in (('ne', 'fuse != 0'), ('pl', 'fuse')):
            for lt in ('int', '_Bool'):
                b = RBODY.replace(RET, '\treturn %s;\n' % re_).replace('\tint fuse = 1;', '\t%s fuse = 1;' % lt)
                ex = [] if ct == 'int' else [(D3, 'int blocks, r, cf, cg, region, i;\n\t%s fuse;' % ct)]
                V['s3_%s_%s_%s_%s' % (ct, rt, lt, rk)] = helper(proto='static %s initFlash(uint8_t *salt)' % rt, body=b, extra=ex)

# sweep 4: single-statement int return expressions (attempt 70's lever: one statement fewer than `!= 0`'s
# compare + conversion left after vrp1)
E4 = {'and1': 'fuse & 1', 'and1p': '(fuse & 1)', 'max0': 'fuse > 0 ? fuse : 0', 'max0b': 'fuse < 0 ? 0 : fuse',
      'min1': 'fuse < 1 ? fuse : 1', 'min1b': 'fuse > 1 ? 1 : fuse', 'min1c': 'fuse >= 1 ? 1 : fuse',
      'or0': 'fuse | 0', 'xor0': 'fuse ^ 0', 'mul': 'fuse * 1', 'mod2': 'fuse % 2', 'shr': 'fuse >> 0',
      'gt1': 'fuse > 0 ? 1 : 0', 'ge1': 'fuse >= 1', 't1f': 'fuse ? 1 : fuse', 'abs': 'abs(fuse)',
      'neg2': '-(-fuse)', 'andm': 'fuse & ~0', 'and1u': 'fuse & 1u', 'notnot_and': '!!fuse & 1',
      'sub0': 'fuse - 0', 'min1d': 'fuse <= 1 ? fuse : 1', 'max0c': 'fuse >= 0 ? fuse : 0'}
for k, e in E4.items():
    V['s4_' + k] = helper(body=RBODY.replace(RET, '\treturn %s;\n' % e))
    # the same with the value kept in fuse first
    V['s4v_' + k] = helper(body=RBODY.replace(RET, '\tfuse = %s;\n\treturn fuse;\n' % e))

# sweep 5: statement forms of the clamp
for k, e in {'ifmin': '\tif (fuse > 1)\n\t\tfuse = 1;\n\treturn fuse;\n', 'ifmax': '\tif (fuse < 0)\n\t\tfuse = 0;\n\treturn fuse;\n',
             'andeq': '\tfuse &= 1;\n\treturn fuse;\n'}.items():
    V['s5_' + k] = helper(body=RBODY.replace(RET, e))
