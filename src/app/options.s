# app/options.s -- console types (xenon...corona), command line options; startup fn
#
# original placement:
#   .eh_frame      00469d48-0046a23c
#   .rdata         00457df0-00458ca4
#   .rdata$zzz     00463abc-00463ae8
#   .text          004236f0-00427500
#   .text.startup  00449640-00449790

.intel_syntax noprefix
.globl FUN_424b60
.globl _applyIniOptions
.globl _iniConsoleType
.globl _loadAddons
.globl _parseCmdOptions
.globl _parseRawPatches
.globl _setConsoleType

.text
.p2align 4
L_4236f0:
          push ESI
          push EBX
          mov ESI,EAX
          sub ESP,1044
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBX
          call _strcpy
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBX
          call _strcat
          mov DWORD PTR [ESP],EBX
          call _FileExists
          add ESP,1044
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_423730:
          cmp BYTE PTR [L_47ad4c],0
          mov EAX,DWORD PTR [ESP+4]
          jne L_423740
          xor EAX,EAX
          ret 
L_423740:
          jmp L_4236f0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_423750:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,2076
          mov ESI,DWORD PTR [ESP+2096]
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],ESI
          call _strcpy
          mov EDX,EBX
L_423773:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423773
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          xor EDI,EDI
          cmp BYTE PTR [L_47ad4c],0
          mov DWORD PTR [EDX],1954051118
          mov BYTE PTR [EDX+4],0
          jne L_4237c5
L_4237b8:
          add ESP,2076
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4237c5:
          lea EBP,DWORD PTR [ESP+1040]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBP
          call _strcpy
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EBP
          call _strcat
          mov DWORD PTR [ESP],EBP
          call _FileExists
          cmp BYTE PTR [L_47ad4c],0
          mov EDI,EAX
          je L_4237b8
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          call _strcpy
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBP
          call _strcat
          mov DWORD PTR [ESP],EBP
          call _FileExists
          add ESP,2076
          or EDI,EAX
          pop EBX
          mov EAX,EDI
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
_iniConsoleType:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov DWORD PTR [ESP],OFFSET L_457e3a
          call FUN_423750
          test EAX,EAX
          jne L_423a82
          mov DWORD PTR [ESP],OFFSET L_457e61
          call FUN_423750
          test EAX,EAX
          jne L_423a10
          mov DWORD PTR [ESP],OFFSET L_457e8a
          call FUN_423750
          test EAX,EAX
          jne L_423b80
          mov DWORD PTR [ESP],OFFSET L_457eb6
          call FUN_423750
          mov DWORD PTR [ESP],OFFSET L_457ebd
          mov EBX,EAX
          call FUN_423750
          or EBX,EAX
          jne L_423b00
          mov DWORD PTR [ESP],OFFSET L_457eea
          call FUN_423750
          test EAX,EAX
          jne L_423bf5
          mov DWORD PTR [ESP],OFFSET L_457f21
          call FUN_423750
          test EAX,EAX
          jne L_423cb0
          mov DWORD PTR [ESP],OFFSET L_457f58
          call FUN_423750
          test EAX,EAX
          jne L_423c30
          mov DWORD PTR [ESP],OFFSET L_457f62
          call FUN_423750
          test EAX,EAX
          jne L_423d30
          mov DWORD PTR [ESP],OFFSET L_457f6c
          call FUN_423750
          test EAX,EAX
          jne L_423dab
          mov DWORD PTR [ESP],OFFSET L_457f97
          call FUN_423750
          test EAX,EAX
          jne L_423e1a
          mov DWORD PTR [ESP],OFFSET L_457fd1
          call FUN_423750
          test EAX,EAX
          jne L_423e95
          mov DWORD PTR [ESP],OFFSET L_45801d
          call FUN_423750
          test EAX,EAX
          jne L_423f1a
          mov DWORD PTR [ESP],OFFSET L_458046
          call FUN_423750
          test EAX,EAX
          jne L_423f8f
          mov DWORD PTR [ESP],OFFSET L_45807c
          call FUN_423750
          test EAX,EAX
          jne L_424005
          mov DWORD PTR [ESP],OFFSET L_4580c8
          call FUN_423750
          test EAX,EAX
          jne L_42404d
          mov DWORD PTR [ESP],OFFSET L_4580fa
          call FUN_423750
          test EAX,EAX
          jne L_424095
          mov DWORD PTR [ESP],OFFSET L_45812e
          call FUN_423750
          test EAX,EAX
          jne L_424125
          mov DWORD PTR [ESP],OFFSET L_458166
          call FUN_423750
          test EAX,EAX
          jne L_4240dd
          mov DWORD PTR [ESP],OFFSET L_4581a4
          call FUN_423750
          test EAX,EAX
          je L_423aeb
          mov DWORD PTR [ESP+4],OFFSET L_4581b8
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_47a94c
          call _log_printf
          or DWORD PTR [L_479ea4],1610612743
          xor EAX,EAX
          or ECX,4294967295
          mov EDX,OFFSET L_4581a4
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,17
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          rep movsb 
          jmp L_423aeb
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_423a10:
          mov DWORD PTR [ESP+4],OFFSET L_457e68
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],2
          mov EDX,OFFSET L_47a94c
L_423a30:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423a30
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          mov EAX,29305
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1752196474
          mov WORD PTR [EDX+L_47a950],AX
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_423aeb
L_423a82:
          mov DWORD PTR [ESP+4],OFFSET L_457e40
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1
          mov EDX,OFFSET L_47a94c
L_423aa2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423aa2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          mov EAX,110
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1869505912
          mov WORD PTR [EDX+L_47a950],AX
L_423aeb:
          xor EAX,EAX
          test BYTE PTR [L_479ea4],7
          setne AL
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x66
          .byte 0x90
L_423b00:
          mov DWORD PTR [ESP+4],OFFSET L_457ec8
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],2147483652
          mov EDX,OFFSET L_47a94c
L_423b23:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423b23
L_423b39:
          mov ECX,EAX
          mov EDI,29285
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov WORD PTR [EDX+L_47a950],DI
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_423aeb
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_423b80:
          mov DWORD PTR [ESP+4],OFFSET L_457e94
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],3
          mov EDX,OFFSET L_47a94c
L_423ba0:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423ba0
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          mov EAX,28271
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1668047206
          mov WORD PTR [EDX+L_47a950],AX
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_423aeb
L_423bf5:
          mov DWORD PTR [ESP+4],OFFSET L_457ef4
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],4
          mov EDX,OFFSET L_47a94c
L_423c15:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423c15
          jmp L_423b39
L_423c30:
          mov DWORD PTR [ESP+4],OFFSET L_457f2c
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1073741828
          mov EDX,OFFSET L_47a94c
L_423c53:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423c53
          mov ECX,EAX
          mov ESI,54
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov DWORD PTR [EDX+L_47a950],892498533
          mov WORD PTR [EDX+L_47a954],SI
          jmp L_423aeb
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_423cb0:
          mov DWORD PTR [ESP+4],OFFSET L_457f2c
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1073741828
          mov EDX,OFFSET L_47a94c
L_423cd3:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423cd3
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov DWORD PTR [EDX+L_47a950],1650618981
          mov BYTE PTR [EDX+L_47a954],0
          jmp L_423aeb
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_423d30:
          mov DWORD PTR [ESP+4],OFFSET L_457f2c
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1073741828
          mov EDX,OFFSET L_47a94c
L_423d53:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423d53
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          mov EBX,50
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov DWORD PTR [EDX+L_47a950],825586277
          mov WORD PTR [EDX+L_47a954],BX
          jmp L_423aeb
L_423dab:
          mov DWORD PTR [ESP+4],OFFSET L_457f74
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],2147483653
          mov EDX,OFFSET L_47a94c
L_423dce:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423dce
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1852404340
          mov DWORD PTR [EDX+L_47a950],7959657
          jmp L_423aeb
L_423e1a:
          mov DWORD PTR [ESP+4],OFFSET L_457fa4
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1073741829
          mov EDX,OFFSET L_47a94c
L_423e3d:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423e3d
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          mov ECX,98
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1852404340
          mov DWORD PTR [EDX+L_47a950],1652126825
          mov WORD PTR [EDX+L_47a954],CX
          jmp L_423aeb
L_423e95:
          mov DWORD PTR [ESP+4],OFFSET L_457fe0
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1610612741
          mov EDX,OFFSET L_47a94c
L_423eb8:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423eb8
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          mov EAX,115
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1852404340
          mov DWORD PTR [EDX+L_47a950],1652126825
          mov DWORD PTR [EDX+L_47a954],1717987177
          mov WORD PTR [EDX+L_47a958],AX
          jmp L_423aeb
L_423f1a:
          mov DWORD PTR [ESP+4],OFFSET L_458024
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],2147483654
          mov EDX,OFFSET L_47a94c
L_423f3d:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423f3d
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1869770595
          mov WORD PTR [EDX+L_47a950],24942
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_423aeb
L_423f8f:
          mov DWORD PTR [ESP+4],OFFSET L_458050
          mov DWORD PTR [ESP],1
          call _log_printf
          or DWORD PTR [L_479ea4],1073741830
          mov EDX,OFFSET L_47a94c
L_423fb2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_423fb2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          mov EBX,EAX
          cmove EDX,ECX
          add BL,AL
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1869770595
          mov DWORD PTR [EDX+L_47a950],1650614638
          mov BYTE PTR [EDX+L_47a954],0
          jmp L_423aeb
L_424005:
          mov DWORD PTR [ESP+4],OFFSET L_45808c
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_47a94c
          call _log_printf
          or DWORD PTR [L_479ea4],1610612742
          xor EAX,EAX
          or ECX,4294967295
          mov EDX,OFFSET L_45807c
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,13
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          rep movsb 
          jmp L_423aeb
