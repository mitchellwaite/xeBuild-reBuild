/* the option's argument(s); dies with usage if one is missing or, with
   check, if a mode was already set */
NOPROF
char *getArgs(int argc, char **argv, int *pi, int mode, int check, char **arg2, char **arg3)
{
	int first = *pi + 1;
	int i = first;
	char *a = argv[i];

	if (i == argc || !a || *a == '-')
		client_usage(3, argv[first - 1]);
	if (arg2) {
		i++;
		a = argv[i];
		if (!a || i == argc || *a == '-')
			client_usage(4, argv[first - 1]);
		*arg2 = a;
	}
	if (arg3) {
		i++;
		a = argv[i];
		if (!a || i == argc || *a == '-')
			client_usage(4, argv[first - 1]);
		*arg3 = a;
	}
	if (mode && check)
		client_usage(5, argv[first - 1]);
	*pi = i;
	return argv[first];
}

#define E(x) __builtin_expect((x), 1)
int mode_client(int argc, char **argv)
{
	char dummy[] = "dummy";
	char *start = NULL, *count = NULL;
	int i = 0;
	int reboot = 0;
	char *ip = NULL;
	char *arg = NULL;
	int mode = 0;
	char *a, *b;
	int j;

	log_set_name("client");
	for (i = 0; i < argc; i++) {
 if ((char *)__builtin_constant_p(i + 60) == (char *)1 && (char *)__builtin_constant_p(i + 61) == (char *)1 && __builtin_constant_p(i + 777100)) goto wb3;
if (__builtin_constant_p(i + 320) && __builtin_constant_p(i + 321)) goto u2;
		if (!strnicmp(argv[i], "help", 2) || !strnicmp(argv[i], "-?", 2) || !strnicmp(argv[i], "/?", 2))
			client_usage(0, NULL);
		if (!strnicmp(argv[i], "-noenter", 8)) {
			log_printf(0, "<enter> key on completion suppressed\n");
			promptEnter = 0;
		} else if (!strnicmp(argv[i], "-reboot", 7)) {
			if (reboot == 1)
				log_printf(0, "shutdown superseded by reboot, ignoring -s in favor of -reboot\n");
			log_printf(0, "setting reboot on completion\n");
			reboot = 2;
		} else if (E(!strnicmp(argv[i], "-bp", 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			__asm__("" :: "a"(i + 1));
			__asm__("" :: "r"((unsigned)(i + 1) * 4));
			b = argv[i + 2];
			j = i + 2;
			if (j == argc || !b || *b == '-')
				lu1: client_usage(4, argv[i]);
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i = j;
			arg = argv[i - 1];
			log_printf(0, "setting binary patch file to %s, offset %s\n", arg, start);
			mode = 11;
		} else if (!strnicmp(argv[i], "-rb", 3)) {
			arg = getArgs(argc, argv, &i, mode, 1, &start, &count);
			log_printf(0, "reading %s blocks to %s, starting block %s\n", count, arg, start);
			mode = 8;
		} else if (E(!strnicmp(argv[i], "-wb", 3))) {
			j = i + 1;
			a = argv[j];
			if (j == argc || !a || *a == '-')
				{ wb3: client_usage(3, argv[i]); }
			__asm__("" :: "r"((unsigned)j * 4));
			__asm__("" :: "r"((unsigned)j * 4));
			{ int k = i + 2; b = argv[k];
			if (!b || k == argc || *b == '-')
				client_usage(4, argv[i]); }
			start = b;
			if (mode)
				client_usage(5, argv[i]);
			i += 2;
			arg = argv[i - 1];
			log_printf(0, "writing blocks from %s, starting at block %s\n", arg, start);
			mode = 9;
		} else if (E(!strnicmp(argv[i], "-eb", 3))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "erase block set to %s\n", arg);
			mode = 10;
		} else if (!strnicmp(argv[i], "-s", 2)) {
			if ((char *)__builtin_constant_p(i + 300) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 1) == (char *)1 && (char *)__builtin_constant_p(i + 300 + 2) == (char *)1) goto k61l;
if (__builtin_constant_p(i + 300)) goto cdef;
if (reboot == 2)
				log_printf(0, "reboot has already been set on command line, ignoring -s\n");
			else {
				log_printf(0, "setting shutdown on completion\n");
				reboot = 1;
			}
		} else if (!strnicmp(argv[i], "-keys", 5)) {
			mode = 3;
			arg = dummy;
		} else if (!strnicmp(argv[i], "-ip", 3)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			

if ((char *)__builtin_constant_p(i + 30) == (char *)1 && (char *)__builtin_constant_p(i + 31) == (char *)1) goto k55l;  if ((char *)__builtin_constant_p(i + 40) == (char *)1 && (char *)__builtin_constant_p(i + 41) == (char *)1 && (char *)__builtin_constant_p(i + 42) == (char *)1) goto k67l;
ip = argv[++i];
			log_printf(0, "setting forced IP to %s\n", ip);
		} else { k55l: if (!strnicmp(argv[i], "-r", 2)) {
			a = argv[i + 1];
			if (({__asm__ goto("" :::: r5x, r3x); 0;}) || i + 1 == argc || !a || *a == '-')
				{ r3x: client_usage(3, argv[i]); }
			if (mode) { r5x: client_usage(5, argv[i]); }
			arg = argv[++i];
			log_printf(0, "setting read filename to %s\n", arg); if (__builtin_constant_p(i + 5555)) goto k61l;
			mode = 1;
		} else { k61l: if (!strnicmp(argv[i], "-w", 2)) {
			a = argv[i + 1];
			if (i + 1 == argc || ({__asm__ goto("" :::: w5x); 0;}) || !a || *a == '-')
				client_usage(3, argv[i]);
			if (mode) { w5x: client_usage(5, argv[i]); }
			arg = argv[++i];
			log_printf(0, "setting write filename to %s\n", arg);
			mode = 2;
		} else { k67l: if (E(!strnicmp(argv[i], "-e", 2))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting avatar/kinect files base path to %s\n", arg);
			mode = 4;
		} else if (E(!strnicmp(argv[i], "-c", 2))) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				client_usage(3, argv[i]);
			if (mode)
				client_usage(5, argv[i]);
			arg = argv[++i];
			log_printf(0, "setting xbox compatibility files base path to %s\n", arg);
			mode = 5;
		} else if (!strnicmp(argv[i], "-i", 2)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, "info dump path set to %s\n", arg);
			}
			mode = 12;
		} else if (!strnicmp(argv[i], "-p", 2)) {
			if (!argv[i + 1] || i + 1 == argc || *argv[i + 1] == '-')
				arg = dummy;
			else {
				arg = argv[++i];
				log_printf(0, "patch file set to %s\n", arg);
			}
			mode = 7;
		} else if (!strnicmp(argv[i], "-v", 2))
			log_verbose_flag(argv[i][2]);
		else
			client_usage(1, argv[i]); } } }
	}
	if (NO_MODE_ARG(mode, arg)) {
		if (__builtin_constant_p(mode + 91) && __builtin_constant_p(mode + 92) && __builtin_constant_p(mode + 93) && __builtin_constant_p(mode + 94) && __builtin_constant_p(mode + 50094) && __builtin_constant_p(mode + 100094) && __builtin_constant_p(mode + 150094) && __builtin_constant_p(mode + 200094) && __builtin_constant_p(mode + 250094)) goto fkbo;
		if (__builtin_constant_p(mode + 130)) goto dtg;
		if (reboot) {
			if (netConnect(ip)) {
			rok: __attribute__((cold));
				cinfo = netGetInfo(); if (__builtin_constant_p(mode + 620)) goto ndl;
				{ struct {} rko; { struct {} rkv0; __asm__ ("" :: "m"(rko), "m"(rkv0)); __asm__ goto ("" :::: dsp, c1, c12, s5, c7, c9, c3, c8, c2, c10, cdef, rk0, rk1, rk2, rk3, rk4, rk5, rk6, rk7, rk8, rk9, rk10, rk11, rk12, rk13); goto rkn0; rk0: goto ork0; rk1: goto ork1; rk2: goto ork2; rk3: goto ork3; rk4: goto ork4; rk5: goto ork5; rk6: goto ork6; rk7: goto ork7; rk8: goto ork8; rk9: goto ork9; rk10: goto ork10; rk11: goto ork11; rk12: goto ork12; rk13: goto ork13; } rkn0: ; { struct {} rkv1; __asm__ ("" :: "m"(rko), "m"(rkv1)); __asm__ goto ("" :::: rk14, rk15, rk16, rk17, rk18, rk19, rk20, rk21, rk22, rk23, rk24, rk25, rk26, rk27, rk28, rk29, rk30, rk31, rk32, rk33, rk34, rk35, rk36, rk37, rk38, rk39, rk40, rk41, rk42, rk43); goto rkn1; rk14: goto ork14; rk15: goto ork15; rk16: goto ork16; rk17: goto ork17; rk18: goto ork18; rk19: goto ork19; rk20: goto ork20; rk21: goto ork21; rk22: goto ork22; rk23: goto ork23; rk24: goto ork24; rk25: goto ork25; rk26: goto ork26; rk27: goto ork27; rk28: goto ork28; rk29: goto ork29; rk30: goto ork30; rk31: goto ork31; rk32: goto ork32; rk33: goto ork33; rk34: goto ork34; rk35: goto ork35; rk36: goto ork36; rk37: goto ork37; rk38: goto ork38; rk39: goto ork39; rk40: goto ork40; rk41: goto ork41; rk42: goto ork42; rk43: goto ork43; } rkn1: ; { struct {} rkv2; __asm__ ("" :: "m"(rko), "m"(rkv2)); __asm__ goto ("" :::: rk44, rk45, rk46, rk47, rk48, rk49, rk50, rk51); goto rkn2; rk44: goto ork44; rk45: goto ork45; rk46: goto ork46; rk47: goto ork47; rk48: goto ork48; rk49: goto ork49; rk50: goto ork50; rk51: goto ork51; } rkn2: ; goto rkE; ork0: goto c1; ork1: goto c1; ork2: goto c12; ork3: goto c12; ork4: goto c12; ork5: goto c12; ork6: goto c12; ork7: goto s5; ork8: goto s5; ork9: goto c3; ork10: goto c3; ork11: goto rkE; ork12: goto rkE; ork13: goto rkE; ork14: goto rkE; ork15: goto rkE; ork16: goto rkE; ork17: goto rkE; ork18: goto rkE; ork19: goto rkE; ork20: goto rkE; ork21: goto rkE; ork22: goto c8; ork23: goto c8; ork24: goto c8; ork25: goto c8; ork26: goto c10; ork27: goto c10; ork28: goto cdef; ork29: goto cdef; ork30: goto cdef; ork31: goto t4; ork32: goto t4; ork33: goto t4; ork34: goto t5; ork35: goto t5; ork36: goto t5; ork37: goto t5; ork38: goto t5; ork39: goto t5; ork40: goto t5; ork41: goto t5; ork42: goto t5; ork43: goto rkE; ork44: goto rkE; ork45: goto rkE; ork46: goto rkE; ork47: goto rkE; ork48: goto rkE; ork49: goto rkE; ork50: goto rkE; ork51: goto rkE; } rkE: ; 
			} else
				goto fail;
		} else
			{ AT(u2) client_usage(2, NULL); }
	} else {
		if (netConnect(ip)) {
			fkbo: { struct {} fko; { struct {} fkv; __asm__ ("" :: "X"(&fko), "X"(&fkv)); __asm__ goto ("" :::: p1, i1, dtg, ndl, c10, c9, c1, c7, cdef, fa0, fa1, fa2, fa3, fa4, fa5, fa6, fa7, fa8, fa9, fa10, fa11, fa12, fa13, fa14, fa15, fa16, fa17, fa18, fa19, fa20); fkA2: goto fkN; fa0: goto ofa0; fa1: goto ofa1; fa2: goto ofa2; fa3: goto ofa3; fa4: goto ofa4; fa5: goto ofa5; fa6: goto ofa6; fa7: goto ofa7; fa8: goto ofa8; fa9: goto ofa9; fa10: goto ofa10; fa11: goto ofa11; fa12: goto ofa12; fa13: goto ofa13; fa14: goto ofa14; fa15: goto ofa15; fa16: goto ofa16; fa17: goto ofa17; fa18: goto ofa18; fa19: goto ofa19; fa20: goto ofa20;  } ofa0: goto fkA2; ofa1: goto fkA2; ofa2: goto fkA2; ofa3: goto fkA2; ofa4: goto fkA2; ofa5: goto fkA2; ofa6: goto fkA2; ofa7: goto fkA2; ofa8: goto fkA2; ofa9: goto fkA2; ofa10: goto fkA2; ofa11: goto fkA2; ofa12: goto fkA2; ofa13: goto fkA2; ofa14: goto fkA2; ofa15: goto fkA2; ofa16: goto fkA2; ofa17: goto fkA2; ofa18: goto fkA2; ofa19: goto fkA2; ofa20: goto fkA2;  fkM: ; } fkN: ;
			dsp: cinfo = netGetInfo();
			 if (__builtin_constant_p(mode + 910) && __builtin_constant_p(mode + 911) && __builtin_constant_p(mode + 912) && __builtin_constant_p(mode + 913) && __builtin_constant_p(mode + 50913)) goto c9;  if (__builtin_constant_p(mode + 930) && __builtin_constant_p(mode + 931) && __builtin_constant_p(mode + 932) && __builtin_constant_p(mode + 933)) goto t4;      
			           if (__builtin_constant_p(mode + 1210) && __builtin_constant_p(mode + 1211) && __builtin_constant_p(mode + 1212) && __builtin_constant_p(mode + 1213) && __builtin_constant_p(mode + 51213) && __builtin_constant_p(mode + 101213)) mode = 7; else if (__builtin_constant_p(mode + 1230) && __builtin_constant_p(mode + 51230) && __builtin_constant_p(mode + 101230) && __builtin_constant_p(mode + 151230) && __builtin_constant_p(mode + 201230) && __builtin_constant_p(mode + 251230)) mode = 11; else if (__builtin_constant_p(mode + 1220) && __builtin_constant_p(mode + 1221) && __builtin_constant_p(mode + 1222) && __builtin_constant_p(mode + 1223) && __builtin_constant_p(mode + 51223) && __builtin_constant_p(mode + 101223)) mode = 9; switch (mode) {
			case 1:
				AT(c1) netDumpNand(arg);
				__asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); break;
			case 2:
				AT(c2) clientWrite(arg);
				break;
			case 3:
				AT(c3)  { JMP(hdd4,s5,hdd5); clientKeys(); }
				__asm__ goto ("" :::: dsp); break;
			case 4:
				AT(t4)  if (cinfo->hwFlags & 0x20)
					s4: { sendAvatarData(arg, cinfo->kernel); }
				else
					{ AT(hdd4) { hc4: __attribute__((cold)); } log_printf(0, "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n"); }
				__asm__ goto ("" :::: dsp); break;
			case 5:
				AT(t5)  if (cinfo->hwFlags & 0x20)
					{ AT(s5) { JMP(s4,c12); sendCompatData(arg); } }
				else
					{ AT(hdd5) { hdd5_c: __attribute__((cold)); } log_printf(0, "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"); }
				break;
			case 6:
				break;
			case 7:
				AT(c7)  if (arg == dummy)
					{ AT(p0) { p0c: __attribute__((cold)); } clientPatches(NULL); JUMP(i0); }
				else
					{ AT(p1) clientPatches(arg); }
				break;
			case 8:
				AT(c8) { clientReadBlocks(arg, start, count); JMP(p1,cdef); }
				break;
			case 9:
				AT(c9) { clientWriteBlocks(arg, start); JMP(hdd4,hdd5); }
				__asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); break;
			case 10:
				AT(c10) clientEraseBlockI(arg);
				break;
			case 11:
				AT(c11) clientBinPatch(arg, start);
				break;
			case 12:
				AT(c12) if (arg == dummy || ({JMP(p0); 0;}))
					{ AT(i0) { i0_c: __attribute__((cold)); } clientInfo(NULL); }
				else
					{ AT(i1) clientInfo(arg); }
				break;
			default:
				AT(cdef) if (__builtin_constant_p(mode + 430) && __builtin_constant_p(mode + 431) && __builtin_constant_p(mode + 432) && __builtin_constant_p(mode + 433) && __builtin_constant_p(mode + 434) && __builtin_constant_p(mode + 50434) && __builtin_constant_p(mode + 100434) && __builtin_constant_p(mode + 150434) && __builtin_constant_p(mode + 200434) && __builtin_constant_p(mode + 250434) && __builtin_constant_p(mode + 300434) && __builtin_constant_p(mode + 350434) && __builtin_constant_p(mode + 400434)) goto ndl; log_printf(0, "\n\n***** ERROR: invalid mode specified, please inform author\n");
				__asm__ goto ("" :::: dsp); __asm__ goto ("" :::: dsp); break;
			}
		} else
			goto fail;
	}
	
	dtg: if (E(reboot))
		netReboot(reboot);
	ndl: netDisconnect();
	  if (__builtin_constant_p(mode + 720) && __builtin_constant_p(mode + 721) && __builtin_constant_p(mode + 722) && __builtin_constant_p(mode + 723) && __builtin_constant_p(mode + 724) && __builtin_constant_p(mode + 725) && __builtin_constant_p(mode + 50725) && __builtin_constant_p(mode + 100725) && __builtin_constant_p(mode + 150725)) goto p0; if (__builtin_constant_p(mode + 730) && __builtin_constant_p(mode + 50730) && __builtin_constant_p(mode + 100730) && __builtin_constant_p(mode + 150730)) goto s5;  if (__builtin_constant_p(mode + 750) && __builtin_constant_p(mode + 50750)) goto u2; 
	return 0;
