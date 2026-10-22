# app/mode_client.s -- "Usage: %s client", network read/write of NAND
#
# mixed: `#@C name` lines are functions from mode_client.c (re/splice.py)
#
# original placement:
#   .bss           0046f160-0046f180
#   .eh_frame      00465b68-00466040
#   .rdata         0044e10c-0044fb60
#   .rdata$zzz     004637fc-00463828
#   .text          00406330-00408ec0

.intel_syntax noprefix
.globl _cinfo
.globl _clientKeys
.globl _client_usage
.globl _mc_44e10c
.globl _mc_44e158
.globl _mc_44e1a8
.globl _mc_44e1f4
.globl _mc_44e234
.globl _mc_44e273
.globl _mc_44e27c
.globl _mc_44e2a9
.globl _mc_44e2b4
.globl _mc_44e2d4
.globl _mc_44e305
.globl _mc_44e314
.globl _mc_44e35c
.globl _mc_44e3c0
.globl _mc_44e3f8
.globl _mc_44e434
.globl _mc_44e4a4
.globl _mc_44e4fc
.globl _mc_44e560
.globl _mc_44e590
.globl _mc_44e5d4
.globl _mc_44e630
.globl _mc_44e684
.globl _mc_44e6d8
.globl _mc_44e720
.globl _mc_44e748
.globl _mc_44e798
.globl _mc_44e7dc
.globl _mc_44e814
.globl _mc_44e850
.globl _mc_44e876
.globl _mc_44e880
.globl _mc_44e8d4
.globl _mc_44e928
.globl _mc_44e95c
.globl _mc_44e9b0
.globl _mc_44e9d8
.globl _mc_44ea04
.globl _mc_44ea50
.globl _mc_44ea58
.globl _mc_44eaa8
.globl _mc_44eaf8
.globl _mc_44eb40
.globl _mc_44eb8b
.globl _mc_44ebc0
.globl _mc_44ebe8
.globl _mc_44ec11
.globl _mc_44ec16
.globl _mc_44ec18
.globl _mc_44ec35
.globl _mc_44ec3f
.globl _mc_44ec48
.globl _mc_44ec5b
.globl _mc_44ec6e
.globl _mc_44ec88
.globl _mc_44eca4
.globl _mc_44ecec
.globl _mc_44ed30
.globl _mc_44ed5c
.globl _mc_44ed74
.globl _mc_44ed8d
.globl _mc_44eda8
.globl _mc_44ee04
.globl _mc_44ee23
.globl _mc_44ee26
.globl _mc_44ee31
.globl _mc_44ee39
.globl _mc_44ee45
.globl _mc_44ee55
.globl _mc_44ee62
.globl _mc_44ee73
.globl _mc_44ee80
.globl _mc_44ee94
.globl _mc_44eee4
.globl _mc_44ef10
.globl _mc_44ef50
.globl _mc_44ef7c
.globl _mc_44efc8
.globl _mc_44efe8
.globl _mc_44f00b
.globl _mc_44f014
.globl _mc_44f037
.globl _mc_44f04c
.globl _mc_44f074
.globl _mc_44f0b8
.globl _mc_44f0ec
.globl _mc_44f118
.globl _mc_44f140
.globl _mc_44f164
.globl _mc_44f184
.globl _mc_44f19a
.globl _mc_44f1b2
.globl _mc_44f1cb
.globl _mc_44f1e4
.globl _mc_44f208
.globl _mc_44f240
.globl _mc_44f288
.globl _mc_44f2b0
.globl _mc_44f2b8
.globl _mc_44f2f0
.globl _mc_44f330
.globl _mc_44f384
.globl _mc_44f3f0
.globl _mc_44f434
.globl _mc_44f464
.globl _mc_44f494
.globl _mc_44f4e8
.globl _mc_44f510
.globl _mc_44f52c
.globl _mc_44f570
.globl _mc_44f594
.globl _mc_44f5d0
.globl _mc_44f5f4
.globl _mc_44f628
.globl _mc_44f684
.globl _mc_44f6d5
.globl _mc_44f6eb
.globl _mc_44f6f8
.globl _mc_44f724
.globl _mode_client

.text
.p2align 4
_client_usage:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          cmp EAX,5
          ja L_406360
          jmp DWORD PTR [EAX*4+L_44eba8]
L_406343:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET _mc_44e1a8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          nop
L_406360:
          mov DWORD PTR [ESP+4],OFFSET _separator
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET _mc_44e273
          mov DWORD PTR [ESP+4],OFFSET _mc_44e27c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e2a9
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET _mc_44e273
          mov DWORD PTR [ESP+4],OFFSET _mc_44e2b4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+8],OFFSET _mc_44e273
          mov DWORD PTR [ESP+4],OFFSET _mc_44e2d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e305
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e314
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e35c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e3c0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e3f8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e434
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e4a4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e4fc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e560
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e590
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e5d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e630
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e684
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e6d8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e720
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e748
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e798
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e7dc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e814
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e850
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e876
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e880
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e8d4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e928
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e95c
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e9b0
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44e9d8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44ea04
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44ea50
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44ea58
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44eaa8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44eaf8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _mc_44eb40
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _separator
          mov DWORD PTR [ESP],0
          call _log_printf
          call _log_finish
          mov EAX,DWORD PTR [_promptEnter]
          test EAX,EAX
          jne L_40669e