L_42404d:
          mov DWORD PTR [ESP+4],OFFSET L_4580d4
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_47a94c
          call _log_printf
          or DWORD PTR [L_479ea4],2415919110
          xor EAX,EAX
          or ECX,4294967295
          mov EDX,OFFSET L_4580c8
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,9
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          rep movsb 
          jmp L_423aeb
L_424095:
          mov DWORD PTR [ESP+4],OFFSET L_458108
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_47a94c
          call _log_printf
          or DWORD PTR [L_479ea4],2147483655
          xor EAX,EAX
          or ECX,4294967295
          mov EDX,OFFSET L_4580fa
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,11
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          rep movsb 
          jmp L_423aeb
L_4240dd:
          mov DWORD PTR [ESP+4],OFFSET L_458174
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_47a94c
          call _log_printf
          or DWORD PTR [L_479ea4],1073741831
          xor EAX,EAX
          or ECX,4294967295
          mov EDX,OFFSET L_458166
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,13
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          rep movsb 
          jmp L_423aeb
L_424125:
          mov DWORD PTR [ESP+4],OFFSET L_45813c
          mov DWORD PTR [ESP],1
          mov EDI,OFFSET L_47a94c
          call _log_printf
          or DWORD PTR [L_479ea4],2415919111
          xor EAX,EAX
          or ECX,4294967295
          mov EDX,OFFSET L_45812e
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,13
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          rep movsb 
          jmp L_423aeb
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_setConsoleType:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_424183
          cmp BYTE PTR [EBX],0
          jne L_424190
L_424183:
          xor EAX,EAX
L_424185:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_424190:
          mov DWORD PTR [ESP+4],OFFSET L_457e3a
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4244a0
          mov DWORD PTR [ESP+4],OFFSET L_457e61
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4243c0
          mov DWORD PTR [ESP+4],OFFSET L_457e8a
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424500
          mov DWORD PTR [ESP+4],OFFSET L_457eb6
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424430
          mov DWORD PTR [ESP+4],OFFSET L_457ebd
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424430
          mov DWORD PTR [ESP+4],OFFSET L_457eea
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424566
          mov DWORD PTR [ESP+4],OFFSET L_457f21
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_42458d
          mov DWORD PTR [ESP+4],OFFSET L_457f58
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4245f4
          mov DWORD PTR [ESP+4],OFFSET L_457f62
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424660
          mov DWORD PTR [ESP+4],OFFSET L_4581f8
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4246c9
          mov DWORD PTR [ESP+4],OFFSET L_457f6c
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_42473a
          mov DWORD PTR [ESP+4],OFFSET L_457f97
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424770
          mov DWORD PTR [ESP+4],OFFSET L_457fd1
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4247a7
          mov DWORD PTR [ESP+4],OFFSET L_45801d
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_42484c
          mov DWORD PTR [ESP+4],OFFSET L_458046
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424815
          mov DWORD PTR [ESP+4],OFFSET L_45807c
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4247de
          mov DWORD PTR [ESP+4],OFFSET L_4580c8
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424908
          mov DWORD PTR [ESP+4],OFFSET L_4580fa
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4248aa
          mov DWORD PTR [ESP+4],OFFSET L_45812e
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_424883
          mov DWORD PTR [ESP+4],OFFSET L_458166
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4248e1
          mov DWORD PTR [ESP+4],OFFSET L_4581a4
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_424183
          or DWORD PTR [L_479ea4],1610612743
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_4581a4
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,17
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          mov EAX,1
          rep movsb 
          jmp L_424185
          .byte 0x90
L_4243c0:
          or DWORD PTR [L_479ea4],2
          mov EDX,OFFSET L_47a94c
L_4243cc:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4243cc
          mov ECX,EAX
          mov ESI,29305
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1752196474
          mov WORD PTR [EDX+L_47a950],SI
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_424185
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_424430:
          or DWORD PTR [L_479ea4],2147483652
          mov EDX,OFFSET L_47a94c
L_42443f:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42443f
L_424455:
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov ECX,29285
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov WORD PTR [EDX+L_47a950],CX
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_424185
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4244a0:
          or DWORD PTR [L_479ea4],1
          mov EDX,OFFSET L_47a94c
L_4244ac:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4244ac
          mov ECX,EAX
          mov EDI,110
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1869505912
          mov WORD PTR [EDX+L_47a950],DI
          jmp L_424185
          .byte 0x90
L_424500:
          or DWORD PTR [L_479ea4],3
          mov EDX,OFFSET L_47a94c
L_42450c:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42450c
          mov ECX,EAX
          mov EBX,28271
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1668047206
          mov WORD PTR [EDX+L_47a950],BX
          mov BYTE PTR [EDX+L_47a952],0
          jmp L_424185
L_424566:
          or DWORD PTR [L_479ea4],4
          mov EDX,OFFSET L_47a94c
L_424572:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_424572
          jmp L_424455
L_42458d:
          or DWORD PTR [L_479ea4],1073741828
          mov EDX,OFFSET L_47a94c
L_42459c:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42459c
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov DWORD PTR [EDX+L_47a950],1650618981
          mov BYTE PTR [EDX+L_47a954],0
          jmp L_424185
L_4245f4:
          or DWORD PTR [L_479ea4],1073741828
          mov EDX,OFFSET L_47a94c
L_424603:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_424603
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,54
          sbb EDX,OFFSET L_47a94f
          mov WORD PTR [EDX+L_47a954],AX
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov EAX,1
          mov DWORD PTR [EDX+L_47a950],892498533
          jmp L_424185
L_424660:
          or DWORD PTR [L_479ea4],1073741828
          mov EDX,OFFSET L_47a94c
L_42466f:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_42466f
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov DWORD PTR [EDX+L_47a950],825586277
          mov WORD PTR [EDX+L_47a954],50
          jmp L_424185
L_4246c9:
          or DWORD PTR [L_479ea4],1610612740
          mov EDX,OFFSET L_47a94c
L_4246d8:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4246d8
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,1
          sbb EDX,OFFSET L_47a94f
          mov DWORD PTR [EDX+L_47a94c],1886609770
          mov DWORD PTR [EDX+L_47a950],1768059493
          mov DWORD PTR [EDX+L_47a954],1936090727
          mov BYTE PTR [EDX+L_47a958],0
          jmp L_424185
L_42473a:
          or DWORD PTR [L_479ea4],2147483653
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          not EAX
          mov DWORD PTR [EAX+L_47a94b],1852404340
          mov DWORD PTR [EAX+L_47a94f],7959657
          mov EAX,1
          jmp L_424185
L_424770:
          or DWORD PTR [L_479ea4],1073741829
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_457f97
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,10
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          mov EAX,1
          rep movsb 
          jmp L_424185
L_4247a7:
          or DWORD PTR [L_479ea4],1610612741
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_457fd1
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,14
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          mov EAX,1
          rep movsb 
          jmp L_424185
L_4247de:
          or DWORD PTR [L_479ea4],1610612742
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_45807c
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          not EAX
          add EAX,OFFSET L_47a94b
L_424800:
          mov EDI,EAX
          mov ECX,13
          mov ESI,EDX
          mov EAX,1
          rep movsb 
          jmp L_424185
L_424815:
          or DWORD PTR [L_479ea4],1073741830
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_458046
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          not EAX
          add EAX,OFFSET L_47a94b
L_424837:
          mov EDI,EAX
          mov ECX,9
          mov ESI,EDX
          mov EAX,1
          rep movsb 
          jmp L_424185
L_42484c:
          or DWORD PTR [L_479ea4],2147483654
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_45801d
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,7
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          mov EAX,1
          rep movsb 
          jmp L_424185
L_424883:
          or DWORD PTR [L_479ea4],2415919111
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_45812e
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          not EAX
          add EAX,OFFSET L_47a94b
          jmp L_424800
L_4248aa:
          or DWORD PTR [L_479ea4],2147483655
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_4580fa
          mov ESI,EDX
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          mov ECX,11
          not EAX
          add EAX,OFFSET L_47a94b
          mov EDI,EAX
          mov EAX,1
          rep movsb 
          jmp L_424185
L_4248e1:
          or DWORD PTR [L_479ea4],1073741831
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_458166
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          not EAX
          add EAX,OFFSET L_47a94b
          jmp L_424800
L_424908:
          or DWORD PTR [L_479ea4],2415919110
          mov EDI,OFFSET L_47a94c
          or ECX,4294967295
          mov EDX,OFFSET L_4580c8
          repne scasb AL,BYTE PTR ES:[EDI]
          mov EAX,ECX
          not EAX
          add EAX,OFFSET L_47a94b
          jmp L_424837
          .byte 0x90
L_424930:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+36]
          test DWORD PTR [L_479f00],EBX
          jne L_424948
          test DWORD PTR [L_479f04],EBX
          je L_424950
L_424948:
          add ESP,24
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x90
L_424950:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call FUN_423750
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+32]
          je L_4249a0
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42497c:
          mov EAX,DWORD PTR [ESP+40]
          not EAX
          and EAX,DWORD PTR [L_479f00]
          or EAX,EBX
          mov DWORD PTR [L_479f00],EAX
          add ESP,24
          mov EAX,1
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4249a0:
          mov DWORD PTR [ESP],EAX
          call FUN_40abf0
          test EAX,EAX
          je L_4249d1
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_424948
L_4249d1:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call FUN_40aad0
          test EAX,EAX
          je L_424948
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_42497c
          .byte 0x66
          .byte 0x90
L_424a10:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          mov ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          call FUN_40ade0
          test EAX,EAX
          je L_424a50
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_424a50:
          mov DWORD PTR [ESP+36],ESI
          mov DWORD PTR [ESP+32],EBX
          add ESP,20
          pop EBX
          pop ESI
          jmp FUN_40acf0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_424a70:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_424aa4
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45828d
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          jne L_424ab0
L_424a9d:
          add ESP,24
          mov EAX,EDX
          pop EBX
          ret 
