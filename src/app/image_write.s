# app/image_write.s -- flash layout (CB/CE/SMC/Mobile*.dat), writing image to disk
#
# mixed: `#@C name` lines are functions from image_write.c (re/splice.py)
#
# original placement:
#   .bss           0046f9c0-004709e0
#   .data          0044a580-0044a5c0
#   .eh_frame      00466be0-004674ac
#   .rdata         00451760-00451fb4
#   .rdata$zzz     0046395c-00463988
#   .text          0040e950-00413090

.intel_syntax noprefix
.globl L_470000
.globl L_47006e
.globl _copyright
.globl _imgAddFile
.globl _iw_451760
.globl _iw_45179c
.globl _iw_4517f8
.globl _iw_451820
.globl _iw_451850
.globl _iw_45187c
.globl _iw_4518a0
.globl _iw_4518e8
.globl _iw_451924
.globl _iw_451978
.globl _iw_4519c4
.globl _iw_4519f4
.globl _iw_451a20
.globl _iw_451a44
.globl _iw_451a6c
.globl _iw_451a94
.globl _iw_451ab8
.globl _iw_451adc
.globl _iw_451b04
.globl _iw_451b2c
.globl _iw_451b54
.globl _iw_451b7a
.globl _iw_451b7d
.globl _iw_451b9a
.globl _iw_451ba4
.globl _iw_451be4
.globl _iw_451c18
.globl _iw_451c38
.globl _iw_451c94
.globl _iw_451cdd
.globl _iw_451ce4
.globl _iw_451d10
.globl _iw_451d54
.globl _iw_451d88
.globl _iw_451dca
.globl _iw_451de0
.globl _iw_451e14
.globl _iw_451e28
.globl _iw_451e84
.globl _iw_451ec0
.globl _iw_451f37
.globl _iw_451f48
.globl _iw_451f80
.globl _mobileOffset
.globl _nFsFiles
.globl _smcPage

.text
.p2align 4
#@C _imgAdd.constprop.1
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _imgWritePage
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
#@C _imgAdd.constprop.3
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
#@C _buildImage
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _imageFree
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _calcEcd
          .byte 0x90
#@C _calcPageEcc
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _pageEccOk
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _blockEccOk
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _pageErased
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
#@C _blockErased
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
#@C _blockPagesErased
L_410037:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _blockIsFF
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _isErased
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _setBlockSpare
          .byte 0x66
          .byte 0x90
#@C _imgSizeAligned
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _setFlashBuild
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
#@C _smcSetLoad
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
#@C _imgSmcOffset
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _setPatchSlot
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imgCfOffset
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _imgCfSize
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _imgSize
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imgSetSize
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _imgBigBlock
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imgAdd
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imgFits
          .byte 0x66
          .byte 0x90
