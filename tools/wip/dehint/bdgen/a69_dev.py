"""Attempt 69: exp_devgl by fuse helpers (IPA- or early-inlined) and fuse-decision shapes, no expect.
python tools/wip/dehint/bdgen/a60lib.py tools/wip/dehint/bdgen/a69_dev.py -p 0 -o "-" [-f label] [-k label]"""
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


def helper(call, proto, body):
    def f(t):
        if OLD not in t:
            raise ValueError('old')
        t = t.replace(OLD, call, 1)
        return t.replace(ANCHOR, proto + '\n{\n' + body + '}\n\n' + ANCHOR, 1)
    return f


def inline(new):
    return [(OLD, new)]


B = {}
B['dret2'] = ('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)',
    '\tint fuse = 1;\n\n\tmemset(salt, 0, 16);\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (%s)\n\t\t\treturn 1;\n\t}\n\treturn fuse;\n' % DEV)
B['dret'] = ('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)',
    '\tint fuse;\n\n\tmemset(salt, 0, 16);\n\tif (xb.type == BUILD_JTAG)\n\t\treturn 1;\n\tfuse = xb.glitch2mfg != 0;\n\tif (%s)\n\t\treturn 1;\n\treturn fuse;\n' % DEV)
V = {k: helper(*v) for k, v in B.items()}

# helper bodies with the salt memset (IPA-inlined: one call), dev arm spellings (sweep 2)
MS = '\tmemset(salt, 0, 16);\n'
H2 = {
 'r_ndev': '\tint fuse;\n\n' + MS + '\tif (xb.type == BUILD_JTAG)\n\t\treturn 1;\n\tfuse = xb.glitch2mfg != 0;\n\tif (!(%s))\n\t\treturn fuse;\n\treturn 1;\n' % DEV,
 'r_tern': '\tint fuse;\n\n' + MS + '\tif (xb.type == BUILD_JTAG)\n\t\treturn 1;\n\tfuse = xb.glitch2mfg != 0;\n\treturn %s ? 1 : fuse;\n' % DEV.replace('xb', '(xb', 1).replace('DEVGL16', 'DEVGL16)'),
 'r_flag1': '\tint fuse = 1;\n\n' + MS + '\tif (xb.type == BUILD_JTAG)\n\t\treturn fuse;\n\tfuse = xb.glitch2mfg != 0;\n\tif (%s)\n\t\tfuse = 1;\n\treturn fuse;\n' % DEV,
 'r_jt1': '\tint fuse;\n\n' + MS + '\tif (xb.type == BUILD_JTAG)\n\t\treturn 1;\n\tfuse = xb.glitch2mfg != 0;\n\tif (%s)\n\t\tfuse = 1;\n\treturn fuse;\n' % DEV,
 'r_nj': '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (!(%s))\n\t\t\treturn fuse;\n\t\treturn 1;\n\t}\n\treturn fuse;\n' % DEV,
 'r_nj2': '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (%s)\n\t\t\treturn 1;\n\t\treturn fuse;\n\t}\n\treturn fuse;\n' % DEV,
 'r_nj3': '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (%s)\n\t\t\tfuse = 1;\n\t}\n\treturn fuse;\n' % DEV,
 'r_bool': '\tBOOL fuse = TRUE;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (%s)\n\t\t\treturn TRUE;\n\t}\n\treturn fuse;\n' % DEV,
}
for k, b in H2.items():
    V[k] = helper('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)', b)

# sweep 3: helper return type (the inlined return block keeps a conversion, attempt 68's lever)
for rt in ('BOOL', 'uint8_t', 'uint32_t', 'unsigned', 'char', 'short', 'uint16_t', '_Bool', 'long'):
    for k in ('dret2', 'r_ndev', 'r_nj2', 'r_nj3'):
        body = B[k][2] if k in B else H2[k]
        V['rt_%s_%s' % (rt, k)] = helper('\tfuse = initFlash(salt);\n', 'static %s initFlash(uint8_t *salt)' % rt, body)

