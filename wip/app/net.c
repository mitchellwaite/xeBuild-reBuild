/* net: talking to the console's updsvr over winsock (TCP port 49 after a
   UDP beacon on port 48): commands, data transfers, console info */
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

static SOCKET netSock = INVALID_SOCKET;
static struct consoleinfo *netInfo;
static u32 netEmpty;		/* returned for a zero-length reply */
time_t netStartTime;

/* receive a length-prefixed reply */
static u8 *netRecv(int *len)
{
	fd_set fds;
	struct timeval tv;
	u8 hdr[4];
	u8 *buf;
	int size, got, r;

	tv.tv_sec = 15;
	tv.tv_usec = 0;
	FD_ZERO(&fds);
	FD_SET(netSock, &fds);
	*len = 0;
	r = select(0, &fds, NULL, NULL, &tv);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "timeout waiting for data, %d\n", WSAGetLastError());
		return NULL;
	}
	r = recv(netSock, (char *)hdr, 4, 0);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "unable to fetch first 4 bytes, %d\n", WSAGetLastError());
		return NULL;
	}
	size = getBeU32(hdr);
	if (size == -1)
		return NULL;
	if (size == 0) {
		*len = 0;
		return (u8 *)&netEmpty;
	}
	buf = calloc(size, 1);
	got = 0;
	while (got < size) {
		r = select(0, &fds, NULL, NULL, &tv);
		if (r == SOCKET_ERROR || r == 0) {
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			goto fail;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			log_printf(0, "could not receive data on socket, error %d\n", WSAGetLastError());
			goto fail;
		}
		got += r;
	}
	if (got != size) {
		log_printf(0, "received only %x of %x bytes! fail\n", got, size);
		goto fail;
	}
	*len = size;
	return buf;
fail:
	if (buf != (u8 *)&netEmpty)
		free(buf);
	return NULL;
}

void netFree(void *p)
{
	if (p && p != &netEmpty)
		free(p);
}

/* wait for the console's UDP beacon; its address, or 0 */
u32 netFindBeacon(void)
{
	SOCKET s;
	int one = 1;
	u32 addr = 0;
	struct sockaddr_in sa, from;
	int fromLen;
	u8 pkt[8];
	fd_set fds;
	struct timeval tv;
	int r;

	s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (s == INVALID_SOCKET) {
		log_printf(0, "unable to open socket, error %d\n", WSAGetLastError());
		return addr;
	}
	if (setsockopt(s, SOL_SOCKET, SO_BROADCAST, (char *)&one, sizeof one) == SOCKET_ERROR) {
		log_printf(0, "unable to set bcast socket option, error %d\n", WSAGetLastError());
		goto out;
	}
	memset(&sa, 0, sizeof sa);
	sa.sin_family = AF_INET;
	sa.sin_port = htons(48);
	sa.sin_addr.s_addr = INADDR_ANY;
	if (bind(s, (struct sockaddr *)&sa, sizeof sa) == SOCKET_ERROR) {
		log_printf(0, "unable to set bind socket, error %d\n", WSAGetLastError());
		goto out;
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
			log_printf(0, "Socket error! %d\n", WSAGetLastError());
			break;
		}
		if (r == 0) {
			log_printf(0, "UDP wait timeout!\n");
			break;
		}
		recvfrom(s, (char *)pkt, sizeof pkt, 0, (struct sockaddr *)&from, &fromLen);
		if (getBeU32(pkt) == BEACON_MAGIC) {
			addr = getLeU32(pkt + 4);
			break;
		}
		log_printf(0, "Beacon received, but the beacon magic %X was not %X!\n",
			   getBeU32(pkt), BEACON_MAGIC);
	}
out:
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
	log_printf(0, "Completed in %.0fs\n", difftime(now, netStartTime));
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

	return send(netSock, s, len, 0) == len;
}

/* netRecv with progress output */
u8 *netRecvVerbose(int *len, int verbose)
{
	fd_set fds;
	struct timeval tv;
	u8 hdr[4];
	u8 *buf;
	int size, got, r;

	tv.tv_sec = 15;
	tv.tv_usec = 0;
	FD_ZERO(&fds);
	FD_SET(netSock, &fds);
	*len = 0;
	r = select(0, &fds, NULL, NULL, &tv);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "timeout waiting for data, %d\n", WSAGetLastError());
		return NULL;
	}
	r = recv(netSock, (char *)hdr, 4, 0);
	if (r == SOCKET_ERROR || r == 0) {
		log_printf(0, "unable to fetch first 4 bytes, %d\n", WSAGetLastError());
		return NULL;
	}
	size = getBeU32(hdr);
	if (size == -1)
		return NULL;
	if (size == 0) {
		*len = 0;
		return (u8 *)&netEmpty;
	}
	buf = calloc(size, 1);
	if (verbose)
		printf("waiting for 0x%x bytes\n", size);
	got = 0;
	while (got < size) {
		r = select(0, &fds, NULL, NULL, &tv);
		if (r == SOCKET_ERROR || r == 0) {
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			goto fail;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %d\n", WSAGetLastError());
			goto fail;
		}
		got += r;
		if (verbose)
			printf("received 0x%08x of 0x%08x\r", got, size);
	}
	if (verbose)
		putchar('\n');
	if (got == size) {
		*len = size;
		return buf;
	}
	if (verbose)
		putchar('\n');
	log_printf(0, "received only %x of %x bytes! fail\n", got, size);
