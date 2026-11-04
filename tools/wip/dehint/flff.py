"""flff.py: fixFileCase shapes without optimize("ira-region=one")."""
import itertools
import fllib as L

s = L.base()
OPT = '__attribute__((optimize("ira-region=one")))\n'
a = s.index(OPT)
b = s.index('/* strip comments and invalid characters')
HEAD, TAIL = s[:a], s[b:]

CHAIN = {
 'else': '''if (stricmp(de->d_name, fnSmc) == 0)
			strcpy(fnSmc, de->d_name);
		else if (stricmp(de->d_name, fnKv) == 0)
			strcpy(fnKv, de->d_name);
		else if (stricmp(de->d_name, fnPatches) == 0)
			strcpy(fnPatches, de->d_name);
''',
 'nest': '''if (stricmp(de->d_name, fnSmc) == 0)
			strcpy(fnSmc, de->d_name);
		else {
			if (stricmp(de->d_name, fnKv) == 0)
				strcpy(fnKv, de->d_name);
			else {
				if (stricmp(de->d_name, fnPatches) == 0)
					strcpy(fnPatches, de->d_name);
			}
		}
''',
 'name': None,
}
STAT = {'cont': 0, 'ge': 1, 'eq': 2, 'eqcont': 3}
SCOPE = {'top': 0, 'st': 1, 'stpath': 2, 'path': 3, 'dir': 4}
ORDER = {'dps': 'char dir[1024], path[1024];', 'pd': 'char path[1024], dir[1024];'}
LOOP = {'while': 0, 'for': 1, 'do': 2, 'whilede': 3}
OPEN = {'early': 0, 'nest': 1}
DIRV = {'arr': 0, 'ptr': 1, 'ptrbase': 2}


def gen(chain, stat, scope, order, loop, opn, dirv):
    decl = ''
    inner = ''
    if scope in ('stpath', 'path'):
        inner += 'char path[1024];\n'
    if scope in ('st', 'stpath'):
        inner += 'struct stat st;\n'
    if scope in ('top', 'st', 'dir'):
        decl += ORDER[order] + '\n'
    elif scope in ('stpath', 'path'):
        decl += 'char dir[1024];\n'
    if scope in ('top', 'path', 'dir'):
        decl += 'struct stat st;\n'
    decl += 'DIR *d;\nstruct dirent *de;\n'
    if dirv == 'ptr':
        decl += 'char *dp = dir;\n'
    dn = 'dp' if dirv == 'ptr' else 'dir'
    ch = CHAIN[chain] if chain != 'name' else CHAIN['else'].replace('de->d_name', 'name')
    if chain == 'name':
        inner += 'char *name = de->d_name;\n'
    nm = 'name' if chain == 'name' else 'de->d_name'
    if stat == 'cont':
        body = 'if (stat(path, &st) < 0)\n continue;\n' + ch
    elif stat == 'eqcont':
        body = 'if (stat(path, &st) != 0)\n continue;\n' + ch
    elif stat == 'ge':
        body = 'if (stat(path, &st) >= 0) {\n' + ch + '}\n'
    else:
        body = 'if (stat(path, &st) == 0) {\n' + ch + '}\n'
    body = inner + 'strcpy(path, %s);\nstrcat(path, %s);\n' % (dn, nm) + body
    if loop == 'while':
        lp = 'while ((de = readdir(d)) != NULL) {\n' + body + '}\n'
    elif loop == 'whilede':
        lp = 'de = readdir(d);\nwhile (de != NULL) {\n' + body.replace('continue;', 'goto next;') + 'next:\nde = readdir(d);\n}\n'
    elif loop == 'for':
        lp = 'for (de = readdir(d); de != NULL; de = readdir(d)) {\n' + body + '}\n'
    else:
        lp = 'de = readdir(d);\nif (de != NULL) do {\n' + body + '} while ((de = readdir(d)) != NULL);\n'
    src = 'void fixFileCase(void)\n{\n' + decl + 'strcpy(dir, xb.baseDir);\nd = opendir(%s);\n' % dn
    if opn == 'early':
        src += 'if (d == NULL)\n return;\n' + lp + 'closedir(d);\n'
    else:
        src += 'if (d != NULL) {\n' + lp + 'closedir(d);\n}\n'
    src += '}\n\n'
    return HEAD + src + TAIL


V = {}
for k in itertools.product(CHAIN, STAT, SCOPE, ORDER, LOOP, OPEN, ['arr', 'ptr']):
    V['_'.join(k)] = gen(*k)
print(len(V))
rs = L.sweep(V, prefix='ff', show=25)
with open(L.BD + '/ff.txt', 'w', newline='\n') as f:
    for n, (sc, st, fd, sd) in rs:
        f.write('%s %s %s %s\n' % (sc, n, fd, sd))