# sweep 4: the caller's conversion of the helper's result
for k in ('dret2', 'dret', 'r_ndev', 'r_nj2'):
    body = B[k][2] if k in B else H2[k]
    V['c_ne_' + k] = helper('\tfuse = initFlash(salt) != 0;\n', 'static int initFlash(uint8_t *salt)', body)
    V['c_nn_' + k] = helper('\tfuse = !!initFlash(salt);\n', 'static int initFlash(uint8_t *salt)', body)
    V['c_bne_' + k] = helper('\tfuse = initFlash(salt) != 0;\n', 'static _Bool initFlash(uint8_t *salt)', body)
    V['c_bb_' + k] = helper('\tfuse = initFlash(salt);\n', 'static _Bool initFlash(uint8_t *salt)', body.replace('int fuse', '_Bool fuse'))
    V['c_bi_' + k] = helper('\tfuse = initFlash(salt);\n', 'static _Bool initFlash(uint8_t *salt)', body)

# sweep 5: helper local type x return type x body (the return block's conversion keeps the JTAG edge off
# the early-return rule; find the typing that keeps the zero-extension on the setne)
TY = ('int', 'unsigned', '_Bool', 'uint8_t', 'uint32_t', 'BOOL', 'char', 'long', 'short')
for lt in TY:
    for rt in TY:
        for k in ('dret2', 'dret', 'r_nj2', 'r_ndev'):
            body = B[k][2] if k in B else H2[k]
            V['t_%s_%s_%s' % (lt, rt, k)] = helper('\tfuse = initFlash(salt);\n', 'static %s initFlash(uint8_t *salt)' % rt,
                                                   body.replace('\tint fuse', '\t%s fuse' % lt))

# sweep 6: int / _Bool helpers whose JTAG return carries an expression (dret2 shape)
D2 = '\t%s fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ')\n\t\t\treturn %s;\n\t}\n\treturn %s;\n'
for rt in ('int', '_Bool', 'BOOL'):
    for lt in ('int', '_Bool', 'BOOL', 'uint8_t', 'unsigned'):
        for one in ('1', 'TRUE'):
            for ret in ('fuse', 'fuse != 0', '!!fuse', 'fuse ? 1 : 0', '(%s)fuse' % rt):
                lab = 'e_%s_%s_%s_%s' % (rt, lt, one, ret.replace(' ', '').replace('!', 'n').replace('?', 'q').replace(':', 'c').replace('(', '').replace(')', '_'))
                V[lab] = helper('\tfuse = initFlash(salt);\n', 'static %s initFlash(uint8_t *salt)' % rt, D2 % (lt, one, ret))
    # caller forms with a _Bool / BOOL / int result
    for cf in ('\tfuse = initFlash(salt);\n', '\tfuse = initFlash(salt) != 0;\n', '\tfuse = initFlash(salt) ? 1 : 0;\n'):
        V['cf_%s_%d' % (rt, len(cf))] = helper(cf, 'static %s initFlash(uint8_t *salt)' % rt, D2 % ('int', '1', 'fuse'))

# sweep 7: the local holds the raw glitch2mfg value, the end tests it
G = '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg;\n\t\tif (' + DEV + ')\n\t\t\treturn 1;\n\t}\n\treturn %s;\n'
for ret in ('fuse != 0', '!!fuse', 'fuse ? 1 : 0'):
    for rt in ('int', 'BOOL', '_Bool'):
        V['g_%s_%d' % (rt, len(ret))] = helper('\tfuse = initFlash(salt);\n', 'static %s initFlash(uint8_t *salt)' % rt, G % ret)
V['g_bool_plain'] = helper('\tfuse = initFlash(salt);\n', 'static _Bool initFlash(uint8_t *salt)', G % 'fuse')

# sweep 8: SSA-numbering spellings of the 2/2 form (e_int_int_1_fusen=0)
def S8(body, call='\tfuse = initFlash(salt);\n', proto='static int initFlash(uint8_t *salt)'):
    return helper(call, proto, body)