fail:
	if (buf != (u8 *)&netEmpty)
		free(buf);
	return NULL;
}

/* send a length-prefixed block */
int netSendData(const u8 *buf, u32 len, int verbose)
{
	u8 hdr[4];
	u32 sent, chunk;
	int r;

	setBeU32(len, hdr);
	if (send(netSock, (char *)hdr, 4, 0) == SOCKET_ERROR) {
		log_printf(0, "socket error sending data size, %d\n", WSAGetLastError());
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
			log_printf(0, "socket error sending data (1), %d\n", WSAGetLastError());
			return 0;
		}
		sent += r;
		if (verbose)
			printf("sent 0x%08x of 0x%08x\r", sent, len);
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
		log_printf(0, "could not create client socket, error %d\n", WSAGetLastError());
		return 0;
	}
	sa.sin_family = AF_INET;
	sa.sin_port = htons(49);
	sa.sin_addr.s_addr = addr;
	if (connect(netSock, (struct sockaddr *)&sa, sizeof sa) < 0) {
		log_printf(0, "could not connect, error %d\n", WSAGetLastError());
		return 0;
	}
	return 1;
}

int netReadInfo(void)
{
	u32 len;
	u32 *p;
	int i;
	struct consoleinfo *info;

	if (netSendStr("GTIN\n")) {
		len = 0;
		info = (struct consoleinfo *)netRecv((int *)&len);
		if (info && len >= sizeof *info) {
			info->pub1bl.reserved = 0;
			netInfo = info;
			p = (u32 *)info;
			for (i = 0; i < 8; i++)
				p[i] = SWAP32(p[i]);
			log_printf(1, "success!\n");
			log_printf(0, "connected to %s", getConsoleTypeStr((netInfo->hwFlags >> 28) + 1));
			log_printf(0, " with updsvr version %d (peek version %d)\n",
				   netInfo->version >> 8, netInfo->version & 0xff);
			log_printf(1, "NAND image size: 0x%x Block size: 0x%x Spare Data: %s\n",
				   netInfo->nandSize, netInfo->blockSize,
				   netInfo->nandSize == 0x3000000 ? "No" : "Yes");
			return 1;
		}
	}
	log_printf(0, "failed!\n");
	return 0;
}

int netConnect(const char *ip)
{
	WSADATA wsa;
	struct sockaddr_in sa;
	int saLen;
	u32 addr;

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
		log_printf(0, "WSAStartup failed, error %d\n", WSAGetLastError());
		return 0;
	}
	if (!ip) {
		log_printf(0, "started, watching network for xbox...");
		addr = netFindBeacon();
		if (!addr) {
			log_printf(0, "failed to find xbox beacon\n");
			return 0;
		}
		log_printf(0, "success, found xbox beacon at %u.%u.%u.%u\n",
			   addr & 0xff, (addr >> 8) & 0xff, (addr >> 16) & 0xff, addr >> 24);
		log_printf(1, "attempting to connect...");
		if (!netOpenSocket(addr))
			return 0;
		log_printf(1, "success!\nGetting console info...");
	} else {
		saLen = sizeof sa;
		if (WSAStringToAddressA((char *)ip, AF_INET, NULL, (struct sockaddr *)&sa, &saLen) != 0) {
			log_printf(0, "attempting to convert %s to an address failed, error %d\n",
				   ip, WSAGetLastError());
			return 0;
		}
		log_printf(0, "attempting forced connection to %u.%u.%u.%u...",
			   sa.sin_addr.S_un.S_un_b.s_b1, sa.sin_addr.S_un.S_un_b.s_b2,
			   sa.sin_addr.S_un.S_un_b.s_b3, sa.sin_addr.S_un.S_un_b.s_b4);
		if (!netOpenSocket(sa.sin_addr.s_addr))
			return 0;
		log_printf(0, "success!\n");
	}
	if (!netReadInfo())
		return 0;
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
	log_printf(0, "\ndisconnecting from server...");
	if (netSendStr("QUIT\n"))
		log_printf(0, "OK\n");
	else
		log_printf(0, "failed\n");
	netClose();
}