_imgAddFile:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [_imgEnd]
          mov EAX,DWORD PTR [ESP+100]
          mov EDX,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+104]
          mov ECX,EBX
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+108]
          and ECX,16383
          mov ESI,EAX
          mov DWORD PTR [ESP+24],EAX
          lea EAX,DWORD PTR [EBX+16384]
          sub EAX,ECX
          test ECX,ECX
          cmovne EBX,EAX
          mov EAX,ESI
          add EAX,EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+52],EAX
          mov EAX,DWORD PTR [L_479ef8]
          add EAX,262143
          shl EAX,14
          cmp EAX,ESI
          jb L_410e90
          mov EAX,EBX
          mov EBP,DWORD PTR [_nFsFiles]
          mov DWORD PTR [ESP+4],EDX
          shr EAX,14
          mov ECX,EAX
          sub AX,WORD PTR [L_479efc]
          sub CX,WORD PTR [L_479efc]
          mov ESI,EBP
          shl ESI,5
          shr CX,8
          shl EAX,8
          add EAX,ECX
          mov ECX,DWORD PTR [ESP+24]
          mov WORD PTR [ESI+L_4c97d6],AX
          mov EAX,ECX
          shr EAX,8
          mov DWORD PTR [ESP+28],EAX
          mov EAX,ECX
          shl ECX,24
          shr EAX,24
          add ECX,EAX
          mov EAX,DWORD PTR [ESP+24]
          shl EAX,8
          and EAX,16711680
          add EAX,ECX
          mov ECX,DWORD PTR [ESP+28]
          and ECX,65280
          add EAX,ECX
          mov DWORD PTR [ESI+L_4c97d8],EAX
          add ESI,OFFSET _fsFiles
          mov DWORD PTR [ESP],ESI
          call _strcpy
          mov EDX,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [EDI]
          test EDX,EDX
          mov DWORD PTR [ESI+28],EAX
          je L_410eb0
          mov EAX,DWORD PTR [L_479ee8]
          cmp DWORD PTR [ESP+52],EAX
          ja L_410ecc
          cmp EBX,EAX
          ja L_410ecc
          mov EAX,EBX
          mov EDX,EBX
          mov EDI,DWORD PTR [ESP+24]
          shr EAX,14
          and EDX,16383
          mov ECX,0
          mov DWORD PTR [ESP+60],EAX
          mov EAX,16384
          sub EAX,EDX
          test EDX,EDX
          cmove EAX,ECX
          cmp EDI,EAX
          ja L_410edd
          add EBX,DWORD PTR [L_479ed8]
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call _memcpy
          test EDI,EDI
          mov DWORD PTR [ESP+56],1
          jne L_410f3d
L_410d06:
          mov EDI,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+60]
          mov EBP,32
          lea EDX,DWORD PTR [EDI+512]
          mov EAX,EDI
          mov ECX,EDI
          shr EAX,9
          shr EDX,9
          and ECX,511
          cmove EDX,EAX
          test ECX,ECX
          mov EBX,EDX
          mov DWORD PTR [ESP+48],EDX
          lea EDX,DWORD PTR [EAX+1]
          cmovne EAX,EDX
          mov EDX,32
          sub EDX,EAX
          mov EAX,ESI
          shl EAX,9
          mov BYTE PTR [ESP+32],DL
          mov DWORD PTR [ESP+40],EAX
          mov EAX,ESI
          add ESI,DWORD PTR [ESP+56]
          cmp EDI,16383
          mov DWORD PTR [ESP+36],EAX
          cmovbe EBP,EBX
          mov DWORD PTR [ESP+44],ESI
L_410d65:
          cmp DWORD PTR [ESP+24],16383
          ja L_410d7b
          mov ESI,DWORD PTR [ESP+48]
          test ESI,ESI
          je L_410e09
L_410d7b:
          mov EAX,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESP+40]
          xor EDX,EDX
          mov ESI,EAX
          mov EDI,EAX
          shr ESI,8
          and ESI,15
          nop
L_410d90:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,ECX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          je L_410f70
          movzx EBX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX],255
          add EDX,1
          add ECX,16
          and EBX,4294967280
          or EBX,ESI
          mov BYTE PTR [EAX+2],BL
          mov EBX,EDI
          mov BYTE PTR [EAX+1],BL
          movzx EBX,BYTE PTR [EAX+12]
          and EBX,4294967232
          or EBX,42
          cmp EBP,EDX
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [L_479ecc]
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [L_479ecd]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [L_479ece]
          mov BYTE PTR [EAX+7],BL
          ja L_410d90
L_410e09:
          add DWORD PTR [ESP+36],1
          add DWORD PTR [ESP+40],512
          mov EAX,DWORD PTR [ESP+36]
          cmp DWORD PTR [ESP+44],EAX
          jne L_410d65
          mov EDI,DWORD PTR [ESP+60]
          mov ECX,DWORD PTR [L_479efc]
          mov ESI,DWORD PTR [ESP+56]
          mov EAX,EDI
          mov EBX,EDI
          sub EAX,ECX
          sub EBX,ECX
          add EAX,1
          add EBX,1
          shl EBX,8
          add ESI,EAX
L_410e45:
          mov EDX,EAX
          shr DX,8
          add EDX,EBX
          add BX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp ESI,EAX
          jne L_410e45