R8 = ['fuse != 0', '!!fuse', 'fuse ? 1 : 0', 'fuse > 0', 'fuse == 1', '(fuse != 0)']
DEVS = [DEV, 'xb.type >= BUILD_DEVGL && xb.type <= BUILD_DEVGL16', 'xb.type == BUILD_DEVGL16 || xb.type == BUILD_DEVGL']
GL = ['xb.glitch2mfg != 0', '!!xb.glitch2mfg', 'xb.glitch2mfg ? 1 : 0']
n = 0
for r in R8:
    for d in DEVS:
        for g in GL:
            for form in range(4):
                if form == 0:
                    b = '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = %s;\n\t\tif (%s)\n\t\t\treturn 1;\n\t}\n\treturn %s;\n' % (g, d, r)
                elif form == 1:
                    b = '\tint fuse;\n\n' + MS + '\tfuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = %s;\n\t\tif (%s)\n\t\t\treturn 1;\n\t}\n\treturn %s;\n' % (g, d, r)
                elif form == 2:
                    b = '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tif (%s)\n\t\t\treturn 1;\n\t\tfuse = %s;\n\t}\n\treturn %s;\n' % (d, g, r)
                else:
                    b = MS.replace('\t', '\tint fuse = 1;\n\n\t', 1) + '\tif (xb.type == BUILD_JTAG)\n\t\tfuse = 1;\n\telse {\n\t\tfuse = %s;\n\t\tif (%s)\n\t\t\treturn 1;\n\t}\n\treturn %s;\n' % (g, d, r)
                V['s8_%d' % n] = S8(b); n += 1

# sweep 9: call / prototype spellings of the 2/2 form (the call's lhs is released by the inline and reused)
B9 = '\tint fuse = 1;\n\n\tmemset(%s, 0, %s);\n\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ')\n\t\t\treturn 1;\n\t}\n\treturn fuse != 0;\n'
n = 0
for proto in ('static int initFlash(uint8_t *salt)', 'static int initFlash(uint8_t salt[16])', 'static int initFlash(void *salt)',
              'static BOOL initFlash(uint8_t *salt)', 'static int initFlash(uint8_t *salt, int len)'):
    for ms in (('salt', '16'), ('salt', '16 * sizeof(*salt)')):
        for call in ('\tfuse = initFlash(salt);\n', '\tfuse = initFlash(&salt[0]);\n', '\tfuse = initFlash(salt) != 0;\n'):
            if 'len' in proto:
                call = call.replace('salt)', 'salt, sizeof(salt))').replace('[0])', '[0], sizeof(salt))')
                ms2 = ('salt', 'len')
            else:
                ms2 = ms
            V['s9_%d' % n] = helper(call, proto, B9 % ms2); n += 1

# sweep 10: caller forms that keep a fuse PHI in buildFlash's early body (the 2/2's one SSA name)
B10 = B9 % ('salt', '16')
for i, call in enumerate(('\tfuse = initFlash(salt) ? 1 : 0;\n', '\tif (initFlash(salt))\n\t\tfuse = 1;\n\telse\n\t\tfuse = 0;\n',
             '\tfuse = 0;\n\tif (initFlash(salt))\n\t\tfuse = 1;\n', '\tfuse = 1;\n\tif (!initFlash(salt))\n\t\tfuse = 0;\n',
             '\tfuse = !!initFlash(salt);\n', '\tfuse = initFlash(salt) == 1;\n')):
    V['s10_%d' % i] = helper(call, 'static int initFlash(uint8_t *salt)', B10)
    V['s10b_%d' % i] = helper(call, 'static int initFlash(uint8_t *salt)', B10.replace('return fuse != 0;', 'return fuse;'))
    V['s10c_%d' % i] = helper(call, 'static _Bool initFlash(uint8_t *salt)', B10.replace('return fuse != 0;', 'return fuse;'))

# sweep 11: buildFlash's fuse type with the _Bool helper
DECL = '\tint fuse, blocks, r, cf, cg, region, i;\n'
for ft in ('_Bool', 'uint8_t', 'unsigned', 'BOOL', 'uint32_t'):
    for rt in ('_Bool', 'int'):
        for k, body in (('pl', B10.replace('return fuse != 0;', 'return fuse;')), ('ne', B10)):
            f0 = helper('\tfuse = initFlash(salt);\n', 'static %s initFlash(uint8_t *salt)' % rt, body)
            V['s11_%s_%s_%s' % (ft, rt, k)] = (lambda f0, ft: lambda t: f0(t).replace(DECL, '\tint blocks, r, cf, cg, region, i;\n\t%s fuse;\n' % ft, 1))(f0, ft)

