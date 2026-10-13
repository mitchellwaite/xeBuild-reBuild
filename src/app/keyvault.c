/* keyvault: keyvault hash check, DVD key, console serial/date formatting */
#include <stdio.h>
#include <string.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;

void log_printf(int level, const char *fmt, ...);
u32 getBeU32(const u8 *p);
int kvVerifySig(u8 *kv, const void *pubKey, const u8 *hmacKey);
int validateString(char *nString);
unsigned char myatox8(char *dat);

extern void *masterPub;
extern u8 cpuKey[];
extern int g479ea8;

static u8 kvBuf[0x4000];
static u8 dvdKey[16];
static u8 *kv;
static u32 kvLoaded;
static int dvdKeySet;
static u32 kvHashOk;
static int kvType;

int kvGetType(void)
{
	if (kvHashOk)
		return kvType;
	return 0;
}

int kvIsLoaded(void)
{
	return kvLoaded;
}

int kvCheckHash(void)
{
	int i;
	u32 v;

	if (!kvLoaded)
		return 0;
	for (i = 0; i < 16; i++) {
		v = getBeU32(kv + 0x1df8 + i * 4);
		if (v != 0 && v != 0xffffffff)
			goto found;
	}
	return 0;
found:
	if (!masterPub) {
		nomaster: __attribute__((cold));
		log_printf(1, "Master RSA pub not available, not checking hash\n");
		kvType = 1;
		return 1;
	}
	if (__builtin_expect(kvVerifySig(kvBuf, masterPub, cpuKey), 1)) {
		kvType = 3;
		log_printf(1, "Keyvault hash is good!\n");
		return 1;
	}
	kvType = 2;
	log_printf(0, "***** WARNING: Keyvault hash is not good! Keyvault may be corrupt or does not belong to this CPU key!\n");
	return 1;
}

void kvSet(u8 *buf)
{
	memcpy(kvBuf, buf, 0x4000);
	kvLoaded = 1;
	kv = kvBuf;
	log_printf(1, "decrypted keyvault has been set for reference\n");
	if (dvdKeySet) {
		if (g479ea8 != 1) {
			memcpy(buf + 0x100, dvdKey, 16);
			memcpy(kv + 0x100, dvdKey, 16);
			log_printf(1, "dvd key patched into keyvault\n");
		} else
			log_printf(1, "retail image, skipping patching dvd key\n");
	}
	kvHashOk = kvCheckHash();
}

int kvGetGameRegion(void)
{
	u16 x;
	u16 f;

	if (!kvLoaded)
		return 0;
	x = *(u16 *)(kv + 0x1c);
	f = ((x & 0xff) << 8) + (x >> 8);
	if (f) {
		if (f & 0x300)
			return 2;
		if (f & 0x20)
			return 1;
	}
	return ((((x & 0xff) << 8) + (x >> 8)) & 0x120) != 0;
}

u8 *kvGetDvdKey(void)
{
	if (!kvLoaded)
		return 0;
	return kv + 0x100;
}

u8 *kvGetConsoleId(void)
{
	if (!kvLoaded)
		return 0;
	return kv + 0xb0;
}

int kvGetSerial(char *out)
{
	u64 v = 0;
	int i;
	int ret = 0;
	u8 digit, *p;

	if (kvLoaded && out) {
		p = kv + 0x9ca;
		v = *p++;
		for (i = 1; i < 5; i++)
			v = (v << 8) + *p++;
		digit = p[-1] & 0xf;
		if (digit <= 9) {
			sprintf(out, "%011I64u%X", v >> 4, digit);
			ret = 1;
		}
	}
	return ret;
}

u8 *kvGetConsoleCert(void)
{
	if (!kvLoaded)
		return 0;
	return kv + 0xc0;
}

int kvGetMfgDate(char *out)
{
	if (!kvLoaded || !out)
		return 0;
	sprintf(out, "%c%c/%c%c/20%c%c", kv[0x9e4], kv[0x9e5], kv[0x9e7], kv[0x9e8], kv[0x9ea], kv[0x9eb]);
	return 1;
}

int kvHashIsOk(void)
{
	return kvHashOk;
}

int kvSetDvdKey(char *key)
{
	int len = strlen(key);
	int i, r;

	if (len == 32) {
		r = validateString(key);
		if (r) {
			for (i = 0; i < 16; i++, key += 2)
				dvdKey[i] = myatox8(key);
			log_printf(1, "DVD Key set to: 0x");
			for (i = 0; i < 16; i++)
				log_printf(1, "%02X", dvdKey[i]);
			log_printf(1, "\n");
			dvdKeySet = 1;
			return 1;
		}
		log_printf(0, "\n******* ERROR: invalid or unexpected characters in DVD key!\n");
		return r;
	}
	log_printf(0, "\n***** ERROR: unable to set dvd key to '%s', %d is not the correct length, 32 chars required!\n", key, len);
	return 0;
}
