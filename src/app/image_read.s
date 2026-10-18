# app/image_read.s -- parsing an existing NAND image: sectors, pairing, LDV, smc.bin
#
# mixed: `#@C name` lines are functions from image_read.c (re/splice.py)
#
# original placement:
#   .bss           00474a20-00478d60
#   .data          0044a5c0-0044a5e0
#   .eh_frame      004676ac-00467fd0
#   .rdata         004521b8-004541f8
#   .rdata$zzz     004639b4-004639e0
#   .text          004136a0-00418240

.intel_syntax noprefix
.globl _anchor
.globl _checkBlock
.globl _copyMmcImage
.globl _detectController
.globl _dumpSize
.globl _findAnchor
.globl _fs
.globl _fsBuf
.globl _fsGetFile
.globl _fsOffset
.globl _fsValid
.globl _getImageKv
.globl _getImageSmc
.globl _ir_4521b8
.globl _ir_4521e0
.globl _ir_452220
.globl _ir_452260
.globl _ir_4522c4
.globl _ir_4522e4
.globl _ir_45230f
.globl _ir_45232c
.globl _ir_45235c
.globl _ir_45238c
.globl _ir_4523bc
.globl _ir_4523ec
.globl _ir_45242c
.globl _ir_452450
.globl _ir_452494
.globl _ir_4524dc
.globl _ir_452508
.globl _ir_452538
.globl _ir_45256c
.globl _ir_4525a8
.globl _ir_4525d0
.globl _ir_45261c
.globl _ir_452674
.globl _ir_4526ac
.globl _ir_4526f0
.globl _ir_45271c
.globl _ir_45276c
.globl _ir_452799
.globl _ir_4527a0
.globl _ir_4527e4
.globl _ir_452824
.globl _ir_452864
.globl _ir_4528a4
.globl _ir_4528e1
.globl _ir_4528fe
.globl _ir_452912
.globl _ir_452930
.globl _ir_452958
.globl _ir_45296a
.globl _ir_452988
.globl _ir_4529d0
.globl _ir_4529f8
.globl _ir_452a24
.globl _ir_452a4c
.globl _ir_452a78
.globl _ir_452aa4
.globl _ir_452acc
.globl _ir_452af8
.globl _ir_452b20
.globl _ir_452b6c
.globl _ir_452bc3
.globl _ir_452bc9
.globl _ir_452bd3
.globl _ir_452bd8
.globl _ir_452c20
.globl _ir_452c47
.globl _ir_452c5e
.globl _ir_452c70
.globl _ir_452cbc
.globl _ir_452d0c
.globl _ir_452d33
.globl _ir_452d4e
.globl _ir_452d55
.globl _ir_452d74
.globl _ir_452db0
.globl _ir_452e09
.globl _ir_452e18
.globl _ir_452e50
.globl _ir_452e80
.globl _ir_452eb0
.globl _ir_452edc
.globl _ir_452f0c
.globl _ir_452f44
.globl _ir_452f7c
.globl _ir_452fb8
.globl _ir_452ffc
.globl _ir_453049
.globl _ir_453064
.globl _ir_45309c
.globl _ir_4530d4
.globl _ir_45310c
.globl _ir_453150
.globl _ir_45318c
.globl _ir_4531b4
.globl _ir_4531e8
.globl _ir_453248
.globl _ir_4532b0
.globl _ir_453310
.globl _ir_453354
.globl _ir_4533a8
.globl _ir_4533ec
.globl _ir_453420
.globl _ir_453474
.globl _ir_4534b8
.globl _ir_4534e9
.globl _ir_4534fc
.globl _ir_453510
.globl _ir_453538
.globl _ir_45355c
.globl _ir_453594
.globl _ir_4535a7
.globl _ir_4535ac
.globl _ir_4535e4
.globl _ir_453610
.globl _ir_453649
.globl _ir_453664
.globl _ir_453694
.globl _ir_4536b8
.globl _ir_4536e0
.globl _ir_453708
.globl _ir_453760
.globl _ir_45378c
.globl _ir_4537b4
.globl _ir_453810
.globl _ir_453828
.globl _ir_45386c
.globl _ir_4538ac
.globl _ir_4538ec
.globl _ir_453928
.globl _ir_45396c
.globl _ir_4539b4
.globl _ir_453a0c
.globl _ir_453a68
.globl _ir_453aac
.globl _ir_453af4
.globl _ir_453b48
.globl _ir_453b98
.globl _ir_453bdc
.globl _ir_453c28
.globl _ir_453c9c
.globl _ir_453d18
.globl _ir_453d3c
.globl _ir_453d78
.globl _ir_453db0
.globl _ir_453dec
.globl _ir_453e2c
.globl _ir_453e64
.globl _ir_453ea4
.globl _ir_453edc
.globl _ir_453f1c
.globl _ir_453f54
.globl _ir_453f94
.globl _ir_453fcc
.globl _ir_454009
.globl _ir_454025
.globl _ir_454044
.globl _ir_454098
.globl _ir_4540dc
.globl _ir_454114
.globl _ir_454138
.globl _ir_45417c
.globl _ir_4541b0
.globl _listFlashFiles
.globl _loadDump
.globl _mobileName
.globl _mobiles
.globl _parseDump
.globl _remapBadBlocks
.globl _scanMobiles
.globl _showMobilePages
.globl _zeropair

.text
.p2align 4
#@C _fsFind
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
#@C _buildCleanup
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _getImageLdv
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
_getImageSmc:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDX,DWORD PTR [_g479f4c]
          mov EAX,DWORD PTR [EDX+124]
          mov EBX,EAX
          mov ECX,EAX
          shl EBX,24
          shr ECX,24
          add ECX,EBX
          mov EBX,EAX
          shr EAX,8
          shl EBX,8
          and EAX,65280
          and EBX,16711680
          add EBX,ECX
          mov ECX,DWORD PTR [EDX+120]
          add EBX,EAX
          mov EDX,ECX
          mov EAX,ECX
          mov ESI,ECX
          shl EAX,24
          shr EDX,24
          shl ESI,8
          and ESI,16711680
          add EDX,EAX
          shr ECX,8
          lea EAX,DWORD PTR [EDX+ESI*1]
          mov ESI,ECX
          and ESI,65280
          add ESI,EAX
          test EBX,EBX
          je L_413cc0
          lea EAX,DWORD PTR [EBX-2048]
          mov EDI,EBX
          test EAX,4294965247
          je L_413bd0
          mov DWORD PTR [ESP+8],EBX
L_413b4b:
          mov DWORD PTR [ESP+4],OFFSET _ir_45232c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,ESI
          and AH,247
          cmp EAX,12288
          je L_413cb0
          mov EBX,4096
          mov EDI,4096
L_413b79:
          mov DWORD PTR [ESP+8],12288
          mov DWORD PTR [ESP+4],OFFSET _ir_45238c
          mov ESI,12288
          mov DWORD PTR [ESP],1
          call _log_printf
L_413b9a:
          imul EAX,DWORD PTR [L_479f5c],528
          cmp EBX,EAX
          jb L_413c20
L_413ba8:
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _ir_452494
          mov DWORD PTR [ESP],1
          call _log_printf
L_413bc4:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_413bd0:
          mov EAX,ESI
          and AH,247
          cmp EAX,12288
          je L_413cb5
          cmp EBX,2048
          jne L_413b79
          mov DWORD PTR [ESP+8],14336
          mov DWORD PTR [ESP+4],OFFSET _ir_45235c
          mov ESI,14336
          mov DWORD PTR [ESP],1
          call _log_printf
          imul EAX,DWORD PTR [L_479f5c],528
          cmp EBX,EAX
          jae L_413ba8
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_413c20:
          mov DWORD PTR [ESP],ESI
          call _malloc
          test EAX,EAX
          mov DWORD PTR [L_47a0e0+4],EAX
          je L_413d10
          add EBX,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [L_47a0e4+4],ESI
          mov DWORD PTR [ESP+4],EBX
          call _memcpy
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _ir_4523bc
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call _unscramble
          test EAX,EAX
          je L_413cd0
          mov DWORD PTR [ESP+4],OFFSET _ir_4523ec
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call _setSmcKey
          jmp L_413bc4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_413cb0:
          mov EDI,4096
L_413cb5:
          mov EBX,EDI
          jmp L_413b9a
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_413cc0:
          mov DWORD PTR [ESP+8],0
          jmp L_413b4b
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_413cd0:
          mov DWORD PTR [ESP+4],OFFSET _ir_45242c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [L_47a0e0+4],0
          mov DWORD PTR [L_47a0e4+4],0
          jmp L_413bc4
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_413d10:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _ir_452450
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_413bc4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_getImageKv:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDX,DWORD PTR [_g479f4c]
          mov EAX,DWORD PTR [EDX+108]
          mov ESI,DWORD PTR [EDX+96]
          mov EDI,EAX
          mov ECX,EAX
          mov EDX,ESI
          shl EDI,24
          shr ECX,24
          mov EBX,ESI
          add ECX,EDI
          mov EDI,EAX
          shl EDX,24
          shl EDI,8
          shl EBX,8
          shr EAX,8
          and EDI,16711680
          and EBX,16711680
          and EAX,65280
          add EDI,ECX
          mov ECX,ESI
          shr ESI,8
          shr ECX,24
          and ESI,65280
          add ECX,EDX
          add EDI,EAX
          lea EDX,DWORD PTR [ECX+EBX*1]
          lea EBX,DWORD PTR [EDX+ESI*1]
          mov ESI,EBX
          je L_413f62
L_413d93:
          lea EAX,DWORD PTR [EBX-16384]
          test EAX,4294950911
          jne L_413f40
L_413da4:
          imul EAX,DWORD PTR [L_479f5c],528
          lea EDX,DWORD PTR [EDI+ESI*1]
          cmp EDX,EAX
          jae L_413f20
          mov DWORD PTR [ESP],16384
          call _malloc
          test EAX,EAX
          mov DWORD PTR [L_47a0e8+4],EAX
          je L_414010
          mov DWORD PTR [ESP+12],16384
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _ir_452538
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [L_47a0ec+4],16384
          add EAX,EDI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call _verifyExtended
          test EAX,EAX
          je L_413f90
          mov DWORD PTR [ESP+4],OFFSET _ir_45256c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e8+4]
          add EAX,16
          mov DWORD PTR [ESP],EAX
          call _setKvSalt
          cmp ESI,32768
          jne L_413f38
          mov DWORD PTR [ESP],16384
          add EDI,16384
          call _malloc
          test EAX,EAX
          mov DWORD PTR [L_47a0f4],EAX
          je L_414030
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+12],16384
          mov DWORD PTR [ESP+4],OFFSET _ir_452674
          mov DWORD PTR [ESP],1
          call _log_printf
          add EDI,DWORD PTR [_g479f4c]
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [L_47a0f8],16384
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDI
          call _memcpy
          mov EAX,DWORD PTR [L_47a0f8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [ESP],EAX
          call _verifyExtended
          test EAX,EAX
          je L_413fd0
          mov DWORD PTR [ESP+4],OFFSET _ir_4526ac
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0f4]
          add EAX,16
          mov DWORD PTR [ESP],EAX
          call _setKvAltSalt
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_413f20:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _ir_45261c
          mov DWORD PTR [ESP],1
          call _log_printf