L_424aa4:
          xor EDX,EDX
          add ESP,24
          mov EAX,EDX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_424ab0:
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_458293
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_424a9d
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45829d
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_424a9d
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_4582a3
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_424a9d
          add ESP,24
          mov EAX,EBX
          pop EBX
          jmp FUN_449640
          .byte 0x66
          .byte 0x90
FUN_424b20:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          call _strlen
          lea ESI,DWORD PTR [EAX+1]
          test ESI,ESI
          jle L_424b56
          xor EAX,EAX
          xor EDX,EDX
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_424b40:
          movzx ECX,BYTE PTR [EBX+EDX*1]
          cmp CL,58
          je L_424b4f
          mov BYTE PTR [EBX+EAX*1],CL
          add EAX,1
L_424b4f:
          add EDX,1
          cmp ESI,EDX
          jne L_424b40
L_424b56:
          add ESP,20
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_424b60:
          cmp BYTE PTR [L_479f44],255
          jne L_424ba0
          cmp BYTE PTR [L_479f45],255
          jne L_424ba0
          cmp BYTE PTR [L_479f46],255
          jne L_424ba0
          cmp BYTE PTR [L_479f47],255
          jne L_424ba0
          cmp BYTE PTR [L_479f48],255
          jne L_424ba0
          xor EAX,EAX
          cmp BYTE PTR [L_479f49],255
          setne AL
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_424ba0:
          mov EAX,1
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_424bb0:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_424c18
          mov DWORD PTR [ESP+4],OFFSET L_4582ad
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_424c00
          mov DWORD PTR [ESP+4],OFFSET L_458478
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424c60
          or DWORD PTR [L_479f04],2
          mov EAX,1
L_424bf5:
          add ESP,20
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_424c00:
          mov DWORD PTR [ESP+4],OFFSET L_4582b3
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_424d10
L_424c18:
          mov DWORD PTR [ESP+4],OFFSET L_458478
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424c90
          mov EAX,DWORD PTR [L_479f00]
          mov DWORD PTR [ESP+4],OFFSET L_4582b8
          mov DWORD PTR [ESP],1
          and EAX,4294967291
          or EAX,2
          mov DWORD PTR [L_479f00],EAX
          call _log_printf
          add ESP,20
          mov EAX,1
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_424c60:
          mov DWORD PTR [ESP+4],OFFSET L_45847e
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424d70
          or DWORD PTR [L_479f04],6
          add ESP,20
          mov EAX,1
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_424c90:
          mov DWORD PTR [ESP+4],OFFSET L_45847e
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          je L_424d20
          mov DWORD PTR [ESP+4],OFFSET L_458485
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          je L_424d45
          mov DWORD PTR [ESP+4],OFFSET L_45848c
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          je L_424d99
          xor EBX,EBX
L_424cd6:
          mov DWORD PTR [ESP+4],OFFSET L_458346
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424dbe
          test EBX,EBX
          je L_424dea
          or DWORD PTR [L_479f04],536870912
          mov EAX,1
          jmp L_424bf5
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_424d10:
          xor EAX,EAX
          jmp L_424bf5
L_424d17:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_424d20:
          mov DWORD PTR [ESP+4],OFFSET L_4582ec
          mov DWORD PTR [ESP],1
          and DWORD PTR [L_479f00],4294967291
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424d45:
          mov DWORD PTR [ESP+4],OFFSET L_45831f
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],1
          call _log_printf
          mov EAX,1
          jmp L_424bf5
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_424d70:
          mov DWORD PTR [ESP+4],OFFSET L_458485
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424ebe
          or DWORD PTR [L_479f04],1
          mov EAX,1
          jmp L_424bf5
L_424d99:
          mov DWORD PTR [ESP+4],OFFSET L_458333
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],8
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424dbe:
          mov DWORD PTR [ESP+4],OFFSET L_458365
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424e12
          test EBX,EBX
          je L_424e3e
          or DWORD PTR [L_479f04],2097152
          mov EAX,1
          jmp L_424bf5
L_424dea:
          mov DWORD PTR [ESP+4],OFFSET L_45834f
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],536870912
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424e12:
          mov DWORD PTR [ESP+4],OFFSET L_458388
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424e66
          test EBX,EBX
          je L_424e96
          or DWORD PTR [L_479f04],1073741824
          mov EAX,1
          jmp L_424bf5
L_424e3e:
          mov DWORD PTR [ESP+4],OFFSET L_458370
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],2097152
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424e66:
          mov DWORD PTR [ESP+4],OFFSET L_4583a5
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424f14
          test EBX,EBX
          je L_424eec
          or DWORD PTR [L_479f04],2147483648
          mov EAX,1
          jmp L_424bf5
L_424e96:
          mov DWORD PTR [ESP+4],OFFSET L_458390
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],1073741824
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424ebe:
          mov DWORD PTR [ESP+4],OFFSET L_45848c
          mov DWORD PTR [ESP],ESI
          mov EBX,1
          call _stricmp
          test EAX,EAX
          jne L_424cd6
          or DWORD PTR [L_479f04],8
          mov EAX,1
          jmp L_424bf5
L_424eec:
          mov DWORD PTR [ESP+4],OFFSET L_4583b0
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],2147483648
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424f14:
          mov DWORD PTR [ESP+4],OFFSET L_4583c8
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424f40
          test EBX,EBX
          je L_424f6c
          or DWORD PTR [L_479f04],268435456
          mov EAX,1
          jmp L_424bf5
L_424f40:
          mov DWORD PTR [ESP+4],OFFSET L_4583e3
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424fbc
          test EBX,EBX
          je L_424f94
          or DWORD PTR [L_479f04],67108864
          mov EAX,1
          jmp L_424bf5
L_424f6c:
          mov DWORD PTR [ESP+4],OFFSET L_4583cf
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],268435456
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424f94:
          mov DWORD PTR [ESP+4],OFFSET L_4583ee
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],67108864
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_424fbc:
          mov DWORD PTR [ESP+4],OFFSET L_458406
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424fe8
          test EBX,EBX
          je L_425014
          or DWORD PTR [L_479f04],16777216
          mov EAX,1
          jmp L_424bf5
L_424fe8:
          mov DWORD PTR [ESP+4],OFFSET L_458413
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_425064
          test EBX,EBX
          je L_42503c
          or DWORD PTR [L_479f04],134217728
          mov EAX,1
          jmp L_424bf5
L_425014:
          mov DWORD PTR [ESP+4],OFFSET L_4583ee
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],16777216
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_42503c:
          mov DWORD PTR [ESP+4],OFFSET L_45841c
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],134217728
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_425064:
          mov DWORD PTR [ESP+4],OFFSET L_458432
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_425090
          test EBX,EBX
          je L_4250c0
          or DWORD PTR [L_479f04],OFFSET __ImageBase
          mov EAX,1
          jmp L_424bf5
L_425090:
          mov DWORD PTR [ESP+4],OFFSET L_458455
          mov DWORD PTR [ESP],ESI
          call _stricmp
          test EAX,EAX
          jne L_424d10
          test EBX,EBX
          je L_4250e8
          or DWORD PTR [L_479f04],8388608
          mov EAX,1
          jmp L_424bf5
L_4250c0:
          mov DWORD PTR [ESP+4],OFFSET L_45843d
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],OFFSET __ImageBase
          call _log_printf
          mov EAX,1
          jmp L_424bf5
L_4250e8:
          mov DWORD PTR [ESP+4],OFFSET L_458460
          mov DWORD PTR [ESP],1
          or DWORD PTR [L_479f00],8388608
          call _log_printf
          mov EAX,1
          jmp L_424bf5
FUN_425110:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EBX
          call _strlen
          test EAX,EAX
          jle L_4252bb
          mov ESI,EAX
          xor EDI,EDI
          xor EAX,EAX
          jmp L_42513a
L_425133:
          add EAX,1
          cmp ESI,EAX
          jle L_42515c
L_42513a:
          lea EDX,DWORD PTR [EBX+EAX*1]
          cmp BYTE PTR [EDX],61
          jne L_425133
          lea EDI,DWORD PTR [EBX+EAX*1+1]
          mov BYTE PTR [EDX],0
          cmp BYTE PTR [EDI],0
          je L_425260
          lea EAX,DWORD PTR [ESI+1]
          add EAX,1
          cmp ESI,EAX
          jg L_42513a
L_42515c:
          mov DWORD PTR [ESP],EBX
          call _strlen
          cmp ESI,EAX
          je L_4252f1
          mov DWORD PTR [ESP],EDI
          call _strlen
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov EBP,EAX
          call FUN_424bb0
          cmp EAX,1
          je L_4252d0
L_42518b:
          mov DWORD PTR [ESP+4],OFFSET L_4584e0
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4251e0
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f18],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4584e8
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_4251e0:
          mov DWORD PTR [ESP+4],OFFSET L_458508
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_425282
          mov DWORD PTR [ESP+4],OFFSET L_458530
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42532c
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f20],EAX
          jne L_4253d8
          .byte 0x66   # nop
          nop
L_425230:
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458948
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_42524e:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_425260:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458494
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_425282:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f1c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458510
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4252bb:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EBX
          call FUN_424bb0
          cmp EAX,1
          jne L_42530a
L_4252d0:
          mov DWORD PTR [ESP+4],OFFSET L_4584de
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4252f1:
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call FUN_424bb0
          cmp EAX,1
          je L_4252d0
          test EDI,EDI
          jne L_4255a4
