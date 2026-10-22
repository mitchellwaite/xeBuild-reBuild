/* net: talking to the console's updsvr over winsock (TCP port 49 after a
   UDP beacon on port 48): commands, data transfers, console info.
   Mixed object: the functions here are spliced into net.s
   (re/splice.py), which still holds the rest and the data, so strings
   name the .s's (splice.py drops gcc's copies; static arrays rather
   than externs so that gcc still folds strlen of them).
   wip/app/net.c is the whole draft; wip/netmixed.py makes this file
   from it. */
#include <winsock2.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;

#define SWAP32(x) (((x) << 24) + (((x) << 8) & 0xff0000) + (((x) >> 8) & 0xff00) + ((x) >> 24))

#define BEACON_MAGIC	0x4e537672	/* "NSvr" */
#define OK_REPLY	0x4f4b	/* "OK" */
/* what GTIN returns; the first 8 words come big-endian */
struct consoleinfo {
	u32 version;			/* 000 updsvr version; low byte: peek version */
	u32 kernel;			/* 004 */
	u32 f008;			/* 008 */
	u32 bootstrap;			/* 00c */
	u32 hwFlags;			/* 010 console type in the top 4 bits */
	u32 nandSize;			/* 014 */
	u32 blockSize;			/* 018 */
	u32 pairing;			/* 01c */
	u8 cpuKey[16];			/* 020 */
	u8 dvdKey[16];			/* 030 */
	u8 fuses[96];			/* 040 */
	u8 vfuses[96];			/* 0a0 */
	u8 key1bl[16];			/* 100 */
	struct {
		u32 cqw;
		u32 exp;
		u64 reserved;		/* 118 */
		u8 mod[256];
	} pub1bl;			/* 110 */
	u8 rest[0x4a0 - 0x220];		/* 220 */
};

void log_printf(int level, const char *fmt, ...);
unsigned int log_get_verbose(void);
const char *getConsoleTypeStr(int type);
u16 getBeU16(const u8 *p);
u32 getBeU32(const u8 *p);
u32 getLeU32(const u8 *p);
void setBeU32(u32 v, u8 *p);
int writeFile(const char *name, const void *buf, size_t size);

/* net.s's data */
static SOCKET netSock;
static struct consoleinfo *netInfo;
static u32 netEmpty;		/* returned for a zero-length reply */
extern time_t netStartTime;

/* strings in net.s */
static const char net_457568[] = "unable to open socket, error %d\n";
static const char net_45758c[] = "unable to set bcast socket option, error %d\n";
static const char net_4575bc[] = "unable to set bind socket, error %d\n";
static const char net_4575e1[] = "Socket error! %d\n";
static const char net_4575f3[] = "UDP wait timeout!\n";
static const char net_457608[] = "Beacon received, but the beacon magic %X was not %X!\n";
static const char net_45763e[] = "Completed in %.0fs\n";
static const char net_457688[] = "socket error sending data size, %d\n";
static const char net_4576ac[] = "socket error sending data (1), %d\n";
static const char net_4576cf[] = "sent 0x%08x of 0x%08x\r";
static const char net_4576e8[] = "could not create client socket, error %d\n";
static const char net_457712[] = "could not connect, error %d\n";
static const char net_45772f[] = "No";
static const char net_457732[] = "Yes";
static const char net_457736[] = "GTIN\n";
static const char net_45773c[] = "success!\n";
static const char net_457746[] = "connected to %s";
static const char net_457758[] = " with updsvr version %d (peek version %d)\n";
static const char net_457784[] = "NAND image size: 0x%x Block size: 0x%x Spare Data: %s\n";
static const char net_4577bb[] = "failed!\n";
static const char net_4578f5[] = "\ndisconnecting from server...";
static const char net_457913[] = "QUIT\n";
static const char net_457919[] = "OK\n";
static const char net_45791d[] = "failed\n";
static const char net_457925[] = "MTPT%s: %s\n";
static const char net_457931[] = "mounting %s to %s:...";
static const char net_457947[] = "UMPT%s:\n";
static const char net_457950[] = "unmounting %s:...";
static const char net_457962[] = "GETF%s\n";
static const char net_45796c[] = "reading flash image from console...";
static const char net_457990[] = "GTFL\n";
static const char net_457998[] = "received 0x%x bytes data OK, writing to file %s...";
static const char net_4579cb[] = "GTBL\n";
static const char net_4579d1[] = "WRFL\n";
static const char net_4579d8[] = "file sent OK, awaiting result...";
static const char net_4579f9[] = "RBLK%04x%04x\n";
static const char net_457a07[] = "WBLK%04x%04x\n";
static const char net_457a15[] = "ERBL%04x%04x\n";
static const char net_457a23[] = "GTBB\n";
static const char net_457a29[] = "FMEX\n";
static const char net_457a2f[] = "FMCM\n";
static const char net_457a35[] = "sending shutdown command...";
static const char net_457a51[] = "SHDN\n";
static const char net_457a57[] = "sending reboot command...";
static const char net_457a71[] = "REEB\n";

