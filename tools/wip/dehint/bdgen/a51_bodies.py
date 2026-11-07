"""Attempt 51: loadBl24 bodies (two defaultBl60 call sites unless said) for a51_pred.py / a51_score.py."""
OLD = '''	if (loadBaseFile(e->name, e))
		return defaultBl60(e);
	if (e->size != 0x60)
		return defaultBl60(e);
	return 0;
}
'''
BODIES = {
    'src': OLD,
    'or': '''	if (loadBaseFile(e->name, e) || e->size != 0x60)
		return defaultBl60(e);
	return 0;
}
''',
}