L_42530a:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4588f8
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,44
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_42532c:
          mov DWORD PTR [ESP+4],OFFSET L_45855e
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_425398
          mov DWORD PTR [ESP+4],OFFSET L_458590
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4253fa
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f28],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45859c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_425398:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f24],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45856c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4253d8:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45853c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4253fa:
          mov DWORD PTR [ESP+4],OFFSET L_4585c0
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42544e
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f2c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4585d0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_42544e:
          mov DWORD PTR [ESP+4],OFFSET L_4585f6
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4254a2
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f30],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458600
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4254a2:
          mov DWORD PTR [ESP+4],OFFSET L_45861f
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4254f6
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f34],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458628
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4254f6:
          mov DWORD PTR [ESP+4],OFFSET L_458647
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_425550
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f38],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458650
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_425550:
          mov DWORD PTR [ESP+4],OFFSET L_458673
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4255ab
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f3c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458680
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4255a4:
          xor EBP,EBP
          jmp L_42518b
L_4255ab:
          mov DWORD PTR [ESP+4],OFFSET L_4586a5
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4255ff
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp EAX,-1
          mov DWORD PTR [L_479f40],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4586b0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4255ff:
          mov DWORD PTR [ESP+4],OFFSET L_4586d4
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42564a
          mov DWORD PTR [ESP],EDI
          call FUN_424a70
          test EAX,EAX
          mov DWORD PTR [L_479f08],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_4586e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_42564a:
          mov DWORD PTR [ESP+4],OFFSET L_458703
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_425695
          mov DWORD PTR [ESP],EDI
          call FUN_424a70
          test EAX,EAX
          mov DWORD PTR [L_479f0c],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_458710
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_425695:
          mov DWORD PTR [ESP+4],OFFSET L_458734
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_4256e0
          mov DWORD PTR [ESP],EDI
          call FUN_424a70
          test EAX,EAX
          mov DWORD PTR [L_479f10],EAX
          je L_425230
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_458740
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_4256e0:
          mov DWORD PTR [ESP+4],OFFSET L_458761
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_42573a
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EDI
          call _myatou32
          cmp AL,32
          mov BYTE PTR [L_479f15],AL
          ja L_425788
          test AL,AL
          je L_425230
          movzx EAX,AL
L_425718:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4587c0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,1
          jmp L_42524e
L_42573a:
          mov DWORD PTR [ESP+4],OFFSET L_4587de
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          mov ESI,EAX
          jne L_425850
          mov DWORD PTR [ESP],EDI
          call FUN_424b20
          mov DWORD PTR [ESP],EDI
          call _strlen
          cmp EAX,12
          je L_4257b4
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458854
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42524e
L_425788:
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458768
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov BYTE PTR [L_479f15],32
          mov EAX,32
          jmp L_425718
L_4257b4:
          mov DWORD PTR [ESP],EDI
          call _validateString
          test EAX,EAX
          je L_42588f
          mov DWORD PTR [ESP+4],OFFSET L_4587e4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          add EDI,2
          call _myatox8
          mov BYTE PTR [L_479f44],AL
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458801
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],1
          call _log_printf
L_425803:
          mov DWORD PTR [ESP+4],OFFSET L_458806
          mov DWORD PTR [ESP],1
          add ESI,1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          add EDI,2
          call _myatox8
          mov BYTE PTR [ESI+L_479f44],AL
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458801
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],1
          call _log_printf
          cmp ESI,5
          jne L_425803
          jmp L_4252d0
L_425850:
          mov DWORD PTR [ESP+4],OFFSET L_45889a
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_4258b4
          test EBP,EBP
          je L_42530a
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4588a4
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          jmp L_42524e
L_42588f:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458808
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+28],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_42524e
L_4258b4:
          mov DWORD PTR [ESP],EDI
          call _kvSetDvdKey
          test EAX,EAX
          je L_425230
          or DWORD PTR [L_479f00],33554432
          mov EAX,1
          jmp L_42524e
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_parseCmdOptions:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,540
          mov ESI,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],ESI
          call _strlen
          test EAX,EAX
          js L_425971
          mov EDI,EAX
          xor EDX,EDX
          xor EBX,EBX
          lea EBP,DWORD PTR [ESP+16]
          jmp L_425922
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_425910:
          test AL,AL
          je L_42592a
          add EBX,1
          mov BYTE PTR [ESP+EDX*1+16],AL
          add EDX,1
          cmp EDI,EBX
          jl L_425971
L_425922:
          movzx EAX,BYTE PTR [ESI+EBX*1]
          cmp AL,59
          jne L_425910
L_42592a:
          mov BYTE PTR [ESP+EDX*1+16],0
          mov EDX,EBP
L_425931:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_425931
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,EBP
          cmp EDX,4
          ja L_425981
          xor EDX,EDX
L_42596a:
          add EBX,1
          cmp EDI,EBX
          jge L_425922
L_425971:
          mov EAX,1
L_425976:
          add ESP,540
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_425981:
          mov DWORD PTR [ESP],EBP
          call FUN_425110
          test EAX,EAX
          je L_425976
          xor EDX,EDX
          jmp L_42596a
L_425991:
          jmp _applyIniOptions
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
_applyIniOptions:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [L_479f00]
          test EAX,536870912
          je L_426350
L_4259b5:
          test EAX,1073741824
          je L_4263b0
L_4259c0:
          test EAX,EAX
          js L_4259d2
          mov ESI,DWORD PTR [L_479f04]
          test ESI,ESI
          jns L_4261c3
L_4259d2:
          test EAX,268435456
          je L_426501
L_4259dd:
          test EAX,67108864
          je L_426450
L_4259e8:
          test EAX,16777216
          je L_4264b0
L_4259f3:
          test EAX,2097152
          je L_426401
L_4259fe:
          cmp BYTE PTR [L_479f15],0
          je L_425e15
L_425a0b:
          cmp DWORD PTR [L_479f30],-1
          je L_425e5d
L_425a18:
          cmp DWORD PTR [L_479f34],-1
          je L_425eb0
L_425a25:
          cmp DWORD PTR [L_479f18],-1
          je L_425f00
L_425a32:
          cmp DWORD PTR [L_479f1c],-1
          je L_425f50
L_425a3f:
          cmp DWORD PTR [L_479f20],-1
          je L_425fa0
L_425a4c:
          cmp DWORD PTR [L_479f24],-1
          je L_425ff0
L_425a59:
          cmp DWORD PTR [L_479f28],-1
          je L_426040
L_425a66:
          cmp DWORD PTR [L_479f2c],-1
          je L_426090
L_425a73:
          cmp DWORD PTR [L_479f38],-1
          je L_4260e0
L_425a80:
          cmp DWORD PTR [L_479f3c],-1
          je L_426130
L_425a8d:
          cmp DWORD PTR [L_479f40],-1
          je L_426180
L_425a9a:
          cmp BYTE PTR [L_479f44],255
          jne L_425b73
          cmp BYTE PTR [L_479f45],255
          jne L_425b73
          cmp BYTE PTR [L_479f46],255
          jne L_425b73
          cmp BYTE PTR [L_479f47],255
          jne L_425b73
          cmp BYTE PTR [L_479f48],255
          jne L_425b73
          cmp BYTE PTR [L_479f49],255
          jne L_425b73
          mov DWORD PTR [ESP],OFFSET L_4587de
          call _getIniValue
          test EAX,EAX
          mov EBX,EAX
          je L_425b73
          mov DWORD PTR [ESP],EAX
          call _strlen
          lea ESI,DWORD PTR [EAX+1]
          test ESI,ESI
          jle L_425b2e
          xor ECX,ECX
          xor EAX,EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_425b10:
          movzx EDX,BYTE PTR [EBX+EAX*1]
          cmp DL,58
          je L_425b1f
          mov BYTE PTR [EBX+ECX*1],DL
          add ECX,1
L_425b1f:
          add EAX,1
          cmp ESI,EAX
          jne L_425b10
          mov DWORD PTR [ESP],EBX
          call _strlen
L_425b2e:
          cmp EAX,12
          je L_426304
          mov DWORD PTR [ESP+4],OFFSET L_458a38
L_425b3f:
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],0
          call _showHexPairs
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458a10
          mov DWORD PTR [ESP],0
          call _log_printf
L_425b73:
          mov EAX,DWORD PTR [_g479ea8]
          sub EAX,2
          cmp EAX,3
          mov EAX,DWORD PTR [L_479f00]
          ja L_425c42
          test AL,1
          je L_426215
L_425b91:
          test AL,8
          je L_426264
L_425b99:
          test EAX,134217728
          je L_4262b3
L_425ba4:
          mov EBX,DWORD PTR [L_479f08]
          test EBX,EBX
          jne L_425d40
          test AL,4
          jne L_425c60
L_425bba:
          test EAX,OFFSET __ImageBase
          je L_4265a3
L_425bc5:
          test EAX,8388608
          je L_426552
L_425bd0:
          mov EDX,DWORD PTR [_g479ea8]
L_425bd6:
          cmp EDX,2
          jne L_425c42
          test AL,2
          je L_426620
L_425be3:
          mov DWORD PTR [ESP],OFFSET L_45847e
          call FUN_423750
          test EAX,EAX
          jne L_4265f4
          mov DWORD PTR [ESP],OFFSET L_45847e
          call FUN_40abf0
          test EAX,EAX
          je L_426dda
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_45847e
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425c30:
          mov EAX,DWORD PTR [L_479f10]
          test EAX,EAX
          je L_426730
L_425c3d:
          mov EAX,DWORD PTR [L_479f00]
L_425c42:
          test EAX,33554432
          je L_425de2
L_425c4d:
          cmp BYTE PTR [L_4c4f54],0
          je L_425db0
L_425c5a:
          add ESP,20
          pop EBX
          pop ESI
          ret 
L_425c60:
          mov DWORD PTR [ESP],OFFSET L_4586d4
          call _getIniValue
          test EAX,EAX
          mov EBX,EAX
          je L_42698e
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45828d
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          je L_426340
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_458293
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_426340
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45829d
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_426340
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_4582a3
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_426340
          mov EAX,EBX
          call FUN_449640
          test EAX,EAX
          mov DWORD PTR [L_479f08],EAX
          jne L_425d38
