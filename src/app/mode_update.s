# app/mode_update.s -- "Usage: %s update", bad block handling
#
# mixed: `#@C name` lines are functions from mode_update.c (re/splice.py)
#
# original placement:
#   .bss           0046f040-0046f160
#   .data          0044a008-0044a020
#   .eh_frame      00465650-0046599c
#   .rdata         0044c6e8-0044deb8
#   .rdata$zzz     004637a4-004637d0
#   .text          004030b0-00405610

.intel_syntax noprefix
.globl L_404000
.globl _clean
.globl _getSecurityFiles
.globl _hasHdd
.globl _info
.globl _mode_update
.globl _mu_44c6e8
.globl _mu_44c70c
.globl _mu_44c730
.globl _mu_44c74c
.globl _mu_44c76c
.globl _mu_44c7ab
.globl _mu_44c7b4
.globl _mu_44c7e1
.globl _mu_44c7ec
.globl _mu_44c810
.globl _mu_44c844
.globl _mu_44c850
.globl _mu_44c888
.globl _mu_44c8ca
.globl _mu_44c8e8
.globl _mu_44c918
.globl _mu_44c95c
.globl _mu_44c9a8
.globl _mu_44c9e8
.globl _mu_44ca2c
.globl _mu_44ca74
.globl _mu_44cac8
.globl _mu_44cb18
.globl _mu_44cb58
.globl _mu_44cb90
.globl _mu_44cbb0
.globl _mu_44cbbc
.globl _mu_44cc04
.globl _mu_44cc58
.globl _mu_44ccc8
.globl _mu_44cd14
.globl _mu_44cd6c
.globl _mu_44cdc0
.globl _mu_44cddb
.globl _mu_44cde8
.globl _mu_44cdf4
.globl _mu_44ce08
.globl _mu_44ce21
.globl _mu_44ce40
.globl _mu_44ce9c
.globl _mu_44cea3
.globl _mu_44cebc
.globl _mu_44ced0
.globl _mu_44cf18
.globl _mu_44cf6c
.globl _mu_44cfac
.globl _mu_44cfd4
.globl _mu_44cfe1
.globl _mu_44cff0
.globl _mu_44d009
.globl _mu_44d010
.globl _mu_44d054
.globl _mu_44d074
.globl _mu_44d090
.globl _mu_44d0d4
.globl _mu_44d0f8
.globl _mu_44d12c
.globl _mu_44d144
.globl _mu_44d171
.globl _mu_44d186
.globl _mu_44d198
.globl _mu_44d1d3
.globl _mu_44d1db
.globl _mu_44d400
.globl _mu_44d424
.globl _mu_44d440
.globl _mu_44d46e
.globl _mu_44d479
.globl _mu_44d484
.globl _mu_44d4b9
.globl _mu_44d4c5
.globl _mu_44d4cc
.globl _mu_44d4fc
.globl _mu_44d528
.globl _mu_44d55c
.globl _mu_44d590
.globl _mu_44d5ba
.globl _mu_44d5d4
.globl _noAvatar
.globl _noReboot
.globl _noWrite
.globl _path
.globl _updating
.globl _useConsoleAddons

.text
.p2align 4
#@C _getBadBlocks
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _update_usage
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _wantFile
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _parseAddonIdx
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
#@C _getAddons
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _getMobileFiles
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
#@C _bldrGetKv
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _bldrGetSmc
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
_getSecurityFiles:
          push EBP
          push EDI
          xor EDI,EDI
          push ESI
          push EBX
          mov ESI,OFFSET L_4c90e8
          mov EBX,OFFSET _flashFiles
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_44d1f4
          mov DWORD PTR [ESP],1
          mov EBP,DWORD PTR [ESP+48]
          call _log_printf
          mov EAX,DWORD PTR [_buildMode]
          test EAX,EAX
          jne L_403ecd
          jmp L_403f22
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_403e50:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _mu_44d1d3
          mov DWORD PTR [ESP],OFFSET _path
          call _sprintf
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _mu_44d1db
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET _path
          call _netGetFile
          test EAX,EAX
          mov DWORD PTR [ESI-40],EAX
          je L_403ea1
          mov EAX,DWORD PTR [ESI]
          test EAX,EAX
          jne L_404165
L_403ea1:
          mov DWORD PTR [ESP+4],OFFSET _mu_44cfe1
          mov DWORD PTR [ESP],1
          call _log_printf
L_403eb5:
          mov EAX,DWORD PTR [_buildMode]
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_403ec0:
          add EDI,1
          add EBX,22
          add ESI,4
          cmp EDI,EAX
          jae L_403f22
L_403ecd:
          cmp BYTE PTR [EBX],0
          je L_403ec0
          mov EDX,DWORD PTR [_clean]
          test EDX,EDX
          je L_403e50
          mov DWORD PTR [ESP+4],OFFSET _mu_44cddb
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          jne L_404130
L_403ef8:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _mu_44ce08
          add EDI,1
          mov DWORD PTR [ESP],1
          add EBX,22
          add ESI,4
          call _log_printf
          mov EAX,DWORD PTR [_buildMode]
          cmp EDI,EAX
          jb L_403ecd
L_403f22:
          mov ECX,DWORD PTR [L_47a088]
          test ECX,ECX
          jne L_403f90
          mov DWORD PTR [ESP+4],OFFSET L_44d23d
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a0ec+4
          mov DWORD PTR [ESP],OFFSET L_44d257
          call _netGetFile
          test EAX,EAX
          mov DWORD PTR [L_47a0e8+4],EAX
          je L_403f6d
          mov EAX,DWORD PTR [L_47a0ec+4]
          cmp EAX,16383
          jg L_404036
