"""parseDump calling the real addRemap (or a clean tail-first addRemapP) instead of the goto copy with asm: how far is it?"""
FOCUS = ['_parseDump']
S1 = 'if (!addRemapP(b2, blk, 0, dst, blocks))'
S2 = 'if (!addRemapP(blk, blk, blk, -1, blocks))'
S3 = 'if (dst != blk && !addRemapP(dst, dst, 0, blk, blocks))'
PIN = '''			b2 = blk;
			__asm__("" : "+r"(b2));
'''
AX1 = [('real', [(S1, 'if (!addRemap(blk, dst, blocks))'), (S2, 'if (!addRemap(blk, -1, blocks))'), (S3, 'if (dst != blk && !addRemap(dst, blk, blocks))'), (PIN, '')]),
       ('realn', [(S1, 'if (!addRemap(n, dst, blocks))'), (S2, 'if (!addRemap(n, -1, blocks))'), (S3, 'if (dst != blk && !addRemap(dst, blk, blocks))'), (PIN, '')]),
       ('p', [(S1, 'if (!addRemapP(blk, blk, 0, dst, blocks))'), (PIN, '')]),
       ]
AX2 = [('', []), ('nolab', [('rem: __attribute__((hot));\n', '')])]
AX3 = [('', []), ('nocb', [('	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));\n', '')])]
AX4 = [('', []), ('nou', [('''			if (blk >= blocks)
				__builtin_unreachable();
''', '')])]
AXES = [AX1, AX2, AX3, AX4]
