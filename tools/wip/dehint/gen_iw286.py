# attempt 23: the two setBeU16 calls at writeFsTable's end as a loop over a table. A top-level loop is left alone by cunrolli (from memory, it only does inner loops; checked by dump below) and goes at cunroll, between dce6 and ivopts, which is where position 6's names are popped.
# `IWB=build/iw/a23/na.c python tools/wip/dehint/iw16sweep.py tools/wip/dehint/gen_iw286.py -n 30 -t 4`
T0 = '''	setBeU16(blk, (uint8_t *)&xb.fsBlock);
	setBeU16(0, (uint8_t *)&xb.fsReserved);
'''
TL = [
 ('', []),
 ('t1', [(T0, '''	{
		uint32_t val[2] = { blk, 0 };
		uint8_t *to[2] = { (uint8_t *)&xb.fsBlock, (uint8_t *)&xb.fsReserved };
		int k;

		for (k = 0; k < 2; k++)
			setBeU16(val[k], to[k]);
	}
''')]),
 ('t2', [(T0, '''	{
		uint8_t *const to[2] = { (uint8_t *)&xb.fsBlock, (uint8_t *)&xb.fsReserved };
		int k;

		for (k = 0; k < 2; k++) {
			setBeU16(blk, to[k]);
			blk = 0;
		}
	}
''')]),
 ('t3', [(T0, '''	{
		static uint8_t *const to[2] = { (uint8_t *)&xb.fsBlock, (uint8_t *)&xb.fsReserved };
		uint32_t val[2];
		int k;

		val[0] = blk;
		val[1] = 0;
		for (k = 0; k < 2; k++)
			setBeU16(val[k], to[k]);
	}
''')]),
 ('t4', [(T0, '''	{
		int k;

		for (k = 0; k < 2; k++)
			setBeU16(k ? 0 : blk, (uint8_t *)(k ? &xb.fsReserved : &xb.fsBlock));
	}
''')]),
]
AXES = [TL]