L_403f6d:
          mov DWORD PTR [ESP+4],OFFSET L_44d300
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
L_403f83:
          add ESP,28
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_403f90:
          mov DWORD PTR [ESP+4],OFFSET L_44d25e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ESI,DWORD PTR [_g47a080]
          mov EAX,DWORD PTR [ESI+96]
          mov DWORD PTR [ESP+4],1
          mov EBX,EAX
          mov EDX,EAX
          shl EBX,24
          shr EDX,24
          add EDX,EBX
          mov EBX,EAX
          shr EAX,8
          shl EBX,8
          and EAX,65280
          and EBX,16711680
          add EBX,EDX
          add EBX,EAX
          mov DWORD PTR [ESP],EBX
          call _calloc
          mov EDI,EAX
          mov EAX,DWORD PTR [ESI+108]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
L_404000:
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          add ESI,EAX
          mov DWORD PTR [ESP+4],ESI
          call _memcpy
          mov DWORD PTR [L_47a0ec+4],EBX
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [L_47a0e8+4],EDI
          cmp EAX,16383
          jle L_403f6d
L_404036:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d278
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call _verifyExtended
          test EAX,EAX
          mov EBX,EAX
          je L_4041b0
          mov DWORD PTR [ESP+4],OFFSET L_44d2ae
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e8+4]
          add EAX,16
          mov DWORD PTR [ESP],EAX
          call _setKvSalt
          test EBP,EBP
          je L_4040b8
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [ESP+4],OFFSET L_44d2c1
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP+8],EAX
          call _writeFileIn
L_4040b8:
          mov EAX,DWORD PTR [L_47a088]
          test EAX,EAX
          jne L_4041d0
          mov DWORD PTR [ESP+4],OFFSET L_44d339
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_47a0e4+4
          mov DWORD PTR [ESP],OFFSET L_44d354
          call _netGetFile
          test EAX,EAX
          mov DWORD PTR [L_47a0e0+4],EAX
          je L_404106
          mov EAX,DWORD PTR [L_47a0e4+4]
          cmp EAX,12287
          jg L_404276
L_404106:
          mov DWORD PTR [ESP+4],OFFSET L_44d3c8
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          add ESP,28
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_404130:
          mov DWORD PTR [ESP+4],OFFSET _mu_44cde8
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_403ef8
          mov DWORD PTR [ESP+4],OFFSET _mu_44cdf4
          mov DWORD PTR [ESP],EBX
          call _stricmp
          test EAX,EAX
          je L_403ef8
          jmp L_403e50
L_404165:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d21c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          call _verifyFlashFile
          test EBP,EBP
          je L_403eb5
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESI-40]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          call _writeFileIn
          mov EAX,DWORD PTR [_buildMode]
          jmp L_403ec0
L_4041b0:
          mov DWORD PTR [ESP+4],OFFSET L_44d2c8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,28
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_4041d0:
          mov DWORD PTR [ESP+4],OFFSET L_44d35c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ESI,DWORD PTR [_g47a080]
          mov EAX,DWORD PTR [ESI+120]
          mov DWORD PTR [ESP+4],1
          mov EBX,EAX
          mov EDX,EAX
          shl EBX,24
          shr EDX,24
          add EDX,EBX
          mov EBX,EAX
          shr EAX,8
          shl EBX,8
          and EAX,65280
          and EBX,16711680
          add EBX,EDX
          add EBX,EAX
          mov DWORD PTR [ESP],EBX
          call _calloc
          mov EDI,EAX
          mov EAX,DWORD PTR [ESI+124]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],EDI
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          add ESI,EAX
          mov DWORD PTR [ESP+4],ESI
          call _memcpy
          mov DWORD PTR [L_47a0e4+4],EBX
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [L_47a0e0+4],EDI
          cmp EAX,12287
          jle L_404106
L_404276:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d278
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call _unscramble
          test EAX,EAX
          je L_4042fd
          mov DWORD PTR [ESP+4],OFFSET L_44d377
          mov DWORD PTR [ESP],1
          mov EBX,1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call _setSmcKey
          test EBP,EBP
          je L_403f83
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [ESP+4],OFFSET L_44d385
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP+8],EAX
          call _writeFileIn
          jmp L_403f83
L_4042fd:
          mov DWORD PTR [ESP+4],OFFSET L_44d390
          mov DWORD PTR [ESP],0
          xor EBX,EBX
          call _log_printf
          jmp L_403f83
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _checkBadBlocks
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getBootloaders
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getConsoleFiles
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _updateGetFile
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
_mode_update:
          push EBP
          push EDI
          mov EAX,4140
          push ESI
          push EBX
          call ___chkstk_ms
          mov ECX,254
          sub ESP,EAX
          xor EAX,EAX
          mov BYTE PTR [L_47ad4c],0
          lea EDI,DWORD PTR [ESP+40]
          mov EBP,DWORD PTR [ESP+4164]
          mov DWORD PTR [ESP+32],1633967150
          mov DWORD PTR [ESP+36],6054260
          mov DWORD PTR [ESP+1056],23598
          rep stosd DWORD PTR ES:[EDI]
          lea EDI,DWORD PTR [ESP+1060]
          mov ECX,255
          rep stosd DWORD PTR ES:[EDI]
          mov DWORD PTR [ESP],OFFSET L_44d5f7
          call _log_set_name
          mov EDX,DWORD PTR [ESP+4160]
          test EDX,EDX
          jle L_405197
          xor EBX,EBX
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [ESP+24],0
          jmp L_404821
