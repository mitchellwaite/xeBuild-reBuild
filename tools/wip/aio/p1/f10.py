"""f10.py OUT VARIANT: from n1.c: natural shapes of optIniBool"""
import re,sys
t=open(__file__.replace('f10.py','n1.c'),newline='').read()
i=t.index('_Bool optIniBool('); j=t.index('int optIniInt(')
sig='_Bool optIniBool(const char *name, uint32_t set, uint32_t clear, int def)\n{\n\tchar *bad;\n\n'
NL=chr(92)+'n'
LOG1='log_printf(1, "Using %s option (perbox file)'+NL+'", name);'
LOG2='log_printf(1, "Using %s option (ini file)'+NL+'", name);'
WARN='log_printf(0, "***** WARNING: options.ini setting '+chr(39)+'%s'+chr(39)+' invalid value '+chr(39)+'%s'+chr(39)+', discarding!'+NL+'", name, bad);'
SET='xb.bootFlags &= ~clear;\n\t\txb.bootFlags |= set;'
V={
'A':f'''	if (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) {{
		if (perboxExists(name)) {{
			{LOG1}
		}} else {{
			bad = iniBoolInvalid(name);
			if (!bad) {{
				if (!getIniBool(name, def))
					return 0;
				{LOG2}
			}} else {{
				{WARN}
				return 0;
			}}
		}}
		{SET}
		return 1;
	}}
	return 0;
}}

''',
'B':f'''	if (!(xb.bootFlags & set)) {{
		if (!(xb.bootFlagsOff & set)) {{
			if (perboxExists(name)) {{
				{LOG1}
			}} else {{
				bad = iniBoolInvalid(name);
				if (!bad) {{
					if (!getIniBool(name, def))
						return 0;
					{LOG2}
				}} else {{
					{WARN}
					return 0;
				}}
			}}
			{SET}
			return 1;
		}}
	}}
	return 0;
}}

''',
'C':f'''	if (xb.bootFlags & set)
		goto out;
	if (xb.bootFlagsOff & set)
		goto out;
	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			if (!getIniBool(name, def))
				goto out;
			{LOG2}
		}} else {{
			{WARN}
			goto out;
		}}
	}}
	{SET}
	return 1;
out:
	return 0;
}}

''',
'D':f'''	_Bool r = 0;
	if (!(xb.bootFlags & set) && !(xb.bootFlagsOff & set)) {{
		if (perboxExists(name)) {{
			{LOG1}
			r = 1;
		}} else {{
			bad = iniBoolInvalid(name);
			if (!bad) {{
				if (getIniBool(name, def)) {{
					{LOG2}
					r = 1;
				}}
			}} else {{
				{WARN}
			}}
		}}
		if (r) {{
		{SET}
		}}
	}}
	return r;
}}

''',
'E':f'''	if (xb.bootFlags & set) {{
		if (__builtin_constant_p(xb.bootFlags + 1))
			goto r;
		return 0;
	}}
	if (xb.bootFlagsOff & set) {{
		if (__builtin_constant_p(xb.bootFlagsOff + 1))
			goto r;
		return 0;
	}}
	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			if (!getIniBool(name, def))
				return 0;
			{LOG2}
		}} else {{
			{WARN}
			return 0;
		}}
	}}
	{SET}
r:
	return 1;
}}

''',
'F':f'''	if (xb.bootFlags & set) {{
		if (__builtin_constant_p(xb.bootFlags + 1))
			goto r;
		return 0;
	}}
	if (xb.bootFlagsOff & set) {{
		if (__builtin_constant_p(xb.bootFlagsOff + 1))
			goto r;
		return 0;
	}}
	if (perboxExists(name)) {{
		{LOG1}
	}} else {{
		bad = iniBoolInvalid(name);
		if (!bad) {{
			if (!getIniBool(name, def))
				return 0;
			{LOG2}
		}} else {{
			{WARN}
			return 0;
		}}
	}}
r:
	{SET}
	return 1;
}}

''',
}
t=t[:i]+sig+V[sys.argv[2]]+t[j:]
open(sys.argv[1],'w',newline='\n').write(t)