L_406692:
          mov DWORD PTR [ESP],1
          call _exit
L_40669e:
          mov DWORD PTR [ESP+4],OFFSET _mc_44eb8b
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP],EAX
          call _fgetc
          jmp L_406692
L_4066c1:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET _mc_44e1f4
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_406360
L_4066e2:
          mov DWORD PTR [ESP+4],OFFSET _mc_44e234
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_406360
L_4066fb:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET _mc_44e10c
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_406360
L_40671c:
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],OFFSET _mc_44e158
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_406360
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _clientInfo
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _clientWrite
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _clientManifest
L_406b57:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _dumpKey
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_clientKeys:
          push EBX
          sub ESP,56
          mov EAX,DWORD PTR [_cinfo]
          cmp BYTE PTR [EAX],1
          jbe L_406d92
          mov DWORD PTR [ESP+12],OFFSET _mc_44ee26
          mov DWORD PTR [ESP+8],OFFSET _mc_44ee31
          lea EBX,DWORD PTR [EAX+256]
          mov DWORD PTR [ESP+4],OFFSET _mc_44ed8d
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+44],16
          call _log_printf
          mov DWORD PTR [ESP],OFFSET _mc_44ee26
          call _FileExists
          test EAX,EAX
          jne L_406db0
L_406cb8:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _sumBytes
          cmp EAX,2435
          je L_406dd0
L_406cd3:
          mov DWORD PTR [ESP+12],OFFSET _mc_44ee26
          mov DWORD PTR [ESP+8],OFFSET _mc_44ee31
          mov DWORD PTR [ESP+4],OFFSET _mc_44eda8
          mov DWORD PTR [ESP],0
          call _log_printf
L_406cf7:
          mov EAX,DWORD PTR [_cinfo]
          mov DWORD PTR [ESP+16],31175
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee39
          mov DWORD PTR [ESP],OFFSET _mc_44ee45
          add EAX,272
          mov DWORD PTR [ESP+8],EAX
          call _dumpKey
          mov EAX,DWORD PTR [_cinfo]
          mov DWORD PTR [ESP+16],32976
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee55
          mov DWORD PTR [ESP],OFFSET _mc_44ee62
          add EAX,544
          mov DWORD PTR [ESP+8],EAX
          call _dumpKey
          mov EAX,DWORD PTR [_cinfo]
          mov DWORD PTR [ESP+16],33852
          mov DWORD PTR [ESP+12],272
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee73
          mov DWORD PTR [ESP],OFFSET _mc_44ee80
          add EAX,816
          mov DWORD PTR [ESP+8],EAX
          call _dumpKey
          add ESP,56
          pop EBX
          ret 
L_406d92:
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee94
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,56
          pop EBX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_406db0:
          lea EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET _mc_44ee26
          mov DWORD PTR [ESP+4],EAX
          call _FileToBuffer
          jmp L_406cb8
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_406dd0:
          mov DWORD PTR [ESP+12],OFFSET _mc_44ee26
          mov DWORD PTR [ESP+8],OFFSET _mc_44ee31
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee04
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          cmp EAX,16
          je L_406e30
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee26
          mov DWORD PTR [ESP],OFFSET _mc_44ee23
          call _writeFileIn
L_406e19:
          test EAX,EAX
          jne L_406cf7
          jmp L_406cd3
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_406e30:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _mc_44ee26
          mov DWORD PTR [ESP],OFFSET _mc_44ee23
          call _writeKeyFile
          jmp L_406e19
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _checkPatches
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _updatePatches
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _clientPatches
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _clientReadBlocks
L_407841:
          jmp _clientWriteBlocks
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
#@C _clientWriteBlocks
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _patchNand
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _clientBinPatch
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d
          .byte 0xbf
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _clientEraseBlock
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getArgs
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_mode_client:
          push EBP
          push EDI
          mov EAX,121
          push ESI
          push EBX
          sub ESP,92
          mov ESI,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP],OFFSET L_44f757
          mov EBX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP+74],1835890020
          mov WORD PTR [ESP+78],AX
          mov DWORD PTR [ESP+60],0
          mov DWORD PTR [ESP+64],0
          mov DWORD PTR [ESP+68],0
          call _log_set_name
          test ESI,ESI
          mov DWORD PTR [ESP+68],0
          jle L_408a30
          xor EAX,EAX
          mov DWORD PTR [ESP+40],0
          xor EBP,EBP
          mov DWORD PTR [ESP+44],0
          xor EDI,EDI
          jmp L_408301
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
L_4082d0:
          mov DWORD PTR [ESP+4],OFFSET L_44f774
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [_promptEnter],0
          add EAX,1