L_4047f3:
          mov DWORD PTR [ESP+4],OFFSET L_44d614
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [_promptEnter],0
L_404811:
          add EBX,1
          cmp DWORD PTR [ESP+4160],EBX
          jle L_404927
L_404821:
          lea ESI,DWORD PTR [EBX*4]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d5fe
          lea EDI,DWORD PTR [EBP+ESI*1]
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_404fd3
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d603
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_404fd3
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d606
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_404fd3
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_44d609
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_4047f3
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44d63a
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_4049a0
          add EBX,1
          cmp DWORD PTR [ESP+4160],EBX
          mov EAX,DWORD PTR [EBP+ESI*1+4]
          mov DWORD PTR [ESP+24],EAX
          je L_404fbf
          test EAX,EAX
          je L_404fbf
          cmp BYTE PTR [EAX],45
          je L_404fbf
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d68a
          add EBX,1
          mov DWORD PTR [ESP],0
          call _log_printf
          cmp DWORD PTR [ESP+4160],EBX
          jg L_404821
L_404927:
          mov EAX,DWORD PTR [ESP+28]
          test EAX,EAX
          je L_40493f
          mov DWORD PTR [ESP],EAX
          call _createDir
          test EAX,EAX
          je L_404ec2
L_40493f:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call _netConnect
          test EAX,EAX
          jne L_404bae
          mov DWORD PTR [ESP+4],OFFSET L_44de80
          mov DWORD PTR [ESP],0
          mov EBX,5
          call _log_printf
L_40496c:
          mov DWORD PTR [_pub1bl],0
          mov DWORD PTR [_pub2a4],0
          mov EAX,EBX
          mov DWORD PTR [_masterPub],0
          add ESP,4140
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_404997:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4049a0:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d6a3
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_404a90
          mov EDX,DWORD PTR [EBP+ESI*1+4]
          add EBX,1
          test EDX,EDX
          je L_4053b8
          cmp DWORD PTR [ESP+4160],EBX
          je L_4053b8
          cmp BYTE PTR [EDX],45
          je L_4053b8
          mov EAX,DWORD PTR [L_4c4f94]
          mov DWORD PTR [_useConsoleAddons],0
          cmp EAX,15
          jg L_404a70
          imul EAX,EAX,1068
          mov DWORD PTR [ESP+4],EDX
          add EAX,OFFSET L_4c0c94
          mov DWORD PTR [ESP],EAX
          call _strcpy
          imul EAX,DWORD PTR [L_4c4f94],1068
          add EAX,OFFSET L_4c0c94
L_404a21:
          mov EDX,DWORD PTR [EAX]
          add EAX,4
          lea ECX,DWORD PTR [EDX-16843009]
          not EDX
          and ECX,EDX
          and ECX,2155905152
          je L_404a21
          mov EDX,ECX
          shr EDX,16
          test ECX,32896
          cmove ECX,EDX
          lea EDX,DWORD PTR [EAX+2]
          cmove EAX,EDX
          mov EDX,ECX
          add DL,CL
          sbb EAX,3
          mov DWORD PTR [EAX],1852400174
          mov BYTE PTR [EAX+4],0
          add DWORD PTR [L_4c4f94],1
          jmp L_404811
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_404a70:
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET L_44d6f4
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_404811
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_404a90:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d73a
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_404b00
          add EBX,1
          cmp DWORD PTR [ESP+4160],EBX
          lea ESI,DWORD PTR [EBP+ESI*1+4]
          mov EAX,DWORD PTR [ESI]
          je L_4054c2
          test EAX,EAX
          je L_4054c2
          cmp BYTE PTR [EAX],45
          je L_4054c2
          cmp BYTE PTR [L_4c4f54],0
          jne L_404b87
L_404ae2:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d7e3
          mov DWORD PTR [ESP],OFFSET L_4c4f54
          call _sprintf
          jmp L_404811
          .byte 0x90
L_404b00:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d7e7
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_404ee3
          lea EDX,DWORD PTR [EBP+ESI*1+4]
          add EBX,1
          mov EAX,DWORD PTR [EDX]
          test EAX,EAX
          je L_4054db
          cmp DWORD PTR [ESP+4160],EBX
          je L_4054db
          cmp BYTE PTR [EAX],45
          je L_4054db
          mov EAX,95
          mov WORD PTR [L_47a14c],AX
          mov EAX,DWORD PTR [EDX]
          mov DWORD PTR [ESP],OFFSET L_47a14d
          mov DWORD PTR [ESP+4],EAX
          call _strcpy
          mov DWORD PTR [ESP+8],OFFSET L_47a14c
          mov DWORD PTR [ESP+4],OFFSET L_44d840
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_404811
L_404b87:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+12],OFFSET L_4c4f55
          mov DWORD PTR [ESP+4],OFFSET L_44d78c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESI]
          jmp L_404ae2
L_404bae:
          call _netGetInfo
          mov DWORD PTR [_info],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+12],OFFSET _hasHdd
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EAX
          call _parseConsoleInfo
          test EAX,EAX
          je L_404f3b
          mov EAX,DWORD PTR [_g479ea8]
          cmp EAX,1
          je L_40514f
          cmp EAX,2
          je L_4051ac
          cmp EAX,3
          je L_40503e
          lea EDX,DWORD PTR [EAX-6]
          cmp EDX,1
          jbe L_405283
          sub EAX,8
          lea EBX,DWORD PTR [ESP+32]
          cmp EAX,1
          jbe L_405325
L_404c1c:
          mov DWORD PTR [ESP+4],OFFSET L_47a14c
          mov DWORD PTR [ESP],EBX
          call _strcat
          mov EDX,EBX
