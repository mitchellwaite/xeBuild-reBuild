"""Borderline review, net: the other netSendStr tests written as compares with 0.

Each `!netSendStr(..)` becomes `netSendStr(..) <= 0` and each truth test `netSendStr(..) > 0`
(or `< 1` / `>= 1`), one site at a time and all together.  If every site matches either way,
the file can use one form throughout and the three upload sites aren't the odd ones out."""
from nbsweep import BASE

DEF = BASE.index('int netSendStr(')
BODY = BASE.index('{', DEF)


def sites(text):
    """(start, end, neg, call) for every netSendStr call after its definition not already compared"""
    out = []
    i = text.index('netSendStr(', BODY)
    while i >= 0:
        j = i + len('netSendStr(')
        depth = 1
        while depth:
            depth += {'(': 1, ')': -1}.get(text[j], 0)
            j += 1
        if not text[j:].startswith(' <= 0'):
            neg = text[i - 1] == '!'
            out.append((i - 1 if neg else i, j, neg, text[i:j]))
        i = text.find('netSendStr(', j)
    return out


FORMS = {'le': ('{} <= 0', '{} > 0'), 'lt': ('{} < 1', '{} >= 1')}


def apply(text, chosen, form):
    for s, e, neg, call in sorted(chosen, reverse=True):
        f = FORMS[form][0 if neg else 1]
        text = text[:s] + f.format(call) + text[e:]
    return text


def fname(text, pos):
    k = text.rfind('\n{', 0, pos)
    line = text.rfind('\n', 0, k)
    return text[line + 1:k].split('(')[0].split()[-1].lstrip('*')


def variants():
    ss = sites(BASE)
    for form in FORMS:
        for n, site in enumerate(ss):
            yield '%s|%d|%s' % (form, n, fname(BASE, site[0])), apply(BASE, [site], form)
        yield '%s|all' % form, apply(BASE, ss, form)
        yield '%s|neg' % form, apply(BASE, [x for x in ss if x[2]], form)