L_4082f5:
          cmp ESI,EAX
          mov DWORD PTR [ESP+68],EAX
          jle L_4083f5
L_408301:
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f75e
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_408885
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f763
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_408885
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f766
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_408885
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],8
          mov DWORD PTR [ESP+4],OFFSET L_44f769
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          je L_4082d0
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],7
          mov DWORD PTR [ESP+4],OFFSET L_44f79a
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408440
          cmp EDI,1
          je L_4085a0
L_4083c9:
          mov DWORD PTR [ESP+4],OFFSET L_44f7e4
          mov DWORD PTR [ESP],0
          mov EDI,2
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          cmp ESI,EAX
          mov DWORD PTR [ESP+68],EAX
          jg L_408301
L_4083f5:
          mov EAX,DWORD PTR [ESP+40]
          test EAX,EAX
          je L_408405
          test EBP,EBP
          jne L_408758
L_408405:
          test EDI,EDI
          je L_408a30
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _netConnect
          test EAX,EAX
          jne L_408812
L_408421:
          mov DWORD PTR [ESP+4],OFFSET L_44fae8
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,92
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_408440:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f802
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408500
          mov ECX,DWORD PTR [ESP+68]
          lea EAX,DWORD PTR [ECX+1]
          mov EBP,DWORD PTR [EBX+EAX*4]
          lea EDX,DWORD PTR [EAX*4]
          test EBP,EBP
          je L_408b9b
          cmp ESI,EAX
          je L_408b9b
          cmp BYTE PTR [EBP],45
          je L_408b9b
          lea EBP,DWORD PTR [ECX+2]
          mov EDX,DWORD PTR [EBX+EDX*1+4]
          cmp ESI,EBP
          je L_408b88
          test EDX,EDX
          je L_408b88
          cmp BYTE PTR [EDX],45
          je L_408b88
          cmp DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+60],EDX
          jne L_408c70
          mov DWORD PTR [ESP+68],EBP
          mov EBP,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+4],OFFSET L_44f808
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EBP
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],11
          add EAX,1
          jmp L_4082f5
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_408500:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f834
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_4085c0
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+16],1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],EAX
          call _getArgs
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],OFFSET L_44f838
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],8
          add EAX,1
          jmp L_4082f5
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4085a0:
          mov DWORD PTR [ESP+4],OFFSET L_44f7a4
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4083c9
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4085c0:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f864
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408680
          mov ECX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [ECX+1]
          cmp ESI,EDX
          lea EAX,DWORD PTR [EDX*4]
          mov EBP,DWORD PTR [EBX+EDX*4]
          je L_408b9b
          test EBP,EBP
          je L_408b9b
          cmp BYTE PTR [EBP],45
          je L_408b9b
          mov EAX,DWORD PTR [EBX+EAX*1+4]
          lea EBP,DWORD PTR [ECX+2]
          test EAX,EAX
          je L_408b88
          cmp ESI,EBP
          je L_408b88
          cmp BYTE PTR [EAX],45
          je L_408b88
          cmp DWORD PTR [ESP+40],0
          mov DWORD PTR [ESP+60],EAX
          jne L_408c70
          mov DWORD PTR [ESP+68],EBP
          mov EBP,DWORD PTR [EBX+EDX*4]
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44f868
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EBP
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],9
          add EAX,1
          jmp L_4082f5
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_408680:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f896
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408703
          mov EDX,DWORD PTR [ESP+68]
          lea EAX,DWORD PTR [EDX+1]
          mov EBP,DWORD PTR [EBX+EAX*4]
          test EBP,EBP
          je L_408c96
          cmp ESI,EAX
          je L_408c96
          cmp BYTE PTR [EBP],45
          je L_408c96
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408c83
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f89a
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],10
          add EAX,1
          jmp L_4082f5
L_408703:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f8b1
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408826
          cmp EDI,2
          je L_408865
          mov DWORD PTR [ESP+4],OFFSET L_44f8f0
          mov DWORD PTR [ESP],0
          mov EDI,1
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_408758:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _netConnect
          test EAX,EAX
          je L_408421
          call _netGetInfo
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [_cinfo],EAX
          cmp ECX,12
          ja L_40896b
          jmp DWORD PTR [ECX*4+L_44fb1c]
L_40878a:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],EBP
          call _myatoh32
          cmp EAX,-1
          mov EBX,EAX
          je L_408c35
          mov ECX,DWORD PTR [_cinfo]
          xor EDX,EDX
          mov EAX,DWORD PTR [ECX+20]
          div DWORD PTR [ECX+24]
          mov DWORD PTR [ESP+8],EBX
          cmp EBX,EAX
          jae L_408acb
          mov DWORD PTR [ESP+4],OFFSET _mc_44f6d5
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBX
          call _netEraseBlock
          test EAX,EAX
          je L_408ae4
          mov DWORD PTR [ESP+4],OFFSET _mc_44f6eb
          mov DWORD PTR [ESP],0
          call _log_printf