L_413f38:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_413f40:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_452508
          mov ESI,16384
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_413da4
L_413f62:
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],OFFSET _ir_4524dc
          mov EDI,16384
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_413d93
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_413f90:
          mov DWORD PTR [ESP+4],OFFSET _ir_4525a8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [L_47a0e8+4],0
          mov DWORD PTR [L_47a0ec+4],0
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_413fd0:
          mov DWORD PTR [ESP+4],OFFSET _ir_4526f0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [L_47a0f4],0
          mov DWORD PTR [L_47a0f8],0
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_414010:
          mov DWORD PTR [ESP+4],OFFSET _ir_4525d0
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_413f38
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_414030:
          mov DWORD PTR [ESP+4],OFFSET _ir_45271c
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_413f38
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _getImageMobiles
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
#@C _getNetKd
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
#@C _loadFlashFile
          .byte 0x66
          .byte 0x90
#@C _fsFindFile
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
_listFlashFiles:
          cmp DWORD PTR [_fsValid],1
          je L_414660
          repz ret 
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_414660:
          push EBP
          push EDI
          push ESI
          push EBX
          xor EBX,EBX
          sub ESP,44
          jmp L_41467f
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_414670:
          add EBX,1
          cmp EBX,256
          je L_41474a
L_41467f:
          mov EDX,DWORD PTR [_fs]
          lea EAX,DWORD PTR [EBX+256]
          shl EAX,5
          add EAX,EDX
          cmp BYTE PTR [EAX],0
          je L_414670
          mov ECX,EBX
          add EBX,1
          shl ECX,5
          lea EBP,DWORD PTR [ECX+EDX*1]
          movzx EDI,WORD PTR [EBP+8214]
          mov EDX,DWORD PTR [EBP+8216]
          mov ECX,EDI
          mov ESI,EDI
          movzx EDI,CH
          mov ECX,DWORD PTR [EBP+8220]
          shl ESI,8
          and ESI,65280
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+4],OFFSET _ir_452988
          add ESI,EDI
          mov DWORD PTR [ESP],1
          mov EAX,ECX
          mov EDI,ECX
          mov DWORD PTR [ESP+8],ESI
          shl EAX,24
          shr EDI,24
          add EDI,EAX
          mov EAX,ECX
          shr ECX,8
          shl EAX,8
          and ECX,65280
          and EAX,16711680
          add EAX,EDI
          add ECX,EAX
          mov EAX,EDX
          mov DWORD PTR [ESP+20],ECX
          mov ECX,EDX
          shl EAX,24
          shr ECX,24
          add ECX,EAX
          mov EAX,EDX
          shr EDX,8
          shl EAX,8
          and EDX,65280
          and EAX,16711680
          add EAX,ECX
          add EDX,EAX
          mov EAX,ESI
          shl EAX,14
          add EAX,DWORD PTR [_fsOffset]
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp EBX,256
          jne L_41467f
L_41474a:
          add ESP,44
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_fsGetFile:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov ESI,DWORD PTR [_fsValid]
          mov EDI,DWORD PTR [ESP+80]
          cmp ESI,1
          je L_414782
L_414776:
          xor ESI,ESI
L_414778:
          add ESP,60
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_414782:
          mov EBP,8192
          xor EBX,EBX
          jmp L_41479e
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_414790:
          add EBX,1
          add EBP,32
          cmp EBX,256
          je L_414776
L_41479e:
          mov EDX,DWORD PTR [_fs]
          lea EAX,DWORD PTR [EBX+256]
          shl EAX,5
          cmp BYTE PTR [EDX+EAX*1],0
          je L_414790
          add EDX,EBP
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDX
          call _stricmp
          test EAX,EAX
          jne L_414790
          mov EAX,DWORD PTR [_fs]
          shl EBX,5
          mov DWORD PTR [ESP+32],EAX
          add EAX,EBX
          mov EDX,DWORD PTR [EAX+8216]
          mov ECX,EDX
          mov EBX,EDX
          shl ECX,24
          shr EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add ECX,EDX
          movzx EDX,WORD PTR [EAX+8214]
          mov EAX,DWORD PTR [EAX+8220]
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+4],1
          mov EBP,ECX
          mov DWORD PTR [ESP+28],ECX
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [_fsOffset]
          mov EBX,EDX
          movzx EDX,DH
          shl EBX,8
          and EBX,65280
          mov DWORD PTR [ESP+20],EAX
          add EBX,EDX
          mov EDI,EBX
          shl EDI,14
          add EDI,EAX
          call _calloc
          mov ECX,DWORD PTR [_g479f4c]
          cmp EBP,16384
          mov DWORD PTR [ESP+36],EAX
          mov DWORD PTR [ESP+24],ECX
          mov ECX,EAX
          jbe L_414944
          mov DWORD PTR [ESP+44],ESI
          mov ESI,EBP
          mov EBP,DWORD PTR [ESP+32]
          mov EAX,EDI
          mov EDI,ECX
          .byte 0x66   # nop
          nop
L_414870:
          add EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EDI
          sub ESI,16384
          mov DWORD PTR [ESP+8],16384
          add EDI,16384
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          movzx EBX,WORD PTR [EBP+EBX*2]
          mov EAX,EBX
          shl EBX,8
          movzx EAX,AH
          add EBX,EAX
          and EBX,8191
          mov EAX,EBX
          shl EAX,14
          add EAX,DWORD PTR [ESP+20]
          cmp ESI,16384
          ja L_414870
          mov EDX,DWORD PTR [ESP+28]
          mov EDI,EAX
          mov ESI,DWORD PTR [ESP+44]
          mov EAX,EDX
          sub EDX,16384
          sub EAX,16385
          mov ECX,EAX
          and ECX,4294950912
          mov EAX,ECX
          sub EDX,ECX
          add EAX,16384
L_4148e2:
          add EAX,DWORD PTR [ESP+36]
          add EDI,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
L_4148fc:
          mov EAX,DWORD PTR [ESP+84]
          mov ECX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX],ECX
          mov EAX,DWORD PTR [ESP+88]
          mov ECX,DWORD PTR [ESP+28]
          mov EDX,EDI
          shl EDX,24
          mov DWORD PTR [EAX],ECX
          mov ECX,EDI
          mov EAX,EDI
          shr ECX,24
          shl EAX,8
          and EAX,16711680
          add ECX,EDX
          lea EDX,DWORD PTR [ECX+EAX*1]
          mov EAX,EDI
          shr EAX,8
          and EAX,65280
          add EAX,EDX
          mov EDX,DWORD PTR [ESP+92]
          mov DWORD PTR [EDX],EAX
          jmp L_414778
L_414944:
          mov EAX,DWORD PTR [ESP+28]
          test EAX,EAX
          je L_4148fc
          mov EDX,DWORD PTR [ESP+28]
          xor EAX,EAX
          jmp L_4148e2
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
_findAnchor:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov DWORD PTR [ESP+4],OFFSET _ir_4529d0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479f4c]
          add EAX,50233368
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov ESI,EAX
          mov EAX,DWORD PTR [_g479f4c]
          add EAX,50249752
          mov DWORD PTR [ESP],EAX
          call _getBeU32
          mov EBX,EAX
          mov EAX,DWORD PTR [_g479f4c]
          add EAX,50233344
          mov DWORD PTR [ESP],EAX
          call _shaSelfCheck
          test EAX,EAX
          mov EDI,EAX
          je L_414a50
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _ir_4529f8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479f4c]
          add EAX,50249728
          mov DWORD PTR [ESP],EAX
          call _shaSelfCheck
          test EAX,EAX
          je L_414a7a
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_452a4c
          mov DWORD PTR [ESP],1
          call _log_printf
          cmp ESI,EBX
          jae L_414a94
L_414a10:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_452a78
          mov EDI,OFFSET _anchor
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479f4c]
          mov ECX,128
          lea ESI,DWORD PTR [EAX+50249728]
          mov EAX,1
          rep movsd 
L_414a44:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_414a50:
          mov DWORD PTR [ESP+4],OFFSET _ir_452a24
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479f4c]
          add EAX,50249728
          mov DWORD PTR [ESP],EAX
          call _shaSelfCheck
          test EAX,EAX
          jne L_414ad0
L_414a7a:
          mov DWORD PTR [ESP+4],OFFSET _ir_452aa4
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
          test EDI,EDI
          je L_414a44
L_414a94:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _ir_452acc
          mov EDI,OFFSET _anchor
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [_g479f4c]
          mov ECX,128
          lea ESI,DWORD PTR [EAX+50233344]
          mov EAX,1
          rep movsd 
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_414ad0:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_452a4c
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_414a10
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _mmcFindMobiles
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _spareVersion
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
_showMobilePages:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EDX,DWORD PTR [L_479f60]
          mov EBX,DWORD PTR [_g479f4c]
          mov EAX,DWORD PTR [L_479f5c]
          test EDX,EDX
          jne L_414e7d
          sub EAX,1152
          mov BYTE PTR [ESP+63],48
          mov DWORD PTR [ESP+56],EAX
L_414c0e:
          mov DWORD PTR [ESP+4],OFFSET _separator
          mov DWORD PTR [ESP],2
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_452af8
          mov DWORD PTR [ESP],2
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _separator
          mov DWORD PTR [ESP],2
          call _log_printf
          mov EAX,DWORD PTR [EBX+100]
          mov ESI,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],OFFSET _ir_452b20
          mov DWORD PTR [ESP],2
          mov EDX,EAX
          mov ECX,EAX
          mov DWORD PTR [ESP+16],ESI
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          shr EAX,9
          mov EDI,EAX
          and EAX,4294967264
          add EAX,32
          test EDI,31
          cmove EAX,EDI
          mov EDX,EAX
          mov EBX,EAX
          mov EDI,EAX
          mov EAX,DWORD PTR [L_479f5c]
          shl EDI,9
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+48],EDI
          mov EDI,EDX
          mov DWORD PTR [ESP+20],EAX
          call _log_printf
          cmp EBX,ESI
          jae L_414df6
          imul EDI,EDI,528
          mov EAX,EBX
          shl EBX,4
          mov EBP,EDI
          mov EDI,EAX
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_414ce0:
          mov ECX,DWORD PTR [L_479f50]
          add ECX,EBX
          movzx EAX,BYTE PTR [ECX+12]
          and EAX,63
          cmp BYTE PTR [ESP+63],AL
          je L_414e30
          lea EDX,DWORD PTR [EAX-49]
          lea ESI,DWORD PTR [EBX+16]
          cmp DL,8
          ja L_414dd9
          movzx ESI,BYTE PTR [ECX+8]
          movzx EDX,BYTE PTR [ECX+7]
          movzx EAX,AL
          add EAX,17
          shl ESI,8
          add ESI,EDX
          movzx EDX,SI
          mov WORD PTR [ESP+60],SI
