"""Attempt 2, model check, NOT natural: a redundant 4th loop exit with its own body, removed after profile_estimate.
Plain select gives a = b = .0225; the model says the threshold passes."""
import itertools
import gen_nr15 as g

EX = {
    'top-ret': 'if (got >= size) {\n\t\t\treturn NULL;\n\t\t}\n\t\t',
    'top-ge': 'if (size <= got)\n\t\t\treturn NULL;\n\t\t',
    'left': 'if (size - got <= 0)\n\t\t\treturn NULL;\n\t\t',
    'top-free': 'if (got >= size) {\n\t\t\tif (buf != (uint8_t *)&netEmpty)\n\t\t\t\tfree(buf);\n\t\t\treturn NULL;\n\t\t}\n\t\t',
}
POS = ('before-select', 'before-recv')


def variants():
    for e, p in itertools.product(EX, POS):
        v = g.src('plain', 'while', 'base')
        if p == 'before-select':
            v = v.replace('r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r', EX[e] + 'r = select(0, &fds, NULL, NULL, &tv);\n\t\tif (r', 1) if False else v
            k = v.index('while (got < size) {\n\t\t') + len('while (got < size) {\n\t\t')
            v = v[:k] + EX[e] + v[k:]
        else:
            k = v.index('r = recv(netSock, (char *)buf + got')
            v = v[:k] + EX[e] + v[k:]
        yield e + '|' + p, v
