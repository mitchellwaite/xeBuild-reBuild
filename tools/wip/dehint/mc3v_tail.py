# mode_client attempt 3: E(reboot) at the tail without the expect, with return-lever shapes
OLD = 'dtg: if (E(reboot))\n\t\t{ netReboot(reboot); JMP(fail); }\n\tndl: netDisconnect();\n'
PLAIN = 'dtg: if (reboot)\n\t\t{ netReboot(reboot); JMP(fail); }\n\tndl: netDisconnect();\n'
V = {
    'plain': [(OLD, PLAIN)],
    'not': [(OLD, 'dtg: if (!reboot) ; else\n\t\t{ netReboot(reboot); JMP(fail); }\n\tndl: netDisconnect();\n')],
    'ne0': [(OLD, 'dtg: if (reboot != 0)\n\t\t{ netReboot(reboot); JMP(fail); }\n\tndl: netDisconnect();\n')],
    'gt0': [(OLD, 'dtg: if (reboot > 0)\n\t\t{ netReboot(reboot); JMP(fail); }\n\tndl: netDisconnect();\n')],
    'ret_after': [(OLD, 'dtg: if (reboot)\n\t\t{ netReboot(reboot); JMP(fail); netDisconnect(); goto ndr; }\n\tndl: netDisconnect();\n'),
                  ('\treturn 0;\nfail:', '\tndr: return 0;\nfail:')],
    'dup': [(OLD, 'dtg: if (reboot)\n\t\t{ netReboot(reboot); JMP(fail); netDisconnect(); return 0; }\n\tndl: netDisconnect();\n')],
}