L_414d23:
          mov ESI,DWORD PTR [L_479f60]
          test ESI,ESI
          je L_414e12
          movzx ESI,BYTE PTR [ECX+5]
          mov DWORD PTR [ESP+52],ESI
L_414d39:
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ESP+28],EDX
          movzx EDX,BYTE PTR [ECX+9]
          mov DWORD PTR [ESP+20],EBP
          mov DWORD PTR [ESP+24],EDX
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+16],EDX
          movzx ESI,BYTE PTR [ECX+3]
          movzx EDX,BYTE PTR [ECX+4]
          shl ESI,8
          shl EDX,16
          or EDX,ESI
          movzx ESI,BYTE PTR [ECX+6]
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _ir_452b6c
          mov DWORD PTR [ESP],2
          shl ESI,24
          or EDX,ESI
          or EDX,DWORD PTR [ESP+52]
          lea ESI,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+12],EDX
          call _log_printf
L_414d91:
          mov EAX,DWORD PTR [L_479f50]
          movzx EAX,BYTE PTR [EAX+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET _ir_452bc3
          add EBX,1
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          cmp EBX,ESI
          jne L_414d91
          cmp WORD PTR [ESP+60],0
          js L_414e50
          mov DWORD PTR [ESP+4],OFFSET _ir_452bd3
          mov DWORD PTR [ESP],2
          call _log_printf
L_414dd9:
          add EDI,1
          add DWORD PTR [ESP+48],512
          add EBP,528
          cmp DWORD PTR [ESP+56],EDI
          mov EBX,ESI
          jne L_414ce0
L_414df6:
          mov DWORD PTR [ESP+4],OFFSET _separator
          mov DWORD PTR [ESP],2
          call _log_printf
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_414e12:
          mov ESI,DWORD PTR [L_479f64]
          test ESI,ESI
          je L_414e70
          movzx ESI,BYTE PTR [ECX]
          mov DWORD PTR [ESP+52],ESI
          jmp L_414d39
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_414e30:
          mov EAX,16384
          mov EDX,16384
          mov WORD PTR [ESP+60],AX
          mov EAX,65
          jmp L_414d23
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_414e50:
          mov DWORD PTR [ESP+4],OFFSET _ir_452bc9
          mov DWORD PTR [ESP],2
          call _log_printf
          jmp L_414dd9
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_414e70:
          movzx ESI,BYTE PTR [ECX+2]
          mov DWORD PTR [ESP+52],ESI
          jmp L_414d39
L_414e7d:
          sub EAX,9216
          mov BYTE PTR [ESP+63],44
          mov DWORD PTR [ESP+56],EAX
          jmp L_414c0e
_scanMobiles:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EDX,DWORD PTR [L_479f60]
          mov EBX,DWORD PTR [_g479f4c]
          mov EAX,DWORD PTR [L_479f5c]
          test EDX,EDX
          jne L_415160
          sub EAX,1152
          mov BYTE PTR [ESP+71],48
          mov DWORD PTR [ESP+64],EAX
          call _log_get_verbose
          cmp EAX,2
          je L_41517c
L_414ecc:
          mov EAX,DWORD PTR [EBX+100]
          mov EDX,EAX
          mov ECX,EAX
          shl EDX,24
          shr ECX,24
          add ECX,EDX
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          shr EAX,9
          mov EBP,EAX
          and EAX,4294967264
          add EAX,32
          test EBP,31
          cmovne EBP,EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_414f10:
          cmp DWORD PTR [ESP+64],EBP
          jbe L_414fe5
L_414f1a:
          mov ESI,DWORD PTR [L_479f50]
          mov EDI,EBP
          shl EDI,4
          add ESI,EDI
          movzx EBX,BYTE PTR [ESI+12]
          and EBX,63
          cmp BYTE PTR [ESP+71],BL
          je L_415082
          lea EAX,DWORD PTR [EBX-49]
          cmp AL,8
          ja L_414ff4
          movzx EAX,BYTE PTR [ESI+8]
          movzx EDX,BYTE PTR [ESI+7]
          movzx EBX,BL
          sub EBX,48
          shl EAX,8
          add EAX,EDX
          mov WORD PTR [ESP+68],AX
L_414f5b:
          mov EAX,DWORD PTR [L_479f60]
          test EAX,EAX
          je L_415071
          movzx ECX,BYTE PTR [ESI+5]
L_414f6c:
          mov EAX,EBP
          shl EAX,9
          mov DWORD PTR [ESP+72],EAX
          movzx EAX,BYTE PTR [ESI+3]
          shl EAX,8
          mov EDX,EAX
          movzx EAX,BYTE PTR [ESI+4]
          shl EAX,16
          or EAX,EDX
          movzx EDX,BYTE PTR [ESI+6]
          shl EDX,24
          or EAX,EDX
          or EAX,ECX
          mov DWORD PTR [ESP+60],EAX
          call _log_get_verbose
          cmp EAX,2
          je L_4150a0
L_414fa4:
          lea EAX,DWORD PTR [EBX+EBX*2]
          mov ECX,DWORD PTR [ESP+60]
          cmp DWORD PTR [EAX*8+L_474a24],ECX
          jbe L_415010
          mov ECX,DWORD PTR [EAX*8+_mobiles]
          test ECX,ECX
          je L_415010
          cmp WORD PTR [ESP+68],0
          jns L_414ff2
          add EBP,1
L_414fca:
          mov EDX,DWORD PTR [L_479f60]
          lea EAX,DWORD PTR [EBP+3]
          and EAX,4294967292
          test EDX,EDX
          cmovne EBP,EAX
          cmp DWORD PTR [ESP+64],EBP
          ja L_414f1a
L_414fe5:
          mov EAX,DWORD PTR [_mobiles]
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_414ff2:
          jne L_41504f
L_414ff4:
          add EBP,1
          mov EAX,EBP
          and EAX,4294967264
          add EAX,32
          test EBP,31
          cmovne EBP,EAX
          jmp L_414f10
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_415010:
          cmp WORD PTR [ESP+68],0
          je L_414ff4
          js L_415143
          lea EDX,DWORD PTR [EBX+EBX*2]
          mov ECX,DWORD PTR [ESP+60]
          lea EAX,DWORD PTR [EDX*8+_mobiles]
          mov DWORD PTR [EDX*8+_mobiles],1
          movzx EDX,WORD PTR [ESP+68]
          mov DWORD PTR [EAX+4],ECX
          mov ECX,DWORD PTR [ESP+72]
          mov DWORD PTR [EAX+20],EDI
          mov DWORD PTR [EAX+8],EBP
          mov DWORD PTR [EAX+12],EDX
          mov DWORD PTR [EAX+16],ECX
L_41504f:
          movzx ECX,WORD PTR [ESP+68]
          mov EAX,ECX
          shr AX,9
          movzx EAX,AX
          add EBP,EAX
          mov EAX,ECX
          and AX,511
          cmp AX,1
          sbb EBP,-1
          jmp L_414fca
L_415071:
          mov EAX,DWORD PTR [L_479f64]
          test EAX,EAX
          je L_415093
          movzx ECX,BYTE PTR [ESI]
          jmp L_414f6c
L_415082:
          mov EAX,16384
          xor EBX,EBX
          mov WORD PTR [ESP+68],AX
          jmp L_414f5b
L_415093:
          movzx ECX,BYTE PTR [ESI+2]
          jmp L_414f6c
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4150a0:
          movzx EAX,WORD PTR [ESP+68]
          mov DWORD PTR [ESP+32],EBP
          mov DWORD PTR [ESP+28],EAX
          movzx EAX,BYTE PTR [ESI+9]
          mov DWORD PTR [ESP+4],OFFSET _ir_452b6c
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+24],EAX
          imul EAX,EBP,528
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [EBX+65]
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          lea EAX,DWORD PTR [EDI+16]
          mov DWORD PTR [ESP+76],EBX
          mov EBX,EDI
          mov ESI,EAX
L_4150f5:
          mov EDX,DWORD PTR [L_479f50]
          movzx EDX,BYTE PTR [EDX+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET _ir_452bc3
          add EBX,1
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+8],EDX
          call _log_printf
          cmp ESI,EBX
          jne L_4150f5
          cmp WORD PTR [ESP+68],0
          mov EBX,DWORD PTR [ESP+76]
          js L_4151a0
          mov DWORD PTR [ESP+4],OFFSET _ir_452bd3
          mov DWORD PTR [ESP],2
          call _log_printf
          jmp L_414fa4
L_415143:
          lea EAX,DWORD PTR [EBX+EBX*2]
          add EBP,1
          mov DWORD PTR [EAX*8+_mobiles],0
          jmp L_414fca
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_415160:
          sub EAX,9216
          mov BYTE PTR [ESP+71],44
          mov DWORD PTR [ESP+64],EAX
          call _log_get_verbose
          cmp EAX,2
          jne L_414ecc
L_41517c:
          mov DWORD PTR [ESP+4],OFFSET _ir_452bd3
          mov DWORD PTR [ESP],2
          call _log_printf
          call _showMobilePages
          jmp L_414ecc
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4151a0:
          mov DWORD PTR [ESP+4],OFFSET _ir_452bc9
          mov DWORD PTR [ESP],2
          call _log_printf
          jmp L_414fa4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setFsOffset
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _findFsRoot
L_4154c7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imgGetSecurityFiles
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
#@C _findSmcConfig
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
_checkBlock:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [L_479f60]
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call _blockErased
          test EAX,EAX
          jne L_415cc0
          mov EAX,DWORD PTR [L_479f60]
          mov ESI,4294967295
          test EAX,EAX
          jne L_415b45
          cmp BYTE PTR [EBX+517],255
          je L_415c30
L_415b3d:
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
L_415b45:
          cmp BYTE PTR [EBX+512],255
          jne L_415b3d
          cmp BYTE PTR [EBX+68096],255
          jne L_415b3d
          movzx ESI,BYTE PTR [EBX+514]
          movzx EAX,BYTE PTR [EBX+513]
          and ESI,15
          shl ESI,8
          add ESI,EAX
          mov EAX,DWORD PTR [ESP+40]
          sub EAX,1
          cmp ESI,EAX
          jge L_415cd0
          mov ECX,DWORD PTR [L_479f70]
          test ECX,ECX
          jne L_415d28
          movzx EAX,BYTE PTR [EBX+524]
          and EAX,63
          movzx EDX,AL
          cmp EDX,41
          jg L_415c90
          test AL,AL
          je L_415c90
          mov DWORD PTR [ESP+4],OFFSET _ir_452e18
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_452e50
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_452e80
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_452eb0
          mov DWORD PTR [ESP],0
          call _log_printf
          test BYTE PTR [L_479f03],16
          jne L_415d55
L_415c05:
          mov DWORD PTR [ESP+4],OFFSET _ir_452f44
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [L_479f70],1
          mov DWORD PTR [L_479f6c],1
          jmp L_415c90
          .byte 0x90