# sweep 12: the 2/2 form plus spellings of the fuse block / showFuses call (SSA numbering of the findFile(24) loop)
FB = '''	if (fuse) {
		struct fileent *e = &xb.files[findFile(24)];
		setFuseCpuKey(e->data);
		if (xb.type != BUILD_JTAG)
			e->offset = imgCfOffset() + imgCfSize();
	}
'''
FBS = {
 'i': '\tif (fuse) {\n\t\ti = findFile(24);\n\t\tsetFuseCpuKey(xb.files[i].data);\n\t\tif (xb.type != BUILD_JTAG)\n\t\t\txb.files[i].offset = imgCfOffset() + imgCfSize();\n\t}\n',
 'plus': FB.replace('&xb.files[findFile(24)]', 'xb.files + findFile(24)'),
 'eout': FB.replace('\t\tstruct fileent *e = &xb.files[findFile(24)];\n', '\t\te = &xb.files[findFile(24)];\n'),
 'idx': FB.replace('\t\tstruct fileent *e = &xb.files[findFile(24)];\n', '\t\tint n = findFile(24);\n\t\tstruct fileent *e = &xb.files[n];\n'),
}
SF = '\tif (fuse)\n\t\tshowFuses(1, "\nVirtual Fuses set to:", xb.files[findFile(24)].data);\n'
SFS = {'-': SF, 'e': SF.replace('xb.files[findFile(24)].data', '&xb.files[findFile(24)]->data')}
NE0 = V['e_int_int_1_fusen=0']
for fk, fb in FBS.items():
    def f(t, fb=fb, fk=fk):
        t = NE0(t)
        assert FB in t
        t = t.replace(FB, fb, 1)
        if fk == 'eout':
            t = t.replace('\tuint16_t t;\n\tchar last;\n', '\tuint16_t t;\n\tchar last;\n\tstruct fileent *e;\n', 1)
        return t
    V['s12_' + fk] = f

# sweep 13: out-parameter forms
P13 = {
 'op1': '\t*fuse = 1;\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\t*fuse = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ')\n\t\t\t*fuse = 1;\n\t}\n',
 'op2': MS + '\t*fuse = 1;\n\tif (xb.type == BUILD_JTAG)\n\t\treturn;\n\t*fuse = xb.glitch2mfg != 0;\n\tif (' + DEV + ')\n\t\t*fuse = 1;\n',
 'op3': '\tint f = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tf = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ') {\n\t\t\t*fuse = 1;\n\t\t\treturn;\n\t\t}\n\t}\n\t*fuse = f;\n',
}
for k, b in P13.items():
    V['s13_' + k] = helper('\tinitFlash(salt, &fuse);\n', 'static void initFlash(uint8_t *salt, int *fuse)', b)

# sweep 14: op3 relatives (out-parameter stored in the return block, dev arm stores 1 and returns)
n = 0
for lt in ('int', 'BOOL', 'unsigned', '_Bool'):
    for init in ('decl', 'after', 'before'):
        for g in ('xb.glitch2mfg != 0', '!!xb.glitch2mfg'):
            for one in ('1', 'TRUE'):
                for order in ('sf', 'fs'):
                    head = '\t%s f%s;\n\n' % (lt, ' = 1' if init == 'decl' else '')
                    if init == 'before':
                        head += '\tf = 1;\n' + MS
                    elif init == 'after':
                        head += MS + '\tf = 1;\n'
                    else:
                        head += MS
                    b = head + '\tif (xb.type != BUILD_JTAG) {\n\t\tf = %s;\n\t\tif (%s) {\n\t\t\t*fuse = %s;\n\t\t\treturn;\n\t\t}\n\t}\n\t*fuse = f;\n' % (g, DEV, one)
                    if order == 'sf':
                        V['s14_%d' % n] = helper('\tinitFlash(salt, &fuse);\n', 'static void initFlash(uint8_t *salt, int *fuse)', b)
                    else:
                        V['s14_%d' % n] = helper('\tinitFlash(&fuse, salt);\n', 'static void initFlash(int *fuse, uint8_t *salt)', b)
                    n += 1

