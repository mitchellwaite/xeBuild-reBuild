/* smc: SMC checksum, type detection, reset-limit/eject/blink patches */

typedef unsigned char u8;
typedef unsigned int u32;

u32 crc32(const u8 *buf, int len);
void log_printf(int level, const char *fmt, ...);
const char *getConsoleTypeStr(int type);
int findInstExists(const u8 *buf, int len, const void *inst, int instLen);
int replaceInst(u8 *buf, int len, const void *inst, int instLen, const void *repl, int replLen);
u32 calcConfigSum(const u8 *buf);

struct knownSmc {
	u32 crc;
	u32 size;
};

struct knownSmc knownSmcs[] = {
	{ 0x3a0059db, 0x137f }, { 0xba42ab9f, 0x13b4 }, { 0x74224600, 0x13b4 },
	{ 0xf9c96639, 0x13b3 }, { 0x5b3aed00, 0x12ba }, { 0x1d0c613e, 0x12a3 },
	{ 0x7e5bc217, 0x12a3 }, { 0x9ad5b7ee, 0x1257 }, { 0xb74ae419, 0x1242 },
	{ 0xcab0c3b2, 0x1180 }, { 0x6dad8fc1, 0x1180 },
};

int smcFindResetLimit(const u8 *smc, int len)
{
	int i;

	for (i = 4; i < len - 6; i++)
		if (smc[i] == 0x05 && smc[i + 2] == 0xe5 && smc[i + 4] == 0xb4 && smc[i + 5] == 0x05)
			return i;
	return 0;
}

int smcCheck(u8 *smc, int len, int type)
{
	u8 pat1[3] = { 0x78, 0xba, 0xb6 };
	u32 pat2 = 0x1b0000d0;
	u32 crc = crc32(smc + 4, len - 4);
	int ver = smc[0x100] >> 4;
	unsigned int i;

	log_printf(1, "SMC checksum: %08x\n", crc);
	for (i = 0; i < sizeof(knownSmcs) / sizeof(knownSmcs[0]); i++) {
		if (crc == knownSmcs[i].crc) {
			log_printf(1, "known clean SMC found, type: %s v%d.%d(%d.%02d)\n", getConsoleTypeStr(ver),
				smc[0x100] >> 4, smc[0x100] & 15, smc[0x101], smc[0x102]);
			return 0;
		}
	}
	log_printf(1, "unknown SMC found, type: %s v%d.%d(%d.%02d)\n", getConsoleTypeStr(ver),
		smc[0x100] >> 4, smc[0x100] & 15, smc[0x101], smc[0x102]);
	if (type == 3)
		return smcFindResetLimit(smc, len) == 0;
	if (type == 2)
		goto patches;
	if (type == 1 || type > 5) {
		if (!smcFindResetLimit(smc, len))
			return 1;
patches:
		if (findInstExists(smc, len, pat1, 3))
			return 1;
		return findInstExists(smc, len, &pat2, 4) != 0;
	}
	return 1;
}

void smcPatch(u8 *smc, int len, u32 flags)
{
	u8 *data = smc + 4;
	int dataLen = len - 4;

	if (flags & 0x8000000) {
		int off = smcFindResetLimit(smc, len);
		if (off) {
			log_printf(1, "patching SMC reset limit at offset: 0x%x\n", off);
			smc[off] = 0;
			smc[off + 1] = 0;
			log_printf(1, "SMC reset limit patched successfully!\n");
		} else
			log_printf(0, "\n******* WARNING: could not patch SMC reset limit!\n\n");
	}
	if (flags & 0x400000) {
		u32 inst = 0x22b390a2, repl = 0x22c3;
		if (replaceInst(data, dataLen, &inst, 4, &repl, 4))
			log_printf(1, "SMC EJECT button disabled successfully!\n");
		else
			log_printf(0, "\n******* WARNING: could not patch SMC to disable EJECT button.\n\n");
	}
	if (flags & 0x800000) {
		u32 inst[2] = { 0x92cfa2e4, 0x22cea2e0 }, repl[2] = { 0x22d3e4, 0 };
		if (replaceInst(data, dataLen, inst, 8, repl, 8))
			log_printf(1, "SMC ROL center blink disabled successfully!\n");
		else
			log_printf(0, "\n******* WARNING: could not patch SMC to disable ROL center blinking\n\n");
	}
}

int smcConfigOk(const u8 *smc)
{
	return ((u32)smc[0] << 24 | smc[1] << 16) == calcConfigSum(smc);
}
