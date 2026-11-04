"""findAnchor: the .rdata order (valid, invalid, ec valid, ec selected, ec invalid, e8 selected)
says the ec-selected block is written inside `if (ok1)`, before the else."""
FOCUS = ['_findAnchor']

OLD = '''	ok0 = shaSelfCheck(xb.dump + 0x2fe8000);
	if (ok0)
		log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);
	else {
		log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");
		/* code-free: emits these two (threaded copies, expanded last) in the original's order */
		__asm__("" : : "i"("anchor block v %d at 0x2fec000 is valid\\n"), "i"("anchor block v %d at 0x2fec000 is selected\\n"));
	}
	ok1 = shaSelfCheck(xb.dump + 0x2fec000);
	if (ok1)
		log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);
	else {
		log_printf(1, "anchor block at 0x2fec000 is invalid\\n");
		__asm__("");	/* dom3 doesn't thread this copy: one log, ok0 tested after it */
	}
	if (__builtin_expect(ok0, 1) && (__builtin_expect(!ok1, 1) || v0 >= v1)) {
		log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;
	}
	if (__builtin_expect(ok1, 1)) {
		log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
		memcpy(anchor, xb.dump + 0x2fec000, 0x200);
		return 1;
	}
	return 0;
'''

HEAD = '''	ok0 = shaSelfCheck(xb.dump + 0x2fe8000);
	if (ok0)
		log_printf(1, "anchor block v %d at 0x2fe8000 is valid\\n", v0);
	else
		log_printf(1, "anchor block at 0x2fe8000 is invalid\\n");
	ok1 = shaSelfCheck(xb.dump + 0x2fec000);
'''
SEL1 = '''log_printf(1, "anchor block v %d at 0x2fec000 is selected\\n", v1);
			memcpy(anchor, xb.dump + 0x2fec000, 0x200);
			return 1;'''
SEL0 = '''	if (ok0) {
		log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
		memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
		return 1;
	}
	return 0;
'''
VALID = 'log_printf(1, "anchor block v %d at 0x2fec000 is valid\\n", v1);'
INV = 'log_printf(1, "anchor block at 0x2fec000 is invalid\\n");'

SHAPES = {
    'or': HEAD + f'''	if (ok1) {{
		{VALID}
		if (!ok0 || v1 > v0) {{
			{SEL1}
		}}
	}} else
		{INV}
''' + SEL0,
    'or2': HEAD + f'''	if (ok1) {{
		{VALID}
		if (v1 > v0 || !ok0) {{
			{SEL1}
		}}
	}} else
		{INV}
''' + SEL0,
    'nest': HEAD + f'''	if (ok1) {{
		{VALID}
		if (ok0) {{
			if (v1 > v0) {{
				{SEL1}
			}}
		}} else {{
			{SEL1}
		}}
	}} else
		{INV}
''' + SEL0,
    'lt': HEAD + f'''	if (ok1) {{
		{VALID}
		if (!ok0 || v0 < v1) {{
			{SEL1}
		}}
	}} else
		{INV}
''' + SEL0,
    'flag': HEAD + f'''	if (ok1) {{
		{VALID}
		if (ok0 && v0 >= v1)
			ok1 = 0;
	}} else
		{INV}
	if (ok1) {{
		{SEL1}
	}}
''' + SEL0,
}

AXES = [[(k, [(OLD, v)]) for k, v in SHAPES.items()]]

SEL0T = '''	log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
	memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
	return 1;
'''
SELECT1 = f'''{SEL1}'''
SHAPES.update({
    'tail1': HEAD + f'''	if (ok1) {{
		{VALID}
		if (!ok0 || v0 < v1) {{
			{SEL1}
		}}
	}} else {{
		{INV}
		if (!ok0)
			return 0;
	}}
''' + SEL0T,
    'tail2': HEAD + f'''	if (!ok1) {{
		{INV}
		if (!ok0)
			return 0;
	}} else {{
		{VALID}
		if (!ok0 || v0 < v1) {{
			{SEL1}
		}}
	}}
''' + SEL0T,
    'tail3': HEAD + f'''	if (ok1) {{
		{VALID}
		if (ok0) {{
			if (v0 < v1) {{
				{SEL1}
			}}
		}} else {{
			{SEL1}
		}}
	}} else {{
		{INV}
		if (!ok0)
			return 0;
	}}
''' + SEL0T,
    'ret0': HEAD + f'''	if (ok1) {{
		{VALID}
		if (!ok0 || v0 < v1) {{
			{SEL1}
		}}
	}} else {{
		{INV}
		if (ok0) {{
			log_printf(1, "anchor block v %d at 0x2fe8000 is selected\\n", v0);
			memcpy(anchor, xb.dump + 0x2fe8000, 0x200);
			return 1;
		}}
		return 0;
	}}
''' + SEL0T,
})
AXES = [[(k, [(OLD, v)]) for k, v in SHAPES.items()]]

BARS = dict(SHAPES)
for k,v in list(SHAPES.items()):
    BARS[k+'_bar'] = v.replace(INV, INV + ' __asm__("");')
AXES = [[(k, [(OLD, v)]) for k, v in BARS.items()]]