L_4087ff:
          test EDI,EDI
          jne L_40881c
L_408803:
          call _netDisconnect
          add ESP,92
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_408812:
          call _netGetInfo
          mov DWORD PTR [_cinfo],EAX
L_40881c:
          mov DWORD PTR [ESP],EDI
          call _netReboot
          jmp L_408803
L_408826:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],5
          mov DWORD PTR [ESP+4],OFFSET L_44f910
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408984
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],3
          lea EBP,DWORD PTR [ESP+74]
          add EAX,1
          jmp L_4082f5
L_408865:
          mov DWORD PTR [ESP+4],OFFSET L_44f8b4
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_408885:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],0
          call _client_usage
L_408899:
          lea EAX,DWORD PTR [ESP+74]
          cmp EBP,EAX
          je L_408c5f
          mov DWORD PTR [ESP],EBP
          call _clientInfo
          jmp L_4087ff
L_4088b2:
          mov DWORD PTR [ESP],EBP
          call _netDumpNand
          jmp L_4087ff
L_4088bf:
          call _clientKeys
          jmp L_4087ff
L_4088c9:
          test BYTE PTR [EAX+16],32
          je L_408a17
          mov EAX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call _sendAvatarData
          jmp L_4087ff
L_4088e7:
          test BYTE PTR [EAX+16],32
          je L_4089fe
          mov DWORD PTR [ESP],EBP
          call _sendCompatData
          jmp L_4087ff
L_4088fe:
          mov DWORD PTR [ESP],EBP
          call _clientWrite
          jmp L_4087ff
L_40890b:
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],EAX
          call _clientReadBlocks
          jmp L_4087ff
L_408928:
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call _clientWriteBlocks
          jmp L_4087ff
L_40893d:
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call _clientBinPatch
          jmp L_4087ff
L_408952:
          lea EAX,DWORD PTR [ESP+74]
          cmp EBP,EAX
          je L_408c4e
          mov DWORD PTR [ESP],EBP
          call _clientPatches
          jmp L_4087ff
L_40896b:
          mov DWORD PTR [ESP+4],OFFSET L_44faa8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408984:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],OFFSET L_44f916
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408a44
          mov EDX,DWORD PTR [ESP+68]
          lea EAX,DWORD PTR [EDX+1]
          mov ECX,DWORD PTR [EBX+EAX*4]
          test ECX,ECX
          mov DWORD PTR [ESP+44],ECX
          je L_408c96
          cmp ESI,EAX
          je L_408c96
          cmp BYTE PTR [ECX],45
          je L_408c96
          mov DWORD PTR [ESP+68],EAX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],OFFSET L_44f91a
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_4089fe:
          mov DWORD PTR [ESP+4],OFFSET L_44fa58
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408a17:
          mov DWORD PTR [ESP+4],OFFSET L_44fa14
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408a30:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],2
          call _client_usage
L_408a44:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f933
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408b01
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          cmp ESI,EDX
          mov EBP,DWORD PTR [EBX+EDX*4]
          je L_408ca9
          test EBP,EBP
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f936
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],1
          add EAX,1
          jmp L_4082f5
L_408acb:
          mov DWORD PTR [ESP+4],OFFSET _mc_44f724
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408ae4:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _mc_44f6f8
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408b01:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f953
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408bae
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          cmp ESI,EDX
          mov EBP,DWORD PTR [EBX+EDX*4]
          je L_408ca9
          test EBP,EBP
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f956
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],2
          add EAX,1
          jmp L_4082f5
L_408b88:
          mov EAX,DWORD PTR [EBX+ECX*4]
          mov DWORD PTR [ESP],4
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408b9b:
          mov EAX,DWORD PTR [EBX+ECX*4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408bae:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f974
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408ccf
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          test EBP,EBP
          je L_408ca9
          cmp ESI,EDX
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f978
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],4
          add EAX,1
          jmp L_4082f5
L_408c35:
          mov DWORD PTR [ESP+4],OFFSET _mc_44f684
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4087ff
L_408c4e:
          mov DWORD PTR [ESP],0
          call _clientPatches
          jmp L_4087ff
L_408c5f:
          mov DWORD PTR [ESP],0
          call _clientInfo
          jmp L_4087ff
L_408c70:
          mov EAX,DWORD PTR [EBX+ECX*4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408c83:
          mov EAX,DWORD PTR [EBX+EDX*4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408c96:
          mov EAX,DWORD PTR [EBX+EDX*4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408ca9:
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408cbc:
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call _client_usage
L_408ccf:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f9a5
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408d42
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          test EBP,EBP
          je L_408ca9
          cmp ESI,EDX
          je L_408ca9
          cmp BYTE PTR [EBP],45
          je L_408ca9
          mov ECX,DWORD PTR [ESP+40]
          test ECX,ECX
          jne L_408cbc
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f9a8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],5
          add EAX,1
          jmp L_4082f5
L_408d42:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f9da
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408dbb
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          mov EAX,EDX
          test EBP,EBP
          je L_408e41
          cmp ESI,EDX
          je L_408e2c
          cmp BYTE PTR [EBP],45
          je L_408e41
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f9dd
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],12
          add EAX,1
          jmp L_4082f5
L_408dbb:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44f9f7
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          jne L_408e6d
          mov EAX,DWORD PTR [ESP+68]
          lea EDX,DWORD PTR [EAX+1]
          mov EBP,DWORD PTR [EBX+EDX*4]
          mov EAX,EDX
          test EBP,EBP
          je L_408e5c
          cmp ESI,EDX
          je L_408e52
          cmp BYTE PTR [EBP],45
          je L_408e5c
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_44f9fa
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+68],EDX
          call _log_printf
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+40],7
          add EAX,1
          jmp L_4082f5