L_404c2e:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_404c2e
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1768843566
          mov BYTE PTR [EDX+4],0
          mov DWORD PTR [ESP],EBX
          call _parseIni
          test EAX,EAX
          je L_40512d
          mov EAX,DWORD PTR [ESP+28]
          test EAX,EAX
          je L_4051f6
          lea EBX,DWORD PTR [ESP+2080]
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44db21
          mov DWORD PTR [ESP],EBX
          call _sprintf
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_47a94c
          call _strcpy
          mov DWORD PTR [ESP],OFFSET L_47a94c
          call _log_set_name
L_404cc3:
          mov ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          call _getConsoleFiles
          test EAX,EAX
          je L_404fd8
          mov DWORD PTR [_updating],1
          call _buildImage
          test EAX,EAX
          mov EBX,EAX
          jne L_40501c
          mov DWORD PTR [ESP],OFFSET _mu_44d4c5
          call _netUnmount
          test ESI,ESI
          je L_404d9c
          mov DWORD PTR [ESP+4],ESI
          lea ESI,DWORD PTR [ESP+3104]
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov EAX,ESI
L_404d19:
          mov ECX,DWORD PTR [EAX]
          add EAX,4
          lea EDX,DWORD PTR [ECX-16843009]
          not ECX
          and EDX,ECX
          and EDX,2155905152
          je L_404d19
          mov ECX,EDX
          shr ECX,16
          test EDX,32896
          cmove EDX,ECX
          lea ECX,DWORD PTR [EAX+2]
          cmove EAX,ECX
          mov ECX,EDX
          add CL,DL
          sbb EAX,3
          mov DWORD PTR [EAX],1684955502
          mov DWORD PTR [EAX+4],1886221668
          mov DWORD PTR [EAX+8],1852400174
          mov BYTE PTR [EAX+12],0
          mov DWORD PTR [ESP+4],OFFSET L_44db30
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],ESI
          call _netDumpNand
          test EAX,EAX
          jne L_404d9c
          mov DWORD PTR [ESP+4],OFFSET _mu_44d479
          mov DWORD PTR [ESP],0
          mov EBX,5
          call _log_printf
L_404d9c:
          mov DWORD PTR [ESP+4],OFFSET L_44db58
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EBP,DWORD PTR [_noWrite]
          test EBP,EBP
          jne L_405222
          lea EAX,DWORD PTR [ESP+3104]
          mov DWORD PTR [ESP],EAX
          call _imageGetBuffer
          mov DWORD PTR [ESP+4],OFFSET L_44db7c
          mov DWORD PTR [ESP],0
          mov ESI,EAX
          call _log_printf
          call _netTimerStart
          mov EAX,DWORD PTR [ESP+3104]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _netSendFlash
          test EAX,EAX
          mov EAX,5
          cmove EBX,EAX
L_404e05:
          mov DWORD PTR [ESP+4],OFFSET L_44dbcc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDI,DWORD PTR [_hasHdd]
          test EDI,EDI
          je L_40530c
          mov ESI,DWORD PTR [_noAvatar]
          test ESI,ESI
          jne L_404e3f
          mov ECX,DWORD PTR [_noWrite]
          test ECX,ECX
          je L_40539e
L_404e3f:
          mov DWORD PTR [ESP+4],OFFSET L_44dbfc
          mov DWORD PTR [ESP],1
          call _log_printf
L_404e53:
          mov EDX,DWORD PTR [_noReboot]
          test EDX,EDX
          jne L_404e71
          test EBX,EBX
          jne L_4052cb
          mov DWORD PTR [ESP],2
          call _netReboot
L_404e71:
          mov EAX,DWORD PTR [ESP+28]
          test EAX,EAX
          je L_404ea1
          mov DWORD PTR [ESP],OFFSET L_47a94c
          call _writeImage
          test EAX,EAX
          jne L_4053d5
L_404e8d:
          mov DWORD PTR [ESP+4],OFFSET _separator
          mov DWORD PTR [ESP],0
          call _log_printf
L_404ea1:
          mov DWORD PTR [ESP+8],OFFSET L_47a94c
          mov DWORD PTR [ESP+4],OFFSET L_44dd67
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40496c
L_404ec2:
          mov DWORD PTR [ESP+4],OFFSET L_44db0e
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+28],0
          jmp L_40493f
L_404ee3:
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_44d882
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_404f59
          mov DWORD PTR [ESP+4],OFFSET L_44d88c
          mov DWORD PTR [ESP],1
          add EBX,1
          mov DWORD PTR [_noWrite],1
          mov DWORD PTR [_noReboot],1
          mov DWORD PTR [_noAvatar],1
          call _log_printf
          jmp L_404811
L_404f3b:
          mov DWORD PTR [ESP+4],OFFSET L_44de38
          mov DWORD PTR [ESP],0
          mov EBX,5
          call _log_printf
          jmp L_40496c
L_404f59:
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_44d8c8
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_404ff6
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_44d910
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_40523b
          mov DWORD PTR [ESP+4],OFFSET L_44d918
          mov DWORD PTR [ESP],1
          add EBX,1
          mov DWORD PTR [_noReboot],1
          call _log_printf
          jmp L_404811
L_404fbf:
          mov DWORD PTR [ESP+4],OFFSET L_44d640
          mov DWORD PTR [ESP],0
          call _log_printf
L_404fd3:
          call _update_usage
L_404fd8:
          mov DWORD PTR [ESP+4],OFFSET L_44ddc0
          mov DWORD PTR [ESP],0
          mov EBX,5
          call _log_printf
          jmp L_40496c
