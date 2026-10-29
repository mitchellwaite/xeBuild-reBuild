# cold attribute on the external HDD-success callees: makes the HDD error arms take the case's whole flow
SA = 'void sendAvatarData(const char *dir, u32 kernel);'
SC = 'u32 sendCompatData(const char *dir);'
CA = '__attribute__((cold)) void sendAvatarData(const char *dir, u32 kernel);'
CC = '__attribute__((cold)) u32 sendCompatData(const char *dir);'
VARS = [
 ('coldA', [(SA, CA)]),
 ('coldC', [(SC, CC)]),
 ('coldAC', [(SA, CA), (SC, CC)]),
]