/* still in net.s; gcc gave it the local calling convention */
u8 *netRecv(int *len) __attribute__((regparm(1)));
u8 *netRecvVerbose(int *len, int verbose);
u32 netConnect(const char *ip);
int netWritePatches(const u8 *buf, u32 len);

void netFree(void *p)
{
	if (p && p != &netEmpty)
		free(p);
}

/* wait for the console's UDP beacon; its address, or 0 */
u32 netFindBeacon(void)
{
	SOCKET s;
	volatile u32 addr;
	int one = 1;
	struct sockaddr_in sa, from;
	int fromLen;
	u8 pkt[8];
	fd_set fds;
	struct timeval tv;
	int r;

	s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	addr = 0;
	if (s == INVALID_SOCKET) {
		log_printf(0, net_457568, WSAGetLastError());
		return addr;
	}
	if (setsockopt(s, SOL_SOCKET, SO_BROADCAST, (char *)&one, sizeof one) == SOCKET_ERROR) {
		log_printf(0, net_45758c, WSAGetLastError());
		closesocket(s);
		return addr;
	}
	memset(&sa, 0, sizeof sa);
	sa.sin_family = AF_INET;
	sa.sin_port = htons(48);
	sa.sin_addr.s_addr = INADDR_ANY;
	if (bind(s, (struct sockaddr *)&sa, sizeof sa) == SOCKET_ERROR) {
		log_printf(0, net_4575bc, WSAGetLastError());
		closesocket(s);
		return addr;
	}
	for (;;) {
		memset(pkt, 0, sizeof pkt);
		fromLen = sizeof from;
		FD_ZERO(&fds);
		FD_SET(s, &fds);
		tv.tv_sec = 30;
		tv.tv_usec = 0;
		r = select(0, &fds, NULL, NULL, &tv);
		if (r == SOCKET_ERROR) {
			log_printf(0, net_4575e1, WSAGetLastError());
			closesocket(s);
			return addr;
		}
		if (r == 0) {
			log_printf(0, net_4575f3);
			closesocket(s);
			return addr;
		}
		recvfrom(s, (char *)pkt, sizeof pkt, 0, (struct sockaddr *)&from, &fromLen);
		if (getBeU32(pkt) == BEACON_MAGIC) {
			addr = getLeU32(pkt + 4);
			break;
		}
		log_printf(0, net_457608,
			   getBeU32(pkt), BEACON_MAGIC);
	}
	closesocket(s);
	return addr;
}

void netTimerStart(void)
{
	time(&netStartTime);
}

void netTimerEnd(void)
{
	time_t now;

	time(&now);
	log_printf(0, net_45763e, difftime(now, netStartTime));
}

double netTimerElapsed(void)
{
	time_t now;

	time(&now);
	return difftime(now, netStartTime);
}

int netSendStr(const char *s)
{
	int len = strlen(s);

	if (send(netSock, s, len, 0) != len)
		return 0;
	return 1;
}

/* send a length-prefixed block */
int netSendData(const u8 *buf, u32 len, int verbose)
{
	u8 hdr[4];
	u32 sent, chunk;
	int r;

	setBeU32(len, hdr);
	if (send(netSock, (char *)hdr, 4, 0) == SOCKET_ERROR) {
		log_printf(0, net_457688, WSAGetLastError());
		return 0;
	}
	sent = 0;
	chunk = 1452;
	while (sent < len) {
		if (len - sent < 1452)
			chunk = len - sent;
		r = send(netSock, (char *)buf + sent, chunk, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, net_4576ac, WSAGetLastError());
			return 0;
		}
		sent += r;
		if (verbose)
			printf(net_4576cf, sent, len);
	}
	if (verbose)
		putchar('\n');
	return 1;
}

