"""pin_cb: how many asm uses of blk does improve_allocation need (r99 l0 cost 5307 without, 5627 with four)?  And where else can they sit: threshold of the cost."""
FOCUS = ['_parseDump']
BASE = 'tools/wip/dehint/drafts/image_read_attempt3.c'
CB = '	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb), "ri"(cb));\n'
AXES = [[('c4', []),
         ('c3', [(CB, '	__asm__("" : : "ri"(cb), "ri"(cb), "ri"(cb));\n')]),
         ('c2', [(CB, '	__asm__("" : : "ri"(cb), "ri"(cb));\n')]),
         ('c1', [(CB, '	__asm__("" : : "ri"(cb));\n')]),
         ('c0', [(CB, '')]),
         ]]
