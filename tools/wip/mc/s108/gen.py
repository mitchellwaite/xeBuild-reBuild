import sys
pre = open('pre.c').read(); post = open('post.c').read()
M = ('#define MI "\\n\\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\\n"\n'
     '#define MO "\\n\\n***** ERROR: Block 0x%x is outside system area!\\n"\n'
     '#define MF "\\n\\n***** ERROR: Failed to erase block 0x%x!\\n"\n')
# optional: argv[2] = file of "old@@new" substitutions applied to post (main) text
subs = []
if len(sys.argv) > 2:
    for ln in open(sys.argv[2]).read().split('\n=====\n'):
        if '@@' in ln:
            o, n = ln.split('@@', 1); subs.append((o, n))
for part in open(sys.argv[1]).read().split('@@ ')[1:]:
    name, body = part.split('\n', 1)
    name = name.split()[0]
    p = post
    for o, n in subs:
        assert o in p, o
        p = p.replace(o, n, 1)
    open('v_%s.c' % name, 'w', newline='\n').write(pre + M + body + '\n' + p)
    print(name)
