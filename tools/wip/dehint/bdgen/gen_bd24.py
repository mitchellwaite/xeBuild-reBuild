# One helper only: loadBl60 keeps its two copies (first arm), the DEVGL arm's load is written out.
# Base: gen_bd23's "helper", which has two helpers.
BASE = 'build/bd/gen_bd23_best.c'
TWO = '''static int loadBl60(struct fileent *e)
{
	if (loadBaseFile(e->name, e) || e->size != 0x60) {
		e->data = malloc(0x60);
		if (!e->data)
			return 1;
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
	}
	return 0;
}

static int loadBl60b('''
ONE = 'static int loadBl60('
ARM1 = '*pr = loadBl60b(e);'
OLD2 = '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16)
			*pr = loadBl60(e);
'''
W1 = '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
			if (loadBaseFile(e->name, e) || e->size != 0x60) {
				e->data = malloc(0x60);
				if (!e->data) {
					*pr = 1;
					break;
				}
				e->size = 0x60;
				memcpy(e->data, defBl60, 0x60);
			}
			*pr = 0;
		}
'''
W2 = W1.replace('			*pr = 0;\n', '')
W3 = '''		if (xb.type == BUILD_DEVGL || xb.type == BUILD_DEVGL16) {
			if (!loadBaseFile(e->name, e) && e->size == 0x60)
				break;
			e->data = malloc(0x60);
			if (!e->data) {
				*pr = 1;
				break;
			}
			e->size = 0x60;
			memcpy(e->data, defBl60, 0x60);
		}
'''
W4 = '''		if (xb.type != BUILD_DEVGL && xb.type != BUILD_DEVGL16)
			break;
		if (!loadBaseFile(e->name, e) && e->size == 0x60)
			break;
		e->data = malloc(0x60);
		if (!e->data) {
			*pr = 1;
			break;
		}
		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
'''
BASEEDIT = [(TWO, ONE), (ARM1, '*pr = loadBl60(e);')]
AXES = [[('', BASEEDIT)], [('w1', [(OLD2, W1)]), ('w2', [(OLD2, W2)]), ('w3', [(OLD2, W3)]), ('w4', [(OLD2, W4)])]]