L_425d1a:
          mov DWORD PTR [ESP+4],OFFSET L_458a60
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_479f08],18
L_425d38:
          mov EAX,DWORD PTR [L_479f00]
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_425d40:
          mov ECX,DWORD PTR [L_479f0c]
          test ECX,ECX
          jne L_425bba
          test AL,4
          je L_425bba
          mov DWORD PTR [ESP],OFFSET L_458703
          call _getIniValue
          xor EDX,EDX
          test EAX,EAX
          mov EBX,EAX
          je L_425d8f
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45828d
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          jne L_4266af
L_425d8f:
          mov DWORD PTR [L_479f0c],EDX
          mov EDX,DWORD PTR [L_479f08]
          test EDX,EDX
          je L_4267f0
L_425da3:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425bba
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_425db0:
          mov DWORD PTR [ESP],OFFSET L_458ade
          call _getIniValue
          test EAX,EAX
          je L_425c5a
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_458ae2
          mov DWORD PTR [ESP],OFFSET L_4c4f54
          call _sprintf
          add ESP,20
          pop EBX
          pop ESI
          ret 
L_425de2:
          mov DWORD PTR [ESP],OFFSET L_45889a
          call _getIniValue
          test EAX,EAX
          je L_425c4d
          mov DWORD PTR [ESP],EAX
          call _kvSetDvdKey
          test EAX,EAX
          je L_425c4d
          or DWORD PTR [L_479f00],33554432
          jmp L_425c4d
L_425e15:
          mov DWORD PTR [ESP],OFFSET L_458761
          call FUN_40ade0
          test EAX,EAX
          je L_4267a0
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458761
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp DWORD PTR [L_479f30],-1
          mov BYTE PTR [L_479f15],0
          jne L_425a18
L_425e5d:
          mov DWORD PTR [ESP],OFFSET L_4585f6
          call FUN_40ade0
          test EAX,EAX
          je L_426a4c
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4585f6
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425e96:
          cmp DWORD PTR [L_479f34],-1
          mov DWORD PTR [L_479f30],EAX
          jne L_425a25
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_425eb0:
          mov DWORD PTR [ESP],OFFSET L_45861f
          call FUN_40ade0
          test EAX,EAX
          je L_426a33
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_45861f
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425ee9:
          cmp DWORD PTR [L_479f18],-1
          mov DWORD PTR [L_479f34],EAX
          jne L_425a32
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425f00:
          mov DWORD PTR [ESP],OFFSET L_4584e0
          call FUN_40ade0
          test EAX,EAX
          je L_4269b6
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4584e0
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425f39:
          cmp DWORD PTR [L_479f1c],-1
          mov DWORD PTR [L_479f18],EAX
          jne L_425a3f
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425f50:
          mov DWORD PTR [ESP],OFFSET L_458508
          call FUN_40ade0
          test EAX,EAX
          je L_42699d
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458508
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425f89:
          cmp DWORD PTR [L_479f20],-1
          mov DWORD PTR [L_479f1c],EAX
          jne L_425a4c
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425fa0:
          mov DWORD PTR [ESP],OFFSET L_458530
          call FUN_40ade0
          test EAX,EAX
          je L_426a7e
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458530
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_425fd9:
          cmp DWORD PTR [L_479f24],-1
          mov DWORD PTR [L_479f20],EAX
          jne L_425a59
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_425ff0:
          mov DWORD PTR [ESP],OFFSET L_45855e
          call FUN_40ade0
          test EAX,EAX
          je L_426a65
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_45855e
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426029:
          cmp DWORD PTR [L_479f28],-1
          mov DWORD PTR [L_479f24],EAX
          jne L_425a66
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426040:
          mov DWORD PTR [ESP],OFFSET L_458590
          call FUN_40ade0
          test EAX,EAX
          je L_426a1a
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458590
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426079:
          cmp DWORD PTR [L_479f2c],-1
          mov DWORD PTR [L_479f28],EAX
          jne L_425a73
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426090:
          mov DWORD PTR [ESP],OFFSET L_4585c0
          call FUN_40ade0
          test EAX,EAX
          je L_426a01
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4585c0
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_4260c9:
          cmp DWORD PTR [L_479f38],-1
          mov DWORD PTR [L_479f2c],EAX
          jne L_425a80
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_4260e0:
          mov DWORD PTR [ESP],OFFSET L_458647
          call FUN_40ade0
          test EAX,EAX
          je L_4269e8
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458647
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426119:
          cmp DWORD PTR [L_479f3c],-1
          mov DWORD PTR [L_479f38],EAX
          jne L_425a8d
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426130:
          mov DWORD PTR [ESP],OFFSET L_458673
          call FUN_40ade0
          test EAX,EAX
          je L_4269cf
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458673
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_426169:
          cmp DWORD PTR [L_479f40],-1
          mov DWORD PTR [L_479f3c],EAX
          jne L_425a9a
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_426180:
          mov DWORD PTR [ESP],OFFSET L_4586a5
          call FUN_40ade0
          test EAX,EAX
          je L_426a97
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4586a5
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,4294967295
L_4261b9:
          mov DWORD PTR [L_479f40],EAX
          jmp L_425a9a
L_4261c3:
          mov DWORD PTR [ESP],OFFSET L_4583a5
          call FUN_423750
          test EAX,EAX
          jne L_426672
          mov DWORD PTR [ESP],OFFSET L_4583a5
          call FUN_40abf0
          test EAX,EAX
          je L_426ca9
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4583a5
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_42620b:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259d2
L_426215:
          test BYTE PTR [L_479f04],1
          jne L_425b91
          mov DWORD PTR [ESP],OFFSET L_458485
          call FUN_423750
          test EAX,EAX
          je L_426ab0
          mov DWORD PTR [ESP+8],OFFSET L_458485
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_426252:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,1
          mov DWORD PTR [L_479f00],EAX
          jmp L_425b91
L_426264:
          test BYTE PTR [L_479f04],8
          jne L_425b99
          mov DWORD PTR [ESP],OFFSET L_45848c
          call FUN_423750
          test EAX,EAX
          je L_426aee
          mov DWORD PTR [ESP+8],OFFSET L_45848c
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_4262a1:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,8
          mov DWORD PTR [L_479f00],EAX
          jmp L_425b99
L_4262b3:
          test BYTE PTR [L_479f07],8
          jne L_425ba4
          mov DWORD PTR [ESP],OFFSET L_458413
          call FUN_423750
          test EAX,EAX
          je L_426bf4
          mov DWORD PTR [ESP+8],OFFSET L_458413
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_4262f0:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,134217728
          mov DWORD PTR [L_479f00],EAX
          jmp L_425ba4
L_426304:
          mov DWORD PTR [ESP],EBX
          call _validateString
          test EAX,EAX
          je L_4266a2
          xor ESI,ESI
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_426320:
          mov DWORD PTR [ESP],EBX
          add ESI,1
          add EBX,2
          call _myatox8
          mov BYTE PTR [ESI+L_479f43],AL
          cmp ESI,6
          jne L_426320
          jmp L_425b73
          .byte 0x66
          .byte 0x90
L_426340:
          mov DWORD PTR [L_479f08],EDX
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425d40
L_426350:
          test BYTE PTR [L_479f07],32
          jne L_4259b5
          mov DWORD PTR [ESP],OFFSET L_458346
          call FUN_423750
          test EAX,EAX
          je L_426890
          mov DWORD PTR [ESP+8],OFFSET L_458346
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42638d:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,536870912
          test EAX,1073741824
          mov DWORD PTR [L_479f00],EAX
          jne L_4259c0
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4263b0:
          test BYTE PTR [L_479f07],64
          jne L_4259c0
          mov DWORD PTR [ESP],OFFSET L_458388
          call FUN_423750
          test EAX,EAX
          je L_426850
          mov DWORD PTR [ESP+8],OFFSET L_458388
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_4263ed:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,1073741824
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259c0
L_426401:
          test BYTE PTR [L_479f06],32
          jne L_4259fe
          mov DWORD PTR [ESP],OFFSET L_458365
          call FUN_423750
          test EAX,EAX
          je L_426910
          mov DWORD PTR [ESP+8],OFFSET L_458365
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42643e:
          or DWORD PTR [L_479f00],2097152
          jmp L_4259fe
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_426450:
          test BYTE PTR [L_479f07],4
          jne L_4259e8
          mov DWORD PTR [ESP],OFFSET L_4583e3
          call FUN_423750
          test EAX,EAX
          je L_426950
          mov DWORD PTR [ESP+8],OFFSET L_4583e3
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42648d:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,67108864
          test EAX,16777216
          mov DWORD PTR [L_479f00],EAX
          jne L_4259f3
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4264b0:
          test BYTE PTR [L_479f07],1
          jne L_4259f3
          mov DWORD PTR [ESP],OFFSET L_458406
          call FUN_423750
          test EAX,EAX
          je L_4268d0
          mov DWORD PTR [ESP+8],OFFSET L_458406
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_4264ed:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,16777216
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259f3
L_426501:
          test BYTE PTR [L_479f07],16
          jne L_4259dd
          mov DWORD PTR [ESP],OFFSET L_4583c8
          call FUN_423750
          test EAX,EAX
          je L_426810
          mov DWORD PTR [ESP+8],OFFSET L_4583c8
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42653e:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,268435456
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259dd
L_426552:
          test BYTE PTR [L_479f06],128
          jne L_425bd0
          mov DWORD PTR [ESP],OFFSET L_458455
          call FUN_423750
          test EAX,EAX
          je L_426bb0
          mov DWORD PTR [ESP+8],OFFSET L_458455
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42658f:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,8388608
          mov DWORD PTR [L_479f00],EAX
          jmp L_425bd0
L_4265a3:
          test BYTE PTR [L_479f06],64
          jne L_425bc5
          mov DWORD PTR [ESP],OFFSET L_458432
          call FUN_423750
          test EAX,EAX
          je L_426c32
          mov DWORD PTR [ESP+8],OFFSET L_458432
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_4265e0:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,OFFSET __ImageBase
          mov DWORD PTR [L_479f00],EAX
          jmp L_425bc5
