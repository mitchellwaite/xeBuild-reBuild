# clientWriteBlocks: shapes for the .rdata literal order without the asm "i" hint
OLD = '''	if (start == -1) {
		log_printf(0, "\\n\\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\\n");
		return;
	}
	/* .rdata order hint: these come before the read error (a nested
	   success-first shape moves the error blocks) */
	__asm__("" :: "i"("Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\\n"),
		"i"("Done! Wrote 0x%x (%d) bytes to console flash!\\n"),
		"i"("\\n\\n***** ERROR: Writing data to console failed!\\n"),
		"i"("\\n\\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\\n"));
	buf = FileToBuffer(file, (size_t *)&len);
	if (!buf || len <= 0) {
		log_printf(0, "\\n\\n***** ERROR: Unable to read file %s!\\n", file);
		return;
	}
	n = len / cinfo->blockSize;
	if (!(len % cinfo->blockSize)) {
		if (start + n <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\\n", n, n, start, start);
			if (netWriteBlocks(buf, len, start, n))
				log_printf(0, "Done! Wrote 0x%x (%d) bytes to console flash!\\n", len, len);
			else
				log_printf(0, "\\n\\n***** ERROR: Writing data to console failed!\\n");
		} else
			log_printf(0, "\\n\\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\\n", cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, "\\n\\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\\n", file, len, cinfo->blockSize);
	free(buf);
}'''
INV = '''		log_printf(0, "\\n\\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\\n");
'''
RD = '''log_printf(0, "\\n\\n***** ERROR: Unable to read file %s!\\n", file);'''
CORE = '''	n = len / cinfo->blockSize;
	if (!(len % cinfo->blockSize)) {
		if (start + n <= cinfo->nandSize / cinfo->blockSize) {
			log_printf(0, "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\\n", n, n, start, start);
			if (netWriteBlocks(buf, len, start, n))
				log_printf(0, "Done! Wrote 0x%x (%d) bytes to console flash!\\n", len, len);
			else
				log_printf(0, "\\n\\n***** ERROR: Writing data to console failed!\\n");
		} else
			log_printf(0, "\\n\\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\\n", cinfo->nandSize / cinfo->blockSize);
	} else
		log_printf(0, "\\n\\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\\n", file, len, cinfo->blockSize);
	free(buf);
'''


def ind(s, k=1):
    return '\n'.join(('\t' * k + l) if l else l for l in s.split('\n'))


EARLY = '''	if (start == -1) {
''' + INV + '''		return;
	}
	buf = FileToBuffer(file, (size_t *)&len);
'''
V = {
    'nohint': [(OLD, EARLY + '''	if (!buf || len <= 0) {
		''' + RD + '''
		return;
	}
''' + CORE + '}')],
    'nest_read': [(OLD, EARLY + '''	if (buf && len > 0) {
''' + ind(CORE) + '''	} else
		''' + RD + '\n}')],
    'nest_read_ret': [(OLD, EARLY + '''	if (buf && len > 0) {
''' + ind(CORE) + '''		return;
	}
	''' + RD + '\n}')],
    'nest_read_ret2': [(OLD, EARLY + '''	if (buf && len > 0) {
''' + ind(CORE) + '''		return;
	} else
		''' + RD + '\n}')],
    'nest_all': [(OLD, '''	if (start != -1) {
		buf = FileToBuffer(file, (size_t *)&len);
		if (buf && len > 0) {
''' + ind(CORE, 2) + '''		} else
			''' + RD + '''
	} else
''' + INV + '}')],
    'nest_all_ret': [(OLD, '''	if (start != -1) {
		buf = FileToBuffer(file, (size_t *)&len);
		if (buf && len > 0) {
''' + ind(CORE, 2) + '''			return;
		}
		''' + RD + '''
	} else
''' + INV + '}')],
    'early_ret_free': [(OLD, EARLY + '''	if (!buf || len <= 0) {
		''' + RD + '''
		return;
	}
''' + CORE + '	return;\n}')],
}