# sweep 15: wider structural variety for the SSA ties (ret-value and out-parameter classes)
S15 = {}
S15['op_ret'] = ('\tinitFlash(salt, &fuse);\n', 'static void initFlash(uint8_t *salt, int *fuse)',
    MS + '\t*fuse = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tint f = xb.glitch2mfg != 0;\n\n\t\tif (' + DEV + ')\n\t\t\treturn;\n\t\t*fuse = f;\n\t}\n')
S15['op_ret2'] = ('\tinitFlash(salt, &fuse);\n', 'static void initFlash(uint8_t *salt, int *fuse)',
    '\tint f;\n\n' + MS + '\tf = 1;\n\tif (xb.type != BUILD_JTAG) {\n\t\tf = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ')\n\t\t\tf = 1;\n\t}\n\t*fuse = f;\n')
S15['op_int'] = ('\tif (initFlash(salt, &fuse))\n\t\tfuse = 1;\n', 'static int initFlash(uint8_t *salt, int *fuse)',
    MS + '\t*fuse = 1;\n\tif (xb.type == BUILD_JTAG)\n\t\treturn 0;\n\t*fuse = xb.glitch2mfg != 0;\n\treturn ' + DEV + ';\n')
S15['ret_dev'] = ('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)',
    '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ')\n\t\t\tfuse = 1;\n\t\telse\n\t\t\treturn fuse != 0;\n\t}\n\treturn fuse;\n')
S15['ret_goto'] = ('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)',
    '\tint fuse = 1;\n\n' + MS + '\tif (xb.type != BUILD_JTAG) {\n\t\tfuse = xb.glitch2mfg != 0;\n\t\tif (' + DEV + ')\n\t\t\treturn 1;\n\t}\n\treturn fuse ? 1 : 0;\n')
S15['ret_two'] = ('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)',
    MS + '\tif (xb.type == BUILD_JTAG)\n\t\tgoto used;\n\tif (' + DEV + ' || xb.glitch2mfg)\n\t\tgoto used;\n\treturn 0;\nused:\n\treturn 1;\n')
for k, v in S15.items():
    V['s15_' + k] = helper(*v)

# sweep 16: parts generator for the two tie classes (ret-value 'r', out-parameter 'o')
n = 0
for cls in ('r', 'o'):
    for tl in (0, 1, 2):
        for g in ('xb.glitch2mfg != 0', 'xb.glitch2mfg ? 1 : 0'):
            for dv in (0, 1, 2):
                T = 't' if tl else 'xb.type'
                d = ('%s == BUILD_DEVGL || %s == BUILD_DEVGL16' % (T, T), '%s >= BUILD_DEVGL && %s <= BUILD_DEVGL16' % (T, T),
                     '%s == BUILD_DEVGL16 || %s == BUILD_DEVGL' % (T, T))[dv]
                loc = 'fuse' if cls == 'r' else 'f'
                b = '\tint %s = 1;\n' % loc
                if tl == 1:
                    b += '\tint t = xb.type;\n'
                b += '\n' + MS
                if tl == 2:
                    b = b.replace('\n' + MS, '\tint t;\n\n' + MS + '\tt = xb.type;\n')
                b += '\tif (%s != BUILD_JTAG) {\n\t\t%s = %s;\n\t\tif (%s)\n' % (T, loc, g, d)
                if cls == 'r':
                    b += '\t\t\treturn 1;\n\t}\n\treturn fuse != 0;\n'
                    V['s16_%d' % n] = helper('\tfuse = initFlash(salt);\n', 'static int initFlash(uint8_t *salt)', b)
                else:
                    b += '\t\t{\n\t\t\t*fuse = 1;\n\t\t\treturn;\n\t\t}\n\t}\n\t*fuse = f;\n'
                    b = b.replace('\t\tif (%s)\n\t\t{' % d, '\t\tif (%s) {' % d)
                    V['s16_%d' % n] = helper('\tinitFlash(salt, &fuse);\n', 'static void initFlash(uint8_t *salt, int *fuse)', b)
                n += 1

