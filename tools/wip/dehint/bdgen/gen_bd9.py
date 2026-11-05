"""the 0x60 copies: size store before rep movs (sched2 needs a dependence, or a priority)"""
FOCUS = ['_loadConsoleBlFiles', '_loadBlFiles']
Q1 = '''		{
		uint8_t *p = e->data;

		__asm__("" : "+r"(p));
		e->size = 0x60;
		memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);
		}
'''
Q2 = '''		{
			uint8_t *p = e->data;

			/* p's points-to unknown: the size store may alias the
			   copy, so sched2 keeps it before the rep movsd setup */
			__asm__("" : "+r"(p));
			e->size = 0x60;
			memcpy(__builtin_assume_aligned(p, 4), defBl60, 0x60);
		}
'''


def both(body):
    return [(Q1, body), (Q2, body)]


AXES = [[
    ('plain', both('''		e->size = 0x60;
		memcpy(e->data, defBl60, 0x60);
''')),
    ('sizeof', both('''		e->size = sizeof(defBl60);
		memcpy(e->data, defBl60, sizeof(defBl60));
''')),
    ('esize', both('''		e->size = 0x60;
		memcpy(e->data, defBl60, e->size);
''')),
    ('move', both('''		e->size = 0x60;
		memmove(e->data, defBl60, 0x60);
''')),
    ('struct', both('''		e->size = 0x60;
		{
			struct bl60 { uint32_t w[0x18]; };

			*(struct bl60 *)e->data = *(struct bl60 *)defBl60;
		}
''')),
    ('src', both('''		{
			const void *src = defBl60;

			e->size = 0x60;
			memcpy(e->data, src, 0x60);
		}
''')),
    ('size2', both('''		{
			uint32_t n = 0x60;

			e->size = n;
			memcpy(e->data, defBl60, n);
		}
''')),
    ('void', both('''		{
			void *p = e->data;

			e->size = 0x60;
			memcpy(p, defBl60, 0x60);
		}
''')),
    ('w32', both('''		{
			uint32_t *p = (uint32_t *)e->data;

			e->size = 0x60;
			memcpy(p, defBl60, 0x60);
		}
''')),
    ('arr', both('''		e->size = 0x60;
		memcpy(&e->data[0], &defBl60[0], 0x60);
''')),
    ('ptr', both('''		{
			struct fileent *f = e;

			f->size = 0x60;
			memcpy(f->data, defBl60, 0x60);
		}
''')),
]]