L_404ff6:
          mov DWORD PTR [ESP+4],OFFSET L_44d8d0
          mov DWORD PTR [ESP],1
          add EBX,1
          mov DWORD PTR [_noAvatar],1
          call _log_printf
          jmp L_404811
L_40501c:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44dd80
          mov EBX,3
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40496c
L_40503e:
          mov EAX,DWORD PTR [L_479eb4]
          lea EBX,DWORD PTR [ESP+32]
          mov EDX,EBX
          test EAX,EAX
          jne L_4050e2
          mov EAX,DWORD PTR [L_479eb0]
          test EAX,EAX
          je L_4050a0
L_40505a:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_40505a
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1768712031
          mov DWORD PTR [EDX+4],845702004
          mov BYTE PTR [EDX+8],0
          jmp L_404c1c
L_4050a0:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4050a0
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1768712031
          mov DWORD PTR [EDX+4],6841204
          jmp L_404c1c
L_4050e2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4050e2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,109
          sbb EDX,3
          mov DWORD PTR [EDX],1768712031
          mov DWORD PTR [EDX+4],845702004
          mov WORD PTR [EDX+8],AX
          jmp L_404c1c
L_40512d:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_44de04
          mov EBX,1
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_40496c
L_40514f:
          lea EBX,DWORD PTR [ESP+32]
          mov EDX,EBX
L_405155:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_405155
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1952805471
          mov DWORD PTR [EDX+4],7104865
          jmp L_404c1c
L_405197:
          mov DWORD PTR [ESP+24],0
          mov DWORD PTR [ESP+28],0
          jmp L_40493f
L_4051ac:
          lea EBX,DWORD PTR [ESP+32]
          mov EDX,EBX
L_4051b2:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_4051b2
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,103
          sbb EDX,3
          mov DWORD PTR [EDX],1635019359
          mov WORD PTR [EDX+4],AX
          jmp L_404c1c
L_4051f6:
          lea EBX,DWORD PTR [ESP+2080]
          mov DWORD PTR [ESP+8],OFFSET L_47a94c
          mov DWORD PTR [ESP+4],OFFSET L_44db26
          mov DWORD PTR [ESP],EBX
          call _sprintf
          mov DWORD PTR [ESP],EBX
          call _log_set_name
          jmp L_404cc3
L_405222:
          mov DWORD PTR [ESP+4],OFFSET L_44dba0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_404e05
L_40523b:
          mov DWORD PTR [ESP+8],6
          mov DWORD PTR [ESP+4],OFFSET L_44d950
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_40536d
          mov DWORD PTR [ESP+4],OFFSET L_44d958
          mov DWORD PTR [ESP],1
          add EBX,1
          mov DWORD PTR [_clean],1
          call _log_printf
          jmp L_404811
L_405283:
          lea EBX,DWORD PTR [ESP+32]
          mov EDX,EBX
L_405289:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_405289
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1986356319
          mov DWORD PTR [EDX+4],7629163
          jmp L_404c1c
L_4052cb:
          mov DWORD PTR [ESP+4],OFFSET L_44dc54
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44dca8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET L_44dcf8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_404e71
L_40530c:
          mov DWORD PTR [ESP+4],OFFSET L_44dc2c
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_404e53
L_405325:
          mov EDX,EBX
L_405327:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_405327
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1936028767
          mov DWORD PTR [EDX+4],1953065844
          mov BYTE PTR [EDX+8],0
          jmp L_404c1c
L_40536d:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d9c7
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_4053fa
          mov EAX,DWORD PTR [EDI]
          movzx EAX,BYTE PTR [EAX+2]
          mov DWORD PTR [ESP],EAX
          call _log_verbose_flag
          jmp L_404811
L_40539e:
          mov EAX,DWORD PTR [L_479eac]
          mov DWORD PTR [ESP],OFFSET L_47b14c
          mov DWORD PTR [ESP+4],EAX
          call _sendAvatarData
          jmp L_404e53
L_4053b8:
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],OFFSET L_44d6a8
          mov DWORD PTR [ESP],0
          call _log_printf
          call _update_usage
L_4053d5:
          mov DWORD PTR [ESP+12],OFFSET L_47a94c
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44dd40
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_404e8d
L_4053fa:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44d9ca
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_405515
          mov EAX,DWORD PTR [EBP+ESI*1+4]
          add EBX,1
          test EAX,EAX
          je L_4054f8
          cmp DWORD PTR [ESP+4160],EBX
          je L_4054f8
          cmp BYTE PTR [EAX],45
          je L_4054f8
          mov DWORD PTR [ESP+4],EAX
          lea EAX,DWORD PTR [ESP+1056]
          mov DWORD PTR [ESP],EAX
          call _strcpy
          lea EDX,DWORD PTR [ESP+1056]
L_40545b:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_40545b
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          mov EAX,92
          sbb EDX,3
          mov WORD PTR [EDX],AX
          lea EAX,DWORD PTR [ESP+1056]
          mov DWORD PTR [ESP+4],OFFSET L_44da21
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          lea EAX,DWORD PTR [ESP+1056]
          mov DWORD PTR [ESP+28],EAX
          jmp L_404811
L_4054c2:
          mov DWORD PTR [ESP+4],OFFSET L_44d740
          mov DWORD PTR [ESP],0
          call _log_printf
          call _update_usage
L_4054db:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d7ec
          mov DWORD PTR [ESP],0
          call _log_printf
          call _update_usage
L_4054f8:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44d9d0
          mov DWORD PTR [ESP],0
          call _log_printf
          call _update_usage
