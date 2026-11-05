"""loadFileCrc, pin_e off: a real use of e or of its fields in the pad log."""
P = '''			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);
			__asm__("" : : "S"(e));
'''
F = {
 'esize': '			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, e->size);\n',
 'esize2': '			log_printf(1, "reading %s (0x%x b pad 0x%x b)", e->name, size, e->size);\n',
 'plain': '			log_printf(1, "reading %s (0x%x b pad 0x%x b)", name, size, (size + 15) & ~15);\n',
 'ename': '			log_printf(1, "reading %s (0x%x b pad 0x%x b)", e->name, size, (size + 15) & ~15);\n',
}
def CASES(base):
    return [(k, base.replace(P, v)) for k, v in F.items()]