L_415c30:
          cmp BYTE PTR [EBX+8965],255
          jne L_415b3d
          movzx EAX,BYTE PTR [EBX+514]
          movzx EDX,BYTE PTR [EBX+513]
          movzx ESI,BYTE PTR [EBX+513]
          and EAX,15
          shl EAX,8
          and ESI,15
          add EAX,EDX
          movzx EDX,BYTE PTR [EBX+512]
          shl ESI,8
          add ESI,EDX
          mov EDX,DWORD PTR [L_479f64]
          test EDX,EDX
          je L_415ce0
          mov ECX,DWORD PTR [ESP+36]
          test ECX,ECX
          je L_415cf5
          cmp DWORD PTR [ESP+36],ESI
          mov ESI,4294967290
          jne L_415cf5
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_415c90:
          mov EAX,DWORD PTR [L_479f00]
          test EAX,EAX
          js L_415b3d
          mov EAX,DWORD PTR [L_479f60]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _blockEccOk
          test EAX,EAX
          mov EAX,4294967292
          cmove ESI,EAX
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
L_415cc0:
          mov ESI,4294967294
          jmp L_415b3d
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_415cd0:
          mov ESI,4294967293
          jmp L_415c90
L_415cd7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_415ce0:
          mov EDX,DWORD PTR [ESP+36]
          test EDX,EDX
          je L_415cf7
          cmp DWORD PTR [ESP+36],EAX
          jne L_415cf7
          mov ESI,4294967290
          jmp L_415c90
L_415cf5:
          mov ESI,EAX
L_415cf7:
          mov EAX,DWORD PTR [ESP+40]
          sub EAX,1
          cmp EAX,ESI
          jle L_415cd0
          test ESI,ESI
          jle L_415c90
          mov EAX,DWORD PTR [ESP+40]
          sub EAX,34
          cmp DWORD PTR [ESP+36],EAX
          .byte 0x0f,0x8d; .long L_415c90-.-4   # jge L_415c90
          cmp DWORD PTR [ESP+36],ESI
          mov EAX,4294967293
          cmovne ESI,EAX
          jmp L_415c90
L_415d28:
          test ESI,ESI
          jle L_415d4e
          mov EAX,DWORD PTR [ESP+40]
          sub EAX,34
          cmp EAX,DWORD PTR [ESP+36]
          jle L_415c90
          cmp ESI,DWORD PTR [ESP+36]
          mov EAX,4294967293
          cmovne ESI,EAX
          jmp L_415c90
L_415d4e:
          xor ESI,ESI
          jmp L_415c90
L_415d55:
          mov DWORD PTR [ESP+4],OFFSET _ir_452edc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_452f0c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_415c05
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
#@C _addRemap
          .byte 0x90
#@C _findFreeRemap
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
_remapBadBlocks:
          push EBP
          push EDI
          push ESI
          push EBX
          xor ESI,ESI
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET _ir_453049
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [L_479f74]
          mov EAX,DWORD PTR [ESP+48]
          test ECX,ECX
          lea EDI,DWORD PTR [EAX-32]
          jne L_415f2e
          jmp L_415fbb
L_415f23:
          add ESI,1
          cmp ESI,ECX
          jae L_415fbb
L_415f2e:
          cmp DWORD PTR [ESI*4+L_479ff8],-1
          jne L_415f23
          mov EBP,DWORD PTR [ESI*4+L_479f78]
          cmp EBP,EDI
          jae L_416009
          mov EAX,DWORD PTR [ESP+48]
          lea EDX,DWORD PTR [EAX-1]
          .byte 0x66   # nop
          nop
L_415f50:
          xor EBX,EBX
          xor EAX,EAX
          jmp L_415f70
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_415f60:
          cmp DWORD PTR [EAX*4+L_479f78],EDX
          je L_415f79
          add EAX,1
          cmp EAX,ECX
          jae L_415f87
L_415f70:
          cmp DWORD PTR [EAX*4+L_479ff8],EDX
          jne L_415f60
L_415f79:
          mov EAX,ECX
          mov EBX,1
          add EAX,1
          cmp EAX,ECX
          jb L_415f70
L_415f87:
          test EBX,EBX
          je L_415fd7
          sub EDX,1
          cmp EDI,EDX
          jle L_415f50
L_415f92:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_45309c
          add ESI,1
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [L_479f74]
          cmp ESI,ECX
          jb L_415f2e
L_415fbb:
          mov DWORD PTR [ESP+4],OFFSET _ir_452d4e
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_415fd7:
          test EDX,EDX
          je L_415f92
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_453064
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESI*4+L_479ff8],EDX
          call _log_printf
          mov ECX,DWORD PTR [L_479f74]
          jmp L_415f23
L_416009:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_4530d4
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESI*4+L_479ff8],4294967291
          mov ECX,DWORD PTR [L_479f74]
          jmp L_415f23
L_416037:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _notZeropair
          .byte 0x90
#@C _spareLbaOk
          .byte 0x8d
          .byte 0x76
          .byte 0x0
_copyMmcImage:
          sub ESP,28
          mov EAX,DWORD PTR [L_479f54]
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],OFFSET _zeropair
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          je L_416130
          mov EAX,1
          add ESP,28
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_416130:
          mov DWORD PTR [ESP+4],OFFSET _ir_45310c
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_parseDump:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          cmp DWORD PTR [L_479f60],1
          mov EBX,DWORD PTR [L_479f5c]
          mov EAX,EBX
          sbb ECX,ECX
          xor EDX,EDX
          and CL,32
          add ECX,256
          div ECX
          mov DWORD PTR [ESP+72],ECX
          test EDX,EDX
          mov DWORD PTR [ESP+52],EAX
          jne L_41669f
          mov DWORD PTR [ESP+4],OFFSET _ir_45318c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ESI,DWORD PTR [ESP+52]
          test ESI,ESI
          je L_4163ef
          imul EAX,DWORD PTR [ESP+72],528
          xor EBP,EBP
          mov DWORD PTR [ESP+44],EBP
          mov DWORD PTR [ESP+64],EAX
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+60],EAX
          mov DWORD PTR [ESP+56],EAX
          mov EAX,DWORD PTR [ESP+52]
          sub EAX,32
          mov DWORD PTR [ESP+76],EAX
          .byte 0x66   # nop
          nop
L_4161d0:
          mov EDX,DWORD PTR [ESP+52]
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+8],EDX
          mov EDX,DWORD PTR [ESP+44]
          mov EBX,EAX
          mov DWORD PTR [ESP],EAX
          sub EBX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],EDX
          call _checkBlock
          cmp EAX,-2
          mov EBP,EAX
          je L_4163d0
          cmp EAX,-1
          je L_416491
          cmp EAX,-3
          je L_416554
          cmp EAX,-6
          je L_416579
          cmp EAX,-4
          je L_4165d8
          mov EAX,DWORD PTR [ESP+44]
          cmp EAX,EBP
          je L_416251
          mov EDX,DWORD PTR [ESP+76]
          cmp EAX,EDX
          jl L_416450
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _ir_453354
          mov DWORD PTR [ESP],1
          call _log_printf
L_416251:
          mov EBX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [_g479f4c]
          test EBX,EBX
          je L_4167aa
L_416263:
          mov EDI,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+68],EBP
          mov EAX,EDI
          imul EAX,EBP
          mov EBX,EAX
          mov EDX,EAX
          add EAX,EDI
          shl EAX,4
          shl EBX,9
          shl EDX,4
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [ESP+60]
          jmp L_416296
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_416290:
          mov ECX,DWORD PTR [_g479f4c]
L_416296:
          mov ESI,DWORD PTR [EAX]
          add ECX,EBX
          add EBX,512
          lea EDI,DWORD PTR [ECX+4]
          mov DWORD PTR [ECX],ESI
          mov ESI,DWORD PTR [EAX+508]
          and EDI,4294967292
          mov DWORD PTR [ECX+508],ESI
          sub ECX,EDI
          mov ESI,EAX
          sub ESI,ECX
          add ECX,512
          add EAX,528
          shr ECX,2
          rep movsd 
          mov ESI,DWORD PTR [EAX-4]
          mov EDI,DWORD PTR [EAX-8]
          mov ECX,DWORD PTR [L_479f50]
          mov EBP,DWORD PTR [EAX-12]
          mov DWORD PTR [ESP+40],ESI
          mov ESI,DWORD PTR [EAX-16]
          mov DWORD PTR [ECX+EDX*1+8],EDI
          mov EDI,DWORD PTR [ESP+40]
          mov DWORD PTR [ECX+EDX*1+4],EBP
          mov DWORD PTR [ECX+EDX*1],ESI
          mov DWORD PTR [ECX+EDX*1+12],EDI
          add EDX,16
          cmp DWORD PTR [ESP+48],EDX
          jne L_416290
          mov EBP,DWORD PTR [ESP+68]
          cmp EBP,DWORD PTR [ESP+44]
          je L_4163d0
          mov EAX,DWORD PTR [L_479f74]
          xor EDX,EDX
          xor EBX,EBX
          test EAX,EAX
          jne L_416327
          jmp L_416796
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_416320:
          add EBX,1
          cmp EBX,EAX
          jae L_416380
L_416327:
          cmp DWORD PTR [EBX*4+L_479f78],EBP
          jne L_416320
          cmp DWORD PTR [EBX*4+L_479ff8],-1
          jne L_416320
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_452f7c
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDI
          call _log_printf
          mov DWORD PTR [EBX*4+L_479ff8],EDI
          mov EAX,DWORD PTR [L_479f74]
          add EBX,1
          mov EDX,1
          cmp EBX,EAX
          jb L_416327
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_416380:
          test EDX,EDX
          jne L_4163d0
          cmp EAX,32
          je L_4165ba
          add EAX,1
L_416390:
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+16],EAX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_452fb8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDI
          call _log_printf
          mov EAX,DWORD PTR [L_479f74]
          mov DWORD PTR [EAX*4+L_479f78],EBP
          mov DWORD PTR [EAX*4+L_479ff8],EDI
          add EAX,1
          mov DWORD PTR [L_479f74],EAX
          nop
L_4163d0:
          add DWORD PTR [ESP+44],1
          mov EDI,DWORD PTR [ESP+64]
          mov EAX,DWORD PTR [ESP+44]
          add DWORD PTR [ESP+56],EDI
          add DWORD PTR [ESP+60],EDI
          cmp DWORD PTR [ESP+52],EAX
          jne L_4161d0
L_4163ef:
          mov DWORD PTR [ESP+4],OFFSET _ir_452d4e
          mov DWORD PTR [ESP],1
          call _log_printf
          test BYTE PTR [L_479f03],64
          je L_4166c5
          mov ECX,DWORD PTR [L_479f74]
          mov EAX,1
          test ECX,ECX
          je L_4165d0
          mov DWORD PTR [ESP+4],OFFSET _ir_4534b8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+40],EAX
          call _log_printf
          mov DWORD PTR [L_479f74],0
          mov EAX,DWORD PTR [ESP+40]
          jmp L_4165d0
          .byte 0x66
          .byte 0x90
