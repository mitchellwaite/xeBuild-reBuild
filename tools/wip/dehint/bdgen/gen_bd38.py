# extractSmcConfig: a signed size param gives the bound tests a conversion's SSA name, so size isn't the low version
# (forwprop's operand order) and neither (void)&size nor perhaps noinline is needed.
FOCUS = ['_extractSmcConfig']
SIG = 'int extractSmcConfig(struct fileent *e, uint8_t *buf, uint32_t size)'
AS = '	(void)&size;\n'
NI = '__attribute__((noinline)) int extractSmcConfig'
T = [('int', [(SIG, SIG.replace('uint32_t size', 'int size'))]), ('long', [(SIG, SIG.replace('uint32_t size', 'long size'))]),
     ('ssize', [(SIG, SIG.replace('uint32_t size', 'ssize_t size'))])]
A = [('', []), ('noaddr', [(AS, '')])]
N = [('', []), ('noinl', [(NI, 'int extractSmcConfig')])]
AXES = [T, A, N]