L_410e61:
          mov EAX,DWORD PTR [ESP+44]
          not ECX
          mov EBP,DWORD PTR [_nFsFiles]
          add EAX,ECX
          mov ECX,4294967071
          mov WORD PTR [EAX+EAX*1+_fsTable],CX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [_imgEnd],EAX
          jmp L_410ecc
L_410e87:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410e90:
          mov DWORD PTR [ESP+104],EDX
          mov DWORD PTR [ESP+100],OFFSET _iw_4518a0
          mov DWORD PTR [ESP+96],0
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _log_printf
L_410eb0:
          mov ECX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+32]
          mov EAX,EBX
          mov DWORD PTR [ESP],65535
          call _imgAdd.constprop.3
          mov EBP,DWORD PTR [_nFsFiles]
L_410ecc:
          add EBP,1
          mov DWORD PTR [_nFsFiles],EBP
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_410edd:
          sub EDI,EAX
          mov ECX,EDI
          mov EAX,EDI
          and ECX,16383
          cmp EDI,16384
          mov ESI,ECX
          cmovb ESI,EDI
          shr EAX,14
          test ESI,ESI
          mov DWORD PTR [ESP+56],EAX
          je L_410fc0
          add EAX,1
          test EDX,EDX
          mov DWORD PTR [ESP+56],EAX
          je L_411005
L_410f12:
          mov EAX,DWORD PTR [ESP+24]
          add EBX,DWORD PTR [L_479ed8]
          add DWORD PTR [ESP+56],1
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          test ESI,ESI
          je L_410d06
L_410f3d:
          mov EDI,DWORD PTR [ESP+52]
          mov EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          mov EAX,EDI
          add EDX,EDI
          add EAX,16383
          mov DWORD PTR [ESP],EDX
          and EAX,4294950912
          sub EAX,EDI
          mov DWORD PTR [ESP+8],EAX
          call _memset
          jmp L_410d06
L_410f70:
          movzx EBX,BYTE PTR [EAX+1]
          add EDX,1
          add ECX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+2],1
          and EBX,4294967280
          or EBX,ESI
          mov BYTE PTR [EAX+1],BL
          mov EBX,EDI
          mov BYTE PTR [EAX],BL
          movzx EBX,BYTE PTR [EAX+12]
          and EBX,4294967232
          or EBX,42
          cmp EDX,EBP
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [ESP+32]
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [ESP+28]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [ESP+24]
          mov BYTE PTR [EAX+7],BL
          jb L_410d90
          jmp L_410e09
L_410fc0:
          test EDX,EDX
          jne L_410f12
          mov EAX,DWORD PTR [ESP+24]
          add EBX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+56]
          test EAX,EAX
          jne L_410d06
          mov EAX,DWORD PTR [ESP+60]
          mov ECX,DWORD PTR [L_479efc]
          mov DWORD PTR [ESP+44],EAX
          jmp L_410e61
L_411005:
          mov EAX,DWORD PTR [ESP+24]
          add EBX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          jmp L_410f3d
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _imgAddFileAs
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
#@C _imgAddMobile
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _fixupFsTable
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _fixupEmptyFsBlocks
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
#@C _addSmcConfig
L_411671:
          jmp _writeInitialHeader
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
#@C _writeInitialHeader
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _checkBootImage
#@C _writeFsTable
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
#@C _copyAnchorBlock
#@C _spareUsed
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imageGetBuffer
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
#@C _writeImage
          .byte 0x8d
          .byte 0x76
          .byte 0x0
#@C _finalizeImage
          .byte 0x90
#@C _fsStartBlock
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _reservedAreaOffset
          jmp _statisticsOffset
          .byte 0x90
          .byte 0x90
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
#@C _statisticsOffset
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _manufacturingOffset
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
#@C _imgAddRaw
          .byte 0x90
          .byte 0x90
          .byte 0x90

.data
.p2align 5
_copyright:
          .byte 0xa9
          .byte 0x20
          .byte 0x32
          .byte 0x30