L_408e2c:
          mov DWORD PTR [ESP+40],12
L_408e34:
          mov DWORD PTR [ESP+68],EAX
          lea EBP,DWORD PTR [ESP+74]
          jmp L_4083f5
L_408e41:
          mov DWORD PTR [ESP+40],12
          lea EBP,DWORD PTR [ESP+74]
          jmp L_4082f5
L_408e52:
          mov DWORD PTR [ESP+40],7
          jmp L_408e34
L_408e5c:
          mov DWORD PTR [ESP+40],7
          lea EBP,DWORD PTR [ESP+74]
          jmp L_4082f5
L_408e6d:
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],OFFSET L_44fa10
          mov EAX,DWORD PTR [EBX+EAX*4]
          mov DWORD PTR [ESP],EAX
          call _strnicmp
          test EAX,EAX
          mov EAX,DWORD PTR [ESP+68]
          mov EAX,DWORD PTR [EBX+EAX*4]
          jne L_408eaf
          movzx EAX,BYTE PTR [EAX+2]
          mov DWORD PTR [ESP],EAX
          call _log_verbose_flag
          mov EAX,DWORD PTR [ESP+68]
          add EAX,1
          jmp L_4082f5
L_408eaf:
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],1
          call _client_usage
          nop

.section .rdata,"dr"
.p2align 2
_mc_44e10c:
          .string "\n\n***** ERROR: option flag %s on command line but no argument provided!\n"
          .zero 3
_mc_44e158:
          .string "\n\n***** ERROR: option flag %s on command line not enough arguments provided!\n"
          .zero 2
_mc_44e1a8:
          .string "\n\n***** ERROR: option flag %s on command line but option was already set!\n"
          .zero 1
_mc_44e1f4:
          .string "\n\n***** ERROR: unknown option '%s' provided on command line!\n"
          .zero 2
_mc_44e234:
          .string "\n\n***** ERROR: not enough info provided to carry out command!\n"
_mc_44e273:
          .string "xeBuild"
          .zero 1
_mc_44e27c:
          .string "Usage   :\n   %s client <switch> [<option>]\n\n"
_mc_44e2a9:
          .string "Examples:\n"
_mc_44e2b4:
          .string "   %s client -r nanddump.bin\n"
          .zero 2
_mc_44e2d4:
          .string "   %s client -w nandflash.bin -ip 192.168.2.100\n"
_mc_44e305:
          .string "\nSwitches:\n"
          .zero 3
_mc_44e314:
          .string "   -i             : connects to console and shows some info about it\n"
          .zero 2
_mc_44e35c:
          .string "*  -i <d>         : collects console information into folder <d>, usually enough for build mode\n"
          .zero 3
_mc_44e3c0:
          .string "   -r <f>         : dumps system area of NAND to <f>\n"
          .zero 2
_mc_44e3f8:
          .string "   -w <f>         : writes system area of NAND from <f>\n"
          .zero 3
_mc_44e434:
          .string "   -e <d>         : format partition and send avatar/kinect data to HDD from <d>, must match running kernel\n"
          .zero 3
_mc_44e4a4:
          .string "   -c <d>         : format partition and send xbox compatibility data to HDD from <d>\n"
          .zero 1
_mc_44e4fc:
          .string "   -p             : will attempt to automatically update patches based on running kernel version\n"
          .zero 2
_mc_44e560:
          .string "   -p <f>         : update patches with <f>\n"
          .zero 3
_mc_44e590:
          .string "   -rb <f> <b> <l>: read series of blocks starting at <b> for <l>\n"
          .zero 1
_mc_44e5d4:
          .string "   -wb <f> <b>    : write series of blocks starting at <b> for the number of blocks in <f>\n"
_mc_44e630:
          .string "   -eb <b>        : attempt to erase a single block, even if marked bad on console\n"
_mc_44e684:
          .string "   -bp <f> <o>    : binary patch NAND with contents of <f> to logical offset <o>\n"
          .zero 2
_mc_44e6d8:
          .string "*  -keys          : will attempt to dump RSA and 1BL keys from console\n"
_mc_44e720:
          .string "   -s             : shutdown console\n"
          .zero 2
_mc_44e748:
          .string "   -ip <add>      : force attempt to connect to addr (ie: -i 192.168.0.100)\n"
          .zero 3
