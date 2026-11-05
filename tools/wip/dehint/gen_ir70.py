"""base2: only the summary's epilogue left, a frequency.  Spellings of the exits and addRemap's return."""
BASE = 'tools/wip/dehint/drafts/image_read_attempt4_base2.c'
FOCUS = ['_parseDump']
S1 = '''			if (!addRemap(blk, dst, blocks))
				return 0;
			goto next;
'''
S2 = '''			if (!addRemap(blk, -1, blocks))
				return 0;
'''
S3 = '''		if (dst != blk && !addRemap(dst, blk, blocks))
			return 0;
'''
def forms(call, tail='', ind='\t\t\t'):
    return {
     '': None,
     'e0': ind + 'if (' + call + ' == 0)\n' + ind + '\treturn 0;\n' + tail,
     'le': ind + 'if (' + call + ' <= 0)\n' + ind + '\treturn 0;\n' + tail,
     }
A1 = [('', [])] + [('s1' + k, [(S1, v)]) for k, v in forms('addRemap(blk, dst, blocks)', '			goto next;\n').items() if v]
A1 += [('s1els', [(S1, '			if (addRemap(blk, dst, blocks))\n				goto next;\n			return 0;\n')])]
A2 = [('', [])] + [('s2' + k, [(S2, v)]) for k, v in forms('addRemap(blk, -1, blocks)').items() if v]
A2 += [('s2els', [(S2, '			if (addRemap(blk, -1, blocks)) {\n				dst = blk;\n			} else\n				return 0;\n')])]
A3 = [('', [])] + [('s3nest', [(S3, '		if (dst != blk) {\n			if (!addRemap(dst, blk, blocks))\n				return 0;\n		}\n')]),
       ('s3le', [(S3, '		if (dst != blk && addRemap(dst, blk, blocks) <= 0)\n			return 0;\n')]),
       ('s3nle', [(S3, '		if (dst != blk) {\n			if (addRemap(dst, blk, blocks) <= 0)\n				return 0;\n		}\n')])]
RET = [('', []),
       ('ul', [('int addRemap(int block, int dest, int numBlocks)\n', 'unsigned long addRemap(int block, int dest, int numBlocks)\n'), ('int addRemap(int block, int dest, int numBlocks);', 'unsigned long addRemap(int block, int dest, int numBlocks);')]),
       ('u', [('int addRemap(int block, int dest, int numBlocks)\n', 'uint32_t addRemap(int block, int dest, int numBlocks)\n'), ('int addRemap(int block, int dest, int numBlocks);', 'uint32_t addRemap(int block, int dest, int numBlocks);')])]
AXES = [A1, A2, A3, RET]