L_416450:
          mov EDI,EAX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET _ir_4533a8
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EDI
          mov EBP,EDI
          mov DWORD PTR [ESP+4],OFFSET _ir_4533ec
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_416251
L_416491:
          mov ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBX
          xor EBX,EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_4531b4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],ESI
          call _log_printf
          mov EAX,DWORD PTR [L_479f74]
          xor EDX,EDX
          test EAX,EAX
          jne L_4164c7
          jmp L_416531
L_4164c0:
          add EBX,1
          cmp EBX,EAX
          jae L_416520
L_4164c7:
          cmp DWORD PTR [EBX*4+L_479f78],ESI
          jne L_4164c0
          cmp DWORD PTR [EBX*4+L_479ff8],-1
          jne L_4164c0
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],4294967295
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _ir_452f7c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [EBX*4+L_479ff8],4294967295
          mov EAX,DWORD PTR [L_479f74]
          add EBX,1
          mov EDX,1
          cmp EBX,EAX
          jb L_4164c7
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_416520:
          test EDX,EDX
          jne L_4163d0
          cmp EAX,32
          je L_4165ba
L_416531:
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [EAX*4+L_479ff8],4294967295
          mov DWORD PTR [EAX*4+L_479f78],EDX
          add EAX,1
          mov DWORD PTR [L_479f74],EAX
          jmp L_4163d0
L_416554:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_4531e8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          jmp L_4163d0
L_416579:
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_453248
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EDI
          call _log_printf
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET _ir_4532b0
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_4163d0
L_4165ba:
          mov DWORD PTR [ESP+4],OFFSET _ir_452ffc
          mov DWORD PTR [ESP],1
          call _log_printf
          xor EAX,EAX
L_4165d0:
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4165d8:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBX
          xor EBX,EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_453310
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call _log_printf
          mov EAX,DWORD PTR [L_479f74]
          xor EDX,EDX
          mov ESI,DWORD PTR [ESP+44]
          test EAX,EAX
          jne L_416617
          jmp L_4167a0
          .byte 0x66
          .byte 0x90
L_416610:
          add EBX,1
          cmp EBX,EAX
          jae L_41666a
L_416617:
          cmp DWORD PTR [EBX*4+L_479f78],ESI
          jne L_416610
          cmp DWORD PTR [EBX*4+L_479ff8],-1
          jne L_416610
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],4294967295
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET _ir_452f7c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [EBX*4+L_479ff8],4294967295
          mov EAX,DWORD PTR [L_479f74]
          add EBX,1
          mov EDX,1
          cmp EBX,EAX
          jb L_416617
L_41666a:
          test EDX,EDX
          jne L_416696
          cmp EAX,32
          je L_4165ba
          lea EDX,DWORD PTR [EAX+1]
L_41667a:
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [EAX*4+L_479ff8],4294967295
          mov DWORD PTR [L_479f74],EDX
          mov DWORD PTR [EAX*4+L_479f78],EDI
L_416696:
          mov EBP,DWORD PTR [ESP+44]
          jmp L_416251
L_41669f:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+4],OFFSET _ir_453150
          mov DWORD PTR [ESP],0
          call _log_printf
          add ESP,92
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4166c5:
          mov EDX,DWORD PTR [L_479f74]
          mov EAX,1
          test EDX,EDX
          je L_4165d0
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _remapBadBlocks
          mov DWORD PTR [ESP+4],OFFSET _ir_4534e9
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f74]
          test EAX,EAX
          je L_416741
          xor EBX,EBX
L_416703:
          mov EAX,DWORD PTR [EBX*4+L_479ff8]
          cmp EAX,-5
          je L_416762
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX*4+L_479f78]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET _ir_453538
          add EBX,1
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp DWORD PTR [L_479f74],EBX
          ja L_416703
L_416741:
          mov DWORD PTR [ESP+4],OFFSET _ir_4534fc
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,92
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_416762:
          mov EAX,DWORD PTR [EBX*4+L_479f78]
          mov DWORD PTR [ESP+8],EBX
          add EBX,1
          mov DWORD PTR [ESP+4],OFFSET _ir_453510
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call _log_printf
          cmp DWORD PTR [L_479f74],EBX
          ja L_416703
          jmp L_416741
L_416796:
          mov EAX,1
          jmp L_416390
L_4167a0:
          mov EDX,1
          jmp L_41667a
L_4167aa:
          lea EAX,DWORD PTR [ECX+16]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],OFFSET _zeropair
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+40]
          je L_416822
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [ESP],EAX
          call _spareLbaOk
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+40]
          jne L_416263
          mov DWORD PTR [ESP+4],OFFSET _ir_453420
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+40],EAX
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_453474
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [ESP+40]
          jmp L_4165d0
L_416822:
          mov DWORD PTR [ESP+4],OFFSET _ir_45310c
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          jmp L_4165d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _copyMuData
          .byte 0x66
          .byte 0x90
_detectController:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBX,DWORD PTR [ESP+68]
          mov ESI,DWORD PTR [ESP+64]
          cmp EBX,50331648
          je L_416c22
          cmp BYTE PTR [ESI+512],255
          je L_416bd0
          cmp BYTE PTR [ESI+517],255
          je L_416af0
          mov DWORD PTR [ESP+4],OFFSET _ir_4537b4
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
L_416ae7:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_416af0:
          mov EAX,EBX
          mov EDX,1041204193
          sar EBX,31
          imul EDX
          mov DWORD PTR [ESP+4],OFFSET _ir_453760
          mov DWORD PTR [ESP],1
          sar EDX,12
          mov EDI,EDX
          sub EDI,EBX
          call _log_printf
          xor EAX,EAX
          cmp EDI,1
          mov DWORD PTR [L_479f60],0
          mov DWORD PTR [L_479f70],1
          jle L_416ae7
          mov EBX,1
          mov DWORD PTR [ESP+28],EAX
          jmp L_416b47
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_416b40:
          add EBX,1
          cmp EDI,EBX
          jle L_416bc0
L_416b47:
          imul EDX,EBX,16896
          add EDX,ESI
          cmp BYTE PTR [EDX+517],255
          jne L_416b40
          movzx ECX,BYTE PTR [EDX+513]
          cmp CL,255
          je L_416b40
          movzx EBP,BYTE PTR [EDX+514]
          movzx EAX,CL
          and EBP,15
          shl EBP,8
          add EBP,EAX
          cmp EBP,EBX
          je L_416c80
          movzx EDX,BYTE PTR [EDX+512]
          and ECX,15
          shl ECX,8
          add ECX,EDX
          cmp ECX,EBX
          jne L_416b40
          mov DWORD PTR [ESP+4],OFFSET _ir_45378c
          mov DWORD PTR [ESP],1
          mov EBX,EDI
          call _log_printf
          mov DWORD PTR [L_479f64],0
          mov DWORD PTR [ESP+28],1
          jmp L_416b40
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_416bc0:
          mov EAX,DWORD PTR [ESP+28]
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_416bd0:
          mov DWORD PTR [ESP+4],OFFSET _ir_4536e0
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_4536b8
          mov DWORD PTR [ESP],1
          call _log_printf
          cmp EBX,69206015
          jle L_416cb0
          mov DWORD PTR [L_479f60],1
          mov DWORD PTR [L_479f64],1
          mov EAX,1
          jmp L_416ae7
L_416c22:
          mov DWORD PTR [ESP+4],OFFSET _ir_453694
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_4536b8
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [L_479f64],1
          mov DWORD PTR [L_479f60],0
          mov EAX,1
          mov DWORD PTR [L_479f70],1
          mov DWORD PTR [L_479f68],1
          jmp L_416ae7
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_416c80:
          mov DWORD PTR [ESP+4],OFFSET _ir_4536b8
          mov DWORD PTR [ESP],1
          mov EBX,EDI
          call _log_printf
          mov DWORD PTR [L_479f64],1
          mov DWORD PTR [ESP+28],1
          jmp L_416b40
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_416cb0:
          mov DWORD PTR [ESP+4],OFFSET _ir_453708
          mov DWORD PTR [ESP],0
          call _log_printf
          xor EAX,EAX
          jmp L_416ae7
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _checkHeader
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _getNonces
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
_loadDump:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1100
          mov EAX,DWORD PTR [ESP+1120]
          test EAX,EAX
          je L_417bd4
          lea EBP,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBP
          call _strcpy
L_4176a9:
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [_dumpSize],0
          test EAX,EAX
          je L_4176c4
          mov DWORD PTR [ESP],EAX
          call _free
L_4176c4:
          mov EAX,DWORD PTR [_g479f4c]
          test EAX,EAX
          je L_4176d5
          mov DWORD PTR [ESP],EAX
          call _free
L_4176d5:
          mov EBX,OFFSET L_47a08c
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [_g479f4c],0
          mov DWORD PTR [L_479f50],0
          mov DWORD PTR [L_479f6c],0
          mov ESI,EBX
          mov DWORD PTR [L_479f70],0
          .byte 0x66   # nop
          nop
L_417710:
          mov EAX,DWORD PTR [ESI]
          test EAX,EAX
          je L_41771e
          mov DWORD PTR [ESP],EAX
          call _free
L_41771e:
          add ESI,8
          cmp ESI,OFFSET L_47a0e0+4
          jne L_417710
          mov ESI,OFFSET _xb
          mov EDI,ESI
L_417730:
          mov EAX,DWORD PTR [EDI+580]
          test EAX,EAX
          je L_417742
          mov DWORD PTR [ESP],EAX
          call _free
L_417742:
          mov DWORD PTR [EDI+584],0
          add EDI,8
          cmp EDI,OFFSET L_479ec0
          jne L_417730
          mov EAX,DWORD PTR [L_47a104]
          test EAX,EAX
          je L_417768
          mov DWORD PTR [ESP],EAX
          call _free
L_417768:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_454009
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP+4],OFFSET _ir_4535a7
          mov DWORD PTR [ESP],EBP
          call _fopen
          test EAX,EAX
          mov EDI,EAX
          je L_417d8b
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBP
          call _checkHeader
          test EAX,EAX
          mov ECX,EAX
          je L_417b20
          cmp EAX,50331648
          mov DWORD PTR [_dumpSize],EAX
          je L_417a50
          mov EDX,1041204193
          imul EDX
          mov EAX,ECX
          sar EAX,31
          sar EDX,7
          sub EDX,EAX
          imul EAX,EDX,528
          cmp ECX,EAX
          jne L_417ada
          cmp ECX,69206015
          jg L_417a30
          cmp ECX,17301504
          mov DWORD PTR [ESP+32],17301504
          mov EAX,32768
          jne L_417b0d
L_417804:
          mov DWORD PTR [L_479f5c],EAX