int netMount(const char *drive, const char *device)
{
	char cmd[260];

	sprintf(cmd, "MTPT%s: %s\n", drive, device);
	log_printf(1, "mounting %s to %s:...", device, drive);
	if (netSendStr(cmd) && netCheckOk()) {
		log_printf(1, "success!\n");
		return 1;
	}
	log_printf(1, "failed!\n");
	return 0;
}

int netUnmount(const char *drive)
{
	char cmd[260];

	sprintf(cmd, "UMPT%s:\n", drive);
	log_printf(1, "unmounting %s:...", drive);
	if (netSendStr(cmd) && netCheckOk()) {
		log_printf(1, "success!\n");
		return 1;
	}
	log_printf(1, "failed!\n");
	return 0;
}

u8 *netGetFile(const char *name, int *len)
{
	char cmd[260];

	sprintf(cmd, "GETF%s\n", name);
	if (netSendStr(cmd))
		return netRecv(len);
	return NULL;
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
	log_printf(0, "reading flash image from console...");
	if (netSendStr("GTFL\n")) {
		buf = netRecvVerbose(&len, log_get_verbose() != 0);
		if (buf) {
			log_printf(1, "received 0x%x bytes data OK, writing to file %s...", len, path);
			if (writeFile(path, buf, len))
				log_printf(0, "success!\n");
			else
				log_printf(0, "failed!\n");
			netTimerEnd();
			netFree(buf);
			return 1;
		}
	}
	log_printf(0, "failed!\n");
	return 0;
}

u8 *netGetBldrs(int *len)
{
	if (netSendStr("GTBL\n"))
		return netRecv(len);
	return NULL;
}

int netSendFlash(const u8 *buf, u32 len)
{
	if (!buf || !netSendStr("WRFL\n"))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0)) {
		log_printf(0, "failed!\n");
		return 0;
	}
	log_printf(0, "file sent OK, awaiting result...");
	if (netCheckOk())
		log_printf(0, "success!\n");
	else
		log_printf(0, "failed!\n");
	netTimerEnd();
	return 1;
}

u8 *netReadBlocks(int *len, u16 start, u16 count)
{
	char cmd[32];

	sprintf(cmd, "RBLK%04x%04x\n", start, count);
	if (netSendStr(cmd))
		return netRecvVerbose(len, log_get_verbose() != 0);
	return NULL;
}

int netWriteBlocks(const u8 *buf, u32 len, u16 start, u16 count)
{
	char cmd[32];

	sprintf(cmd, "WBLK%04x%04x\n", start, count);
	if (!netSendStr(cmd))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0))
		return 0;
	return netCheckOk();
}

int netEraseBlock(u16 block, u16 count)
{
	char cmd[32];

	sprintf(cmd, "ERBL%04x%04x\n", block, count);
	if (!netSendStr(cmd))
		return 0;
	return netCheckOk();
}

u8 *netGetBadBlocks(int *len)
{
	if (netSendStr("GTBB\n"))
		return netRecv(len);
	return NULL;
}

int netSendFile(const char *name, const u8 *buf, u32 len)
{
	char cmd[264] = "SNDF";

	if (!name || !buf)
		return 0;
	strcpy(cmd + 4, name);
	strcat(cmd, "\n");
	if (!netSendStr(cmd))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0))
		return 0;
	return netCheckOk();
}

int netFormatSysex(void)
{
	if (!netSendStr("FMEX\n"))
		return 0;
	return netCheckOk();
}

int netFormatCompat(void)
{
	if (!netSendStr("FMCM\n"))
		return 0;
	return netCheckOk();
}

int netMkdir(const char *name)
{
	char cmd[264] = "MKDR";

	if (!name)
		return 0;
	strcpy(cmd + 4, name);
	strcat(cmd, "\n");
	if (!netSendStr(cmd))
		return 0;
	return netCheckOk();
}

int netReboot(int how)
{
	int ok;

	if (how == 1) {
		log_printf(0, "sending shutdown command...");
		ok = netSendStr("SHDN\n");
	} else if (how == 2) {
		log_printf(0, "sending reboot command...");
		ok = netSendStr("REEB\n");
	} else
		return 1;
	if (ok)
		log_printf(0, "OK\n");
	else
		log_printf(0, "failed\n");
	return 1;
}

int netWritePatches(const u8 *buf, u32 len)
{
	if (!netSendStr("WBPT\n"))
		return 0;
	if (!netSendData(buf, len, 0))
		return 0;
	return netCheckOk();
}