/* the reply to a command: "OK" */
int netCheckOk(void)
{
	int len, ok;
	u8 *r = netRecv(&len);

	if (!r)
		return 0;
	ok = 0;
	if (len == 2)
		ok = getBeU16(r) == OK_REPLY;
	netFree(r);
	return ok;
}

int netOpenSocket(u32 addr)
{
	struct sockaddr_in sa;

	netSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (netSock == INVALID_SOCKET) {
		log_printf(0, net_4576e8, WSAGetLastError());
		return 0;
	}
	sa.sin_family = AF_INET;
	sa.sin_port = htons(49);
	sa.sin_addr.s_addr = addr;
	if (connect(netSock, (struct sockaddr *)&sa, sizeof sa) < 0) {
		log_printf(0, net_457712, WSAGetLastError());
		return 0;
	}
	return 1;
}

int netReadInfo(void)
{
	u32 len;
	struct consoleinfo *info;
	int ok = 0;

	if (send(netSock, net_457736, 5, 0) == 5) {
		len = 0;
		info = (struct consoleinfo *)netRecv((int *)&len);
		if (info && len >= sizeof *info)
			ok = 1;
	}
	if (!ok) {
		log_printf(0, net_4577bb);
		return 0;
	}
	info->pub1bl.reserved = 0;
	netInfo = info;
	info->version = SWAP32(info->version);
	info->kernel = SWAP32(info->kernel);
	info->f008 = SWAP32(info->f008);
	info->bootstrap = SWAP32(info->bootstrap);
	info->hwFlags = SWAP32(info->hwFlags);
	info->nandSize = SWAP32(info->nandSize);
	info->blockSize = SWAP32(info->blockSize);
	info->pairing = SWAP32(info->pairing);
	log_printf(1, net_45773c);
	log_printf(0, net_457746, getConsoleTypeStr((netInfo->hwFlags >> 28) + 1));
	log_printf(0, net_457758,
		   netInfo->version >> 8, netInfo->version & 0xff);
	log_printf(1, net_457784,
		   netInfo->nandSize, netInfo->blockSize,
		   netInfo->nandSize == 0x3000000 ? net_45772f : net_457732);
	return 1;
}

void netClose(void)
{
	netFree(netInfo);
	if (netSock != INVALID_SOCKET)
		closesocket(netSock);
}

void netDisconnect(void)
{
	log_printf(0, net_4578f5);
	if (netSendStr(net_457913))
		log_printf(0, net_457919);
	else
		log_printf(0, net_45791d);
	netClose();
}

u32 netMount(const char *drive, const char *device)
{
	char cmd[260];

	sprintf(cmd, net_457925, drive, device);
	log_printf(1, net_457931, device, drive);
	if (netSendStr(cmd) && netCheckOk()) {
		log_printf(1, net_45773c);
		return 1;
	}
	log_printf(1, net_4577bb);
	return 0;
}

u32 netUnmount(const char *drive)
{
	char cmd[260];

	sprintf(cmd, net_457947, drive);
	log_printf(1, net_457950, drive);
	if (netSendStr(cmd) && netCheckOk()) {
		log_printf(1, net_45773c);
		return 1;
	}
	log_printf(1, net_4577bb);
	return 0;
}

u32 netGetFile(const char *name, int *len)
{
	char cmd[260];

	sprintf(cmd, net_457962, name);
	if (netSendStr(cmd))
		return (u32)netRecv(len);
	return 0;
}

struct consoleinfo *netGetInfo(void)
{
	return netInfo;
}

int netDumpNand(const char *path)
{
	int len;
	u8 *buf;

	netTimerStart();
	log_printf(0, net_45796c);
	if (send(netSock, net_457990, 5, 0) == 5) {
		buf = netRecvVerbose(&len, log_get_verbose() != 0);
		if (buf) {
			log_printf(1, net_457998, len, path);
			if (writeFile(path, buf, len))
				log_printf(0, net_45773c);
			else
				log_printf(0, net_4577bb);
			netTimerEnd();
			netFree(buf);
			return 1;
		}
	}
	log_printf(0, net_4577bb);
	return 0;
}

u32 netGetBldrs(int *len)
{
	if (netSendStr(net_4579cb))
		return (u32)netRecv(len);
	return 0;
}

