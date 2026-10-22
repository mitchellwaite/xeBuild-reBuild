/* the rest of parseButton after its inlined first tests (gcc's ipa-split
   part; local, so its argument comes in eax) */
int parseButtonPart(const char *s) __asm__("_parseButton.part.1") __attribute__((regparm(1)));

/* written in the original's block order: gcc's block reordering is off
   for it (see README) */
__attribute__((optimize("no-tree-tail-merge")))
void applyIniOptions(void)
{
	char *s;
	const char *msg;
	u32 v, t;
	int b, i;

	if (!(xb.bootFlags & 0x20000000))
		goto nomobile;
nomobile_done:
	if (!(xb.bootFlags & 0x40000000))
		goto noremap;
noremap_done:
	if (!(xb.bootFlags & 0x80000000) && !(xb.bootFlagsOff & 0x80000000))
		goto noecdremap;
noecdremap_done:
	if (!(xb.bootFlags & 0x10000000))
		goto nandmu;
nandmu_done:
	if (!(xb.bootFlags & 0x4000000))
		goto nosecurity;
nosecurity_done:
	if (!(xb.bootFlags & 0x1000000))
		goto nosusecurity;
nosusecurity_done:
	if (!(xb.bootFlags & 0x200000))
		goto smcnocheck;
smcnocheck_done:
	if (!xb.cfLdv)
		goto cfldv;
cfldv_done:
	if (xb.cpuFan == -1)
		goto cpufan;
cpufan_done:
	if (xb.gpuFan == -1)
		goto gpufan;
gpufan_done:
	if (xb.cpuTemp == -1)
		goto cputemp;
cputemp_done:
	if (xb.gpuTemp == -1)
		goto gputemp;
gputemp_done:
	if (xb.edramTemp == -1)
		goto edramtemp;
edramtemp_done:
	if (xb.overCpuTemp == -1)
		goto overcputemp;
overcputemp_done:
	if (xb.overGpuTemp == -1)
		goto overgputemp;
overgputemp_done:
	if (xb.overEdramTemp == -1)
		goto overedramtemp;
overedramtemp_done:
	if (xb.avRegion == -1)
		goto avregion;
avregion_done:
	if (xb.gameRegion == -1)
		goto gameregion;
gameregion_done:
	if (xb.dvdRegion == -1)
		goto dvdregion;
dvdregion_done:
	if (!macidSet()) {
		s = getIniValue(str_macid);
		if (s) {
			stripColons(s);
			if (strlen(s) == 12)
				goto macid_len;
			msg = "***** WARNING: invalid length macid '";
macid_bad:
			log_printf(0, msg);
			showHexPairs(0, s);
			log_printf(0, "' provided in ini file! Discarding!\n", s);
		}
	}
macid_done:
	if (xb.type - 2 > 3)
		goto type_done;
	if (!(xb.bootFlags & 1))
		goto cygnos;
cygnos_done:
	if (!(xb.bootFlags & 8))
		goto demon;
demon_done:
	if (!(xb.bootFlags & 0x8000000))
		goto patchsmc;
patchsmc_done:
	if (xb.xellButton)
		goto xell2;
	if (xb.bootFlags & 4)
		goto xell;
xell2_done:
	if (!(xb.bootFlags & 0x400000))
		goto smcnoeject;
smcnoeject_done:
	if (!(xb.bootFlags & 0x800000))
		goto smcnoblink;
smcnoblink_done:
	t = xb.type;
smcnoblink_type:
	if (t != 2)
		goto type_done;
	if (!(xb.bootFlags & 2))
		goto nodvd;
olddvd:
	if (perboxExists(str_olddvd))
		goto olddvd_perbox;
	s = iniBoolInvalid(str_olddvd);
	if (!s)
		goto olddvd_ini;
	log_printf(0, msg_iniInvalid, str_olddvd, s);
olddvd_done:
	if (!xb.dualButton)
		goto dualboot;
dualboot_done:
type_done:
	if (!(xb.bootFlags & 0x2000000))
		goto dvdkey;
dvdkey_done:
	if (!xb.blSuffix[0])
		goto rev;
	return;

xell:
	s = getIniValue(str_xellbutton);
	if (!s)
		goto xell_null;
	b = 0x11;
	if (!strnicmp(s, str_power, 5))
		goto xell_const;
	b = 0x20;
	if (!strnicmp(s, str_remopower, 9))
		goto xell_const;
	b = 0x22;
	if (!strnicmp(s, str_remox, 5))
		goto xell_const;
	b = 0x24;
	if (!strnicmp(s, str_winbutton, 9))
		goto xell_const;
	xb.xellButton = parseButtonPart(s);
	if (xb.xellButton)
		goto xell_done;
xell_default:
	log_printf(1, "default console DVD eject button is being used to start xell\n");
	xb.xellButton = 0x12;
xell_done:
xell2:
	if (xb.xellAltButton || !(xb.bootFlags & 4))
		goto xell2_done;
	s = getIniValue(str_xellbutton2);
	b = 0;
	if (!s)
		goto xell2_set;
	b = 0x11;
	if (strnicmp(s, str_power, 5))
		goto xell2_more;
xell2_set:
	xb.xellAltButton = b;
	if (!xb.xellButton)
		goto xell2_off;
xell2_off_done:
	goto xell2_done;

rev:
	s = getIniValue("rev");
	if (!s)
		return;
	sprintf(xb.blSuffix, "_%s", s);
	return;

dvdkey:
	s = getIniValue(str_dvdkey);
	if (!s || !kvSetDvdKey(s))
		goto dvdkey_done;
	xb.bootFlags |= 0x2000000;
	goto dvdkey_done;

cfldv:
	s = iniU32Invalid(str_cfldv);
	if (!s)
		goto cfldv_ini;
	log_printf(0, msg_iniInvalid, str_cfldv, s);
	xb.cfLdv = 0;
	if (xb.cpuFan != -1)
		goto cpufan_done;
cpufan:
	s = iniU32Invalid(str_cpufan);
	if (!s)
		goto cpufan_ini;
	log_printf(0, msg_iniInvalid, str_cpufan, s);
	v = -1;
cpufan_set:
	xb.cpuFan = v;
	if (xb.gpuFan != -1)
		goto gpufan_done;
gpufan:
	s = iniU32Invalid(str_gpufan);
	if (!s)
		goto gpufan_ini;
	log_printf(0, msg_iniInvalid, str_gpufan, s);
	v = -1;
gpufan_set:
	xb.gpuFan = v;
	if (xb.cpuTemp != -1)
		goto cputemp_done;
cputemp:
	s = iniU32Invalid(str_cputemp);
	if (!s)
		goto cputemp_ini;
	log_printf(0, msg_iniInvalid, str_cputemp, s);
	v = -1;
cputemp_set:
	xb.cpuTemp = v;
	if (xb.gpuTemp != -1)
		goto gputemp_done;
gputemp:
	s = iniU32Invalid(str_gputemp);
	if (!s)
		goto gputemp_ini;
	log_printf(0, msg_iniInvalid, str_gputemp, s);
	v = -1;
gputemp_set:
	xb.gpuTemp = v;
	if (xb.edramTemp != -1)
		goto edramtemp_done;
edramtemp:
	s = iniU32Invalid(str_edramtemp);
	if (!s)
		goto edramtemp_ini;
	log_printf(0, msg_iniInvalid, str_edramtemp, s);
	v = -1;
edramtemp_set:
	xb.edramTemp = v;
	if (xb.overCpuTemp != -1)
		goto overcputemp_done;
overcputemp:
	s = iniU32Invalid(str_overcputemp);
	if (!s)
		goto overcputemp_ini;
	log_printf(0, msg_iniInvalid, str_overcputemp, s);
	v = -1;
overcputemp_set:
	xb.overCpuTemp = v;
	if (xb.overGpuTemp != -1)
		goto overgputemp_done;
overgputemp:
	s = iniU32Invalid(str_overgputemp);
	if (!s)
		goto overgputemp_ini;
	log_printf(0, msg_iniInvalid, str_overgputemp, s);
	v = -1;
overgputemp_set:
	xb.overGpuTemp = v;
	if (xb.overEdramTemp != -1)
		goto overedramtemp_done;
overedramtemp:
	s = iniU32Invalid(str_overedramtemp);
	if (!s)
		goto overedramtemp_ini;
	log_printf(0, msg_iniInvalid, str_overedramtemp, s);
	v = -1;
overedramtemp_set:
	xb.overEdramTemp = v;
	if (xb.avRegion != -1)
		goto avregion_done;
avregion:
	s = iniU32Invalid(str_avregion);
	if (!s)
		goto avregion_ini;
	log_printf(0, msg_iniInvalid, str_avregion, s);
	v = -1;
avregion_set:
	xb.avRegion = v;
	if (xb.gameRegion != -1)
		goto gameregion_done;
gameregion:
	s = iniU32Invalid(str_gameregion);
	if (!s)
		goto gameregion_ini;
	log_printf(0, msg_iniInvalid, str_gameregion, s);
	v = -1;
gameregion_set:
	xb.gameRegion = v;
	if (xb.dvdRegion != -1)
		goto dvdregion_done;
dvdregion:
	s = iniU32Invalid(str_dvdregion);
	if (!s)
		goto dvdregion_ini;
	log_printf(0, msg_iniInvalid, str_dvdregion, s);
	v = -1;
dvdregion_set:
	xb.dvdRegion = v;
	goto dvdregion_done;

noecdremap:
	if (perboxExists(str_noecdremap))
		goto noecdremap_perbox;
	s = iniBoolInvalid(str_noecdremap);
	if (!s)
		goto noecdremap_ini;
	log_printf(0, msg_iniInvalid, str_noecdremap, s);
noecdremap_skip:
	goto noecdremap_done;

cygnos:
	if (xb.bootFlagsOff & 1)
		goto cygnos_done;
	if (!perboxExists(str_cygnos))
		goto cygnos_noperbox;
	log_printf(1, msg_optPerbox, str_cygnos);
cygnos_set:
	xb.bootFlags |= 1;
	goto cygnos_done;

demon:
	if (xb.bootFlagsOff & 8)
		goto demon_done;
	if (!perboxExists(str_demon))
		goto demon_noperbox;
	log_printf(1, msg_optPerbox, str_demon);
demon_set:
	xb.bootFlags |= 8;
	goto demon_done;

patchsmc:
	if (xb.bootFlagsOff & 0x8000000)
		goto patchsmc_done;
	if (!perboxExists(str_patchsmc))
		goto patchsmc_noperbox;
	log_printf(1, msg_optPerbox, str_patchsmc);
patchsmc_set:
	xb.bootFlags |= 0x8000000;
	goto patchsmc_done;

macid_len:
	if (!validateString(s))
		goto macid_chars;
	for (i = 0; i < 6; i++) {
		xb.macid[i] = myatox8(s);
		s += 2;
	}
	goto macid_done;

xell_const:
	xb.xellButton = b;
	goto xell2;

nomobile:
	if (xb.bootFlagsOff & 0x20000000)
		goto nomobile_done;
	if (!perboxExists(str_nomobile))
		goto nomobile_noperbox;
	log_printf(1, msg_optPerbox, str_nomobile);
nomobile_set:
	xb.bootFlags |= 0x20000000;
	if (xb.bootFlags & 0x40000000)
		goto noremap_done;
noremap:
	if (xb.bootFlagsOff & 0x40000000)
		goto noremap_done;
	if (!perboxExists(str_noremap))
		goto noremap_noperbox;
	log_printf(1, msg_optPerbox, str_noremap);
noremap_set:
	xb.bootFlags |= 0x40000000;
	goto noremap_done;

smcnocheck:
	if (xb.bootFlagsOff & 0x200000)
		goto smcnocheck_done;
	if (!perboxExists(str_smcnocheck))
		goto smcnocheck_noperbox;
	log_printf(1, msg_optPerbox, str_smcnocheck);
smcnocheck_set:
	xb.bootFlags |= 0x200000;
	goto smcnocheck_done;

nosecurity:
	if (xb.bootFlagsOff & 0x4000000)
		goto nosecurity_done;
	if (!perboxExists(str_nosecurity))
		goto nosecurity_noperbox;
	log_printf(1, msg_optPerbox, str_nosecurity);
nosecurity_set:
	xb.bootFlags |= 0x4000000;
	if (xb.bootFlags & 0x1000000)
		goto nosusecurity_done;
nosusecurity:
	if (xb.bootFlagsOff & 0x1000000)
		goto nosusecurity_done;
	if (!perboxExists(str_nosusecurity))
		goto nosusecurity_noperbox;
	log_printf(1, msg_optPerbox, str_nosusecurity);
nosusecurity_set:
	xb.bootFlags |= 0x1000000;
	goto nosusecurity_done;

nandmu:
	if (xb.bootFlagsOff & 0x10000000)
		goto nandmu_done;
	if (!perboxExists(str_nandmu))
		goto nandmu_noperbox;
	log_printf(1, msg_optPerbox, str_nandmu);
nandmu_set:
	xb.bootFlags |= 0x10000000;
	goto nandmu_done;

smcnoblink:
	if (xb.bootFlagsOff & 0x800000)
		goto smcnoblink_done;
	if (!perboxExists(str_smcnoblink))
		goto smcnoblink_noperbox;
	log_printf(1, msg_optPerbox, str_smcnoblink);
smcnoblink_set:
	xb.bootFlags |= 0x800000;
	goto smcnoblink_done;

smcnoeject:
	if (xb.bootFlagsOff & 0x400000)
		goto smcnoeject_done;
	if (!perboxExists(str_smcnoeject))
		goto smcnoeject_noperbox;
	log_printf(1, msg_optPerbox, str_smcnoeject);
smcnoeject_set:
	xb.bootFlags |= 0x400000;
	goto smcnoeject_done;

olddvd_perbox:
	log_printf(1, msg_optPerbox, str_olddvd);
olddvd_set:
	xb.bootFlags &= ~4;
	goto olddvd_done;

nodvd:
	if (xb.bootFlagsOff & 2)
		goto olddvd;
	if (!perboxExists(str_nodvd))
		goto nodvd_noperbox;
	log_printf(1, msg_optPerbox, str_nodvd);
nodvd_set:
	xb.bootFlags = (xb.bootFlags & ~4) | 2;
	goto olddvd;

noecdremap_perbox:
	log_printf(1, msg_optPerbox, str_noecdremap);
noecdremap_set:
	xb.bootFlags |= 0x80000000;
	goto noecdremap_done;

macid_chars:
	msg = "***** WARNING: invalid characters in macid '";
	goto macid_bad;

xell2_more:
	b = 0x20;
	if (!strnicmp(s, str_remopower, 9))
		goto xell2_set;
	b = 0x22;
	if (!strnicmp(s, str_remox, 5))
		goto xell2_set;
	b = 0x24;
	if (!strnicmp(s, str_winbutton, 9))
		goto xell2_set;
	b = parseButtonPart(s);
	goto xell2_set;

dualboot:
	s = getIniValue(str_dualboot);
	b = 0;
	if (!s)
		goto dualboot_set;
	b = 0x11;
	if (strnicmp(s, str_power, 5))
		goto dualboot_more;
dualboot_set:
	xb.dualButton = b;
	if (xb.xellButton != b)
		goto dualboot_done;
	log_printf(1, "dualboot setting ignored!\n");
	xb.dualButton = 0;
	goto dualboot_done;

cfldv_ini:
	xb.cfLdv = getIniU32(str_cfldv, 0);
	if (xb.cfLdv <= 32)
		goto cfldv_done;
	log_printf(0, "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n", xb.cfLdv);
	xb.cfLdv = 32;
	goto cfldv_done;

xell2_off:
	log_printf(1, "alternate xell button is disabled\n");
	goto xell2_off_done;

nandmu_noperbox:
	s = iniBoolInvalid(str_nandmu);
	if (!s)
		goto nandmu_ini;
	log_printf(0, msg_iniInvalid, str_nandmu, s);
nandmu_skip:
	goto nandmu_done;

noremap_noperbox:
	s = iniBoolInvalid(str_noremap);
	if (!s)
		goto noremap_ini;
	log_printf(0, msg_iniInvalid, str_noremap, s);
noremap_skip:
	goto noremap_done;

nomobile_noperbox:
	s = iniBoolInvalid(str_nomobile);
	if (!s)
		goto nomobile_ini;
	log_printf(0, msg_iniInvalid, str_nomobile, s);
nomobile_skip:
	goto nomobile_done;

nosusecurity_noperbox:
	s = iniBoolInvalid(str_nosusecurity);
	if (!s)
		goto nosusecurity_ini;
	log_printf(0, msg_iniInvalid, str_nosusecurity, s);
nosusecurity_skip:
	goto nosusecurity_done;

smcnocheck_noperbox:
	s = iniBoolInvalid(str_smcnocheck);
	if (!s)
		goto smcnocheck_ini;
	log_printf(0, msg_iniInvalid, str_smcnocheck, s);
	goto smcnocheck_done;

nosecurity_noperbox:
	s = iniBoolInvalid(str_nosecurity);
	if (!s)
		goto nosecurity_ini;
	log_printf(0, msg_iniInvalid, str_nosecurity, s);
nosecurity_skip:
	goto nosecurity_done;

xell_null:
	xb.xellButton = 0;
	goto xell_default;

gputemp_ini:
	v = getIniU32(str_gputemp, -1);
	goto gputemp_set;
cputemp_ini:
	v = getIniU32(str_cputemp, -1);
	goto cputemp_set;
gameregion_ini:
	v = getIniU32(str_gameregion, -1);
	goto gameregion_set;
avregion_ini:
	v = getIniU32(str_avregion, -1);
	goto avregion_set;
overedramtemp_ini:
	v = getIniU32(str_overedramtemp, -1);
	goto overedramtemp_set;
overgputemp_ini:
	v = getIniU32(str_overgputemp, -1);
	goto overgputemp_set;
gpufan_ini:
	v = getIniU32(str_gpufan, -1);
	goto gpufan_set;
cpufan_ini:
	v = getIniU32(str_cpufan, -1);
	goto cpufan_set;
overcputemp_ini:
	v = getIniU32(str_overcputemp, -1);
	goto overcputemp_set;
edramtemp_ini:
	v = getIniU32(str_edramtemp, -1);
	goto edramtemp_set;
dvdregion_ini:
	v = getIniU32(str_dvdregion, -1);
	goto dvdregion_set;

cygnos_noperbox:
	s = iniBoolInvalid(str_cygnos);
	if (!s)
		goto cygnos_ini;
	log_printf(0, msg_iniInvalid, str_cygnos, s);
cygnos_skip:
	goto cygnos_done;

demon_noperbox:
	s = iniBoolInvalid(str_demon);
	if (!s)
		goto demon_ini;
	log_printf(0, msg_iniInvalid, str_demon, s);
demon_skip:
	goto demon_done;

dualboot_more:
	b = 0x20;
	if (!strnicmp(s, str_remopower, 9))
		goto dualboot_set;
	b = 0x22;
	if (!strnicmp(s, str_remox, 5))
		goto dualboot_set;
	b = 0x24;
	if (!strnicmp(s, str_winbutton, 9))
		goto dualboot_set;
	b = parseButtonPart(s);
	goto dualboot_set;

smcnoblink_noperbox:
	s = iniBoolInvalid(str_smcnoblink);
	if (!s)
		goto smcnoblink_ini;
	log_printf(0, msg_iniInvalid, str_smcnoblink, s);
smcnoblink_skip:
	t = xb.type;
	goto smcnoblink_type;

patchsmc_noperbox:
	s = iniBoolInvalid(str_patchsmc);
	if (!s)
		goto patchsmc_ini;
	log_printf(0, msg_iniInvalid, str_patchsmc, s);
patchsmc_skip:
	goto patchsmc_done;

smcnoeject_noperbox:
	s = iniBoolInvalid(str_smcnoeject);
	if (!s)
		goto smcnoeject_ini;
	log_printf(0, msg_iniInvalid, str_smcnoeject, s);
smcnoeject_skip:
	goto smcnoeject_done;

nodvd_noperbox:
	s = iniBoolInvalid(str_nodvd);
	if (!s)
		goto nodvd_ini;
	log_printf(0, msg_iniInvalid, str_nodvd, s);
	goto olddvd;

noecdremap_ini:
	if (!getIniBool(str_noecdremap, 0))
		goto noecdremap_skip;
	log_printf(1, msg_optIni, str_noecdremap);
	goto noecdremap_set;
noremap_ini:
	if (!getIniBool(str_noremap, 0))
		goto noremap_skip;
	log_printf(1, msg_optIni, str_noremap);
	goto noremap_set;
nosusecurity_ini:
	if (!getIniBool(str_nosusecurity, 0))
		goto nosusecurity_skip;
	log_printf(1, msg_optIni, str_nosusecurity);
	goto nosusecurity_set;
nomobile_ini:
	if (!getIniBool(str_nomobile, 0))
		goto nomobile_skip;
	log_printf(1, msg_optIni, str_nomobile);
	goto nomobile_set;
smcnocheck_ini:
	if (!getIniBool(str_smcnocheck, 0))
		goto smcnocheck_done;
	log_printf(1, msg_optIni, str_smcnocheck);
	goto smcnocheck_set;
olddvd_ini:
	if (!getIniBool(str_olddvd, 0))
		goto olddvd_done;
	log_printf(1, msg_optIni, str_olddvd);
	goto olddvd_set;
nosecurity_ini:
	if (!getIniBool(str_nosecurity, 0))
		goto nosecurity_skip;
	log_printf(1, msg_optIni, str_nosecurity);
	goto nosecurity_set;
nandmu_ini:
	if (!getIniBool(str_nandmu, 0))
		goto nandmu_skip;
	log_printf(1, msg_optIni, str_nandmu);
	goto nandmu_set;
demon_ini:
	if (!getIniBool(str_demon, 0))
		goto demon_skip;
	log_printf(1, msg_optIni, str_demon);
	goto demon_set;
patchsmc_ini:
	if (!getIniBool(str_patchsmc, 0))
		goto patchsmc_skip;
	log_printf(1, msg_optIni, str_patchsmc);
	goto patchsmc_set;
smcnoblink_ini:
	if (!getIniBool(str_smcnoblink, 0))
		goto smcnoblink_skip;
	log_printf(1, msg_optIni, str_smcnoblink);
	goto smcnoblink_set;
smcnoeject_ini:
	if (!getIniBool(str_smcnoeject, 0))
		goto smcnoeject_skip;
	log_printf(1, msg_optIni, str_smcnoeject);
	goto smcnoeject_set;
cygnos_ini:
	if (!getIniBool(str_cygnos, 0))
		goto cygnos_skip;
	log_printf(1, msg_optIni, str_cygnos);
	goto cygnos_set;
nodvd_ini:
	if (!getIniBool(str_nodvd, 0))
		goto olddvd;
	log_printf(1, msg_optIni, str_nodvd);
	goto nodvd_set;
}