L_405515:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44da3d
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_4055cb
          lea ESI,DWORD PTR [EBP+ESI*1+4]
          add EBX,1
          mov EAX,DWORD PTR [ESI]
          test EAX,EAX
          je L_4055ea
          cmp DWORD PTR [ESP+4160],EBX
          je L_4055ea
          cmp BYTE PTR [EAX],45
          je L_4055ea
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_44da91
          mov DWORD PTR [ESP],EAX
          call _sprintf
          lea EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],OFFSET L_44da98
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+4],OFFSET L_44da91
          mov DWORD PTR [ESP],OFFSET L_47b14c
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+4],OFFSET L_44dac6
          mov DWORD PTR [ESP],OFFSET L_47a54c
          mov DWORD PTR [ESP+8],EAX
          call _sprintf
          jmp L_404811
L_4055cb:
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP+4],OFFSET L_44dad0
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          call _update_usage
L_4055ea:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44da40
          mov DWORD PTR [ESP],0
          call _log_printf
          call _update_usage
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop

.data
.p2align 3
_useConsoleAddons:
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0

.section .rdata,"dr"
.p2align 3
_mu_44c6e8:
          .string "\n------ getting bad blocks ------\n"
          .zero 1
_mu_44c70c:
          .string "processing %d bad blocks on device\n"
_mu_44c730:
          .string "marking bad block at 0x%x\n"
          .zero 1
_mu_44c74c:
          .string "no bad blocks found on device\n"
          .zero 1
_mu_44c76c:
          .string "\n\n***** ERROR: unable to retrieve bad block list from device!\n"
_mu_44c7ab:
          .string "xeBuild"
          .zero 1
_mu_44c7b4:
          .string "Usage   :\n   %s update <switch> [<option>]\n\n"
_mu_44c7e1:
          .string "Examples:\n"
_mu_44c7ec:
          .string "   %s update -f 16197 -a nofcrt\n"
          .zero 3
_mu_44c810:
          .string "   %s update -f 16203 -d myflash -ip 192.168.2.100\n"
_mu_44c844:
          .string "\nSwitches:\n"
_mu_44c850:
          .string "   -f <dir> : use different data dir and file lists\n"
          .zero 3
_mu_44c888:
          .string "   -d <dir> : dumps NAND and other data to <dir> before flashing\n"
_mu_44c8ca:
          .string "   -a <name>: append patches\n"
_mu_44c8e8:
          .string "   -ip <add>: force attempt to connect to addr\n"
_mu_44c918:
          .string "   -i <ext> : adds _<ext> into firmware ini and patches file names\n"
_mu_44c95c:
          .string "   -r <ext> : adds _<ext> into ini bl section name and patches file names\n"
          .zero 1
_mu_44c9a8:
          .string "   -nowrite : will not write anything to console flash or HDD\n"
          .zero 1
_mu_44c9e8:
          .string "              without -d results of update are not kept anywhere\n"
          .zero 2
_mu_44ca2c:
          .string "   -noava   : will not send avatar data if available and HDD present\n"
          .zero 2
_mu_44ca74:
          .string "   -clean   : secdata, extended and statistics will not be retrieved from console\n"
          .zero 1
_mu_44cac8:
          .string "   -noreeb  : do not automatically reboot console after writes are completed\n"
          .zero 2
_mu_44cb18:
          .string "   -noenter : suppresses prompt for enter key when finished\n"
          .zero 3
_mu_44cb58:
          .string "   -v       : shows more info during update process\n"
          .zero 3
_mu_44cb90:
          .string "   -?       : shows this help\n\n"
_mu_44cbb0:
          .string "legend:\n"
          .zero 3
_mu_44cbbc:
          .string "<name>      = name.bin contents will be appended to hv/kernel patches\n\n"
_mu_44cc04:
          .string "<dir>       = path, absolute or relative, to a directory - do not terminate with \\\n"
_mu_44cc58:
          .string "<ext>       = using this option would cause the builder to look for _glitch_<ext>.ini instead of _glitch.ini\n"
          .zero 2
_mu_44ccc8:
          .string "              and patches_jasper_<ext>.bin instead of patches_jasper.bin\n"
          .zero 2
_mu_44cd14:
          .string "<add>       = without this option network will be scanned for server broadcast beacon\n"
          .zero 1
_mu_44cd6c:
          .string "              If provided the correct format is an IPv4 address like 192.168.0.100\n"
_mu_44cdc0:
          .string "\npress <enter> to quit...\n"
_mu_44cddb:
          .string "extended.bin"
_mu_44cde8:
          .string "secdata.bin"
_mu_44cdf4:
          .string "Statistics.settings"
_mu_44ce08:
          .string "skipping %s, -clean flag"
_mu_44ce21:
          .string "addon patch from console: %s\n"
          .zero 1
_mu_44ce40:
          .string "***** WARNING: exceeded total number of optional patches while processing %s from console!\n"
_mu_44ce9c:
          .string "addons"
_mu_44cea3:
          .string "OK, received 0x%x bytes\n"
_mu_44cebc:
          .string ".\\%d\\bin\\addon.idx"
          .zero 1
_mu_44ced0:
          .string "\n\n***** WARNING: unable to open %s to parse addons.bin from console!\n"
          .zero 2
_mu_44cf18:
          .string "\n\n***** WARNING: addons.bin from console is not a multiple of 4 bytes! Skipping!\n"
          .zero 2
_mu_44cf6c:
          .string "\n\n***** WARNING: Unable to retrieve addons.bin from console!\n"
          .zero 2
_mu_44cfac:
          .string "\n------ getting mobile settings ------\n"
_mu_44cfd4:
          .string "Mobile%c.dat"
_mu_44cfe1:
          .string "not available\n"
_mu_44cff0:
          .string "retrieving USVR\\blmod..."
_mu_44d009:
          .string "blmod"
          .zero 1