L_4265f4:
          mov DWORD PTR [ESP+8],OFFSET L_45847e
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_426610:
          and DWORD PTR [L_479f00],4294967291
          jmp L_425c30
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_426620:
          test BYTE PTR [L_479f04],2
          jne L_425be3
          mov DWORD PTR [ESP],OFFSET L_458478
          call FUN_423750
          test EAX,EAX
          je L_426c70
          mov DWORD PTR [ESP+8],OFFSET L_458478
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42665d:
          mov EAX,DWORD PTR [L_479f00]
          and EAX,4294967291
          or EAX,2
          mov DWORD PTR [L_479f00],EAX
          jmp L_425be3
L_426672:
          mov DWORD PTR [ESP+8],OFFSET L_4583a5
          mov DWORD PTR [ESP+4],OFFSET L_458208
          mov DWORD PTR [ESP],1
          call _log_printf
L_42668e:
          mov EAX,DWORD PTR [L_479f00]
          or EAX,2147483648
          mov DWORD PTR [L_479f00],EAX
          jmp L_4259d2
L_4266a2:
          mov DWORD PTR [ESP+4],OFFSET L_4589e0
          jmp L_425b3f
L_4266af:
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_458293
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_425d8f
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45829d
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_425d8f
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_4582a3
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_425d8f
          mov EAX,EBX
          call FUN_449640
          mov EDX,EAX
          jmp L_425d8f
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_426730:
          mov DWORD PTR [ESP],OFFSET L_458734
          call _getIniValue
          xor EDX,EDX
          test EAX,EAX
          mov EBX,EAX
          je L_426769
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45828d
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,17
          jne L_426b2c
L_426769:
          cmp DWORD PTR [L_479f08],EDX
          mov DWORD PTR [L_479f10],EDX
          jne L_425c3d
          mov DWORD PTR [ESP+4],OFFSET L_458ac3
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_479f10],0
          jmp L_425c3d
          .byte 0x66
          .byte 0x90
L_4267a0:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458761
          call FUN_40acf0
          cmp AL,32
          mov BYTE PTR [L_479f15],AL
          jbe L_425a0b
          movzx EAX,AL
          mov DWORD PTR [ESP+4],OFFSET L_458988
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov BYTE PTR [L_479f15],32
          jmp L_425a0b
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4267f0:
          mov DWORD PTR [ESP+4],OFFSET L_458aa0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_425da3
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_426810:
          mov DWORD PTR [ESP],OFFSET L_4583c8
          call FUN_40abf0
          test EAX,EAX
          je L_426e54
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4583c8
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426844:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259dd
          .byte 0x66
          .byte 0x90
L_426850:
          mov DWORD PTR [ESP],OFFSET L_458388
          call FUN_40abf0
          test EAX,EAX
          je L_426ce6
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458388
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426884:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259c0
          .byte 0x66
          .byte 0x90
L_426890:
          mov DWORD PTR [ESP],OFFSET L_458346
          call FUN_40abf0
          test EAX,EAX
          je L_426d60
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458346
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_4268c4:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259b5
          .byte 0x66
          .byte 0x90
L_4268d0:
          mov DWORD PTR [ESP],OFFSET L_458406
          call FUN_40abf0
          test EAX,EAX
          je L_426d23
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458406
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426904:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259f3
          .byte 0x66
          .byte 0x90
L_426910:
          mov DWORD PTR [ESP],OFFSET L_458365
          call FUN_40abf0
          test EAX,EAX
          je L_426d9d
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458365
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4259fe
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_426950:
          mov DWORD PTR [ESP],OFFSET L_4583e3
          call FUN_40abf0
          test EAX,EAX
          je L_426e17
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_4583e3
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426984:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_4259e8
L_42698e:
          mov DWORD PTR [L_479f08],0
          jmp L_425d1a
L_42699d:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458508
          call FUN_40acf0
          jmp L_425f89
L_4269b6:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4584e0
          call FUN_40acf0
          jmp L_425f39
L_4269cf:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458673
          call FUN_40acf0
          jmp L_426169
L_4269e8:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458647
          call FUN_40acf0
          jmp L_426119
L_426a01:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4585c0
          call FUN_40acf0
          jmp L_4260c9
L_426a1a:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458590
          call FUN_40acf0
          jmp L_426079
L_426a33:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_45861f
          call FUN_40acf0
          jmp L_425ee9
L_426a4c:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4585f6
          call FUN_40acf0
          jmp L_425e96
L_426a65:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_45855e
          call FUN_40acf0
          jmp L_426029
L_426a7e:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_458530
          call FUN_40acf0
          jmp L_425fd9
L_426a97:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],OFFSET L_4586a5
          call FUN_40acf0
          jmp L_4261b9
L_426ab0:
          mov DWORD PTR [ESP],OFFSET L_458485
          call FUN_40abf0
          test EAX,EAX
          je L_426f85
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458485
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426ae4:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425b91
L_426aee:
          mov DWORD PTR [ESP],OFFSET L_45848c
          call FUN_40abf0
          test EAX,EAX
          je L_426e91
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_45848c
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426b22:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425b99
L_426b2c:
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_458293
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,32
          je L_426769
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_45829d
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,34
          je L_426769
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_4582a3
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,36
          je L_426769
          mov EAX,EBX
          call FUN_449640
          mov EDX,EAX
          jmp L_426769
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_426bb0:
          mov DWORD PTR [ESP],OFFSET L_458455
          call FUN_40abf0
          test EAX,EAX
          je L_426f0b
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458455
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426be4:
          mov EDX,DWORD PTR [_g479ea8]
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425bd6
L_426bf4:
          mov DWORD PTR [ESP],OFFSET L_458413
          call FUN_40abf0
          test EAX,EAX
          je L_426ece
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458413
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426c28:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425ba4
L_426c32:
          mov DWORD PTR [ESP],OFFSET L_458432
          call FUN_40abf0
          test EAX,EAX
          je L_426f48
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458432
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
L_426c66:
          mov EAX,DWORD PTR [L_479f00]
          jmp L_425bc5
L_426c70:
          mov DWORD PTR [ESP],OFFSET L_458478
          call FUN_40abf0
          test EAX,EAX
          je L_426fc2
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],OFFSET L_458478
          mov DWORD PTR [ESP+4],OFFSET L_458244
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_425be3
L_426ca9:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4583a5
          call FUN_40aad0
          test EAX,EAX
          je L_42620b
          mov DWORD PTR [ESP+8],OFFSET L_4583a5
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42668e
L_426ce6:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458388
          call FUN_40aad0
          test EAX,EAX
          je L_426884
          mov DWORD PTR [ESP+8],OFFSET L_458388
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4263ed
L_426d23:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458406
          call FUN_40aad0
          test EAX,EAX
          je L_426904
          mov DWORD PTR [ESP+8],OFFSET L_458406
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4264ed
L_426d60:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458346
          call FUN_40aad0
          test EAX,EAX
          je L_4268c4
          mov DWORD PTR [ESP+8],OFFSET L_458346
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42638d
L_426d9d:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458365
          call FUN_40aad0
          test EAX,EAX
          je L_4259fe
          mov DWORD PTR [ESP+8],OFFSET L_458365
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42643e
L_426dda:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_45847e
          call FUN_40aad0
          test EAX,EAX
          je L_425c30
          mov DWORD PTR [ESP+8],OFFSET L_45847e
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_426610
L_426e17:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4583e3
          call FUN_40aad0
          test EAX,EAX
          je L_426984
          mov DWORD PTR [ESP+8],OFFSET L_4583e3
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42648d
L_426e54:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4583c8
          call FUN_40aad0
          test EAX,EAX
          je L_426844
          mov DWORD PTR [ESP+8],OFFSET L_4583c8
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42653e
L_426e91:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_45848c
          call FUN_40aad0
          test EAX,EAX
          je L_426b22
          mov DWORD PTR [ESP+8],OFFSET L_45848c
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4262a1
L_426ece:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458413
          call FUN_40aad0
          test EAX,EAX
          je L_426c28
          mov DWORD PTR [ESP+8],OFFSET L_458413
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4262f0
L_426f0b:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458455
          call FUN_40aad0
          test EAX,EAX
          je L_426be4
          mov DWORD PTR [ESP+8],OFFSET L_458455
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42658f
L_426f48:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458432
          call FUN_40aad0
          test EAX,EAX
          je L_426c66
          mov DWORD PTR [ESP+8],OFFSET L_458432
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4265e0
L_426f85:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458485
          call FUN_40aad0
          test EAX,EAX
          je L_426ae4
          mov DWORD PTR [ESP+8],OFFSET L_458485
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_426252
L_426fc2:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_458478
          call FUN_40aad0
          test EAX,EAX
          je L_425be3
          mov DWORD PTR [ESP+8],OFFSET L_458478
          mov DWORD PTR [ESP+4],OFFSET L_458227
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_42665d
          .byte 0x90
FUN_427000:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EBX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EBX
          call _strlen
          test EAX,EAX
          jle L_427172
          mov ESI,EAX
          xor EDI,EDI
          xor EAX,EAX
          jmp L_427029
L_427022:
          add EAX,1
          cmp ESI,EAX
          jle L_42704b
L_427029:
          lea EDX,DWORD PTR [EBX+EAX*1]
          cmp BYTE PTR [EDX],44
          jne L_427022
          lea EDI,DWORD PTR [EBX+EAX*1+1]
          mov BYTE PTR [EDX],0
          cmp BYTE PTR [EDI],0
          je L_427130
          lea EAX,DWORD PTR [ESI+1]
          add EAX,1
          cmp ESI,EAX
          jg L_427029