# sweep 17: the helper takes the build type (and glitch2mfg) as parameters: more early names in buildFlash
for cls in ('r', 'o', 'b'):
    for ps in ('t', 'tg', 'gt'):
        T = 'type'
        G = 'glitch2mfg' if 'g' in ps else 'xb.glitch2mfg'
        loc = 'f' if cls == 'o' else 'fuse'
        b = '\tint %s = 1;\n\n' % loc + MS + '\tif (type != BUILD_JTAG) {\n\t\t%s = %s != 0;\n\t\tif (type == BUILD_DEVGL || type == BUILD_DEVGL16)\n' % (loc, G)
        if cls == 'o':
            b += '\t\t{\n\t\t\t*fuse = 1;\n\t\t\treturn;\n\t\t}\n\t}\n\t*fuse = f;\n'
            b = b.replace('BUILD_DEVGL16)\n\t\t{', 'BUILD_DEVGL16) {')
        else:
            b += '\t\t\treturn 1;\n\t}\n\treturn fuse%s;\n' % (' != 0' if cls == 'r' else '')
        args = {'t': ('int type', 'xb.type'), 'tg': ('int type, int glitch2mfg', 'xb.type, xb.glitch2mfg'),
                'gt': ('int glitch2mfg, int type', 'xb.glitch2mfg, xb.type')}[ps]
        rt = {'r': 'int', 'o': 'void', 'b': '_Bool'}[cls]
        if cls == 'o':
            call = '\tinitFlash(salt, %s, &fuse);\n' % args[1]; proto = 'static void initFlash(uint8_t *salt, %s, int *fuse)' % args[0]
        else:
            call = '\tfuse = initFlash(salt, %s);\n' % args[1]; proto = 'static %s initFlash(uint8_t *salt, %s)' % (rt, args[0])
        V['s17_%s_%s' % (cls, ps)] = helper(call, proto, b)

# sweep 18: product of parameter shapes x class
def body18(cls, T, jt):
    loc = 'f' if cls == 'o' else 'fuse'
    cond = '!jtag' if jt else '%s != BUILD_JTAG' % T
    b = '\tint %s = 1;\n\n' % loc + MS + '\tif (%s) {\n\t\t%s = xb.glitch2mfg != 0;\n\t\tif (%s == BUILD_DEVGL || %s == BUILD_DEVGL16)' % (cond, loc, T, T)
    if cls == 'o':
        b += ' {\n\t\t\t*fuse = 1;\n\t\t\treturn;\n\t\t}\n\t}\n\t*fuse = f;\n'
    else:
        b += '\n\t\t\treturn 1;\n\t}\n\treturn fuse != 0;\n'
    return b
n = 0
for cls in ('r', 'o'):
    for ps in ('s', 'st', 'ts', 'sj', 'stu', 'sT'):
        T = 'xb.type' if ps in ('s', 'sj') else 'type'
        jt = ps == 'sj'
        plist, alist = ['uint8_t *salt'], ['salt']
        if ps in ('st', 'sT'):
            plist.append('int type' if ps == 'st' else 'enum_type'); alist.append('xb.type')
        if ps == 'stu':
            plist.append('uint32_t type'); alist.append('xb.type')
        if ps == 'ts':
            plist.insert(0, 'int type'); alist.insert(0, 'xb.type')
        if ps == 'sj':
            plist.append('int jtag'); alist.append('xb.type == BUILD_JTAG')
        if ps == 'sT':
            plist[-1] = 'unsigned type'
        if cls == 'o':
            plist.append('int *fuse'); alist.append('&fuse')
            call = '\tinitFlash(%s);\n' % ', '.join(alist); proto = 'static void initFlash(%s)' % ', '.join(plist)
        else:
            call = '\tfuse = initFlash(%s);\n' % ', '.join(alist); proto = 'static int initFlash(%s)' % ', '.join(plist)
        V['s18_%s_%s' % (cls, ps)] = helper(call, proto, body18(cls, T, jt))

# sweep 19: fuse's declaration position (DECL_UID order: into-SSA / update_address_taken numbering)
LOCS = '''	uint8_t salt[16];
	uint32_t ts;
	FILETIME ft;
	const char *name, *base;
	uint32_t area, off, raw, save, a, b, k, crc, len, end;
	int fuse, blocks, r, cf, cg, region, i;
	uint16_t t;
	char last;
'''
def mvdecl(pos):
    L = LOCS.replace('int fuse, blocks', 'int blocks')
    lines = L.split('\n')
    lines.insert(pos, '\tint fuse;')
    return '\n'.join(lines)
