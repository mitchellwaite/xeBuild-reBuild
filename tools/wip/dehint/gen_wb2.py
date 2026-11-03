"""netWriteBlocks: spelling of the netSendStr test (opcode predictor) on the scoped-rlen shape."""
import itertools

BODY = '''int netWriteBlocks(const uint8_t *buf, uint32_t len, uint32_t start, uint32_t count)
{
	int ret;
	uint8_t *r;
	char cmd[32];

	sprintf(cmd, "WBLK%%04x%%04x\\n", (uint16_t)start, (uint16_t)count);
	%s
	{
		int rlen;

		r = netRecv(&rlen);
		if (!r)
			return 0;
		ret = 0;
		if (rlen == 2 && getBeU16(r) == OK_REPLY)
			ret = 1;
		netFree(r);
	}
	if (ret)
		return 1;
	return 0;
}
'''
SEND = 'netSendData(buf, len, log_get_verbose() != 0)'
STR = 'netSendStr(cmd)'
HEADS = {
    'plain': 'if (!%s)\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;' % (STR, SEND),
    'le0': 'if (%s <= 0)\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;' % (STR, SEND),
    'lt1': 'if (%s < 1)\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;' % (STR, SEND),
    'ne1': 'if (%s != 1)\n\t\treturn 0;\n\tif (!%s)\n\t\treturn 0;' % (STR, SEND),
    'le0or': 'if (%s <= 0 || !%s)\n\t\treturn 0;' % (STR, SEND),
    'dle0': 'if (!%s)\n\t\treturn 0;\n\tif (%s <= 0)\n\t\treturn 0;' % (STR, SEND),
    'bothle0': 'if (%s <= 0)\n\t\treturn 0;\n\tif (%s <= 0)\n\t\treturn 0;' % (STR, SEND),
}


def variants():
    for k, h in HEADS.items():
        yield k, BODY % h