u32 netSendFlash(const u8 *buf, u32 len)
{
	if (!buf || !netSendStr(net_4579d1))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0)) {
		log_printf(0, net_4577bb);
		return 0;
	}
	log_printf(0, net_4579d8);
	{
		int rlen;
		u8 *r = netRecv(&rlen);

		if (r && rlen == 2 && getBeU16(r) == OK_REPLY) {
			netFree(r);
			log_printf(0, net_45773c);
		} else {
			netFree(r);
			log_printf(0, net_4577bb);
		}
	}
	netTimerEnd();
	return 1;
}

u32 netReadBlocks(int *len, u16 start, u16 count)
{
	char cmd[32];

	sprintf(cmd, net_4579f9, start, count);
	if (netSendStr(cmd))
		return (u32)netRecvVerbose(len, log_get_verbose() != 0);
	return 0;
}

__attribute__((optimize("no-crossjumping", "no-early-inlining")))
int netWriteBlocks(const u8 *buf, u32 len, u16 start, u16 count)
{
	int rlen, ret;
	u8 *r;
	char cmd[32];

	sprintf(cmd, net_457a07, start, count);
	if (!netSendStr(cmd))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0))
		return 0;
	r = netRecv(&rlen);
	if (!r)
		return 0;
	ret = 0;
	if (rlen == 2 && getBeU16(r) == OK_REPLY)
		ret = 1;
	netFree(r);
	if (ret)
		return 1;
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netEraseBlock(u16 block, u16 count)
{
	int rlen, ret;
	u8 *r;
	char cmd[32];

	sprintf(cmd, net_457a15, block, count);
	if (!netSendStr(cmd))
		return 0;
	r = netRecv(&rlen);
	if (!r)
		return 0;
	ret = 0;
	if (rlen == 2 && getBeU16(r) == OK_REPLY)
		ret = 1;
	netFree(r);
	if (ret)
		return 1;
	return 0;
}

u32 netGetBadBlocks(int *len)
{
	if (netSendStr(net_457a23))
		return (u32)netRecv(len);
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netSendFile(const char *name, const u8 *buf, u32 len)
{
	int rlen, ret;
	u8 *r;

	/* the hint (with builtin-expect-probability=60, 55-65 work) makes the
	   shared return-0 block frequent enough to be aligned */
	if (__builtin_expect(!name, 0))
		return 0;
	if (!buf)
		return 0;
	/* buf's uses are just over IRA's callee-saved threshold */
	__asm__("" : : "m"(buf));
	char cmd[264] = "SNDF";

	strcpy(cmd + 4, name);
	strcat(cmd, "\n");
	if (!netSendStr(cmd))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0))
		return 0;
	r = netRecv(&rlen);
	if (!r)
		return 0;
	ret = 0;
	if (rlen == 2 && getBeU16(r) == OK_REPLY)
		ret = 1;
	netFree(r);
	if (ret)
		return 1;
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netFormatSysex(void)
{
	int len, ret;
	u8 *r;

	if (!netSendStr(net_457a29))
		return 0;
	r = netRecv(&len);
	if (!r)
		return 0;
	ret = 0;
	if (len == 2 && getBeU16(r) == OK_REPLY)
		ret = 1;
	netFree(r);
	if (ret)
		return 1;
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netFormatCompat(void)
{
	int len, ret;
	u8 *r;

	if (!netSendStr(net_457a2f))
		return 0;
	r = netRecv(&len);
	if (!r)
		return 0;
	ret = 0;
	if (len == 2 && getBeU16(r) == OK_REPLY)
		ret = 1;
	netFree(r);
	if (ret)
		return 1;
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netMkdir(const char *name)
{
	int rlen, ret;
	u8 *r;

	if (name) {
		char cmd[264] = "MKDR";

		strcpy(cmd + 4, name);
		strcat(cmd, "\n");
		if (!netSendStr(cmd))
			return 0;
		r = netRecv(&rlen);
		if (!r)
			return 0;
		ret = 0;
		if (rlen == 2 && getBeU16(r) == OK_REPLY)
			ret = 1;
		netFree(r);
		if (ret)
			return 1;
		return 0;
	}
	return 0;
}

int netReboot(int how)
{
	if (how == 1) {
		log_printf(0, net_457a35);
		if (netSendStr(net_457a51))
			log_printf(0, net_457919);
		else
			log_printf(0, net_45791d);
	} else if (how == 2) {
		log_printf(0, net_457a57);
		if (netSendStr(net_457a71))
			log_printf(0, net_457919);
		else
			log_printf(0, net_45791d);
	}
	return 1;
}