_mu_44d010:
          .string "\n\n***** WARNING: Unable to retrieve blmod.bin data from console!\n"
          .zero 2
_mu_44d054:
          .string "console has no available blmod\n"
_mu_44d074:
          .string "retrieving USVR\\addons..."
          .zero 2
_mu_44d090:
          .string "skipping USVR\\addons, addons have been specified on command line\n"
          .zero 2
_mu_44d0d4:
          .string "console has no available addons\n"
          .zero 3
_mu_44d0f8:
          .string "retrieving USVR\\Static.settings (smc_config.bin)..."
_mu_44d12c:
          .string "usv:\\Static.settings"
          .zero 3
_mu_44d144:
          .string "OK, received 0x%x bytes\n        verifying..."
_mu_44d171:
          .string "smc_config is good!\n"
_mu_44d186:
          .string "smc_config.bin"
          .zero 3
_mu_44d198:
          .string "\n***** ERROR: could not retrieve smc_config from console!\n"
_mu_44d1d3:
          .string "usv:\\%s"
_mu_44d1db:
          .string "retrieving USVR\\%s..."
          .zero 3
L_44d1f4:
          .string "\n------ getting security files ------\n"
          .zero 1
L_44d21c:
          .string "OK, received 0x%x bytes\n        "
L_44d23d:
          .string "retrieving USVR\\kv_enc..."
L_44d257:
          .string "kv_enc"
L_44d25e:
          .string "extracting BLDR\\kv_enc..."
L_44d278:
          .string "OK, received 0x%x bytes\n        decrypt and verify..."
L_44d2ae:
          .string "keyvault is good!\n"
L_44d2c1:
          .string "kv.bin"
L_44d2c8:
          .string "\n***** ERROR: could not decrypt keyvault from console!\n"
L_44d300:
          .string "\n***** ERROR: could not retrieve keyvault from console!\n"
L_44d339:
          .string "retrieving USVR\\smc_enc..."
L_44d354:
          .string "smc_enc"
L_44d35c:
          .string "extracting BLDR\\smc_enc..."
L_44d377:
          .string "smc is good!\n"
L_44d385:
          .string "smc.bin"
          .zero 3
L_44d390:
          .string "\n***** ERROR: could not decrypt smc.bin from console!\n"
          .zero 1
L_44d3c8:
          .string "\n***** ERROR: could not retrieve smc.bin from console!\n"
_mu_44d400:
          .string "\n------ getting bootloaders ------\n"
_mu_44d424:
          .string "reading bootloader data..."
          .zero 1
_mu_44d440:
          .string "success! Bootloader size with xell is 0x%08x\n"
_mu_44d46e:
          .string "fbldrs.bin"
_mu_44d479:
          .string "failed!\n"
          .zero 2
_mu_44d484:
          .string "Skipping getting bootloaders on non-glitch machine!\n"
_mu_44d4b9:
          .string "\\SystemRoot"
_mu_44d4c5:
          .string "usv"
          .zero 3
_mu_44d4cc:
          .string "\n***** ERROR: getting raw boot loaders failed!\n"
_mu_44d4fc:
          .string "\n***** ERROR: getting mobile files failed!\n"
_mu_44d528:
          .string "\n***** ERROR: retrieving security files failed!\n"
          .zero 3
_mu_44d55c:
          .string "\n***** ERROR: mounting remote SystemRoot failed!\n"
          .zero 2
_mu_44d590:
          .string "\n***** ERROR: getting bad blocks failed!\n"
_mu_44d5ba:
          .string "failed! received 0 bytes\n"
_mu_44d5d4:
          .string "failed! file not found on console\n"
L_44d5f7:
          .string "update"
L_44d5fe:
          .string "help"
L_44d603:
          .string "-?"
L_44d606:
          .string "/?"
L_44d609:
          .string "-noenter"
          .zero 2
L_44d614:
          .string "<enter> key on completion suppressed\n"
L_44d63a:
          .string "-ip"
          .zero 2
L_44d640:
          .string "\n\n***** ERROR: option flag -ip on command line but no argument provided!\n"
L_44d68a:
          .string "setting forced IP to %s\n"
L_44d6a3:
          .string "-a"
          .zero 2
L_44d6a8:
          .string "\n\n***** ERROR: option flag -a on command line but no argument provided!\n"
          .zero 3
L_44d6f4:
          .string "***** WARNING: exceeded total number of optional patches with -a %s!\n"
L_44d73a:
          .string "-r"
          .zero 3
L_44d740:
          .string "\n\n***** ERROR: option flag -r on command line but no argument provided!\n"
          .zero 3
L_44d78c:
          .string "***** WARNING: option flag -r %s on command line replacing previous setting of -r %s!\n"
L_44d7e3:
          .string "_%s"
L_44d7e7:
          .string "-i"
          .zero 2
L_44d7ec:
          .string "\n\n***** ERROR: data directory flag -i on command line but no argument provided!\n"
          .zero 3
L_44d840:
          .string "suffix '%s' added from command line to ini and patches filenames\n"
L_44d882:
          .string "-nowrite"
          .zero 1
L_44d88c:
          .string "-nowrite: flash image and avatars will not be sent to xbox\n"
L_44d8c8:
          .string "-noava"
          .zero 1
L_44d8d0:
          .string "-noava: avatar data, if available, will not be sent to console\n"
L_44d910:
          .string "-noreeb"
L_44d918:
          .string "-noreeb: console will not reboot after writes are done\n"
L_44d950:
          .string "-clean"
          .zero 1
L_44d958:
          .string "-clean: secdata, extended and statistics will not be retrieved from console, builder will make clean versions\n"
