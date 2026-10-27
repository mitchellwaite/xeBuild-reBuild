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
.globl _dumpSize
.globl _fs
.globl _fsBuf
.globl _fsOffset
.globl _fsValid
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
.globl _mobileName
.globl _mobiles
.globl _parseDump
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
#@C _getImageKv
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
#@C _listFlashFiles
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
#@C _fsGetFile
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
#@C _findAnchor
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
#@C _showMobilePages
#@C _scanMobiles
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
#@C _checkBlock
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
#@C _remapBadBlocks
L_416037:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _notZeropair
          .byte 0x90
#@C _spareLbaOk
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _copyMmcImage
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
#@C _detectController
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
#@C _loadDump
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