_mc_44e798:
          .string "   -noenter       : suppresses prompt for enter key when finished\n"
          .zero 1
_mc_44e7dc:
          .string "   -reboot        : causes the console to hard reboot\n"
          .zero 1
_mc_44e814:
          .string "   -v             : shows more info during client process\n"
          .zero 1
_mc_44e850:
          .string "   -?             : shows this help\n\n"
_mc_44e876:
          .string "legend:\n"
          .zero 1
_mc_44e880:
          .string "<add>    = without this option network will be scanned for server broadcast beacon\n"
_mc_44e8d4:
          .string "           If provided the correct format is an IPv4 address like 192.168.0.100\n"
          .zero 3
_mc_44e928:
          .string "<f>      = path, absolute or relative, to a file\n"
          .zero 2
_mc_44e95c:
          .string "<d>      = path, absolute or relative, to a directory - do not terminate with /\n"
          .zero 3
_mc_44e9b0:
          .string "<b>      = hexadecimal block number\n"
          .zero 3
_mc_44e9d8:
          .string "<l>      = hexadecimal number of blocks\n"
          .zero 3
_mc_44ea04:
          .string "<o>      = hexadecimal logical offset (spare data not considered) in flash\n"
_mc_44ea50:
          .string "notes:\n"
_mc_44ea58:
          .string "* functions not fully supported with older patch versions, use with caution.\n"
          .zero 2
_mc_44eaa8:
          .string "- client mode tends to operate on a single command basis, stacking commands.\n"
          .zero 2
_mc_44eaf8:
          .string "  is not possible with the exception of v, noenter, ip, s and reboot.\n"
          .zero 1
_mc_44eb40:
          .string "- patch update (-p) will retain any addon patches already on the console.\n"
_mc_44eb8b:
          .string "\npress <enter> to quit...\n"
          .zero 2
L_44eba8:
          .long L_406360
          .long L_4066c1
          .long L_4066e2
          .long L_4066fb
          .long L_40671c
          .long L_406343
_mc_44ebc0:
          .string "creating mydata folder output at %s\n"
          .zero 3
_mc_44ebe8:
          .string "unable to dump details to %s, disabling\n"
_mc_44ec11:
          .string "0x%x"
_mc_44ec16:
          .string ","
_mc_44ec18:
          .string "dumping console flash to %s\n"
_mc_44ec35:
          .string "success!\n"
_mc_44ec3f:
          .string "failed!\n"
_mc_44ec48:
          .string "Bad Block list  : "
_mc_44ec5b:
          .string "reading file %s..."
_mc_44ec6e:
          .string "success, read 0x%x bytes\n"
_mc_44ec88:
          .string "sending data to console...\n"
_mc_44eca4:
          .string "\n\n***** ERROR: file size should be 0x%x but its 0x%x bytes! Aborted!\n"
          .zero 2
_mc_44ecec:
          .string "\n\n***** ERROR: image magic should be 0xFF4F but its 0x%x! Aborted!\n"
_mc_44ed30:
          .string "\n\n***** ERROR: unable to read file to send\n"
_mc_44ed5c:
          .string "manifest, %08x %08x %s\n"
_mc_44ed74:
          .string "item %03d: %08x %08x %s\n"
_mc_44ed8d:
          .string "checking %s (file ./%s)\n"
          .zero 2
_mc_44eda8:
          .string "\n\n****** ERROR: unable to dump %s to file ./%s, key is not valid or file is inaccessible!\n"
          .zero 1
_mc_44ee04:
          .string "dumping valid %s to file ./%s\n"
_mc_44ee23:
          .string "./"
_mc_44ee26:
          .string "1blkey.txt"
_mc_44ee31:
          .string "1BL key"
_mc_44ee39:
          .string "1BL_pub.bin"
_mc_44ee45:
          .string "1BL RSA pub key"
_mc_44ee55:
          .string "PIRS_pub.bin"
_mc_44ee62:
          .string "PIRS RSA pub key"
_mc_44ee73:
          .string "MAST_pub.bin"
_mc_44ee80:
          .string "MASTER RSA pub key"
          .zero 1
_mc_44ee94:
          .string "\n\n****** ERROR: console patches need to be updated to support this operation!\n"
          .zero 1
_mc_44eee4:
          .string "checking patch sections for glitch console\n"
_mc_44ef10:
          .string "\n\n***** ERROR: patches do not contain all segments, aborting!\n"
          .zero 1
_mc_44ef50:
          .string "checking patch sections for JTAG console\n"
          .zero 2
_mc_44ef7c:
          .string "\n\n***** ERROR: patches do not contain all segments, counted %d - aborting!\n"
_mc_44efc8:
          .string "loaded %s size 0x%x (%d) bytes\n"
_mc_44efe8:
          .string "retrieving patches from console..."
_mc_44f00b:
          .string "patches"
          .zero 1
_mc_44f014:
          .string "success! received 0x%x (%d) bytes\n"
_mc_44f037:
          .string "patches updated OK!\n"