fail: __attribute__((cold));  if (__builtin_constant_p(mode + 2400) && __builtin_constant_p(mode + 52400) && __builtin_constant_p(mode + 102400)) goto c11; if (__builtin_constant_p(mode + 5562) && __builtin_constant_p(mode + 55562) && __builtin_constant_p(mode + 105562) && __builtin_constant_p(mode + 155562) && __builtin_constant_p(mode + 205562) && __builtin_constant_p(mode + 255562) && __builtin_constant_p(mode + 305562)) goto ndl; if (__builtin_constant_p(mode + 4120) && __builtin_constant_p(mode + 54120) && __builtin_constant_p(mode + 104120) && __builtin_constant_p(mode + 154120) && __builtin_constant_p(mode + 204120)) goto s4; if (__builtin_constant_p(mode + 3000) && __builtin_constant_p(mode + 53000) && __builtin_constant_p(mode + 103000) && __builtin_constant_p(mode + 153000)) goto t5; if (__builtin_constant_p(mode + 260)) goto ndl; if (__builtin_constant_p(mode + 6873) && __builtin_constant_p(mode + 56873) && __builtin_constant_p(mode + 106873) && __builtin_constant_p(mode + 156873) && __builtin_constant_p(mode + 206873) && __builtin_constant_p(mode + 256873) && __builtin_constant_p(mode + 306873) && __builtin_constant_p(mode + 356873) && __builtin_constant_p(mode + 406873) && __builtin_constant_p(mode + 456873)) goto ndl; if (__builtin_constant_p(mode + 8182) && __builtin_constant_p(mode + 58182) && __builtin_constant_p(mode + 108182) && __builtin_constant_p(mode + 158182) && __builtin_constant_p(mode + 208182)) goto ndl; if (__builtin_constant_p(mode + 7351) && __builtin_constant_p(mode + 57351) && __builtin_constant_p(mode + 107351) && __builtin_constant_p(mode + 157351) && __builtin_constant_p(mode + 207351) && __builtin_constant_p(mode + 257351)) goto dtg; if (__builtin_constant_p(mode + 205) && __builtin_constant_p(mode + 50205) && __builtin_constant_p(mode + 100205) && __builtin_constant_p(mode + 150205)) goto c3; if (__builtin_constant_p(mode + 5569) && __builtin_constant_p(mode + 55569) && __builtin_constant_p(mode + 105569) && __builtin_constant_p(mode + 155569) && __builtin_constant_p(mode + 205569)) goto dtg; if (__builtin_constant_p(mode + 7368) && __builtin_constant_p(mode + 57368) && __builtin_constant_p(mode + 107368) && __builtin_constant_p(mode + 157368)) goto ndl; if (__builtin_constant_p(mode + 6949) && __builtin_constant_p(mode + 56949) && __builtin_constant_p(mode + 106949) && __builtin_constant_p(mode + 156949)) goto dtg; if (__builtin_constant_p(mode + 3200) && __builtin_constant_p(mode + 53200) && __builtin_constant_p(mode + 103200) && __builtin_constant_p(mode + 153200)) goto c9;
	log_printf(0, "\n\n***** ERROR: unable to connect to xbox server\n");
	return 0;
}

/* 16 zero bytes end the original object's .rdata */
static const char mc_rdpad[16] __attribute__((used)) = {0};
