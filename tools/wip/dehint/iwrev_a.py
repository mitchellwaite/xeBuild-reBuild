# imgAdd: `partial > 0` on a 0-or-1 flag
T = '\t\tif (partial > 0) {\n'
P = '\t\tpartial = len < 0x4000;\n'
D = '\tint partial;\n'
V = [
    ('base', []),
    ('if', [(T, '\t\tif (partial) {\n')]),
    ('ne0', [(T, '\t\tif (partial != 0) {\n')]),
    ('ge1', [(T, '\t\tif (partial >= 1) {\n')]),
    ('eq1', [(T, '\t\tif (partial == 1) {\n')]),
    ('len', [(T, '\t\tif (len < 0x4000) {\n')]),
    ('bool', [(D, '\t_Bool partial;\n'), (T, '\t\tif (partial) {\n')]),
    ('boolgt', [(D, '\t_Bool partial;\n')]),
    # a count, where `> 0` is the natural test: room left in a block
    ('room', [(P, '\t\tpartial = 0x4000 - len;\n')]),
    ('roomi', [(P, '\t\tpartial = 0x4000 - (int)len;\n')]),
    ('roomp', [(P, '\t\tpartial = (0x4000 - len) / 512;\n')]),
    # pages of a block the data needs fewer than
    ('short', [(P, '\t\tpartial = 32 - len / 512;\n')]),
    ('and', [(T + '\t\t\tif (small) {\n', '\t\tif (partial && small) {\n\t\t\t{\n')]),
    ('andgt', [(T + '\t\t\tif (small) {\n', '\t\tif (partial > 0 && small) {\n\t\t\t{\n')]),
]