L_417809:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+36],ECX
          mov DWORD PTR [ESP],EAX
          call _malloc
          test EAX,EAX
          mov DWORD PTR [ESP+28],EAX
          mov ECX,DWORD PTR [ESP+36]
          je L_417db0
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],OFFSET _ir_454114
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+36],ECX
          call _log_printf
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _fread
          mov DWORD PTR [ESP],EDI
          call _fclose
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_452d4e
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479f5c]
          mov EDX,EAX
          shl EAX,4
          shl EDX,9
          mov EDI,EAX
          mov DWORD PTR [ESP+44],EAX
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+40],EDX
          mov DWORD PTR [L_479f54],EDX
          mov DWORD PTR [L_479f58],EAX
          call _malloc
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [_g479f4c],EAX
          mov DWORD PTR [ESP+32],EAX
          call _malloc
          mov EDX,DWORD PTR [ESP+32]
          mov EDI,EAX
          mov DWORD PTR [L_479f50],EAX
          test EDX,EDX
          je L_417c82
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+36]
          je L_417c82
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP+32],ECX
          mov DWORD PTR [ESP+8],EAX
          call _memset
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP+8],EAX
          call _memset
          mov DWORD PTR [ESP+4],OFFSET _ir_45417c
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [ESP+32]
          mov EDI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EDI
          call _detectController
          test EAX,EAX
          je L_417d6c
          mov EAX,DWORD PTR [L_479f68]
          test EAX,EAX
          jne L_417a70
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _parseDump
          test EAX,EAX
          mov EDI,EAX
          jne L_417c40
L_417966:
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [_dumpSize],0
          test EAX,EAX
          je L_417981
          mov DWORD PTR [ESP],EAX
          call _free
L_417981:
          mov EAX,DWORD PTR [_g479f4c]
          test EAX,EAX
          je L_417992
          mov DWORD PTR [ESP],EAX
          call _free
L_417992:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [_g479f4c],0
          mov DWORD PTR [L_479f50],0
          mov DWORD PTR [L_479f6c],0
          mov DWORD PTR [L_479f70],0
L_4179c4:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_4179d2
          mov DWORD PTR [ESP],EAX
          call _free
L_4179d2:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_4179c4
L_4179dd:
          mov EAX,DWORD PTR [ESI+580]
          test EAX,EAX
          je L_4179ef
          mov DWORD PTR [ESP],EAX
          call _free
L_4179ef:
          mov DWORD PTR [ESI+584],0
          add ESI,8
          cmp ESI,OFFSET L_479ec0
          jne L_4179dd
          mov EAX,DWORD PTR [L_47a104]
          xor EDI,EDI
          test EAX,EAX
          je L_417a17
          mov DWORD PTR [ESP],EAX
          call _free
L_417a17:
          mov EAX,DWORD PTR [ESP+28]
L_417a1b:
          mov DWORD PTR [ESP],EAX
          call _free
L_417a23:
          add ESP,1100
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_417a30:
          mov DWORD PTR [ESP+32],69206016
          mov EAX,131072
          mov ECX,69206016
          jmp L_417804
L_417a47:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_417a50:
          mov DWORD PTR [L_479f5c],98304
          mov DWORD PTR [ESP+32],50331648
          jmp L_417809
L_417a67:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_417a70:
          mov EAX,DWORD PTR [L_479f54]
          mov DWORD PTR [ESP+4],EDI
          mov EDI,1
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [_g479f4c]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],OFFSET _zeropair
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call _memcmp
          test EAX,EAX
          jne L_417c40
          mov DWORD PTR [ESP+4],OFFSET _ir_45310c
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_417966
L_417ada:
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_454098
L_417aea:
          mov DWORD PTR [ESP],1
          call _log_printf
          mov DWORD PTR [ESP],EDI
          xor EDI,EDI
          call _fclose
          add ESP,1100
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_417b0d:
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_454044
          jmp L_417aea
          .byte 0x90
L_417b20:
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [_dumpSize],0
          test EAX,EAX
          je L_417b3b
          mov DWORD PTR [ESP],EAX
          call _free
L_417b3b:
          mov EAX,DWORD PTR [_g479f4c]
          test EAX,EAX
          je L_417b4c
          mov DWORD PTR [ESP],EAX
          call _free
L_417b4c:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [_g479f4c],0
          mov DWORD PTR [L_479f50],0
          mov DWORD PTR [L_479f6c],0
          mov DWORD PTR [L_479f70],0
          .byte 0x66   # nop
          nop
L_417b80:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_417b8e
          mov DWORD PTR [ESP],EAX
          call _free
L_417b8e:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_417b80
L_417b99:
          mov EAX,DWORD PTR [ESI+580]
          test EAX,EAX
          je L_417bab
          mov DWORD PTR [ESP],EAX
          call _free
L_417bab:
          mov DWORD PTR [ESI+584],0
          add ESI,8
          cmp ESI,OFFSET L_479ec0
          jne L_417b99
          mov EAX,DWORD PTR [L_47a104]
          xor EDI,EDI
          test EAX,EAX
          jne L_417a1b
          jmp L_417a23
L_417bd4:
          lea EBP,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBP
          call _strcpy
          mov EDX,EBP
L_417bea:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_417bea
          mov ECX,EAX
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,3
          mov DWORD PTR [EDX],1684955502
          mov DWORD PTR [EDX+4],1886221668
          mov DWORD PTR [EDX+8],1852400174
          mov BYTE PTR [EDX+12],0
          jmp L_4176a9
L_417c37:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_417c40:
          call _getImageKv
          call _getImageSmc
          call _findSmcConfig
          call _getImageLdv
          call _findFsRoot
          test EAX,EAX
          je L_417c78
          mov EAX,DWORD PTR [L_479f00]
          test EAX,536870912
          je L_417f27
L_417c6d:
          test EAX,67108864
          je L_417dd7
L_417c78:
          call _getNonces
          jmp L_417a17
L_417c82:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_454138
          mov DWORD PTR [ESP],0
          call _log_printf
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [_dumpSize],0
          test EAX,EAX
          je L_417cb5
          mov DWORD PTR [ESP],EAX
          call _free
L_417cb5:
          mov EAX,DWORD PTR [_g479f4c]
          test EAX,EAX
          je L_417cc6
          mov DWORD PTR [ESP],EAX
          call _free
L_417cc6:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [_g479f4c],0
          mov DWORD PTR [L_479f50],0
          mov DWORD PTR [L_479f6c],0
          mov DWORD PTR [L_479f70],0
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_417d00:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_417d0e
          mov DWORD PTR [ESP],EAX
          call _free
L_417d0e:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_417d00
L_417d19:
          mov EAX,DWORD PTR [ESI+580]
          test EAX,EAX
          je L_417d2b
          mov DWORD PTR [ESP],EAX
          call _free
L_417d2b:
          mov DWORD PTR [ESI+584],0
          add ESI,8
          cmp ESI,OFFSET L_479ec0
          jne L_417d19
          mov EAX,DWORD PTR [L_47a104]
          test EAX,EAX
          je L_417d51
          mov DWORD PTR [ESP],EAX
          call _free
L_417d51:
          mov EAX,DWORD PTR [ESP+28]
          xor EDI,EDI
          mov DWORD PTR [ESP],EAX
          call _free
          add ESP,1100
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_417d6c:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_4541b0
          xor EDI,EDI
          mov DWORD PTR [ESP],0
          call _log_printf
          jmp L_417a17
L_417d8b:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_454025
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,1100
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_417db0:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET _ir_4540dc
          mov DWORD PTR [ESP],0
          call _log_printf
          mov DWORD PTR [ESP],EDI
          xor EDI,EDI
          call _fclose
          jmp L_417a23
L_417dd7:
          mov DWORD PTR [ESP+4],OFFSET _ir_452d33
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [_buildMode]
          test EDX,EDX
          je L_417f0e
          cmp BYTE PTR [_flashFiles],0
          je L_417e0f
          cmp DWORD PTR [_fsValid],1
          je L_417f77
L_417e0f:
          cmp EDX,1
          jbe L_417f0e
          cmp BYTE PTR [L_4c8ffa],0
          je L_417e2e
          cmp DWORD PTR [_fsValid],1
          je L_4180b3
L_417e2e:
          cmp EDX,2
          jbe L_417f0e
          cmp BYTE PTR [L_4c9010],0
          je L_417e4d
          cmp DWORD PTR [_fsValid],1
          je L_418102
L_417e4d:
          cmp EDX,3
          jbe L_417f0e
          cmp BYTE PTR [L_4c9026],0
          je L_417e6c
          cmp DWORD PTR [_fsValid],1
          je L_418151
L_417e6c:
          cmp EDX,4
          jbe L_417f0e
          cmp BYTE PTR [L_4c903c],0
          je L_417e8b
          cmp DWORD PTR [_fsValid],1
          je L_4181a0
L_417e8b:
          cmp EDX,5
          jbe L_417f0e
          cmp BYTE PTR [L_4c9052],0
          je L_417ea6
          cmp DWORD PTR [_fsValid],1
          je L_4181ef
L_417ea6:
          cmp EDX,6
          jbe L_417f0e
          cmp BYTE PTR [L_4c9068],0
          je L_417ec1
          cmp DWORD PTR [_fsValid],1
          je L_417fc6
L_417ec1:
          cmp EDX,7
          jbe L_417f0e
          cmp BYTE PTR [L_4c907e],0
          je L_417edc
          cmp DWORD PTR [_fsValid],1
          je L_418015
L_417edc:
          cmp EDX,8
          jbe L_417f0e
          cmp BYTE PTR [L_4c9094],0
          je L_417ef7
          cmp DWORD PTR [_fsValid],1
          je L_418064
L_417ef7:
          cmp EDX,9
          jbe L_417f0e
          cmp BYTE PTR [L_4c90aa],0
          je L_417f0e
          cmp DWORD PTR [_fsValid],1
          je L_417f3b
L_417f0e:
          mov DWORD PTR [ESP+4],OFFSET _ir_452d4e
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_417c78
L_417f27:
          call _getNetKd
          call _getImageMobiles
          mov EAX,DWORD PTR [L_479f00]
          jmp L_417c6d
L_417f3b:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9134
          mov ECX,OFFSET L_4c910c
          mov EAX,OFFSET L_4c90aa
          call _fsFind
          test EAX,EAX
          je L_417f0e
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],9
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          jmp L_417f0e
L_417f77:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9110
          mov ECX,OFFSET L_4c90e8
          mov EAX,OFFSET _flashFiles
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417e0f
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417e0f
L_417fc6:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9128
          mov ECX,OFFSET L_4c9100
          mov EAX,OFFSET L_4c9068
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417ec1
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],6
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417ec1
L_418015:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c912c
          mov ECX,OFFSET L_4c9104
          mov EAX,OFFSET L_4c907e
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417edc
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],7
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417edc
L_418064:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9130
          mov ECX,OFFSET L_4c9108
          mov EAX,OFFSET L_4c9094
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417ef7
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417ef7
L_4180b3:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9114
          mov ECX,OFFSET L_4c90ec
          mov EAX,OFFSET L_4c8ffa
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417e2e
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417e2e
L_418102:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9118
          mov ECX,OFFSET L_4c90f0
          mov EAX,OFFSET L_4c9010
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417e4d
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417e4d
L_418151:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c911c
          mov ECX,OFFSET L_4c90f4
          mov EAX,OFFSET L_4c9026
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417e6c
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417e6c
L_4181a0:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9120
          mov ECX,OFFSET L_4c90f8
          mov EAX,OFFSET L_4c903c
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417e8b
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],4
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417e8b
L_4181ef:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9124
          mov ECX,OFFSET L_4c90fc
          mov EAX,OFFSET L_4c9052
          call _fsFind
          test EAX,EAX
          mov EDX,DWORD PTR [_buildMode]
          je L_417ea6
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call _loadFlashFile
          mov EDX,DWORD PTR [_buildMode]
          jmp L_417ea6
          .byte 0x90
          .byte 0x90

