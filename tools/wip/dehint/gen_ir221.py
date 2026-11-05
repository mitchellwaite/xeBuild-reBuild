"""irwin3: findAnchor near miss (attempt 15's Dbmr), every test in steps of 1 (attempt 16; measurement only).
python tools/wip/dehint/irwin3.py tools/wip/dehint/drafts/image_read_attempt15.c tools/wip/dehint/gen_ir221.py"""
FN = '_findAnchor'
REMOVE = []
PS = list(range(2, 99, 2)) + list(range(3, 99, 2))
PS.sort()
E = '__builtin_expect(!!(%s), 1)'
TESTS = {
 'ok0t': ('\tif (ok0)\n\t\tlog_printf(1, "anchor block v %d at 0x2fe8000 is valid', '\tif (' + E % 'ok0' + ')\n\t\tlog_printf(1, "anchor block v %d at 0x2fe8000 is valid'),
 'ok1t': ('\tif (ok1) {\n\t\tlog_printf(1, "anchor block v %d at 0x2fec000 is valid', '\tif (' + E % 'ok1' + ') {\n\t\tlog_printf(1, "anchor block v %d at 0x2fec000 is valid'),
 'cmp': ('if (ok0 && v0 < v1)', 'if (ok0 && ' + E % 'v0 < v1' + ')'),
 'ok0c': ('if (ok0 && v0 < v1)', 'if (' + E % 'ok0' + ' && v0 < v1)'),
 'sel': ('if (!ok0 && ok1) {', 'if (' + E % '!ok0 && ok1' + ') {'),
 'ret': ('if (!ok0)\n\t\treturn 0;', 'if (' + E % '!ok0' + ')\n\t\treturn 0;'),
}