L_44a584:
          .ascii "04-2"
L_44a588:
          .ascii "0"
L_44a589:
          .ascii "0"
L_44a58a:
          .zero 1
          .ascii " "
L_44a58c:
          .ascii "Micr"
L_44a590:
          .ascii "osof"
L_44a594:
          .ascii "t Co"
L_44a598:
          .ascii "rpor"
L_44a59c:
          .ascii "atio"
L_44a5a0:
          .ascii "n. A"
L_44a5a4:
          .ascii "ll r"
L_44a5a8:
          .ascii "ight"
L_44a5ac:
          .ascii "s re"
L_44a5b0:
          .ascii "serv"
L_44a5b4:
          .string "ed."
L_44a5b8:
          .zero 4
L_44a5bc:
          .zero 4

.section .rdata,"dr"
.p2align 2
_iw_451760:
          .string "***** WARNING: cfldv was not set anywhere, setting it to 1\n"
_iw_45179c:
          .string "      please set it in ini or on command line and rebuild!\n"
L_4517d8:
#@J _buildImage 0 8
_iw_4517f8:
          .string "flash header build version set to v.%d\n"
_iw_451820:
          .string "\n***** ERROR: SMC size 0x%x not supported!!!\n\n"
          .zero 1
_iw_451850:
          .string "reset smc load address to 0x%x size 0x%x\n"
          .zero 2
_iw_45187c:
          .string "patch slot offset reset to: 0x%x\n"
          .zero 2
_iw_4518a0:
          .string "\n******* ERROR: adding %s will exceed available flash space! Skipped!\n\n"
_iw_4518e8:
          .string "\tadding as %s at raw offset 0x%x len 0x%08x (end 0x%08x)\n"
          .zero 2
_iw_451924:
          .string "\n******* ERROR: adding Mobile%c.dat will exceed available flash space! Skipped!\n\n"
          .zero 2
_iw_451978:
          .string "\tadding Mobile%c.dat as type 0x%x at raw offset 0x%x len 0x%x (end 0x%x)\n"
          .zero 2
_iw_4519c4:
          .string "adding smc config to offset 0x%08x, len 0x%x\n"
          .zero 2
_iw_4519f4:
          .string "Inserting netKd data from dump into header\n"
_iw_451a20:
          .string "%c%c v%d at 0x%x size 0x%x (CB)\n"
          .zero 3
_iw_451a44:
          .string "%c%c v%d at 0x%x size 0x%x (dual CB)\n"
          .zero 2
_iw_451a6c:
          .string "%c%c v%d at 0x%x size 0x%x (devkit CC)\n"
_iw_451a94:
          .string "%c%c v%d at 0x%x size 0x%x (CD)\n"
          .zero 3
_iw_451ab8:
          .string "%c%c v%d at 0x%x size 0x%x (CE)\n"
          .zero 3
_iw_451adc:
          .string "final truncated bootloader size 0x%x\n"
          .zero 2
_iw_451b04:
          .string "offset 0x%x len 0x4000 (end 0x%x)..."
          .zero 3
_iw_451b2c:
          .string "copying anchor block %d to offset 0x%x\n"
_iw_451b54:
          .string "\n------ writing image to disk ------\n"
_iw_451b7a:
          .string "wb"
_iw_451b7d:
          .string "writing file '%s' to disk..."
_iw_451b9a:
          .string "failed!\n"
          .zero 1
_iw_451ba4:
          .string "\n***** ERROR: was not able to write %d bytes to the file %s!\n"
          .zero 2
_iw_451be4:
          .string "done!\ncreating SHA-1 hash from system area data..."
          .zero 1
_iw_451c18:
          .string "done!\nwriting SHA-1 to file..."
          .zero 1
_iw_451c38:
          .string "done!\nchecking and copying > 64M NAND data from dump file if present and updating SHA-1...\n"
_iw_451c94:
          .string "done!\nchecking and copying > 64M NAND data from dump file if present...\n"
_iw_451cdd:
          .string "done!\n"
_iw_451ce4:
          .string "fixing up big block LBA numbers in spare..."
