"""Attempt 6: a5while with i live after the loop ("all sent" instead of the flag), to refuse find_if_case_2 (i live at then).
Axes: head x body order x failure stop x post-loop test x item."""
import itertools, re, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A5 = open(os.path.join(ROOT, 'tools', 'wip', 'dehint', 'drafts', 'console_hdd_sendAvatarData_a5while.c')).read()
PREP = A5[A5.index('int prepSysex(void)'):A5.index('long sendAvatarData')]

LOG = r'log_printf(1, "sending %03d: 0x%08x (%d) bytes, %s\n", i + 1, e->len, e->len, e->path);'
SEND = 'ret = netSendFile(e->path, e->data, e->len);'
FAIL = r'log_printf(0, "aborting sending avatar data, failed to send %s\n", e->path);'
MFS = r'log_printf(1, "sending manifest to %s\n", manifest.path);'
ARMS = r'''if (!netSendFile(manifest.path, manifest.data, manifest.size)) {
ret = 0;
log_printf(0, "aborting sending avatar data, failed to send %s\n", manifest.path);
} else {
log_printf(0, "success! Avatar data is successfully sent to the console!\n");
netTimerEnd();
ret = 1;
}
'''
FRAME = r'''long sendAvatarData(const char *dir, uint32_t ver)
{
	int i;
	long ret;
	int n;

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
@LOOP@
@TAIL@
		}
		netUnmount(SYSEX);
		freeManifest();
	} else {
		log_printf(0, "***** WARNING: avatar data skipped, unable to load data!\n");
		ret = 1;
	}
	return ret;
}
'''
HEADS = {'wh': 'while (i < n) {', 'wr': 'while (i < n && ret) {', 'rw': 'while (ret && i < n) {', 'wa': 'while ((i < n) & (ret != 0)) {'}
# what ends the body; %(f)s is the failure log
STOPS = {
    'brk': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\nbreak;\n}\n',
    'brk2': 'if (!ret) {\n%(f)s\nbreak;\n}\nn = manifest.count;\ni++;\n',
    'log': 'n = manifest.count;\ni += ret != 0;\nif (!ret)\n%(f)s\n',
    'neg': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = -1;\n}\n',
    'big': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n + 1;\n}\n',
    'iN': 'n = manifest.count;\ni += ret != 0;\nif (!ret) {\n%(f)s\ni = n;\n}\n',
}
POST = {
    'ret': 'if (ret) {',
    'ge': 'if (i >= n) {',
    'eq': 'if (i == n) {',
    'nlt': 'if (!(i < n)) {',
    'ger': 'if (i >= n && ret) {',
    'rge': 'if (ret && i >= n) {',
    'eqr': 'if (i == n && ret) {',
    'req': 'if (ret && i == n) {',
    'and': 'if ((i >= n) & (ret != 0)) {',
    'gec': 'if (i >= manifest.count) {',
    'eqc': 'if (i == manifest.count) {',
    'gecr': 'if (ret && i >= manifest.count) {',
    'eqcr': 'if (ret && i == manifest.count) {',
    'pos': 'if (i >= 0) {',
    'posr': 'if (ret && i >= 0) {',
}
ITEM = 'struct manifestItem *e = &manifest.e[(size_t)i];\n'


def variants():
    for h, st, p in itertools.product(HEADS, STOPS, POST):
        body = ITEM + LOG + '\n' + SEND + '\n' + STOPS[st] % {'f': FAIL}
        loop = 'i = 0;\nn = manifest.count;\n' + HEADS[h] + '\n' + body + '}\n'
        tail = POST[p] + '\n' + MFS + '\n' + ARMS + '}\n'
        yield '|'.join((h, st, p)), PREP + FRAME.replace('@LOOP@', loop).replace('@TAIL@', tail)