L_42704b:
          mov DWORD PTR [ESP],EBX
          call _strlen
          cmp ESI,EAX
          je L_427172
          mov EDX,DWORD PTR [L_4c8fe0]
          cmp EDX,15
          jg L_427101
          imul EDX,EDX,1028
          add EAX,1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          add EDX,OFFSET L_4c4fa0
          mov DWORD PTR [ESP],EDX
          call _memcpy
          mov ESI,DWORD PTR [L_4c8fe0]
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EDI
          call _myatou32
          imul ESI,ESI,1028
          mov DWORD PTR [ESI+L_4c53a0],EAX
          mov EAX,DWORD PTR [L_4c8fe0]
          imul EDX,EAX,1028
          mov ECX,DWORD PTR [EDX+L_4c53a0]
          cmp ECX,-1
          je L_427151
          add EAX,1
          add EDX,OFFSET L_4c4fa0
          mov DWORD PTR [ESP+16],ECX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],OFFSET L_458ae8
          mov DWORD PTR [ESP],1
          call _log_printf
          add DWORD PTR [L_4c8fe0],1
          add ESP,32
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
L_427101:
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],16
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET L_458b80
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,32
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x66
          .byte 0x90
L_427130:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458494
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,32
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_427151:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458b28
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,32
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_427172:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_458bbc
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,32
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_parseRawPatches:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,540
          mov ESI,DWORD PTR [ESP+560]
          mov DWORD PTR [ESP],ESI
          call _strlen
          test EAX,EAX
          js L_427231
          mov EDI,EAX
          xor EDX,EDX
          xor EBX,EBX
          lea EBP,DWORD PTR [ESP+16]
          jmp L_4271e2
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4271d0:
          test AL,AL
          je L_4271ea
          add EBX,1
          mov BYTE PTR [ESP+EDX*1+16],AL
          add EDX,1
          cmp EDI,EBX
          jl L_427231
L_4271e2:
          movzx EAX,BYTE PTR [ESI+EBX*1]
          cmp AL,59
          jne L_4271d0
L_4271ea:
          mov BYTE PTR [ESP+EDX*1+16],0
          mov EDX,EBP
L_4271f1:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4271f1
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          sub EDX,EBP
          cmp EDX,4
          ja L_427241
          xor EDX,EDX
L_42722a:
          add EBX,1
          cmp EDI,EBX
          jge L_4271e2
L_427231:
          mov EAX,1
L_427236:
          add ESP,540
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_427241:
          mov DWORD PTR [ESP],EBP
          call FUN_427000
          test EAX,EAX
          je L_427236
          xor EDX,EDX
          jmp L_42722a
L_427251:
          jmp L_427260
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
L_427260:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1052
          cmp DWORD PTR [L_4c4f94],15
          mov EBP,DWORD PTR [ESP+1072]
          mov DWORD PTR [ESP+8],EBP
          jg L_4272f0
          lea EDI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_458bf5
          mov DWORD PTR [ESP],EDI
          call _sprintf
          mov EAX,DWORD PTR [L_4c4f94]
          test EAX,EAX
          jle L_427310
          mov EBX,OFFSET L_4c0c94
          xor ESI,ESI
          jmp L_4272b6
L_4272a4:
          mov EAX,DWORD PTR [L_4c4f94]
          add ESI,1
          add EBX,1068
          cmp EAX,ESI
          jle L_427310
L_4272b6:
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call _stricmp
          test EAX,EAX
          jne L_4272a4
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_458bfc
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,1052
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4272f0:
          mov DWORD PTR [ESP+4],OFFSET L_458c54
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,1052
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_427310:
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+4],EDI
          add EAX,OFFSET L_4c0c94
          mov DWORD PTR [ESP],EAX
          call _strcpy
          add DWORD PTR [L_4c4f94],1
          add ESP,1052
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_loadAddons:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1580
          mov DWORD PTR [ESP],OFFSET L_458c9c
          call _getIniValue
          test EAX,EAX
          je L_42748e
          mov DWORD PTR [ESP],EAX
          mov EBX,EAX
          call _strlen
          test EAX,EAX
          mov DWORD PTR [ESP+24],EAX
          js L_42748e
          xor EAX,EAX
          xor EBP,EBP
          jmp L_427398
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_427380:
          test DL,DL
          je L_4273a1
          mov BYTE PTR [ESP+EAX*1+32],DL
          add EAX,1
L_42738b:
          add EBP,1
          cmp DWORD PTR [ESP+24],EBP
          jl L_42748e
L_427398:
          movzx EDX,BYTE PTR [EBX+EBP*1]
          cmp DL,58
          jne L_427380
L_4273a1:
          lea EDX,DWORD PTR [ESP+32]
          mov BYTE PTR [ESP+EAX*1+32],0
L_4273aa:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4273aa
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          lea EAX,DWORD PTR [ESP+32]
          sbb EDX,3
          sub EDX,EAX
          xor EAX,EAX
          cmp EDX,4
          jbe L_42738b
          cmp DWORD PTR [L_4c4f94],15
          jg L_4274a0
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_458bf5
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP],EAX
          call _sprintf
          mov EAX,DWORD PTR [L_4c4f94]
          test EAX,EAX
          jle L_4274d0
          mov EDI,OFFSET L_4c0c94
          xor ESI,ESI
          jmp L_427446
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_427430:
          mov EAX,DWORD PTR [L_4c4f94]
          add ESI,1
          add EDI,1068
          cmp ESI,EAX
          jge L_4274d0
L_427446:
          lea EAX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _stricmp
          test EAX,EAX
          jne L_427430
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_458bfc
          mov DWORD PTR [ESP],1
          add EBP,1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp DWORD PTR [ESP+24],EBP
          mov EAX,DWORD PTR [ESP+28]
          jge L_427398
L_42748e:
          add ESP,1580
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_4274a0:
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_458c54
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+28]
          jmp L_42738b
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4274d0:
          imul EAX,EAX,1068
          lea EDI,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+4],EDI
          add EAX,OFFSET L_4c0c94
          mov DWORD PTR [ESP],EAX
          call _strcpy
          add DWORD PTR [L_4c4f94],1
          xor EAX,EAX
          jmp L_42738b
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .text.startup,"xr"
.p2align 4
FUN_449640:
          push EBX
          mov EBX,EAX
          sub ESP,24
          mov DWORD PTR [ESP+8],9
          mov DWORD PTR [ESP+4],OFFSET L_457df0
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EDX,85
          je L_44977b
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_457dfa
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          jne L_44973a
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_457e01
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,89
          je L_44977b
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_457e0a
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,88
          je L_44977b
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_457e13
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          je L_449733
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_457e1c
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,86
          je L_44977b
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_457e25
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,87
          je L_44977b
L_449733:
          mov EDX,90
          jmp L_44977b
L_44973a:
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457e2e
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          test EAX,EAX
          mov EDX,18
          je L_44977b
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_457e34
          mov DWORD PTR [ESP],EBX
          call _strnicmp
          cmp EAX,1
          sbb EDX,EDX
          and EDX,65
L_44977b:
          add ESP,24
          mov EAX,EDX
          pop EBX
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66
          .byte 0x90
          .byte 0x66   # nop
          nop

.section .rdata,"dr"
.p2align 2
L_457df0:
          .string "wirelessx"
L_457dfa:
          .string "wiredx"
L_457e01:
          .string "wiredxb1"
L_457e0a:
          .string "wiredxb2"
L_457e13:
          .string "wiredxb3"
L_457e1c:
          .string "wiredxf1"
L_457e25:
          .string "wiredxf2"
L_457e2e:
          .string "eject"
L_457e34:
          .string "kiosk"
L_457e3a:
          .string "xenon"
L_457e40:
          .string "Using xenon ctype (perbox file)\n"
L_457e61:
          .string "zephyr"
L_457e68:
          .string "Using zephyr ctype (perbox file)\n"
L_457e8a:
          .string "falcon"
          .zero 3
L_457e94:
          .string "Using falcon ctype (perbox file)\n"
L_457eb6:
          .string "jasper"
L_457ebd:
          .string "jasperbc"
          .zero 2
L_457ec8:
          .string "Using jasper ctype (perbox file)\n"
L_457eea:
          .string "jaspersb"
          .zero 1
L_457ef4:
          .string "Using jasper smallblock ctype (perbox file)\n"
L_457f21:
          .string "jasperbb"
          .zero 2
L_457f2c:
          .string "Using jasper big block ctype (perbox file)\n"
L_457f58:
          .string "jasper256"
L_457f62:
          .string "jasper512"
L_457f6c:
          .string "trinity"
L_457f74:
          .string "Using trinity ctype (perbox file)\n"
L_457f97:
          .string "trinitybb"
          .zero 3
L_457fa4:
          .string "Using trinity big block ctype (perbox file)\n"
L_457fd1:
          .string "trinitybigffs"
          .zero 1
L_457fe0:
          .string "Using trinity big block big file system ctype (perbox file)\n"
L_45801d:
          .string "corona"
L_458024:
          .string "Using corona ctype (perbox file)\n"
L_458046:
          .string "coronabb"
          .zero 1
L_458050:
          .string "Using corona big block ctype (perbox file)\n"
L_45807c:
          .string "coronabigffs"
          .zero 3
L_45808c:
          .string "Using corona big block big file system ctype (perbox file)\n"
L_4580c8:
          .string "corona4g"
          .zero 3
L_4580d4:
          .string "Using corona MMC ctype (perbox file)\n"
L_4580fa:
          .string "winchester"
          .zero 3
L_458108:
          .string "Using winchester ctype (perbox file)\n"
L_45812e:
          .string "winchester4g"
          .zero 1
L_45813c:
          .string "Using winchester MMC ctype (perbox file)\n"
L_458166:
          .string "winchesterbb"
          .zero 1
L_458174:
          .string "Using winchester big block ctype (perbox file)\n"
L_4581a4:
          .string "winchesterbigffs"
          .zero 3