_iw_451d10:
          .string "fixing up big block controller on small block NAND LBA numbers..."
          .zero 2
_iw_451d54:
          .string "calculating ECD bytes and assembling raw image..."
          .zero 2
_iw_451d88:
          .string "attempting to restore NAND MU data to big block unit from dump..."
_iw_451dca:
          .string "remapping %d blocks\n"
          .zero 1
_iw_451de0:
          .string "    copying 0x%x bytes of LBA 0x%x to block 0x%x..."
_iw_451e14:
          .string "zero fill origin..."
_iw_451e28:
          .string "\n\n***** ERROR: Remapping block 0x%x to block 0x%x is not sane on a NAND with 0x%x blocks!\n"
          .zero 1
_iw_451e84:
          .string "    Remapping block 0x%x is not required, zerofilling..."
          .zero 3
_iw_451ec0:
          .string "\n\n***** ERROR: if you had given the same small/big block style NAND donor image I'd be remapping %d bad blocks now...\n"
_iw_451f37:
          .string "done remapping!\n"
_iw_451f48:
          .string "\n        dest block is empty, fixing up LBA and ECD..."
          .zero 1
_iw_451f80:
          .string "\tadding %s at raw offset 0x%x len 0x%x (end 0x%x)\n"
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _imgAdd.constprop.1 - .
          .byte 0x6c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4d
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
          .byte 0x43
          .byte 0xe
          .byte 0x50
          .byte 0x3
          .byte 0x3f
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
          .byte 0x41
          .byte 0xb
          .byte 0x3
          .byte 0xd9
          .byte 0x1
          .byte 0xe
          .byte 0x4
          .byte 0xc3
          .byte 0xc5
          .byte 0xc6
          .byte 0xc7
          .byte 0x46
          .byte 0xe
          .byte 0x50
          .byte 0x83
          .byte 0x5
          .byte 0x85
          .byte 0x2
          .byte 0x86
          .byte 0x4
          .byte 0x87
          .byte 0x3
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _imgWritePage - .
          .byte 0x22
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
          .byte 0x2c
          .byte 0x3
          .byte 0x8d
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
          .byte 0x48
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _imgAdd.constprop.3 - .
          .byte 0x35
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
          .byte 0x50
          .byte 0x3
          .byte 0xbf
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long _buildImage - .
          .byte 0xd9
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
          .byte 0x3
          .byte 0x44
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
          .byte 0x45
          .byte 0xb
          .byte 0x3
          .byte 0x6e
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
          .byte 0x4a
          .byte 0xb
          .byte 0x3
          .byte 0xe3
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
          .byte 0x44
          .byte 0xb
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _imageFree - .
          .byte 0x4b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x47
          .byte 0xe
          .byte 0x4
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _calcEcd - .
          .byte 0x4f
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x2
          .byte 0x45
          .byte 0xc3
          .byte 0xe
          .byte 0xc
          .byte 0x43
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _calcPageEcc - .
          .byte 0x76
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x2
          .byte 0x6e
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
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long _pageEccOk - .
          .byte 0x8a
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
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x2
          .byte 0x61
          .byte 0xa
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
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _blockEccOk - .
          .byte 0xec
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
          .byte 0x28
          .byte 0x2
          .byte 0xaf
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
          .byte 0x1c
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
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _pageErased - .
          .byte 0x83
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _blockErased - .
          .byte 0x35
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _blockPagesErased - .
          .byte 0xb7
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x76
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x2
          .byte 0x76
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xac
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _blockIsFF - .
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _isErased - .
          .byte 0x36
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long _setBlockSpare - .
          .byte 0x6e
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
          .byte 0x1c
          .byte 0x3
          .byte 0x1c
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _imgSizeAligned - .
          .byte 0x1b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _setFlashBuild - .
          .byte 0x42
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x7e
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _smcSetLoad - .
          .byte 0xb3
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
          .byte 0x7b
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
          .byte 0x4a
          .byte 0xb
          .byte 0x5d
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
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _imgSmcOffset - .
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _setPatchSlot - .
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
          .byte 0x8d
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
          .byte 0x48
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _imgCfOffset - .
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe8
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long _imgCfSize - .
          .byte 0x39
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x46
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x72
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgSize - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x18
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgSetSize - .
          .byte 0xa
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgBigBlock - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x40
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgAdd - .
          .byte 0x86
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
          .byte 0x90
          .byte 0x1
          .byte 0x3
          .byte 0xf2
          .byte 0x3
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
          .byte 0x43
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgFits - .
          .byte 0x1e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x98
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgAddFile - .
          .byte 0x78
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
          .byte 0x60
          .byte 0x3
          .byte 0xf0
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
          .byte 0x45
          .byte 0xb
          .byte 0x68
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
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf0
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long _imgAddFileAs - .
          .byte 0x74
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
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _imgAddMobile - .
          .byte 0xfa
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
          .byte 0xf9
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
          .byte 0x5a
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
          .byte 0x45
          .byte 0xb
          .byte 0x18
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x88
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _fixupFsTable - .
          .byte 0x3d
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x83
          .byte 0x2
          .byte 0x7b
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _fixupEmptyFsBlocks - .
          .byte 0x3
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
          .byte 0x1c
          .byte 0x3
          .byte 0x5e
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
          .byte 0x47
          .byte 0xb
          .byte 0x70
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
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x5
          .byte 0x0
          .byte 0x0
          .long _addSmcConfig - .
          .byte 0x71
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x87
          .byte 0x2
          .byte 0x46
          .byte 0xe
          .byte 0xc
          .byte 0x86
          .byte 0x3
          .byte 0x4f
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x4f
          .byte 0xe
          .byte 0xc
          .byte 0x46
          .byte 0xc6
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc7
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _writeInitialHeader - .
          .byte 0x79
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
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0xce
          .byte 0xa
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0x73
          .byte 0xa
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
          .byte 0x60
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
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _checkBootImage - .
          .byte 0xd0
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
          .byte 0x40
          .byte 0x3
          .byte 0x7b
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
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x86
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x48
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
          .byte 0xa7
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
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xdc
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .long _writeFsTable - .
          .byte 0x3b
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
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x3
          .byte 0x60
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
          .byte 0x45
          .byte 0xb
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _copyAnchorBlock - .
          .byte 0xa0
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
          .byte 0x46
          .byte 0xe
          .byte 0x10
          .byte 0x83
          .byte 0x4
          .byte 0x4d
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x87
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _spareUsed - .
          .byte 0x76
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x64
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _imageGetBuffer - .
          .byte 0x29
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
          .byte 0x78
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _writeImage - .
          .byte 0x3d
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
          .byte 0x46
          .byte 0xe
          .byte 0xb0
          .byte 0x1
          .byte 0x2
          .byte 0xb2
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
          .byte 0xa8
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
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc4
          .byte 0x7
          .byte 0x0
          .byte 0x0
          .long _finalizeImage - .
          .byte 0x2f
          .byte 0x8
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
          .byte 0x43
          .byte 0xe
          .byte 0x60
          .byte 0x55
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
          .byte 0x48
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
          .byte 0x2
          .byte 0xbb
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _fsStartBlock - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x48
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _reservedAreaOffset - .
          .byte 0xa1
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
          .byte 0x74
          .byte 0xa
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x49
          .byte 0xb
          .byte 0x68
          .byte 0xa
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
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _statisticsOffset - .
          .byte 0xc6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _manufacturingOffset - .
          .byte 0xc6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa4
          .byte 0x8
          .byte 0x0
          .byte 0x0
          .long _imgAddRaw - .
          .byte 0x5d
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
          .byte 0x4d
          .byte 0xe
          .byte 0xc
          .byte 0x45
          .byte 0xc3
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc6
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0

.bss
.p2align 5
_mobileOffset:
          .zero 4
_nFsFiles:
          .zero 28
_smcPage:
          .zero 1568
L_470000:
          .zero 110
L_47006e:
          .zero 2418
