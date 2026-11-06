# mode_client attempt 4: E(reboot) without the expect.  The expect (param 50) makes the
# reboot test exactly 50%; plain gives 29% (call heuristic on the netReboot arm only).
# These shapes give the else arm its own netDisconnect() call, dominated by the test, so
# the call heuristic predicts both edges and DS combines them to 50%.
OLD = 'dtg: if (E(reboot))\n\t\t{ netReboot(reboot); JMP(fail); }\n\tndl: netDisconnect();\n'
V = {
    'both_ndl_then': [(OLD, 'dtg: if (reboot)\n\t\t{ netReboot(reboot); JMP(fail); ndl: netDisconnect(); }\n\telse\n\t\tnetDisconnect();\n')],
    'both_ndl_else': [(OLD, 'dtg: if (reboot)\n\t\t{ netReboot(reboot); JMP(fail); netDisconnect(); }\n\telse\n\t\t{ ndl: netDisconnect(); }\n')],
    'both_ndl_out': [(OLD, 'dtg: if (reboot)\n\t\t{ netReboot(reboot); JMP(fail); netDisconnect(); }\n\telse\n\t\tnetDisconnect();\n\tif (0) { ndl: netDisconnect(); }\n')],
    'not_then': [(OLD, 'dtg: if (!reboot)\n\t\tnetDisconnect();\n\telse\n\t\t{ netReboot(reboot); JMP(fail); ndl: netDisconnect(); }\n')],
}
