Q='return __builtin_expect(type == 23 || type == 15, 0) || type == 16 || type == 9 || type == 10 || type == 24 || type == 25;'
FOCUS=['_addUpdateBls']
L='type == 15 || type == 16 || type == 9 || type == 10 || type == 24 || type == 25'
AXES=[[
 ('if23',[(Q,'if (type == 23)\n\t\treturn 1;\n\treturn %s;'%L)]),
 ('paren',[(Q,'return type == 23 || (%s);'%L)]),
 ('last',[(Q,'return %s || type == 23;'%L)]),
 ('sw',[(Q,'switch (type) {\n\tcase 23:\n\tcase 15: case 16: case 9: case 10: case 24: case 25:\n\t\treturn 1;\n\t}\n\treturn 0;')]),
 ('sw2',[(Q,'switch (type) {\n\tcase 23:\n\t\treturn 1;\n\tcase 15: case 16: case 9: case 10: case 24: case 25:\n\t\treturn 1;\n\tdefault:\n\t\treturn 0;\n\t}')]),
 ('ifs',[(Q,'if (type == 23 || type == 15)\n\t\treturn 1;\n\tif (type == 16 || type == 9 || type == 10 || type == 24 || type == 25)\n\t\treturn 1;\n\treturn 0;')]),
 ('ifs2',[(Q,'if (type == 23)\n\t\treturn 1;\n\tif (%s)\n\t\treturn 1;\n\treturn 0;'%L)]),
 ('ifs3',[(Q,'if (type != 23) {\n\t\tif (%s)\n\t\t\treturn 1;\n\t\treturn 0;\n\t}\n\treturn 1;'%L)]),
 ('order',[(Q,'return type == 23 || type == 25 || type == 24 || type == 10 || type == 9 || type == 16 || type == 15;')]),
 ('asc',[(Q,'return type == 23 || type == 9 || type == 10 || type == 15 || type == 16 || type == 24 || type == 25;')]),
 ('rng',[(Q,'return type == 23 || type == 9 || type == 10 || type == 15 || type == 16 || (type >= 24 && type <= 25);')]),
]]