_mc_44f04c:
          .string "\n\n***** ERROR: patch update failed!\n"
          .zero 3
_mc_44f074:
          .string "\n\n***** ERROR: failed to retrieve current patches from console!\n"
          .zero 3
_mc_44f0b8:
          .string "\n\n***** ERROR: %s exists but is 0 len, aborting\n"
          .zero 3
_mc_44f0ec:
          .string "\n\n***** ERROR: could not load %s, aborting\n"
_mc_44f118:
          .string "sending update patches to console..."
          .zero 3
_mc_44f140:
          .string "patches are already up to date!\n"
          .zero 3
_mc_44f164:
          .string "Updating patches from file: %s\n"
_mc_44f184:
          .string "%d/bin/patches_%s.bin"
_mc_44f19a:
          .string "%d/bin/patches_g2%s.bin"
_mc_44f1b2:
          .string "%d/bin/patches_g2m%s.bin"
_mc_44f1cb:
          .string "%d/bin/patches_fat.bin"
          .zero 2
_mc_44f1e4:
          .string "Updating patches in auto mode: %s\n"
          .zero 1
_mc_44f208:
          .string "\n***** ERROR: unable to determine console hack type!\n"
          .zero 2
_mc_44f240:
          .string "Reading 0x%x (%d) blocks from console starting at block 0x%x (%d)...\n"
          .zero 2
_mc_44f288:
          .string "Done!\nWriting 0x%x (%d) bytes to %s...\n"
_mc_44f2b0:
          .string "Done!\n"
          .zero 1
_mc_44f2b8:
          .string "\n\n***** ERROR: Failed to write block data to file %s!\n"
          .zero 1
_mc_44f2f0:
          .string "\n\n***** ERROR: Trying to read blocks from the console failed!\n"
          .zero 1
_mc_44f330:
          .string "\n\n***** ERROR: This read command will exceed the system area size of 0x%x blocks!\n"
          .zero 1
_mc_44f384:
          .string "\n\n***** ERROR: Invalid arguments specified, please provide hex only for start block and number of blocks!\n"
          .zero 1
_mc_44f3f0:
          .string "Writing 0x%x (%d) blocks to console starting at block 0x%x (%d)...\n"
_mc_44f434:
          .string "Done! Wrote 0x%x (%d) bytes to console flash!\n"
          .zero 1
_mc_44f464:
          .string "\n\n***** ERROR: Writing data to console failed!\n"
_mc_44f494:
          .string "\n\n***** ERROR: File %s size (0x%x) is not a multiple of console block size (0x%x)!\n"
_mc_44f4e8:
          .string "\n\n***** ERROR: Unable to read file %s!\n"
_mc_44f510:
          .string "file: %s start offset 0x%x\n"
_mc_44f52c:
          .string "Reading 0x%x blocks from console starting at block 0x%x (%d)...\n"
          .zero 3
_mc_44f570:
          .string "Success!\nPatching in binary data..."
_mc_44f594:
          .string "Writing 0x%x blocks from console starting at block 0x%x...\n"
_mc_44f5d0:
          .string "Success! Completed patching NAND!\n"
          .zero 1
_mc_44f5f4:
          .string "\n\n***** ERROR: Reading data from console failed!\n"
          .zero 2
_mc_44f628:
          .string "\n\n***** ERROR: File %s size patched into offset 0x%x will exceed NAND system area (0x%x)!\n"
          .zero 1
_mc_44f684:
          .string "\n\n***** ERROR: Invalid arguments specified, please provide hex only for offset!\n"
_mc_44f6d5:
          .string "erasing block 0x%x..."
_mc_44f6eb:
          .string "Success!\n"
          .zero 3
_mc_44f6f8:
          .string "\n\n***** ERROR: Failed to erase block 0x%x!\n"
_mc_44f724:
          .string "\n\n***** ERROR: Block 0x%x is outside system area!\n"
L_44f757:
          .string "client"
L_44f75e:
          .string "help"
L_44f763:
          .string "-?"
L_44f766:
          .string "/?"
L_44f769:
          .string "-noenter"
          .zero 2
L_44f774:
          .string "<enter> key on completion suppressed\n"
L_44f79a:
          .string "-reboot"
          .zero 2
L_44f7a4:
          .string "shutdown superseded by reboot, ignoring -s in favor of -reboot\n"
L_44f7e4:
          .string "setting reboot on completion\n"
L_44f802:
          .string "-bp"
          .zero 2
L_44f808:
          .string "setting binary patch file to %s, offset %s\n"
L_44f834:
          .string "-rb"
L_44f838:
          .string "reading %s blocks to %s, starting block %s\n"
L_44f864:
          .string "-wb"
L_44f868:
          .string "writing blocks from %s, starting at block %s\n"
L_44f896:
          .string "-eb"
L_44f89a:
          .string "erase block set to %s\n"
L_44f8b1:
          .string "-s"
L_44f8b4:
          .string "reboot has already been set on command line, ignoring -s\n"
          .zero 2
