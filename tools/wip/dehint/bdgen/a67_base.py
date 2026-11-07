"""Attempt 67: src with exp_pr off (r != 0) and with (int)r < 0, for a63_diff.py."""
V = {'src': [],
     'nopr': [('if (__builtin_expect(r != 0, 0))', 'if (r != 0)')],
     'neg': [('if (__builtin_expect(r != 0, 0))', 'if ((int)r < 0)')]}
