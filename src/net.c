/* net: talking to the console's updsvr over winsock (TCP port 49 after a
   UDP beacon on port 48): commands, data transfers, console info */
#include <winsock2.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "xebuild.h"
#include "fileutil.h"
#include "log.h"
#include "net.h"


#define BEACON_MAGIC	0x4e537672	/* "NSvr" */
#define OK_REPLY	0x4f4b	/* "OK" */

/* not static: as a public variable *len may alias it, so sched2 keeps
   netRecv's `*len = 0` after the netSock load (anti-dependence) */
SOCKET netSock = INVALID_SOCKET;
/* gcc emits the statics in reverse: netInfo ends up first in .bss */
static uint32_t netEmpty;	/* returned for a zero-length reply */
static struct consoleinfo *netInfo;
time_t netStartTime;

void netFree(void *p)
{
	if (p && p != &netEmpty)
		free(p);
}

/* wait for the console's UDP beacon; its address, or 0 */
uint32_t netFindBeacon(void)
{
	SOCKET s;
	volatile uint32_t addr;
	int one = 1;
	struct sockaddr_in sa, from;
	int fromLen;
	uint8_t pkt[8];
	fd_set fds;
	struct timeval tv;
	int r;

	s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	addr = 0;
	if (s == INVALID_SOCKET) {
		log_printf(0, "unable to open socket, error %d\n", WSAGetLastError());
		return addr;
	}
	if (setsockopt(s, SOL_SOCKET, SO_BROADCAST, (char *)&one, sizeof one) == SOCKET_ERROR) {
		log_printf(0, "unable to set bcast socket option, error %d\n", WSAGetLastError());
		closesocket(s);
		return addr;
	}
	memset(&sa, 0, sizeof sa);
	sa.sin_family = AF_INET;
	sa.sin_port = htons(48);
	sa.sin_addr.s_addr = INADDR_ANY;
	if (bind(s, (struct sockaddr *)&sa, sizeof sa) == SOCKET_ERROR) {
		log_printf(0, "unable to set bind socket, error %d\n", WSAGetLastError());
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
			log_printf(0, "Socket error! %d\n", WSAGetLastError());
			closesocket(s);
			return addr;
		}
		if (r == 0) {
			log_printf(0, "UDP wait timeout!\n");
			closesocket(s);
			return addr;
		}
		recvfrom(s, (char *)pkt, sizeof pkt, 0, (struct sockaddr *)&from, &fromLen);
		if (getBeU32(pkt) == BEACON_MAGIC) {
			addr = getLeU32(pkt + 4);
			break;
		}
		log_printf(0, "Beacon received, but the beacon magic %X was not %X!\n",
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

	if (send(netSock, s, len, 0) != len)
		return 0;
	return 1;
}

/* receive a length-prefixed reply, with progress output if verbose;
   netRecv is its IPA-CP clone for verbose 0.  verbose is unsigned: as an
   int, uncprop reuses it for got's 0 and keeps it in a register.  The
   expect hint (with builtin-expect-probability
   65; 60 aligns the verbose size <= 0 exit) starts the verbose loop's trace
   before the shared recv-failure block.  Hinting every test also matches,
   but then IPA-CP doesn't clone.  The asm (a use of got on the short-count
   path) puts got over IRA's caller-save threshold in the clone, which
   then allocates size/buf/got to ebx/esi/edi. */
uint8_t *netRecvVerbose(int *len, uint32_t verbose)
{
	fd_set fds;
	struct timeval tv;
	uint8_t hdr[4];
	uint8_t *buf;
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
		return (uint8_t *)&netEmpty;
	}
	buf = calloc(size, 1);
	if (__builtin_expect(verbose, 0))
		printf("waiting for 0x%x bytes\n", size);
	got = 0;
	while (got < size) {
		r = select(0, &fds, NULL, NULL, &tv);
		if (r == SOCKET_ERROR || r == 0) {
			log_printf(0, "timeout waiting for data, error %d\n", WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
		}
		r = recv(netSock, (char *)buf + got, size - got, 0);
		if (r == SOCKET_ERROR) {
			if (verbose)
				putchar('\n');
			log_printf(0, "could not receive data on socket, error %d\n",
				   WSAGetLastError());
			if (buf != (uint8_t *)&netEmpty)
				free(buf);
			return NULL;
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
	__asm__ ("" : : "g"(got));
	log_printf(0, "received only %x of %x bytes! fail\n", got, size);
	if (buf != (uint8_t *)&netEmpty)
		free(buf);
	return NULL;
}

#define netRecv(len) netRecvVerbose(len, 0)

/* send a length-prefixed block */
int netSendData(const uint8_t *buf, uint32_t len, int verbose)
{
	uint8_t hdr[4];
	uint32_t sent, chunk;
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
	uint8_t *r = netRecv(&len);

	if (!r)
		return 0;
	ok = 0;
	if (len == 2)
		ok = getBeU16(r) == OK_REPLY;
	netFree(r);
	return ok;
}

int netOpenSocket(uint32_t addr)
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

/* info starts NULL so a failed send threads straight to "failed!",
   leaving the success block before it (the .rdata string order) */
int netReadInfo(void)
{
	uint32_t len;
	struct consoleinfo *info = NULL;

	if (send(netSock, "GTIN\n", 5, 0) == 5) {
		len = 0;
		info = (struct consoleinfo *)netRecv((int *)&len);
	}
	if (info && len >= sizeof *info) {
		info->pub1bl.reserved = 0;
		netInfo = info;
		info->version = SWAP32(info->version);
		info->kernel = SWAP32(info->kernel);
		info->usvrFlags = SWAP32(info->usvrFlags);
		info->bootstrap = SWAP32(info->bootstrap);
		info->hwFlags = SWAP32(info->hwFlags);
		info->nandSize = SWAP32(info->nandSize);
		info->blockSize = SWAP32(info->blockSize);
		info->pairing = SWAP32(info->pairing);
		log_printf(1, "success!\n");
		log_printf(0, "connected to %s", getConsoleTypeStr((netInfo->hwFlags >> 28) + 1));
		log_printf(0, " with updsvr version %d (peek version %d)\n",
			   netInfo->version >> 8, netInfo->version & 0xff);
		log_printf(1, "NAND image size: 0x%x Block size: 0x%x Spare Data: %s\n",
			   netInfo->nandSize, netInfo->blockSize,
			   netInfo->nandSize == 0x3000000 ? "No" : "Yes");
		return 1;
	}
	log_printf(0, "failed!\n");
	return 0;
}

/* Failures fall through to one return 0.  Each branch has its own sockaddr
   (the socket code written out, as in netOpenSocket) and its own
   netReadInfo: the branch's clobber block keeps phiopt off the readinfo
   test, ce2 speculates the 1 into both copies and jump2 crossjumps them;
   goto ok keeps the success block from following the test.  The beacon
   branch tests a connected flag (netOpenSocket inlined, as it were): jump
   threading moves its success block to the end of the function, where the
   original's .rdata has its string. */
uint32_t netConnect(const char *ip)
{
	WSADATA wsa;

	if (WSAStartup(MAKEWORD(2, 2), &wsa) == 0) {
		if (ip == NULL) {
			struct sockaddr_in server;
			uint32_t addr;
			int connected = 0;

			log_printf(0, "started, watching network for xbox...");
			addr = netFindBeacon();
			if (addr != 0) {
				log_printf(0, "success, found xbox beacon at %u.%u.%u.%u\n",
					   addr & 0xff, (addr >> 8) & 0xff, (addr >> 16) & 0xff, addr >> 24);
				log_printf(1, "attempting to connect...");
				netSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
				if (netSock != INVALID_SOCKET) {
					server.sin_family = AF_INET;
					server.sin_port = htons(49);
					server.sin_addr.s_addr = addr;
					if (connect(netSock, (struct sockaddr *)&server, sizeof server) >= 0)
						connected = 1;
					else
						log_printf(0, "could not connect, error %d\n",
							   WSAGetLastError());
				} else
					log_printf(0, "could not create client socket, error %d\n",
						   WSAGetLastError());
				if (connected) {
					log_printf(1, "success!\nGetting console info...");
					if (netReadInfo())
						goto ok;
				}
			} else
				log_printf(0, "failed to find xbox beacon\n");
		} else {
			struct sockaddr_in sa, server;
			int saLen = sizeof sa;
			uint32_t addr;

			if (WSAStringToAddressA((char *)ip, AF_INET, NULL, (struct sockaddr *)&sa, &saLen) == 0) {
				log_printf(0, "attempting forced connection to %u.%u.%u.%u...",
					   sa.sin_addr.S_un.S_un_b.s_b1, sa.sin_addr.S_un.S_un_b.s_b2,
					   sa.sin_addr.S_un.S_un_b.s_b3, sa.sin_addr.S_un.S_un_b.s_b4);
				addr = sa.sin_addr.s_addr;
				netSock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
				if (netSock != INVALID_SOCKET) {
					server.sin_family = AF_INET;
					server.sin_port = htons(49);
					server.sin_addr.s_addr = addr;
					if (connect(netSock, (struct sockaddr *)&server, sizeof server) >= 0) {
						log_printf(0, "success!\n");
						if (netReadInfo())
							goto ok;
					} else
						log_printf(0, "could not connect, error %d\n",
							   WSAGetLastError());
				} else
					log_printf(0, "could not create client socket, error %d\n",
						   WSAGetLastError());
			} else
				log_printf(0, "attempting to convert %s to an address failed, error %d\n",
					   ip, WSAGetLastError());
		}
	} else
		log_printf(0, "WSAStartup failed, error %d\n", WSAGetLastError());
	return 0;
ok:
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

uint32_t netMount(const char *drive, const char *device)
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

uint32_t netUnmount(const char *drive)
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

uint8_t *netGetFile(const char *name, int *len)
{
	char cmd[260];

	sprintf(cmd, "GETF%s\n", name);
	if (netSendStr(cmd))
		return netRecv(len);
	return 0;
}

struct consoleinfo *netGetInfo(void)
{
	return netInfo;
}

int netDumpNand(const char *path)
{
	int len;
	uint8_t *buf;

	netTimerStart();
	log_printf(0, "reading flash image from console...");
	if (send(netSock, "GTFL\n", 5, 0) == 5) {
		buf = netRecvVerbose(&len, log_get_verbose() != 0);
		if (buf) {
			log_printf(1, "received 0x%x bytes data OK, writing to file %s...",
				   len, path);
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

uint8_t *netGetBldrs(int *len)
{
	if (netSendStr("GTBL\n"))
		return netRecv(len);
	return 0;
}

uint32_t netSendFlash(const uint8_t *buf, uint32_t len)
{
	if (!buf || !netSendStr("WRFL\n"))
		return 0;
	if (!netSendData(buf, len, log_get_verbose() != 0)) {
		log_printf(0, "failed!\n");
		return 0;
	}
	log_printf(0, "file sent OK, awaiting result...");
	{
		int rlen;
		uint8_t *r = netRecv(&rlen);

		if (r && rlen == 2 && getBeU16(r) == OK_REPLY) {
			netFree(r);
			log_printf(0, "success!\n");
		} else {
			netFree(r);
			log_printf(0, "failed!\n");
		}
	}
	netTimerEnd();
	return 1;
}

uint8_t *netReadBlocks(int *len, uint16_t start, uint16_t count)
{
	char cmd[32];

	sprintf(cmd, "RBLK%04x%04x\n", start, count);
	if (netSendStr(cmd))
		return netRecvVerbose(len, log_get_verbose() != 0);
	return 0;
}

__attribute__((optimize("no-crossjumping", "no-early-inlining")))
int netWriteBlocks(const uint8_t *buf, uint32_t len, uint16_t start, uint16_t count)
{
	int rlen, ret;
	uint8_t *r;
	char cmd[32];

	sprintf(cmd, "WBLK%04x%04x\n", start, count);
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

int netEraseBlock(uint16_t block, uint16_t count)
{
	int ret;
	uint8_t *r;
	char cmd[32];

	sprintf(cmd, "ERBL%04x%04x\n", block, count);
	{
		int rlen;

		if (!netSendStr(cmd))
			return 0;
		r = netRecv(&rlen);
		if (!r)
			return 0;
		ret = rlen == 2 && getBeU16(r) == OK_REPLY;
		netFree(r);
	}
	if (ret)
		return 1;
	return 0;
}

uint8_t *netGetBadBlocks(int *len)
{
	if (netSendStr("GTBB\n"))
		return netRecv(len);
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netSendFile(const char *name, const void *buf, uint32_t len)
{
	int rlen, ret;
	uint8_t *r;

	/* the hint (with builtin-expect-probability=65, 55-65 work) makes the
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

int netFormatSysex(void)
{
	int ret;
	uint8_t *r;

	{
		int len;

		if (!netSendStr("FMEX\n"))
			return 0;
		r = netRecv(&len);
		if (!r)
			return 0;
		ret = len == 2 && getBeU16(r) == OK_REPLY;
		netFree(r);
	}
	if (ret)
		return 1;
	return 0;
}

int netFormatCompat(void)
{
	int ret;
	uint8_t *r;

	{
		int len;

		if (!netSendStr("FMCM\n"))
			return 0;
		r = netRecv(&len);
		if (!r)
			return 0;
		ret = len == 2 && getBeU16(r) == OK_REPLY;
		netFree(r);
	}
	if (ret)
		return 1;
	return 0;
}

__attribute__((optimize("no-crossjumping")))
int netMkdir(const char *name)
{
	int rlen, ret;
	uint8_t *r;

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
		log_printf(0, "sending shutdown command...");
		if (netSendStr("SHDN\n"))
			log_printf(0, "OK\n");
		else
			log_printf(0, "failed\n");
	} else if (how == 2) {
		log_printf(0, "sending reboot command...");
		if (netSendStr("REEB\n"))
			log_printf(0, "OK\n");
		else
			log_printf(0, "failed\n");
	}
	return 1;
}

__attribute__((optimize("no-early-inlining")))
int netWritePatches(const uint8_t *buf, uint32_t len)
{
	int ret;
	uint8_t *r;

	{
		int rlen;

		if (!netSendStr("WBPT\n") || !netSendData(buf, len, 0) || !(r = netRecv(&rlen)))
			return 0;
		ret = rlen == 2 && getBeU16(r) == OK_REPLY;
		netFree(r);
	}
	if (ret)
		return 1;
	return 0;
}