L_44f8f0:
          .string "setting shutdown on completion\n"
L_44f910:
          .string "-keys"
L_44f916:
          .string "-ip"
L_44f91a:
          .string "setting forced IP to %s\n"
L_44f933:
          .string "-r"
L_44f936:
          .string "setting read filename to %s\n"
L_44f953:
          .string "-w"
L_44f956:
          .string "setting write filename to %s\n"
L_44f974:
          .string "-e"
          .zero 1
L_44f978:
          .string "setting avatar/kinect files base path to %s\n"
L_44f9a5:
          .string "-c"
L_44f9a8:
          .string "setting xbox compatibility files base path to %s\n"
L_44f9da:
          .string "-i"
L_44f9dd:
          .string "info dump path set to %s\n"
L_44f9f7:
          .string "-p"
L_44f9fa:
          .string "patch file set to %s\n"
L_44fa10:
          .string "-v"
          .zero 1
L_44fa14:
          .string "\n\n***** ERROR: cannot send avatar data when a HDD does not exist!\n"
          .zero 1
L_44fa58:
          .string "\n\n***** ERROR: cannot send xbox compatibility data when a HDD does not exist!\n"
          .zero 1
L_44faa8:
          .string "\n\n***** ERROR: invalid mode specified, please inform author\n"
          .zero 3
L_44fae8:
          .string "\n\n***** ERROR: unable to connect to xbox server\n"
          .zero 3
L_44fb1c:
          .long L_40896b
          .long L_4088b2
          .long L_4088fe
          .long L_4088bf
          .long L_4088c9
          .long L_4088e7
          .long L_4087ff
          .long L_408952
          .long L_40890b
          .long L_408928
          .long L_40878a
          .long L_40893d
          .long L_408899
          .zero 16

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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _client_usage - .
          .byte 0xd
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _clientInfo - .
          .byte 0x3a
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
          .byte 0x46
          .byte 0xe
          .byte 0xc0
          .byte 0x8
          .byte 0x3
          .byte 0x12
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
          .byte 0x2
          .byte 0xec
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _clientWrite - .
          .byte 0x1b
          .byte 0x1
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
          .byte 0x30
          .byte 0x2
          .byte 0x95
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x49
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
          .byte 0x43
          .byte 0xb
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _clientManifest - .
          .byte 0xb7
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
          .byte 0x30
          .byte 0x2
          .byte 0xa5
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
          .byte 0x45
          .byte 0xb
          .byte 0x43
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
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _dumpKey - .
          .byte 0xf6
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
          .byte 0x69
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
          .byte 0x2
          .byte 0x63
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
          .byte 0x48
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _clientKeys - .
          .byte 0xea
          .byte 0x1
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
          .byte 0x40
          .byte 0x3
          .byte 0x2c
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _checkPatches - .
          .byte 0x9
          .byte 0x3
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
          .byte 0x50
          .byte 0x2
          .byte 0x6b
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
          .byte 0x3
          .byte 0x5f
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
          .byte 0x2
          .byte 0x61
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _updatePatches - .
          .byte 0xb9
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
          .byte 0x40
          .byte 0x2
          .byte 0x49
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
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _clientPatches - .
          .byte 0x89
          .byte 0x3
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
          .byte 0xd0
          .byte 0x8
          .byte 0x2
          .byte 0xc4
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
          .byte 0x2
          .byte 0xe7
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
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _clientReadBlocks - .
          .byte 0x91
          .byte 0x1
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
          .byte 0x40
          .byte 0x3
          .byte 0xb
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
          .byte 0x57
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
          .byte 0x44
          .byte 0xb
          .byte 0x5b
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
          .byte 0x43
          .byte 0xb
          .byte 0x57
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
          .byte 0x47
          .byte 0xb
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _clientWriteBlocks - .
          .byte 0xa6
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
          .byte 0x60
          .byte 0x3
          .byte 0x8
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
          .byte 0x57
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
          .byte 0x63
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _patchNand - .
          .byte 0xeb
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
          .byte 0x50
          .byte 0x3
          .byte 0xf
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
          .byte 0x46
          .byte 0xb
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
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _clientBinPatch - .
          .byte 0x84
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
          .byte 0x80
          .byte 0x1
          .byte 0x3
          .byte 0x3f
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
          .byte 0x46
          .byte 0xb
          .byte 0x5b
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
          .byte 0x57
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
          .byte 0x45
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _clientEraseBlock - .
          .byte 0xd9
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
          .byte 0x2
          .byte 0x78
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x57
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x57
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _getArgs - .
          .byte 0xf2
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xa1
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
          .byte 0x44
          .byte 0xb
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _mode_client - .
          .byte 0x5f
          .byte 0xc
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
          .byte 0x43
          .byte 0xe
          .byte 0x70
          .byte 0x3
          .byte 0xcc
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
          .byte 0x42
          .byte 0xb
          .byte 0x3
          .byte 0xcb
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
          .byte 0x41
          .byte 0xb

.bss
.p2align 5
_cinfo:
          .zero 32