L_44d9c7:
          .string "-v"
L_44d9ca:
          .string "-d"
          .zero 3
L_44d9d0:
          .string "\n\n***** ERROR: dump directory flag -d on command line but no argument provided!\n"
L_44da21:
          .string "dump directory set to '%s'\n"
L_44da3d:
          .string "-f"
L_44da40:
          .string "\n\n***** ERROR: data directory flag -f on command line but no argument provided!\n"
L_44da91:
          .string "%s\\"
          .zero 3
L_44da98:
          .string "data directory set from command line to '%s'\n"
L_44dac6:
          .string "%s\\bin\\"
          .zero 2
L_44dad0:
          .string "\n\n***** ERROR: unknown option '%s' provided on command line!\n"
L_44db0e:
          .string "Dumping disabled!\n"
L_44db21:
          .string "%s%s"
L_44db26:
          .string "%s_update"
L_44db30:
          .string "\n------ dumping console flash ------\n"
          .zero 2
L_44db58:
          .string "\n------ flashing console ------\n"
          .zero 3
L_44db7c:
          .string "sending flash data to console...\n"
          .zero 2
L_44dba0:
          .string "flashing console skipped, -nowrite used\n"
          .zero 3
L_44dbcc:
          .string "\n------ loading and sending avatar data ------\n"
L_44dbfc:
          .string "avatar data skipped, -noava or -nowrite used\n"
          .zero 2
L_44dc2c:
          .string "avatar data skipped, no HDD detected\n"
          .zero 2
L_44dc54:
          .string "\n***** WARNING: due to previous possible errors, console reboot is not being done\n"
          .zero 1
L_44dca8:
          .string "               it is not recommended to use update mode on this console again\n"
          .zero 1
L_44dcf8:
          .string "               until you have determined it's got a good image on it\n\n"
          .zero 1
L_44dd40:
          .string "\n\n***** ERROR: %i writing to file %s\n\n"
L_44dd67:
          .string "%s image built, info:\n"
          .zero 2
L_44dd80:
          .string "\n\n***** FATAL UPDATE ERROR: %i unable to complete NAND image\n\n"
          .zero 1
L_44ddc0:
          .string "\n\n***** FATAL UPDATE ERROR: unable to get console unique files\n\n"
          .zero 3
L_44de04:
          .string "\n\n***** FATAL UPDATE ERROR: unable to parse %s\n\n"
          .zero 3
L_44de38:
          .string "\n\n***** FATAL UPDATE ERROR: unable to parse info reply from console!\n\n"
          .zero 1
L_44de80:
          .string "\n\n***** FATAL UPDATE ERROR: unable to find console!\n\n"
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _getBadBlocks - .
          .byte 0x1b
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x56
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _update_usage - .
          .byte 0x88
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _wantFile - .
          .byte 0x89
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x53
          .byte 0xe
          .byte 0x20
          .byte 0x79
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x78
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _parseAddonIdx - .
          .byte 0x2
          .byte 0x2
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
          .byte 0x4b
          .byte 0xe
          .byte 0xc0
          .byte 0x8
          .byte 0x2
          .byte 0xac
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
          .byte 0x3
          .byte 0x36
          .byte 0x1
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
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _getAddons - .
          .byte 0x1d
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x8
          .byte 0x2
          .byte 0x54
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
          .byte 0x41
          .byte 0xb
          .byte 0x2
          .byte 0x99
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
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getMobileFiles - .
          .byte 0xc3
          .byte 0x4
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
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4a
          .byte 0xe
          .byte 0x80
          .byte 0x1
          .byte 0x3
          .byte 0x1c
          .byte 0x3
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _bldrGetKv - .
          .byte 0x8b
          .byte 0x0
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
          .byte 0x2
          .byte 0x7f
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _bldrGetSmc - .
          .byte 0x8b
          .byte 0x0
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
          .byte 0x2
          .byte 0x7f
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe0
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getSecurityFiles - .
          .byte 0x8
          .byte 0x5
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4d
          .byte 0xe
          .byte 0x30
          .byte 0x3
          .byte 0x63
          .byte 0x1
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
          .byte 0x44
          .byte 0xb
          .byte 0x3
          .byte 0x8f
          .byte 0x1
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x97
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _checkBadBlocks - .
          .byte 0x15
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _getBootloaders - .
          .byte 0xe9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x79
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x4b
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x2
          .byte 0x58
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _getConsoleFiles - .
          .byte 0xc5
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0xc3
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x4a
          .byte 0xb
          .byte 0x59
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x47
          .byte 0xb
          .byte 0x2
          .byte 0x7f
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _updateGetFile - .
          .byte 0x6b
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
          .byte 0x2
          .byte 0x2
          .byte 0xd9
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
          .byte 0x49
          .byte 0xb
          .byte 0x67
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
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _mode_update - .
          .byte 0x97
          .byte 0xe
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
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x86
          .byte 0x4
          .byte 0x41
          .byte 0xe
          .byte 0x14
          .byte 0x83
          .byte 0x5
          .byte 0x4c
          .byte 0xe
          .byte 0xc0
          .byte 0x20
          .byte 0x3
          .byte 0xd
          .byte 0x2
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
          .byte 0x4a
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0

.bss
.p2align 5
_path:
          .zero 4
L_46f044:
          .zero 4
L_46f048:
          .zero 4
L_46f04c:
          .zero 4
L_46f050:
          .zero 244
_noReboot:
          .zero 4
_noAvatar:
          .zero 4
_noWrite:
          .zero 4
_clean:
          .zero 4
_hasHdd:
          .zero 4
_updating:
          .zero 4
_info:
          .zero 4