.data
.p2align 5
_zeropair:
          .string "zeropair image"
          .zero 1
_mobileName:
          .ascii "Mobile"
L_44a5d6:
          .string "A"
_fs:
          .long _fsBuf
          .zero 4

.section .rdata,"dr"
.p2align 3
_ir_4521b8:
          .string "%s found in sector 0x%x size 0x%x..."
          .zero 3
_ir_4521e0:
          .string "Did not find a LDV value to use, setting it to 0 for devkit!\n"
          .zero 2
_ir_452220:
          .string "Did not find a LDV value to use, setting it to 0 for testkit!\n"
          .zero 1
_ir_452260:
          .string "***** WARNING: could not find a non-zero CF LDV to use, setting it to 1 but that may be incorrect!\n"
_ir_4522c4:
          .string "setting LDV from image to %d\n"
          .zero 2
_ir_4522e4:
          .string "setting pairing data from image to 0x%06x\n"
_ir_45230f:
          .string "LDV was already set to %d\n"
          .zero 2
_ir_45232c:
          .string "smc.bin should not be at 0x%x, trying 0x1000\n"
          .zero 2
_ir_45235c:
          .string "smc.bin should not be 0x%x bytes, using 0x3800\n"
_ir_45238c:
          .string "smc.bin should not be 0x%x bytes, using 0x3000\n"
_ir_4523bc:
          .string "decrypting SMC at address 0x%x of size 0x%x\n"
          .zero 3
_ir_4523ec:
          .string "SMC decrypted OK, will use if no external smc.bin is provided\n"
          .zero 1
_ir_45242c:
          .string "SMC did not decrypt, discarding it\n"
_ir_452450:
          .string "Wasn't able to alloc 0x%x bytes memory for SMC bin, not using...\n"
          .zero 2
_ir_452494:
          .string "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\n"
          .zero 2
_ir_4524dc:
          .string "KeyVault cannot be at 0x0, trying 0x4000\n"
          .zero 2
_ir_452508:
          .string "KeyVault cannot be 0x%x bytes, using 0x4000\n"
          .zero 3
_ir_452538:
          .string "decrypting KeyVault at address 0x%x of size 0x%x\n"
          .zero 2
_ir_45256c:
          .string "keyvault decrypted OK, will use if no kv.bin is provided\n"
          .zero 2
_ir_4525a8:
          .string "keyvault decrypt failed, discarding\n"
          .zero 3
_ir_4525d0:
          .string "Wasn't able to alloc 0x4000 bytes memory for KeyVault bin, not using...\n"
          .zero 3
_ir_45261c:
          .string "KeyVault at address 0x%x of size 0x4000 is not sane, skipping KeyVault in NAND image\n"
          .zero 2
_ir_452674:
          .string "decrypting alt KeyVault at address 0x%x of size 0x%x\n"
          .zero 2
_ir_4526ac:
          .string "alt KeyVault decrypted OK, will use if no kv_alt.bin is provided\n"
          .zero 2
_ir_4526f0:
          .string "alt KeyVault decrypt failed, discarding\n"
          .zero 3
_ir_45271c:
          .string "Wasn't able to alloc 0x4000 bytes memory for alt KeyVault bin, not using...\n"
          .zero 3
_ir_45276c:
          .string "Unable to allocate memory for %s 0x%x bytes\n"
_ir_452799:
          .string "%s.dat"
_ir_4527a0:
          .string "extracting %s from page 0x%x (offset 0x%x), size %d (0x%x) bytes\n"
          .zero 2
_ir_4527e4:
          .string "Statistics.settings found at offset 0x%x, size %d (0x%x) bytes\n"
_ir_452824:
          .string "Unable to allocate memory for Statistics.settings 0x%x bytes\n"
          .zero 2
_ir_452864:
          .string "Manufacturing.data found at offset 0x%x, size %d (0x%x) bytes\n"
          .zero 1
_ir_4528a4:
          .string "Unable to allocate memory for Manufacturing.data 0x%x bytes\n"
_ir_4528e1:
          .string "netKd info found, size 0x%x\n"
_ir_4528fe:
          .string "    version : 0x%x\n"
_ir_452912:
          .string "    xbox IP : %d.%d.%d.%d\n"
          .zero 3
_ir_452930:
          .string "    xbox MAC: %02x:%02x:%02x:%02x:%02x\n"
_ir_452958:
          .string "    port    : %d\n"
_ir_45296a:
          .string "    host IP : %d.%d.%d.%d\n"
          .zero 3
_ir_452988:
          .string "sector: 0x%04x offset: 0x%08x size: 0x%08x timestamp: 0x%08x name: %s\n"
          .zero 1
_ir_4529d0:
          .string "attempting to find valid anchor block\n"
          .zero 1
_ir_4529f8:
          .string "anchor block v %d at 0x2fe8000 is valid\n"
          .zero 3
_ir_452a24:
          .string "anchor block at 0x2fe8000 is invalid\n"
          .zero 2
_ir_452a4c:
          .string "anchor block v %d at 0x2fec000 is valid\n"
          .zero 3
_ir_452a78:
          .string "anchor block v %d at 0x2fec000 is selected\n"
_ir_452aa4:
          .string "anchor block at 0x2fec000 is invalid\n"
          .zero 2
_ir_452acc:
          .string "anchor block v %d at 0x2fe8000 is selected\n"
_ir_452af8:
          .string "Showing all pages with mobile info:\n"
          .zero 3
_ir_452b20:
          .string "starting mobile scan at page 0x%x (offset 0x%x) of 0x%x pages (0x%x total)\n"
_ir_452b6c:
          .string "mobile%c.dat ver %02d offset 0x%08x (dump:0x%08x) count 0x%02x len 0x%04x page 0x%08x "
_ir_452bc3:
          .string "%02x "
_ir_452bc9:
          .string "(DELETE)\n"
_ir_452bd3:
          .string "\n"
          .zero 3
_ir_452bd8:
          .string "bigblock file system offset set to 0x%x fsb: %x meta: %x lbaend: %x\n"
          .zero 3
_ir_452c20:
          .string "Scanning for mobile data and fsroot..."
_ir_452c47:
          .string "done! fsroot found ok!"
_ir_452c5e:
          .string "Mobiles found:\n"
          .zero 2
_ir_452c70:
          .string "    fsroot      version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n"
_ir_452cbc:
          .string "    mobile%c.dat version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n"
          .zero 3
_ir_452d0c:
          .string "\n\n***** ERROR! Could not find fsroot!\n"
_ir_452d33:
          .string "seeking security files...\n"
_ir_452d4e:
          .string "done!\n"
_ir_452d55:
          .string "seeking smc config in dump..."
          .zero 1
_ir_452d74:
          .string "found at offset 0x%x! Using if no smc config is provided.\n"
          .zero 1
_ir_452db0:
          .string "found at offset 0x%x! Unable to allocate 0x400 bytes of memory for smc config, skipping\n"
_ir_452e09:
          .string "not found!\n"
          .zero 3
_ir_452e18:
          .string "\n\n****************  WARNING  *************************\n"
_ir_452e50:
          .string "  nanddump.bin has NAND memory unit data, make\n"
_ir_452e80:
          .string "  sure you back up any important data off the\n"
          .zero 1
_ir_452eb0:
          .string "  internal MU before flashing a new image!\n"
_ir_452edc:
          .string "\n  xeBuild will attempt to keep this data, but\n"
_ir_452f0c:
          .string "  many things could cause it to be invalid/corrupt.\n"
          .zero 3
_ir_452f44:
          .string "****************************************************\n\n"
          .zero 1
_ir_452f7c:
          .string "block 0x%x was remapped to block 0x%x at remap instance %d\n"
_ir_452fb8:
          .string "block 0x%x was remapped to block 0x%x, entering remap instance %d\n"
          .zero 1
_ir_452ffc:
          .string "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\n"
_ir_453049:
          .string "cleaning up stray remaps\n"
          .zero 1
_ir_453064:
          .string "block 0x%x had no remap, assigning remap block 0x%x\n"
          .zero 3
_ir_45309c:
          .string "block 0x%x had no remap, and I could not assign one!\n"
          .zero 2
_ir_4530d4:
          .string "block 0x%x had no need of remap, it's in the wear area\n"
_ir_45310c:
          .string "\n\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\n"
          .zero 2
_ir_453150:
          .string "UNEXPECTED DUMP PARSE ERROR: %d pages cannot divide by %d!\n"
_ir_45318c:
          .string "parsing dump into user and spare...\n"
          .zero 3
_ir_4531b4:
          .string "bad block at 0x%x (raw offset 0x%x), block ignored\n"
_ir_4531e8:
          .string "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\n"
          .zero 2
_ir_453248:
          .string "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\n"
          .zero 1
_ir_4532b0:
          .string "               this is likely caused by previously using jaspersb on a jasper type console!\n"
          .zero 3
_ir_453310:
          .string "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\n"
          .zero 1
_ir_453354:
          .string "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\n"
          .zero 1
_ir_4533a8:
          .string "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\n"
_ir_4533ec:
          .string "               this dump may have some bad data!\n"
          .zero 2
_ir_453420:
          .string "\n\n***** ERROR: nanddump.bin has mixed LBA in the same block which usually occurs\n"
          .zero 2
_ir_453474:
          .string "             due to an improper nandpro write method, discarding\n"
          .zero 2
_ir_4534b8:
          .string "Discarding remap data as NOREMAP was specified!\n"
_ir_4534e9:
          .string "--remap summary--\n"
_ir_4534fc:
          .string "-----------------\n"
          .zero 1
_ir_453510:
          .string "%d: source: 0x%04x dest: (NONE/BAD)\n"
          .zero 3
_ir_453538:
          .string "%d: source: 0x%04x dest: 0x%04x\n"
          .zero 3
_ir_45355c:
          .string "size is not a multiple of %d bytes, not copying data..\n"
_ir_453594:
          .string "no data to copy..\n"
_ir_4535a7:
          .string "rb"
          .zero 2
_ir_4535ac:
          .string "could not re-open '%s' for reading, not copying data..\n"
_ir_4535e4:
          .string "could not seek to 0x%x, not copying data..\n"
_ir_453610:
          .string "could not allocate 0x%x byte buffer, not copying data..\n"
_ir_453649:
          .string "reading nanddump.bin...\n"
          .zero 2
_ir_453664:
          .string "writing nanddump.bin MU area to output file..."
          .zero 1
_ir_453694:
          .string "\tNAND dump is from a mmc machine\n"
          .zero 2