L_4581b8:
          .string "Using winchester big block big file system ctype (perbox file)\n"
L_4581f8:
          .string "jasperbigffs"
          .zero 3
L_458208:
          .string "Using %s option (perbox file)\n"
L_458227:
          .string "Using %s option (ini file)\n"
          .zero 1
L_458244:
          .string "***** WARNING: options.ini setting '%s' invalid value '%s', discarding!\n"
L_45828d:
          .string "power"
L_458293:
          .string "remopower"
L_45829d:
          .string "remox"
L_4582a3:
          .string "winbutton"
L_4582ad:
          .string "false"
L_4582b3:
          .string "true"
L_4582b8:
          .string "Using NODVD (tray status fully open check) option"
          .zero 2
L_4582ec:
          .string "Using OLDDVD (tray status not closed check) option"
L_45831f:
          .string "Using CYGNOS option"
L_458333:
          .string "Using DEMON option"
L_458346:
          .string "nomobile"
L_45834f:
          .string "Using NOMOBILE option"
L_458365:
          .string "smcnocheck"
L_458370:
          .string "Using SMCNOCHECK option"
L_458388:
          .string "noremap"
L_458390:
          .string "Using NOREMAP option"
L_4583a5:
          .string "noecdremap"
L_4583b0:
          .string "Using NOECDREMAP option"
L_4583c8:
          .string "nandmu"
L_4583cf:
          .string "Using NANDMU option"
L_4583e3:
          .string "nosecurity"
L_4583ee:
          .string "Using NOSECURITY option"
L_458406:
          .string "nosusecurity"
L_458413:
          .string "patchsmc"
L_45841c:
          .string "Using PATCHSMC option"
L_458432:
          .string "smcnoeject"
L_45843d:
          .string "Using SMCNOEJECT option"
L_458455:
          .string "smcnoblink"
L_458460:
          .string "Using SMCNOBLINK option"
L_458478:
          .string "nodvd"
L_45847e:
          .string "olddvd"
L_458485:
          .string "cygnos"
L_45848c:
          .string "demon"
          .zero 2
L_458494:
          .string "\n\n***** ERROR: option '%s' provided on command line with = but no value!\n"
L_4584de:
          .string "\n"
L_4584e0:
          .string "cputemp"
L_4584e8:
          .string "Using CPUTEMP option, value %d\n"
L_458508:
          .string "gputemp"
L_458510:
          .string "Using GPUTEMP option, value %d\n"
L_458530:
          .string "edramtemp"
          .zero 2
L_45853c:
          .string "Using EDRAMTEMP option, value %d\n"
L_45855e:
          .string "overcputemp"
          .zero 2
L_45856c:
          .string "Using OVERCPUTEMP option, value %d\n"
L_458590:
          .string "overgputemp"
L_45859c:
          .string "Using OVERGPUTEMP option, value %d\n"
L_4585c0:
          .string "overedramtemp"
          .zero 2
L_4585d0:
          .string "Using OVEREDRAMTEMP option, value %d\n"
L_4585f6:
          .string "cpufan"
          .zero 3
L_458600:
          .string "Using CPUFAN option, value %d\n"
L_45861f:
          .string "gpufan"
          .zero 2
L_458628:
          .string "Using GPUFAN option, value %d\n"
L_458647:
          .string "avregion"
L_458650:
          .string "Using AVREGION option, value 0x%x\n"
L_458673:
          .string "gameregion"
          .zero 2
L_458680:
          .string "Using GAMEREGION option, value 0x%x\n"
L_4586a5:
          .string "dvdregion"
          .zero 1
L_4586b0:
          .string "Using DVDREGION option, value 0x%x\n"
L_4586d4:
          .string "xellbutton"
          .zero 1
L_4586e0:
          .string "Using XELLBUTTON option, value %s\n"
L_458703:
          .string "xellbutton2"
          .zero 1
L_458710:
          .string "Using XELLBUTTON2 option, value %s\n"
L_458734:
          .string "dualboot"
          .zero 3
L_458740:
          .string "Using DUALBOOT option, value %s\n"
L_458761:
          .string "cfldv"
          .zero 1
L_458768:
          .string "***** WARNING: cfldv value %d on command line is too large, setting to max value of 32\n"
L_4587c0:
          .string "Using CFLDV option, value %d\n"
L_4587de:
          .string "macid"
L_4587e4:
          .string "Using MACID option address: "
L_458801:
          .string "%02x"
L_458806:
          .string ":"
L_458808:
          .string "\n\n***** ERROR: invalid values in macid %s provided on the command line!\n"
          .zero 3
L_458854:
          .string "\n\n***** ERROR: invalid length macid %s provided on the command line!\n"
L_45889a:
          .string "dvdkey"
          .zero 3
L_4588a4:
          .string "\n\n***** ERROR: unknown option '%s' with value '%s' provided on the command line!\n"
          .zero 2
L_4588f8:
          .string "\n\n***** ERROR: unknown or incomplete option '%s' provided on the command line!\n"
L_458948:
          .string "\n\n***** ERROR: parsing option '%s', value '%s' is incorrect!\n"
          .zero 2
L_458988:
          .string "***** WARNING: cfldv value %d in options.ini is too large, setting to max value of 32\n"
          .zero 1
L_4589e0:
          .string "***** WARNING: invalid characters in macid '"
          .zero 3
L_458a10:
          .string "' provided in ini file! Discarding!\n"
          .zero 3
L_458a38:
          .string "***** WARNING: invalid length macid '"
          .zero 2
L_458a60:
          .string "default console DVD eject button is being used to start xell\n"
          .zero 2
L_458aa0:
          .string "alternate xell button is disabled\n"
L_458ac3:
          .string "dualboot setting ignored!\n"
L_458ade:
          .string "rev"
L_458ae2:
          .string "_%s"
          .zero 2
L_458ae8:
          .string "parsed [rawpatch] (%d) from command line file '%s' offset 0x%x\n"
L_458b28:
          .string "***** ERROR: [rawpatch] command option '%s' does not appear to have sane offset info!\n"
          .zero 1
L_458b80:
          .string "***** ERROR: %d of %d [rawpatch] slots are already full!\n"
          .zero 2
L_458bbc:
          .string "***** ERROR: parsing optional patch string '%s' failed!\n"
L_458bf5:
          .string "%s.bin"
L_458bfc:
          .string "***** WARNING: %s was provided both on command line and in ini, filtered duplicate!\n"
          .zero 3
L_458c54:
          .string "***** WARNING: exceeded total number of optional patches with ini  %s!\n"
L_458c9c:
          .string "addon"
          .zero 2

.section .rdata$zzz,"dr"
.p2align 2
          .byte 0x47
          .byte 0x43
          .byte 0x43
          .byte 0x3a
          .byte 0x20
          .byte 0x28
          .byte 0x52
          .byte 0x65
          .byte 0x76
          .byte 0x32
          .byte 0x2c
          .byte 0x20
          .byte 0x42
          .byte 0x75
          .byte 0x69
          .byte 0x6c
          .byte 0x74
          .byte 0x20
          .byte 0x62
          .byte 0x79
          .byte 0x20
          .byte 0x4d
          .byte 0x53
          .byte 0x59
          .byte 0x53
          .byte 0x32
          .byte 0x20
          .byte 0x70
          .byte 0x72
          .byte 0x6f
          .byte 0x6a
          .byte 0x65
          .byte 0x63
          .byte 0x74
          .byte 0x29
          .byte 0x20
          .byte 0x36
          .byte 0x2e
          .byte 0x32
          .byte 0x2e
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .eh_frame,"dr"
.p2align 2
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1
          .byte 0x7a
          .byte 0x52
          .byte 0x0
          .byte 0x1
          .byte 0x7c
          .byte 0x8
          .byte 0x1
          .byte 0x1b
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x88
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4236f0 - .
          .byte 0x3b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x48
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x6e
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_449640 - .
          .byte 0x42
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x45
          .byte 0xe
          .byte 0x20
          .byte 0x3
          .byte 0x38
          .byte 0x1
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_423730 - .
          .byte 0x12
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_423750 - .
          .byte 0xde
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x10
          .byte 0x2
          .byte 0x64
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x60
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _iniConsoleType - .
          .byte 0x3d
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x3
          .byte 0xc4
          .byte 0x2
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _setConsoleType - .
          .byte 0xbf
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x52
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_424930 - .
          .byte 0xde
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x42
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_424a10 - .
          .byte 0x52
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x73
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x4b
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_424a70 - .
          .byte 0xae
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x6c
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x45
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x66
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_424b20 - .
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x74
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_424b60 - .
          .byte 0x46
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_424bb0 - .
          .byte 0x60
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x43
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x2
          .byte 0x53
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x62
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_425110 - .
          .byte 0xc8
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xbd
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x2
          .byte 0x71
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x4b
          .byte 0xb
          .byte 0x5b
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x65
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x74
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _parseCmdOptions - .
          .byte 0xb1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x4
          .byte 0x2
          .byte 0x92
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _applyIniOptions - .
          .byte 0x5f
          .byte 0x16
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x3
          .byte 0xb8
          .byte 0x2
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x3
          .byte 0x7f
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long FUN_427000 - .
          .byte 0x93
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0xf2
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x67
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x5b
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x5b
          .byte 0xa
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x5b
          .byte 0xe
          .byte 0x10
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _parseRawPatches - .
          .byte 0xb1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x4
          .byte 0x2
          .byte 0x92
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_427260 - .
          .byte 0xd9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0x7a
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x5a
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x42
          .byte 0xb
          .byte 0x64
          .byte 0xe
          .byte 0x14
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _loadAddons - .
          .byte 0xbc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x87
          .byte 0x3
          .byte 0x41
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x46
          .byte 0xe
          .byte 0xc0
          .byte 0xc
          .byte 0x3
          .byte 0x4a
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0xc
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc5
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
