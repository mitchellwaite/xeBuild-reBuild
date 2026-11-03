# writeFsTable without the optimize attribute: forms of the two imgAdd calls and the tail
BASE = 'tools/wip/dehint/drafts/image_write.c'
FOCUS = ['_writeFsTable']
A = '__attribute__((optimize("no-tree-scev-cprop"))) void writeFsTable'
CALLS = '''	if (!xb.bigBlock)
		goto small;
	imgAdd(off, buf, i * 0x400, 0x2c, 0x1ffe, 0);
	goto done;
small:
	imgAdd(off, buf, i * 0x400, 0x30, 0x1ffd, 0);
done:
	setBeU16(blk, (uint8_t *)&xb.fsBlock);
	setBeU16(0, (uint8_t *)&xb.fsReserved);
	free(buf);
'''
TAIL = '''	setBeU16(blk, (uint8_t *)&xb.fsBlock);
	setBeU16(0, (uint8_t *)&xb.fsReserved);
	free(buf);
'''
L = 'i * 0x400'
BIG = lambda l: f'imgAdd(off, buf, {l}, 0x2c, 0x1ffe, 0);'
SM = lambda l: f'imgAdd(off, buf, {l}, 0x30, 0x1ffd, 0);'
forms = {
    'goto-big': f'	if (!xb.bigBlock)\n		goto small;\n	{BIG(L)}\n	goto done;\nsmall:\n	{SM(L)}\ndone:\n',
    'goto-small': f'	if (xb.bigBlock)\n		goto big;\n	{SM(L)}\n	goto done;\nbig:\n	{BIG(L)}\ndone:\n',
    'if': f'	if (xb.bigBlock)\n		{BIG(L)}\n	else\n		{SM(L)}\n',
    'ifn': f'	if (!xb.bigBlock)\n		{SM(L)}\n	else\n		{BIG(L)}\n',
    'ifret': f'	if (xb.bigBlock) {{\n		{BIG(L)}\n{TAIL}		return;\n	}}\n	{SM(L)}\n',
    'ifretn': f'	if (!xb.bigBlock) {{\n		{SM(L)}\n{TAIL}		return;\n	}}\n	{BIG(L)}\n',
    'n-goto-big': f'	n = i * 0x400;\n	if (!xb.bigBlock)\n		goto small;\n	{BIG("n")}\n	goto done;\nsmall:\n	{SM("n")}\ndone:\n',
    'n-if': f'	n = i * 0x400;\n	if (xb.bigBlock)\n		{BIG("n")}\n	else\n		{SM("n")}\n',
    'n-ifn': f'	n = i * 0x400;\n	if (!xb.bigBlock)\n		{SM("n")}\n	else\n		{BIG("n")}\n',
    'late': f'	if (!xb.bigBlock)\n		goto small;\n	{BIG(L)}\n	goto done;\nsmall:\n	{SM("0x400 * i")}\ndone:\n',
    'early': f'	if (!xb.bigBlock)\n		goto small;\n	{BIG("0x400 * i")}\n	goto done;\nsmall:\n	{SM(L)}\ndone:\n',
}
TY = {
    'int': [],
    'u32': [('	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n', '	uint8_t *buf, *p;\n	uint32_t blk;\n	uint32_t i;\n')],
}
axis = []
for k, v in forms.items():
    for t, ed in TY.items():
        e = [(A, 'void writeFsTable'), (CALLS, v + TAIL if 'ifret' not in k else v + '')] + ed
        if k.startswith('n-'):
            decl = ed[0][1] if ed else '	uint8_t *buf, *p;\n	uint32_t blk;\n	int i;\n'
            e.append((decl, decl + '	uint32_t n;\n'))
        axis.append((k + '+' + t, e))
AXES = [axis]