BASES = {'r': V['s18_r_s'], 'o': V['s18_o_s'], 'rst': V['s18_r_st'], 'ost': V['s18_o_st'], 'osj': V['s18_o_sj'], 'rsj': V['s18_r_sj']}
for bk, bf in BASES.items():
    for pos in range(0, 9):
        V['s19_%s_%d' % (bk, pos)] = (lambda bf, pos: lambda t: bf(t).replace(LOCS, mvdecl(pos), 1))(bf, pos)
    V['s19_%s_x' % bk] = (lambda bf: lambda t: bf(t).replace(LOCS, LOCS.replace('int fuse, blocks, r, cf, cg, region, i;', 'int blocks, r, cf, cg, region, i, fuse;'), 1))(bf)

# sweep 20: parameter combinations (salt, len, type) in every order, both classes
import itertools
PDEF = {'salt': ('uint8_t *salt', 'salt'), 'len': ('int len', 'sizeof(salt)'), 'type': ('int type', 'xb.type'), 'fuse': ('int *fuse', '&fuse')}
def body20(cls, T, lenp):
    b = body18(cls, T, False)
    if lenp:
        b = b.replace('memset(salt, 0, 16)', 'memset(salt, 0, len)')
    return b
for cls in ('r', 'o'):
    for extra in ((), ('len',), ('type',), ('len', 'type')):
        ps = ('salt',) + extra + (('fuse',) if cls == 'o' else ())
        for perm in itertools.permutations(ps):
            if perm[0] != 'salt' and len(ps) > 3:
                continue
            T = 'type' if 'type' in ps else 'xb.type'
            plist = ', '.join(PDEF[p][0] for p in perm); alist = ', '.join(PDEF[p][1] for p in perm)
            if cls == 'o':
                call = '\tinitFlash(%s);\n' % alist; proto = 'static void initFlash(%s)' % plist
            else:
                call = '\tfuse = initFlash(%s);\n' % alist; proto = 'static int initFlash(%s)' % plist
            V['s20_%s_%s' % (cls, '-'.join(perm))] = helper(call, proto, body20(cls, T, 'len' in ps))

# sweep 21: the 2/2 and op3 forms on attempt 65's buildFlash restructurings (equal base 'ld', others)
import importlib.util as _ilu, os as _os
_s = _ilu.spec_from_file_location('a65', _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'a65_bf.py'))
A65 = _ilu.module_from_spec(_s); _s.loader.exec_module(A65)
def _ap(t, v):
    for e in v:
        assert e[0] in t, e[0][:60]
        t = t.replace(e[0], e[1], 1)
    return t
for k65, v65 in A65.V.items():
    if not isinstance(v65, list):
        continue
    for mine in ('s18_r_s', 's18_o_s', 's18_o_st', 's20_r_salt-len'):
        def f(t, v65=v65, mine=mine):
            t = t.replace('__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0)', 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16')
            v = [(a.replace('__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0)', 'xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16'), b) for a, b in v65]
            t = _ap(t, v)
            return V[mine](t.replace('if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)\n\t\t\tfuse = 1;', 'if (__builtin_expect(xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16, 0))\n\t\t\tfuse = 1;', 1))
        V['s21_%s_%s' % (k65, mine)] = f

# sweep 22: class x params x buildFlash's fuse type
for base in ('s18_r_s', 's20_r_salt-len', 's18_r_st', 's18_r_sj', 's18_o_s', 's20_o_salt-len-fuse', 's18_o_st', 's18_o_sj'):
    for ft in ('unsigned', 'uint8_t', 'BOOL', '_Bool', 'uint32_t', 'char', 'short', 'long'):
        def f(t, base=base, ft=ft):
            t = V[base](t)
            t = t.replace(DECL, '\tint blocks, r, cf, cg, region, i;\n\t%s fuse;\n' % ft, 1)
            if '_o_' in base:
                t = t.replace('int *fuse)', '%s *fuse)' % ft, 1)
            return t
        V['s22_%s_%s' % (base, ft)] = f
