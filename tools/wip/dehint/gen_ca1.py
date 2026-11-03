"""Plain baseline shapes of sendAvatarData."""
PREP = r'''
int prepSysex(void)
{
	if (netFormatSysex()) {
		if (netMount(SYSEX, "\\SEP"))
			return createSysexDirs();
		log_printf(0, "ERROR: unable to mount sysex partition!\n");
	} else
		log_printf(0, "ERROR: unable to format sysex partition!\n");
	return 0;
}
'''

BODY = r'''
long sendAvatarData(const char *dir, uint32_t ver)
{
	int i;
	long ret;

	netTimerStart();
	log_printf(0, "loading avatar data...\n");
	ver &= ~0xf;
	addTitleId(ver);
	if (loadManifest(dir, ver)) {
		log_printf(0, "success!\nFormatting HDD partition...\n");
		ret = 1;
		if (prepSysex()) {
			log_printf(0, "success!\nSending avatar files to HDD partition...\n");
			log_printf(1, "sending %d items to xbox\n", manifest.count);
			for (i = 0; i < manifest.count; i++) {
				log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, manifest.e[i].len,
					manifest.e[i].len, manifest.e[i].path);
				ret = netSendFile(manifest.e[i].path, manifest.e[i].data, manifest.e[i].len);
				if (!ret) {
					log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.e[i].path);
					goto out;
				}
			}
			log_printf(1, "sending manifest to %s\n", manifest.path);
			if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
				ret = 0;
				log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
			} else {
				log_printf(0, "success! Avatar data is successfully sent to the console!\n");
				netTimerEnd();
				ret = 1;
			}
		}
out:
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''


def variants():
    yield 'plain', PREP + BODY