_ir_4536b8:
          .string "\tNAND dump uses big block controller\n"
          .zero 2
_ir_4536e0:
          .string "\tNAND dump is from a big block machine\n"
_ir_453708:
          .string "***** WARNING: NAND dump too small to be from a big block machine, discarding dump!\n"
          .zero 3
_ir_453760:
          .string "\tNAND dump is from a small block machine\n"
          .zero 2
_ir_45378c:
          .string "\tNAND dump uses small block controller\n"
_ir_4537b4:
          .string "***** WARNING: NAND dump does not appear to have a good block at block 0, discarding dump!\n"
_ir_453810:
          .string "%s file size: 0x%llx\n"
          .zero 2
_ir_453828:
          .string "******* ERROR loading '%s', file size 0x%llx is not large enough\n"
          .zero 2
_ir_45386c:
          .string "******* ERROR loading '%s', flash header magic is incorrect\n"
          .zero 3
_ir_4538ac:
          .string "******* ERROR loading '%s', flash header Entry is too large\n"
          .zero 3
_ir_4538ec:
          .string "******* ERROR loading '%s', flash header Size is too large\n"
_ir_453928:
          .string "******* ERROR loading '%s', flash header KeyVaultSize is too large\n"
_ir_45396c:
          .string "******* ERROR loading '%s', flash header SysUpdateAddr is malformed\n"
          .zero 3
_ir_4539b4:
          .string "******* ERROR loading '%s', flash header SysUpdateCount is not 2, continuing anyway\n"
          .zero 3
_ir_453a0c:
          .string "******* ERROR loading '%s', flash header KeyVaultVersion is not 0x0712, continuing anyway\n"
          .zero 1
_ir_453a68:
          .string "******* ERROR loading '%s', flash header KeyVaultAddr is too large\n"
_ir_453aac:
          .string "******* ERROR loading '%s', flash header FileSystemAddr is too large\n"
          .zero 2
_ir_453af4:
          .string "******* ERROR loading '%s', flash header SmcConfigAddr is not 0, continuing anyway\n"
_ir_453b48:
          .string "******* ERROR loading '%s', flash header SmcBootSize is not 0x3000 or 0x3800\n"
          .zero 2
_ir_453b98:
          .string "******* ERROR loading '%s', flash header SmcBootAddr is too large\n"
          .zero 1
_ir_453bdc:
          .string "FATX magic found, truncating load size to 0x3000000 bytes for mmc consoles\n"
_ir_453c28:
          .string "First page does not contain a valid ECC, assuming this is an mmc dump and truncating load size to 0x3000000 bytes!\n"
_ir_453c9c:
          .string "First page contains a valid ECC, assuming this is a big block flash overdump and truncating load size to 0x4200000 bytes\n"
          .zero 2
_ir_453d18:
          .string "nanddump header checks passed OK!\n"
          .zero 1
_ir_453d3c:
          .string "**** Warning: error getting CB/CBA Nonce offset, aborting!\n"
_ir_453d78:
          .string "**** Warning: error getting CB/CBA Nonce, aborting!\n"
          .zero 3
_ir_453db0:
          .string "**** Warning: error getting CBB Nonce offset, aborting!\n"
          .zero 3
_ir_453dec:
          .string "**** Warning: error getting CBB Nonce, offset 0x%x aborting!\n"
          .zero 2
_ir_453e2c:
          .string "**** Warning: error getting CD Nonce offset, aborting!\n"
_ir_453e64:
          .string "**** Warning: error getting CD Nonce, offset 0x%x aborting!\n"
          .zero 3
_ir_453ea4:
          .string "**** Warning: error getting CE Nonce offset, aborting!\n"
_ir_453edc:
          .string "**** Warning: error getting CE Nonce, offset 0x%x aborting!\n"
          .zero 3
_ir_453f1c:
          .string "**** Warning: error getting CF Nonce offset, aborting!\n"
_ir_453f54:
          .string "**** Warning: error getting CF Nonce, offset 0x%x aborting!\n"
          .zero 3
_ir_453f94:
          .string "**** Warning: error getting CG Nonce offset, aborting!\n"
_ir_453fcc:
          .string "**** Warning: error getting CG Nonce, offset 0x%x aborting!\n"
_ir_454009:
          .string "\n------ Checking %s ------\n"
_ir_454025:
          .string "NAND dump not found at '%s'\n"
          .zero 2
_ir_454044:
          .string "NAND dump '%s' is not a correct raw (with ecc) dump size (0x%x bytes), ignoring\n"
          .zero 3
_ir_454098:
          .string "NAND dump '%s' is not a correct dump size (0x%x bytes), ignoring\n"
          .zero 2
_ir_4540dc:
          .string "******* ERROR loading '%s', unable to allocate memory\n"
          .zero 1
_ir_454114:
          .string "Loading NAND dump (0x%x bytes)..."
          .zero 2
_ir_454138:
          .string "******* ERROR loading '%s', unable to allocate user/spare memory\n"
          .zero 2
_ir_45417c:
          .string "Detecting NAND controller type from dump data...\n"
          .zero 2
_ir_4541b0:
          .string "******* ERROR loading '%s', unable to determine NAND controller type!\n"
          .zero 1

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
          .byte 0x64
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _fsFind - .
          .byte 0x43
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
          .byte 0x4c
          .byte 0xe
          .byte 0x50
          .byte 0x2
          .byte 0xe2
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
          .byte 0x43
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
          .byte 0x74
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _buildCleanup - .
          .byte 0xcd
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
          .byte 0x2
          .byte 0xc5
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
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _getImageLdv - .
          .byte 0xb
          .byte 0x2
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
          .byte 0xc9
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
          .byte 0xc3
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
          .byte 0x47
          .byte 0xb
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
          .byte 0x44
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
          .long _getImageSmc - .
          .byte 0x5d
          .byte 0x2
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
          .byte 0xf1
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
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getImageKv - .
          .byte 0x19
          .byte 0x3
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
          .byte 0xe1
          .byte 0x1
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
          .byte 0x46
          .byte 0xb
          .byte 0x5b
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
          .byte 0x42
          .byte 0xb
          .byte 0x2
          .byte 0x88
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
          .byte 0x78
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _getImageMobiles - .
          .byte 0xa2
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
          .byte 0x4d
          .byte 0xe
          .byte 0x70
          .byte 0x3
          .byte 0x67
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
          .byte 0x7e
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _getNetKd - .
          .byte 0xd4
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
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x96
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
          .byte 0x47
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _loadFlashFile - .
          .byte 0x2e
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
          .byte 0x3
          .byte 0xe
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
          .byte 0x45
          .byte 0xb
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x94
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _fsFindFile - .
          .byte 0x33
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0xe
          .byte 0x8
          .byte 0x86
          .byte 0x2
          .byte 0x41
          .byte 0xe
          .byte 0xc
          .byte 0x83
          .byte 0x3
          .byte 0x59
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x49
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _listFlashFiles - .
          .byte 0x2
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x51
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
          .byte 0x45
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xe4
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _fsGetFile - .
          .byte 0xf4
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
          .byte 0x54
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
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _findAnchor - .
          .byte 0x8d
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
          .byte 0x20
          .byte 0x2
          .byte 0xe1
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
          .byte 0x46
          .byte 0xb
          .byte 0x2
          .byte 0x7b
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
          .byte 0x42
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _mmcFindMobiles - .
          .byte 0x9c
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
          .byte 0x30
          .byte 0x2
          .byte 0x86
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
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _spareVersion - .
          .byte 0x4b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x47
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x71
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xec
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _showMobilePages - .
          .byte 0xb0
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
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x3
          .byte 0x26
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
          .byte 0x41
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _scanMobiles - .
          .byte 0x29
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
          .byte 0x70
          .byte 0x3
          .byte 0x56
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _setFsOffset - .
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x57
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0x50
          .byte 0xe
          .byte 0x4
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _findFsRoot - .
          .byte 0x97
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x44
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
          .byte 0x3
          .byte 0x1e
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
          .byte 0x4a
          .byte 0xb
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgGetSecurityFiles - .
          .byte 0x93
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x2
          .byte 0xf5
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _findSmcConfig - .
          .byte 0x83
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
          .byte 0x20
          .byte 0x2
          .byte 0xf3
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
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0x75
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
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _checkBlock - .
          .byte 0x82
          .byte 0x2
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
          .byte 0x7b
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
          .byte 0x41
          .byte 0xb
          .byte 0x3
          .byte 0x76
          .byte 0x1
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
          .byte 0x41
          .byte 0xb
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x80
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _addRemap - .
          .byte 0xff
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
          .byte 0x50
          .byte 0x2
          .byte 0xcf
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
          .byte 0x5f
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _findFreeRemap - .
          .byte 0x57
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
          .byte 0x2
          .byte 0x53
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _remapBadBlocks - .
          .byte 0x47
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
          .byte 0x45
          .byte 0xe
          .byte 0x30
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _notZeropair - .
          .byte 0x2f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x68
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _spareLbaOk - .
          .byte 0x5d
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
          .byte 0x30
          .byte 0x7e
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
          .byte 0x43
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _copyMmcImage - .
          .byte 0x7a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x54
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x59
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _parseDump - .
          .byte 0xed
          .byte 0x6
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
          .byte 0x70
          .byte 0x3
          .byte 0x7c
          .byte 0x4
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
          .byte 0xe6
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
          .byte 0x93
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _copyMuData - .
          .byte 0x5e
          .byte 0x2
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
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x8
          .byte 0x3
          .byte 0x98
          .byte 0x1
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
          .byte 0x42
          .byte 0xb
          .byte 0x5c
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
          .byte 0x62
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
          .byte 0x49
          .byte 0xb
          .byte 0x6a
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
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _detectController - .
          .byte 0x2b
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0x43
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
          .byte 0x2
          .byte 0xd7
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _checkHeader - .
          .byte 0xeb
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
          .byte 0xf0
          .byte 0x5
          .byte 0x2
          .byte 0xf6
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
          .byte 0xcf
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
          .byte 0x46
          .byte 0xb
          .byte 0x48
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _getNonces - .
          .byte 0xb9
          .byte 0x3
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
          .byte 0x44
          .byte 0xb
          .byte 0x2
          .byte 0xa7
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
          .byte 0x46
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa0
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _loadDump - .
          .byte 0xbe
          .byte 0xb
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
          .byte 0xe0
          .byte 0x8
          .byte 0x3
          .byte 0x9f
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
          .byte 0x2
          .byte 0xd6
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
          .byte 0x3
          .byte 0x58
          .byte 0x2
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
          .byte 0x7d
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

.bss
.p2align 5
_mobiles:
          .zero 4
L_474a24:
          .zero 4
L_474a28:
          .zero 4
L_474a2c:
          .zero 4
L_474a30:
          .zero 224
L_474b10:
          .zero 16
_anchor:
          .zero 28
L_474b3c:
          .zero 484
_fsOffset:
          .zero 4
_fsValid:
          .zero 28
_fsBuf:
          .zero 8192
L_476d40:
          .zero 8192
_dumpSize:
          .zero 32
