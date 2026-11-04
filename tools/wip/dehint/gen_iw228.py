# attempt 16: `pages` in a15_dead, both arms: real spellings, crossed. C1's bound is pages_106 (first copy's len / 512).
BASE = 'tools/wip/dehint/drafts/image_write_a15_dead.c'
B0 = '''						pages = len / 512;
						if (len % 512)
							pages++;
'''
S0 = '''				pages = len % 512 ? len / 512 + 1 : len / 512;
'''
F = [('a', 'pages = len / 512;\n{I}if (len % 512)\n{I}	pages++;\n'),
     ('t', 'pages = len % 512 ? len / 512 + 1 : len / 512;\n'),
     ('r', 'pages = (len + 511) / 512;\n'),
     ('n', 'pages = len / 512 + (len % 512 != 0);\n'),
     ('i', 'if (len % 512)\n{I}	pages = len / 512 + 1;\n{I}else\n{I}	pages = len / 512;\n'),
     ('j', 'if (len % 512)\n{I}	pages = (len + 512) / 512;\n{I}else\n{I}	pages = len / 512;\n'),
     ('k', 'pages = len / 512;\n{I}if ((len & 511) != 0)\n{I}	pages++;\n'),
     ('m', 'pages = len >> 9;\n{I}if (len & 511)\n{I}	pages++;\n'),
     ('u', 'pages = (len + 512) / 512;\n{I}if (!(len % 512))\n{I}	pages--;\n'),
     ('v', 'pages = len % 512 ? (len + 512) / 512 : len / 512;\n')]
AB = [('b' + l, [(B0, '\t' * 6 + f.replace('{I}', '\t' * 6))]) for l, f in F]
AS = [('s' + l, [(S0, '\t' * 4 + f.replace('{I}', '\t' * 4))]) for l, f in F]
AXES = [AB, AS]
FLAGS = []
