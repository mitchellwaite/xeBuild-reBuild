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
.globl _finalizeImage
.globl _imgAdd
.globl _imgAddFile
.globl _imgWriteStart
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
.globl _iw_451f80
.globl _mobileOffset
.globl _nFsFiles
.globl _smcPage
.globl _writeFsTable

.text
.p2align 4
_imgWriteStart:
          cmp DWORD PTR [L_479ee8],EDX
          jb L_40ec84
          push EBP
          push EDI
          mov EDI,EDX
          push ESI
          push EBX
          sub ESP,60
          test EDX,EDX
          mov DWORD PTR [ESP+36],ECX
          mov DWORD PTR [ESP+32],EDX
          je L_40eaab
          cmp EDX,16383
          jbe L_40ec26
          shr EDI,14
          mov DWORD PTR [ESP+28],EDI
          mov EDI,EDX
          and EDI,16383
          jne L_40ec22
L_40e996:
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
L_40e9af:
          mov ESI,512
          xor EBP,EBP
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40e9c0:
          mov EBX,EBP
          mov EDX,EBP
          mov EDI,EBP
          shr EBX,8
          shl EDX,9
          and EBX,15
          nop
L_40e9d0:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ECX,DWORD PTR [L_479ef0]
          test ECX,ECX
          je L_40eac0
          movzx ECX,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+2],CL
          mov ECX,EDI
          mov BYTE PTR [EAX+1],CL
          jne L_40e9d0
          add EBP,1
          add ESI,512
          cmp EBP,DWORD PTR [ESP+28]
          jne L_40e9c0
L_40ea2a:
          mov EAX,DWORD PTR [ESP+36]
          cmp AX,61937
          je L_40ea98
          mov EDI,EAX
          sub EAX,1
          mov EBX,DWORD PTR [L_479efc]
          rol DI,8
          cmp AX,-3
          jbe L_40eaf7
          mov EDI,DWORD PTR [ESP+28]
          mov EAX,1
          mov ECX,EBX
          sub EAX,EBX
          neg ECX
          shl ECX,8
          lea ESI,DWORD PTR [EAX+EDI*1]
          add CX,256
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_40ea70:
          mov EDX,EAX
          shr DX,8
          add EDX,ECX
          add CX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp EAX,ESI
          jne L_40ea70
L_40ea8c:
          cmp WORD PTR [ESP+36],-1
          je L_40ec08
L_40ea98:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [_imgEnd],EAX
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_40eaab:
          mov DWORD PTR [ESP+28],1
          jmp L_40e996
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_40eac0:
          movzx ECX,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          and ECX,4294967280
          or ECX,EBX
          cmp EDX,ESI
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDI
          mov BYTE PTR [EAX],CL
          jne L_40e9d0
          add EBP,1
          add ESI,512
          cmp EBP,DWORD PTR [ESP+28]
          jne L_40e9c0
          jmp L_40ea2a
L_40eaf7:
          mov EAX,EBX
          neg EAX
          lea EAX,DWORD PTR [EAX+EAX*1+_fsTable]
          shr EAX,1
          and EAX,1
          cmp EBP,6
          mov ESI,EAX
          ja L_40ec75
          mov ESI,EBP
L_40eb14:
          mov EAX,EBX
          neg EAX
          cmp ESI,1
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
          je L_40ec94
          mov EAX,1
          sub EAX,EBX
          cmp ESI,2
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
          je L_40ec9e
          mov EAX,2
          sub EAX,EBX
          cmp ESI,3
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
          je L_40eca8
          mov EAX,3
          sub EAX,EBX
          cmp ESI,4
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
          je L_40ecb2
          mov EAX,4
          sub EAX,EBX
          cmp ESI,5
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
          je L_40ec8a
          mov EAX,5
          mov ECX,6
          sub EAX,EBX
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
L_40eb9d:
          cmp EBP,ESI
          je L_40ea8c
L_40eba5:
          sub EBP,ESI
          lea EDX,DWORD PTR [EBP-2]
          mov DWORD PTR [ESP+44],EBP
          shr EDX,1
          add EDX,1
          cmp EBP,1
          lea EAX,DWORD PTR [EDX+EDX*1]
          mov DWORD PTR [ESP+40],EAX
          je L_40ebf0
          mov EAX,EDI
          movzx EBP,DI
          shl EAX,16
          or EBP,EAX
          mov EAX,ESI
          sub EAX,EBX
          lea ESI,DWORD PTR [EAX+EAX*1+_fsTable]
          xor EAX,EAX
L_40ebd6:
          mov DWORD PTR [ESI+EAX*4],EBP
          add EAX,1
          cmp EDX,EAX
          ja L_40ebd6
          mov EAX,DWORD PTR [ESP+40]
          add ECX,EAX
          cmp EAX,DWORD PTR [ESP+44]
          je L_40ea8c
L_40ebf0:
          mov EAX,ECX
          sub EAX,EBX
          cmp WORD PTR [ESP+36],-1
          mov WORD PTR [EAX+EAX*1+_fsTable],DI
          jne L_40ea98
L_40ec08:
          mov EAX,EBX
          mov EDX,4294967071
          not EAX
          add EAX,DWORD PTR [ESP+28]
          mov WORD PTR [EAX+EAX*1+_fsTable],DX
          jmp L_40ea98
L_40ec22:
          mov EDI,DWORD PTR [ESP+32]
L_40ec26:
          mov DWORD PTR [ESP+4],EAX
          mov EDX,EDI
          mov EAX,DWORD PTR [L_479ed8]
          shr EDX,14
          mov DWORD PTR [ESP+8],EDI
          lea ESI,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+28],ESI
          call _memcpy
          mov EDX,EDI
          lea EAX,DWORD PTR [EDI+16383]
          add EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          and EAX,4294950912
          sub EAX,EDI
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],EDX
          call _memset
          jmp L_40e9af
L_40ec75:
          test EAX,EAX
          jne L_40eb14
          xor ECX,ECX
          jmp L_40eba5
L_40ec84:
          mov EAX,4294967295
          ret 
L_40ec8a:
          mov ECX,5
          jmp L_40eb9d
L_40ec94:
          mov ECX,1
          jmp L_40eb9d
L_40ec9e:
          mov ECX,2
          jmp L_40eb9d
L_40eca8:
          mov ECX,3
          jmp L_40eb9d
L_40ecb2:
          mov ECX,4
          jmp L_40eb9d
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
#@C _imgAdd.constprop.2
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
_imgAdd:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,124
          mov EAX,DWORD PTR [ESP+160]
          mov ESI,DWORD PTR [ESP+156]
          mov EDI,DWORD PTR [ESP+144]
          mov DWORD PTR [ESP+104],EAX
          mov EAX,ESI
          mov BYTE PTR [ESP+24],AL
          mov EAX,DWORD PTR [L_479ee8]
          cmp EAX,EDI
          jb L_410b29
          mov ECX,DWORD PTR [ESP+152]
          add ECX,EDI
          cmp EAX,ECX
          mov DWORD PTR [ESP+108],ECX
          jb L_410b29
          mov EAX,EDI
          mov EDX,0
          and EAX,16383
          mov ECX,EAX
          mov DWORD PTR [ESP+88],EAX
          mov EAX,EDI
          shr EAX,14
          mov DWORD PTR [ESP+96],EAX
          mov EAX,16384
          sub EAX,ECX
          test ECX,ECX
          cmove EAX,EDX
          cmp EAX,DWORD PTR [ESP+152]
          jae L_4105e2
          mov ECX,DWORD PTR [ESP+152]
          sub ECX,EAX
          cmp ECX,16383
          mov EAX,ECX
          jbe L_410a33
          shr ECX,14
          test EAX,16383
          mov DWORD PTR [ESP+100],ECX
          jne L_410a3b
          mov EAX,DWORD PTR [ESP+88]
          test EAX,EAX
          je L_410a9c
          add DWORD PTR [ESP+100],1
          xor EBX,EBX
L_4105b4:
          mov ECX,DWORD PTR [ESP+152]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],ECX
          add EAX,EDI
          mov ECX,DWORD PTR [ESP+148]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          test BL,BL
          je L_410628
          jmp L_410a69
L_4105e2:
          mov ECX,DWORD PTR [ESP+152]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+148]
          add EAX,EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          cmp DWORD PTR [ESP+164],1
          jne L_410620
          mov EAX,DWORD PTR [ESP+152]
          test EAX,EAX
          jne L_410a61
L_410620:
          mov DWORD PTR [ESP+100],1
L_410628:
          mov EAX,ESI
          lea ECX,DWORD PTR [ESI-49]
          test AL,AL
          setne DL
          cmp AL,48
          mov BYTE PTR [ESP+82],CL
          setne AL
          mov ECX,DWORD PTR [ESP+152]
          and EDX,EAX
          cmp DWORD PTR [ESP+152],16383
          mov EAX,DWORD PTR [ESP+152]
          mov EBP,EDX
          lea EDX,DWORD PTR [ECX+512]
          mov EBX,ECX
          setbe BYTE PTR [ESP+28]
          shr EAX,9
          shr EDX,9
          lea ECX,DWORD PTR [EAX+1]
          and EBX,511
          cmove EDX,EAX
          test EBX,EBX
          mov EBX,DWORD PTR [ESP+152]
          cmove ECX,EAX
          mov EAX,32
          and EDI,131071
          sub EAX,ECX
          mov DWORD PTR [ESP+92],EDI
          mov BYTE PTR [ESP+71],AL
          lea EAX,DWORD PTR [ESI-42]
          shr EBX,8
          mov DWORD PTR [ESP+32],EBX
          and EAX,4294967293
          mov BYTE PTR [ESP+70],AL
          lea EAX,DWORD PTR [ECX+4]
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+96]
          and EBX,4294967292
          mov ESI,EAX
          shl ESI,5
          mov DWORD PTR [ESP+72],ESI
          mov ESI,DWORD PTR [ESP+100]
          add ESI,EAX
          mov EAX,EBP
          and AL,BYTE PTR [ESP+28]
          mov DWORD PTR [ESP+76],ESI
          mov ESI,DWORD PTR [ESP+96]
          mov BYTE PTR [ESP+83],AL
          mov EAX,32
          mov DWORD PTR [ESP+64],ESI
          cmovne EAX,EDX
          mov EDX,EDI
          mov DWORD PTR [ESP+84],EAX
          mov EAX,256
          shr EDX,9
          mov EBP,EAX
          sub EBP,EDX
          test EDI,EDI
          mov EDX,EBP
          cmove EDX,EAX
          movzx EAX,BYTE PTR [ESP+24]
          test CL,3
          cmove EBX,ECX
          sub EDX,EBX
          shr EDX,2
          and EAX,63
          mov DWORD PTR [ESP+48],EDX
          mov BYTE PTR [ESP+28],AL
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410720:
          cmp BYTE PTR [ESP+83],0
          je L_410940
          xor EDX,EDX
          cmp BYTE PTR [ESP+82],14
          ja L_41074f
L_410734:
          mov ESI,DWORD PTR [L_479ef0]
          mov EDX,DWORD PTR [ESP+88]
          test ESI,ESI
          cmovne EDX,DWORD PTR [ESP+92]
          mov EAX,EDX
          shr EAX,9
          test EDX,EDX
          cmovne EDX,EAX
L_41074f:
          mov EAX,DWORD PTR [ESP+84]
          lea EDI,DWORD PTR [EDX+EAX*1]
          cmp EDX,EDI
          jae L_41086e
L_41075e:
          mov EAX,DWORD PTR [ESP+64]
          mov ESI,EAX
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+72]
          shr ESI,8
          and ESI,15
          lea ECX,DWORD PTR [EAX+EDX*1]
          shl ECX,4
          jmp L_4107e1
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_410780:
          movzx EBX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX],255
          and EBX,4294967280
          or EBX,ESI
          cmp BYTE PTR [ESP+24],1
          mov BYTE PTR [EAX+2],BL
          mov EBX,EBP
          mov BYTE PTR [EAX+1],BL
          jbe L_4107d3
          movzx EBX,BYTE PTR [EAX+12]
          and EBX,4294967232
          or BL,BYTE PTR [ESP+28]
          cmp BYTE PTR [ESP+70],0
          mov BYTE PTR [EAX+12],BL
          je L_410900
          movzx EBX,BYTE PTR [ESP+48]
          mov BYTE PTR [EAX+5],1
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [ESP+32]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [ESP+152]
          mov BYTE PTR [EAX+7],BL
L_4107d3:
          add EDX,1
          add ECX,16
          cmp EDX,EDI
          jae L_41086e
L_4107e1:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,ECX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          jne L_410780
          movzx EBX,BYTE PTR [EAX+1]
          mov BYTE PTR [EAX+5],255
          and EBX,4294967280
          or EBX,ESI
          cmp BYTE PTR [ESP+24],1
          mov BYTE PTR [EAX+1],BL
          mov EBX,EBP
          mov BYTE PTR [EAX],BL
          jbe L_4107d3
          movzx EBX,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+2],1
          and EBX,4294967232
          or BL,BYTE PTR [ESP+28]
          cmp BYTE PTR [ESP+24],48
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [ESP+71]
          mov BYTE PTR [EAX+9],BL
          je L_4107d3
          movzx EBX,BYTE PTR [ESP+32]
          add EDX,1
          add ECX,16
          cmp EDX,EDI
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [ESP+152]
          mov BYTE PTR [EAX+7],BL
          jb L_4107e1
L_41086e:
          add DWORD PTR [ESP+64],1
          add DWORD PTR [ESP+72],32
          mov EAX,DWORD PTR [ESP+64]
          cmp DWORD PTR [ESP+76],EAX
          jne L_410720
          mov EDI,DWORD PTR [ESP+104]
          cmp DI,61937
          je L_4108eb
          mov ECX,DWORD PTR [ESP+96]
          mov EBP,DWORD PTR [L_479efc]
          lea EDX,DWORD PTR [EDI-1]
          mov ESI,EDI
          rol SI,8
          mov EAX,ECX
          sub EAX,EBP
          cmp DX,-3
          jbe L_410957
          mov EBX,DWORD PTR [ESP+100]
          sub ECX,EBP
          add EAX,1
          add ECX,1
          shl ECX,8
          add EBX,EAX
L_4108c3:
          mov EDX,EAX
          shr DX,8
          add EDX,ECX
          add CX,256
          mov WORD PTR [EAX+EAX*1+L_4cb7be],DX
          add EAX,1
          cmp EBX,EAX
          jne L_4108c3
L_4108df:
          cmp WORD PTR [ESP+104],-1
          je L_410a19
L_4108eb:
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [_imgEnd],EAX
          xor EAX,EAX
L_4108f6:
          add ESP,124
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_410900:
          cmp BYTE PTR [ESP+24],44
          je L_410930
L_410907:
          movzx EBX,BYTE PTR [L_479ecc]
          mov BYTE PTR [EAX+9],BL
          movzx EBX,BYTE PTR [L_479ecd]
          mov BYTE PTR [EAX+8],BL
          movzx EBX,BYTE PTR [L_479ece]
          mov BYTE PTR [EAX+7],BL
          jmp L_4107d3
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_410930:
          mov BYTE PTR [EAX+5],1
          jmp L_410907
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_410940:
          cmp BYTE PTR [ESP+82],14
          jbe L_410734
          mov EDI,32
          xor EDX,EDX
          jmp L_41075e
L_410957:
          lea EDX,DWORD PTR [EAX+EAX*1+_fsTable]
          shr EDX,1
          and EDX,1
          cmp DWORD PTR [ESP+100],6
          ja L_410ac6
          mov EDI,DWORD PTR [ESP+100]
          mov WORD PTR [EAX+EAX*1+_fsTable],SI
          cmp EDI,1
          je L_410b4a
          cmp EDI,2
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],SI
          je L_410b59
          cmp EDI,3
          mov WORD PTR [EAX+EAX*1+L_4cb7c4],SI
          je L_410b68
          cmp EDI,4
          mov WORD PTR [EAX+EAX*1+L_4cb7c6],SI
          je L_410b77
          cmp EDI,5
          mov WORD PTR [EAX+EAX*1+L_4cb7c8],SI
          je L_410b33
          mov EBX,EDI
          mov WORD PTR [EAX+EAX*1+L_4cb7ca],SI
          mov EDI,6
L_4109d6:
          mov ECX,DWORD PTR [ESP+100]
          cmp ECX,EBX
          je L_4108df
          sub ECX,EBX
          lea EDX,DWORD PTR [ECX-2]
          mov DWORD PTR [ESP+32],ECX
          shr EDX,1
          add EDX,1
          mov DWORD PTR [ESP+28],EDX
          add EDX,EDX
          cmp ECX,1
          mov DWORD PTR [ESP+24],EDX
          jne L_410ae8
L_410a03:
          add EAX,EDI
          cmp WORD PTR [ESP+104],-1
          mov WORD PTR [EAX+EAX*1+_fsTable],SI
          jne L_4108eb
L_410a19:
          mov EAX,EBP
          mov EDX,4294967071
          not EAX
          add EAX,DWORD PTR [ESP+76]
          mov WORD PTR [EAX+EAX*1+_fsTable],DX
          jmp L_4108eb
L_410a33:
          mov DWORD PTR [ESP+100],0
L_410a3b:
          add DWORD PTR [ESP+100],1
          cmp DWORD PTR [ESP+164],1
          mov EBP,DWORD PTR [ESP+88]
          sete BL
          test EBP,EBP
          je L_4105b4
          add DWORD PTR [ESP+100],1
          jmp L_4105b4
L_410a61:
          mov DWORD PTR [ESP+100],1
L_410a69:
          mov ECX,DWORD PTR [ESP+108]
          mov EDX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+4],0
          mov EAX,ECX
          add EDX,ECX
          add EAX,16383
          mov DWORD PTR [ESP],EDX
          and EAX,4294950912
          sub EAX,ECX
          mov DWORD PTR [ESP+8],EAX
          call _memset
          jmp L_410628
L_410a9c:
          mov ECX,DWORD PTR [ESP+152]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+148]
          add EAX,EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          jmp L_410628
L_410ac6:
          test EDX,EDX
          jne L_410b42
          mov EDI,DWORD PTR [ESP+100]
          xor EBX,EBX
          lea EDX,DWORD PTR [EDI-2]
          mov DWORD PTR [ESP+32],EDI
          xor EDI,EDI
          shr EDX,1
          lea ECX,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP+28],ECX
          add ECX,ECX
          mov DWORD PTR [ESP+24],ECX
L_410ae8:
          mov EDX,ESI
          movzx ECX,SI
          mov DWORD PTR [ESP+64],EAX
          shl EDX,16
          or ECX,EDX
          lea EDX,DWORD PTR [EAX+EBX*1]
          mov EAX,DWORD PTR [ESP+28]
          lea EBX,DWORD PTR [EDX+EDX*1+_fsTable]
          xor EDX,EDX
L_410b06:
          mov DWORD PTR [EBX+EDX*4],ECX
          add EDX,1
          cmp EDX,EAX
          jb L_410b06
          mov ECX,DWORD PTR [ESP+24]
          mov EAX,DWORD PTR [ESP+64]
          add EDI,ECX
          cmp ECX,DWORD PTR [ESP+32]
          jne L_410a03
          jmp L_4108df
L_410b29:
          mov EAX,4294967295
          jmp L_4108f6
L_410b33:
          mov EBX,5
          mov EDI,5
          jmp L_4109d6
L_410b42:
          mov WORD PTR [EAX+EAX*1+_fsTable],SI
L_410b4a:
          mov EBX,1
          mov EDI,1
          jmp L_4109d6
L_410b59:
          mov EBX,2
          mov EDI,2
          jmp L_4109d6
L_410b68:
          mov EBX,3
          mov EDI,3
          jmp L_4109d6
L_410b77:
          mov EBX,4
          mov EDI,4
          jmp L_4109d6
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
          call _imgAdd.constprop.2
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
_writeFsTable:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EDI,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [ESP+96]
          mov ESI,EAX
          mov DWORD PTR [ESP+28],EAX
          shr ESI,14
          test EDI,EDI
          mov DWORD PTR [ESP+48],ESI
          je L_411bfd
          test EAX,131071
          jne L_411eef
L_411bfd:
          mov EAX,DWORD PTR [ESP+48]
          sub EAX,DWORD PTR [L_479efc]
          mov ESI,4294966559
          mov DWORD PTR [ESP],16384
          mov EBX,OFFSET _fsTable
          mov EBP,OFFSET _fsFiles
          mov WORD PTR [EAX+EAX*1+_fsTable],SI
          call _malloc
          mov DWORD PTR [ESP+52],EAX
          .byte 0x66   # nop
          nop
L_411c30:
          mov ESI,EBX
          lea EDX,DWORD PTR [EAX+512]
          add EBX,512
          mov EDI,EAX
          mov ECX,128
          add EAX,1024
          rep movsd 
          mov ESI,EBP
          add EBP,512
          cmp EBX,OFFSET _hdrTemplate
          mov ECX,128
          mov EDI,EDX
          rep movsd 
          jne L_411c30
          mov ESI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],OFFSET L_451b04
          mov DWORD PTR [ESP],1
          mov EAX,ESI
          mov DWORD PTR [ESP+8],ESI
          add EAX,16384
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+56],EAX
          call _log_printf
          mov EBX,DWORD PTR [L_479ef0]
          mov EAX,DWORD PTR [L_479ee8]
          mov ESI,DWORD PTR [ESP+28]
          test EBX,EBX
          jne L_411f60
          cmp ESI,EAX
          ja L_411e03
          cmp DWORD PTR [ESP+56],EAX
          ja L_411e03
          mov EAX,ESI
          mov EDX,ESI
          and EAX,16383
          shr EDX,14
          test EAX,EAX
          mov DWORD PTR [ESP+60],EDX
          mov EAX,ESI
          je L_4120e0
          add EAX,DWORD PTR [L_479ed8]
          mov ESI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+40],2
L_411cf9:
          mov EAX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+32],0
          and EAX,131071
          mov EDX,EAX
          mov DWORD PTR [ESP+44],EAX
          mov EAX,224
          shr EDX,9
          sub EAX,EDX
          mov EDX,ESI
          shr EAX,2
          shl EDX,9
          mov DWORD PTR [ESP+36],EAX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_411d30:
          mov EAX,DWORD PTR [ESP+44]
          mov EBP,ESI
          mov EBX,ESI
          shr EBP,8
          lea ECX,DWORD PTR [EDX+512]
          mov BYTE PTR [ESP+28],BL
          and EBP,15
          test EAX,EAX
          jne L_411e7b
L_411d50:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EDI,DWORD PTR [L_479ef0]
          test EDI,EDI
          jne L_411f10
          movzx EDI,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+9],0
          mov BYTE PTR [EAX+2],1
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+1],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          jne L_411d50
L_411db7:
          add DWORD PTR [ESP+32],1
          add ESI,1
          mov EDX,ECX
          mov EAX,DWORD PTR [ESP+32]
          cmp DWORD PTR [ESP+40],EAX
          ja L_411d30
          mov EAX,DWORD PTR [ESP+60]
          sub EAX,DWORD PTR [L_479efc]
          mov ECX,4294966559
          cmp DWORD PTR [ESP+40],2
          mov WORD PTR [EAX+EAX*1+_fsTable],CX
          jne L_411dfa
          mov EDX,4294966559
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],DX
L_411dfa:
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [_imgEnd],EAX
L_411e03:
          movzx EAX,WORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],OFFSET L_4c9180
          mov DWORD PTR [ESP],EAX
          call _setBeU16
          mov DWORD PTR [ESP+4],OFFSET L_4c9182
          mov DWORD PTR [ESP],0
          call _setBeU16
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+96],EAX
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
L_411e40:
          movzx EDI,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+9],0
          mov BYTE PTR [EAX+2],1
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+1],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          je L_411db7
L_411e7b:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov EBX,DWORD PTR [L_479ef0]
          test EBX,EBX
          je L_411e40
          movzx EDI,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          mov BYTE PTR [EAX+5],1
          mov BYTE PTR [EAX+8],64
          mov BYTE PTR [EAX+7],0
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+2],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX+1],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          movzx EBX,BYTE PTR [ESP+36]
          mov BYTE PTR [EAX+9],BL
          jne L_411e7b
          jmp L_411db7
L_411eef:
          add EAX,131072
          and EAX,4294836224
          mov DWORD PTR [ESP+28],EAX
          shr EAX,14
          mov DWORD PTR [ESP+48],EAX
          jmp L_411bfd
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_411f10:
          movzx EDI,BYTE PTR [EAX+2]
          add EDX,16
          mov BYTE PTR [EAX],255
          mov BYTE PTR [EAX+9],56
          mov BYTE PTR [EAX+5],1
          mov BYTE PTR [EAX+8],64
          mov BYTE PTR [EAX+7],0
          and EDI,4294967280
          or EDI,EBP
          mov EBX,EDI
          movzx EDI,BYTE PTR [EAX+12]
          mov BYTE PTR [EAX+2],BL
          movzx EBX,BYTE PTR [ESP+28]
          and EDI,4294967232
          or EDI,48
          mov BYTE PTR [EAX+1],BL
          cmp EDX,ECX
          mov EBX,EDI
          mov BYTE PTR [EAX+12],BL
          jne L_411d50
          jmp L_411db7
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_411f60:
          cmp ESI,EAX
          ja L_411e03
          cmp DWORD PTR [ESP+56],EAX
          ja L_411e03
          mov EAX,ESI
          mov EDX,ESI
          shr ESI,14
          and EAX,16383
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+32],ESI
          test EAX,EAX
          mov EBP,ESI
          setne AL
          movzx EAX,AL
          add EAX,1
          mov EBX,EAX
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [L_479ed8]
          add EAX,EDX
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call _memcpy
          mov EDX,ESI
          add ESI,EBX
          shl EDX,9
          mov DWORD PTR [ESP+28],ESI
          nop
L_411fc0:
          mov EBX,EBP
          lea ESI,DWORD PTR [EDX+512]
          mov EDI,EBP
          shr EBX,8
          and EBX,15
L_411fd0:
          mov EAX,DWORD PTR [L_479ed0]
          add EAX,EDX
          mov DWORD PTR [EAX],0
          mov DWORD PTR [EAX+4],0
          mov DWORD PTR [EAX+8],0
          mov DWORD PTR [EAX+12],0
          mov ECX,DWORD PTR [L_479ef0]
          test ECX,ECX
          je L_412090
          movzx ECX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX],255
          add EDX,16
          mov BYTE PTR [EAX+5],1
          and ECX,4294967280
          or ECX,EBX
          mov BYTE PTR [EAX+2],CL
          mov ECX,EDI
          mov BYTE PTR [EAX+1],CL
          movzx ECX,BYTE PTR [EAX+12]
          and ECX,4294967232
          or ECX,44
          cmp ESI,EDX
          mov BYTE PTR [EAX+12],CL
          movzx ECX,BYTE PTR [L_479ecc]
          mov BYTE PTR [EAX+9],CL
          movzx ECX,BYTE PTR [L_479ecd]
          mov BYTE PTR [EAX+8],CL
          movzx ECX,BYTE PTR [L_479ece]
          mov BYTE PTR [EAX+7],CL
          jne L_411fd0
          add EBP,1
          cmp DWORD PTR [ESP+28],EBP
          mov EDX,ESI
          jne L_411fc0
L_412059:
          mov EAX,DWORD PTR [ESP+32]
          sub EAX,DWORD PTR [L_479efc]
          mov ECX,4294966815
          cmp DWORD PTR [ESP+36],2
          mov WORD PTR [EAX+EAX*1+_fsTable],CX
          jne L_411dfa
          mov EDX,4294966815
          mov WORD PTR [EAX+EAX*1+L_4cb7c2],DX
          jmp L_411dfa
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_412090:
          movzx ECX,BYTE PTR [EAX+1]
          add EDX,16
          mov BYTE PTR [EAX+5],255
          mov BYTE PTR [EAX+9],0
          mov BYTE PTR [EAX+2],1
          mov BYTE PTR [EAX+8],64
          mov BYTE PTR [EAX+7],0
          and ECX,4294967280
          or ECX,EBX
          mov BYTE PTR [EAX+1],CL
          mov ECX,EDI
          mov BYTE PTR [EAX],CL
          movzx ECX,BYTE PTR [EAX+12]
          and ECX,4294967232
          or ECX,44
          cmp ESI,EDX
          mov BYTE PTR [EAX+12],CL
          jne L_411fd0
          add EBP,1
          cmp DWORD PTR [ESP+28],EBP
          mov EDX,ESI
          jne L_411fc0
          jmp L_412059
L_4120e0:
          add EAX,DWORD PTR [L_479ed8]
          mov ESI,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov DWORD PTR [ESP+40],1
          jmp L_411cf9
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
_finalizeImage:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,76
          mov EBX,DWORD PTR [L_479ea4]
          and EBX,268435456
          mov DWORD PTR [ESP+60],EBX
          je L_4125c3
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4125c3:
          mov EAX,DWORD PTR [L_479ee8]
          mov DWORD PTR [ESP],EAX
          call _malloc
          test EAX,EAX
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [L_479ee0],EAX
          je L_4128ca
          mov EDI,DWORD PTR [L_479ef0]
          test EDI,EDI
          jne L_412d46
          mov ESI,DWORD PTR [L_479ef4]
          test ESI,ESI
          jne L_412be3
L_4125fd:
          mov DWORD PTR [ESP+4],OFFSET L_451d54
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EBX,DWORD PTR [L_479ee4]
          test EBX,EBX
          je L_412785
          mov EBX,DWORD PTR [ESP+40]
          mov EBP,DWORD PTR [L_479ed0]
          mov EAX,DWORD PTR [L_479ed8]
          mov DWORD PTR [ESP+56],0
          mov ESI,EBX
L_412638:
          mov EDX,DWORD PTR [ESP+56]
          mov EBX,EDX
          shl EBX,9
          mov DWORD PTR [ESP+44],EBX
          mov EBX,EDX
          lea EDX,DWORD PTR [ESI+16896]
          shl EBX,14
          mov DWORD PTR [ESP+40],EBX
          mov DWORD PTR [ESP+52],EDX
          mov EBX,ESI
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_412660:
          mov EDX,DWORD PTR [ESP+44]
          mov ESI,DWORD PTR [ESP+40]
          xor ECX,ECX
          add EDX,EBP
          add ESI,EAX
          jmp L_41267f
L_412670:
          add ECX,1
          cmp ECX,512
          je L_412812
L_41267f:
          cmp BYTE PTR [ESI+ECX*1],255
          je L_412670
L_412685:
          movzx EAX,BYTE PTR [EDX+12]
          mov BYTE PTR [ESP+48],AL
L_41268d:
          xor EAX,EAX
          xor EDI,EDI
          xor ECX,ECX
          mov EBP,EAX
L_412695:
          test CL,31
          jne L_4126ac
          mov EAX,ESI
          cmp ECX,4096
          cmove EAX,EDX
          mov EDI,DWORD PTR [EAX]
          lea ESI,DWORD PTR [EAX+4]
          not EDI
L_4126ac:
          mov EAX,EDI
          shr EDI,1
          and EAX,1
          xor EAX,EBP
          mov EBP,EAX
          xor EBP,110445913
          test AL,1
          cmovne EAX,EBP
          add ECX,1
          shr EAX,1
          cmp ECX,4198
          mov EBP,EAX
          jne L_412695
          movzx ECX,BYTE PTR [ESP+48]
          not EAX
          mov ESI,EAX
          shl ESI,6
          and ECX,63
          add ECX,ESI
          mov BYTE PTR [EDX+12],CL
          mov ECX,EAX
          shr ECX,2
          mov BYTE PTR [EDX+13],CL
          mov ECX,EAX
          shr EAX,18
          shr ECX,10
          mov BYTE PTR [EDX+15],AL
          mov BYTE PTR [EDX+14],CL
          mov EDX,DWORD PTR [ESP+40]
          mov EAX,DWORD PTR [L_479ed8]
          mov EBP,DWORD PTR [L_479ed0]
          lea ESI,DWORD PTR [EAX+EDX*1]
          mov EDX,DWORD PTR [ESP+44]
          add EDX,EBP
L_412713:
          mov ECX,DWORD PTR [ESI]
          lea EDI,DWORD PTR [EBX+4]
          and EDI,4294967292
          mov DWORD PTR [EBX],ECX
          mov ECX,DWORD PTR [ESI+508]
          mov DWORD PTR [EBX+508],ECX
          mov ECX,EBX
          add EBX,528
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          rep movsd 
          mov EDI,DWORD PTR [EDX]
          mov ESI,DWORD PTR [EDX+4]
          mov ECX,DWORD PTR [EDX+8]
          mov EDX,DWORD PTR [EDX+12]
          add DWORD PTR [ESP+44],16
          add DWORD PTR [ESP+40],512
          mov DWORD PTR [EBX-16],EDI
          mov DWORD PTR [EBX-12],ESI
          mov DWORD PTR [EBX-8],ECX
          mov DWORD PTR [EBX-4],EDX
          cmp EBX,DWORD PTR [ESP+52]
          jne L_412660
          add DWORD PTR [ESP+56],1
          mov ESI,EBX
          mov EBX,DWORD PTR [ESP+56]
          cmp DWORD PTR [L_479ee4],EBX
          ja L_412638
L_412785:
          mov DWORD PTR [ESP+4],OFFSET _iw_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ECX,DWORD PTR [L_479f6c]
          test ECX,ECX
          je L_4127b0
          test BYTE PTR [L_479f03],16
          jne L_412ae3
L_4127b0:
          mov EAX,DWORD PTR [L_479f74]
          lea EDX,DWORD PTR [EAX-1]
          cmp EDX,31
          ja L_4127f4
          mov EBX,DWORD PTR [L_479f60]
          cmp DWORD PTR [L_479ef0],EBX
          je L_4128d7
          cmp DWORD PTR [_xb],2
          je L_4128d7
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451ec0
          mov DWORD PTR [ESP],1
          call _log_printf
L_4127f4:
          mov DWORD PTR [ESP+4],OFFSET L_451f37
          mov DWORD PTR [ESP],1
          call _log_printf
          add ESP,76
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_412812:
          cmp BYTE PTR [EDX],255
          jne L_412685
          cmp BYTE PTR [EDX+1],255
          jne L_412685
          cmp BYTE PTR [EDX+2],255
          jne L_412685
          cmp BYTE PTR [EDX+3],255
          jne L_412685
          cmp BYTE PTR [EDX+4],255
          jne L_412685
          cmp BYTE PTR [EDX+5],255
          jne L_412685
          cmp BYTE PTR [EDX+6],255
          jne L_412685
          cmp BYTE PTR [EDX+7],255
          jne L_412685
          cmp BYTE PTR [EDX+8],255
          jne L_412685
          cmp BYTE PTR [EDX+9],255
          jne L_412685
          cmp BYTE PTR [EDX+10],255
          jne L_412685
          cmp BYTE PTR [EDX+11],255
          jne L_412685
          movzx ECX,BYTE PTR [EDX+12]
          cmp CL,255
          mov BYTE PTR [ESP+48],CL
          jne L_41268d
          cmp BYTE PTR [EDX+13],255
          jne L_41268d
          movzx ECX,BYTE PTR [EDX+14]
          cmp CL,255
          mov BYTE PTR [ESP+48],CL
          jne L_4128c0
          cmp BYTE PTR [EDX+15],255
          je L_412713
          jmp L_41268d
L_4128c0:
          mov BYTE PTR [ESP+48],255
          jmp L_41268d
L_4128ca:
          add ESP,76
          mov EAX,4294967295
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4128d7:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451dca
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EDX,DWORD PTR [L_479ef0]
          test EDX,EDX
          jne L_412ac7
          mov EAX,DWORD PTR [_g479ea8]
          mov EBX,16896
          mov DWORD PTR [ESP+40],16896
          sub EAX,6
          and EAX,4294967293
          cmp EAX,1
          sbb EBP,EBP
          and EBP,3072
          add EBP,1024
          mov EDI,EBP
L_412928:
          mov EAX,DWORD PTR [L_479f74]
          test EAX,EAX
          je L_4127f4
          mov DWORD PTR [ESP+48],EDI
          mov EDI,DWORD PTR [ESP+60]
          jmp L_412973
          .byte 0x90
L_412940:
          mov ESI,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451e28
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+16],ESI
          call _log_printf
L_412964:
          add EDI,1
          cmp DWORD PTR [L_479f74],EDI
          jbe L_4127f4
L_412973:
          mov EAX,DWORD PTR [EDI*4+L_479f78]
          mov EDX,DWORD PTR [EDI*4+L_479ff8]
          cmp EAX,EBP
          jae L_412989
          cmp EDX,EBP
          jb L_4129dc
L_412989:
          cmp EDX,-5
          jne L_412940
          mov ESI,EAX
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_451e84
          mov DWORD PTR [ESP],1
          call _log_printf
          imul ESI,EBX
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],0
          add EAX,ESI
          mov DWORD PTR [ESP],EAX
          call _memset
L_4129c6:
          mov DWORD PTR [ESP+4],OFFSET _iw_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_412964
L_4129dc:
          mov ESI,EAX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+40]
          imul ESI,EBX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+4],OFFSET L_451de0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+44],ESI
          mov ESI,EDX
          imul ESI,EBX
          call _log_printf
          mov EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EBX
          lea EDX,DWORD PTR [EAX+ESI*1]
          add EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov DWORD PTR [ESP+4],OFFSET L_451e14
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [ESP+44]
          add EAX,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EAX
          call _memset
          cmp DWORD PTR [L_479ef0],1
          mov EAX,DWORD PTR [L_479ee0]
          lea EDX,DWORD PTR [EAX+ESI*1]
          sbb ECX,ECX
          and ECX,4294849024
          lea ECX,DWORD PTR [ESI+ECX*1+135168]
          add EAX,ECX
L_412a7c:
          cmp BYTE PTR [EDX],255
          jne L_4129c6
          add EDX,1
          cmp EDX,EAX
          jne L_412a7c
          mov DWORD PTR [ESP+4],OFFSET L_451f48
          mov DWORD PTR [ESP],1
          call _log_printf
          mov EAX,DWORD PTR [L_479ef0]
          add ESI,DWORD PTR [L_479ee0]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [EDI*4+L_479f78]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],EAX
          call _setBlockSpare
          jmp L_4129c6
L_412ac7:
          mov EBX,135168
          mov EBP,512
          mov EDI,512
          mov DWORD PTR [ESP+40],135168
          jmp L_412928
L_412ae3:
          mov DWORD PTR [ESP+4],OFFSET L_451d88
          mov DWORD PTR [ESP],1
          call _log_printf
          movzx EAX,BYTE PTR [L_479ece]
          mov EBX,DWORD PTR [L_479ee0]
          imul EDX,EAX,135168
          mov DWORD PTR [ESP+44],EAX
          add EBX,EDX
          mov EDX,EAX
          shl EAX,17
          mov DWORD PTR [ESP+52],EAX
          mov EAX,EDX
          shl EAX,12
          cmp DWORD PTR [L_479ec8],EDX
          mov DWORD PTR [ESP+48],EAX
          jbe L_412bca
L_412b2e:
          lea EAX,DWORD PTR [EBX+135168]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESP+48]
L_412b40:
          mov ESI,DWORD PTR [_g479f4c]
          lea EDI,DWORD PTR [EBX+4]
          and EDI,4294967292
          add ESI,EDX
          add EDX,512
          mov ECX,DWORD PTR [ESI]
          mov DWORD PTR [EBX],ECX
          mov ECX,DWORD PTR [ESI+508]
          mov DWORD PTR [EBX+508],ECX
          mov ECX,EBX
          add EBX,528
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          rep movsd 
          mov ECX,DWORD PTR [L_479f50]
          mov EBP,DWORD PTR [ECX+EAX*1]
          mov EDI,DWORD PTR [ECX+EAX*1+4]
          mov ESI,DWORD PTR [ECX+EAX*1+8]
          mov ECX,DWORD PTR [ECX+EAX*1+12]
          add EAX,16
          mov DWORD PTR [EBX-16],EBP
          mov DWORD PTR [EBX-12],EDI
          mov DWORD PTR [EBX-8],ESI
          mov DWORD PTR [EBX-4],ECX
          cmp EBX,DWORD PTR [ESP+40]
          jne L_412b40
          add DWORD PTR [ESP+44],1
          add DWORD PTR [ESP+52],131072
          mov EAX,DWORD PTR [ESP+44]
          add DWORD PTR [ESP+48],4096
          cmp DWORD PTR [L_479ec8],EAX
          ja L_412b2e
L_412bca:
          mov DWORD PTR [ESP+4],OFFSET _iw_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4127b0
L_412be3:
          mov DWORD PTR [ESP+4],OFFSET L_451d10
          mov DWORD PTR [ESP],1
          call _log_printf
          mov ESI,DWORD PTR [L_479ee4]
          mov EAX,ESI
          shl EAX,5
          test EAX,EAX
          je L_412d2d
          xor EBP,EBP
          mov EDX,2
          jmp L_412cd5
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_412c20:
          cmp BYTE PTR [EBX+EDX*1-1],255
          lea EAX,DWORD PTR [EDX-1]
          movzx ECX,BYTE PTR [EBX+EDX*1]
          jne L_412cfa
          cmp CL,255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+1],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+2],255
          jne L_412dc5
          movzx ECX,BYTE PTR [EBX+EDX*1+3]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+4],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+5],255
          jne L_412dc5
          movzx ECX,BYTE PTR [EBX+EDX*1+6]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+7],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+8],255
          jne L_412dc5
          movzx ECX,BYTE PTR [EBX+EDX*1+9]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+10],255
          jne L_412cfa
          cmp BYTE PTR [EBX+EDX*1+11],255
          jne L_412cfa
          movzx ECX,BYTE PTR [EBX+EDX*1+12]
          cmp CL,255
          jne L_412dc5
          cmp BYTE PTR [EBX+EDX*1+13],255
          jne L_412cfa
          mov EAX,ESI
          add EBP,1
          add EDX,16
          shl EAX,5
          cmp EAX,EBP
          jbe L_412d2d
L_412cd5:
          mov EBX,DWORD PTR [L_479ed0]
          mov EAX,EBP
          shl EAX,4
          add EAX,EBX
          movzx EDI,BYTE PTR [EAX]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,EDI
          cmp AL,255
          je L_412c20
          movzx ECX,BYTE PTR [EBX+EDX*1]
          lea EAX,DWORD PTR [EDX-1]
L_412cfa:
          mov EBX,DWORD PTR [ESP+44]
          add EBP,1
          mov BYTE PTR [EBX],CL
          mov EBX,DWORD PTR [L_479ed0]
          movzx ECX,BYTE PTR [EBX+EAX*1]
          mov BYTE PTR [EBX+EDX*1],CL
          mov ECX,DWORD PTR [L_479ed0]
          mov EBX,EDI
          add EDX,16
          mov BYTE PTR [ECX+EAX*1],BL
          mov ESI,DWORD PTR [L_479ee4]
          mov EAX,ESI
          shl EAX,5
          cmp EAX,EBP
          ja L_412cd5
L_412d2d:
          mov DWORD PTR [ESP+4],OFFSET _iw_451cdd
          mov DWORD PTR [ESP],1
          call _log_printf
          jmp L_4125fd
L_412d46:
          mov DWORD PTR [ESP+4],OFFSET L_451ce4
          mov DWORD PTR [ESP],1
          xor EBX,EBX
          call _log_printf
          mov EDI,DWORD PTR [L_479ee4]
          mov EAX,DWORD PTR [L_479ed0]
          shr EDI,3
          lea ECX,DWORD PTR [EAX+4096]
          test EDI,EDI
          je L_412d2d
L_412d74:
          mov ESI,EBX
          lea EAX,DWORD PTR [ECX-4096]
          shr ESI,8
          and ESI,15
          jmp L_412d9a
L_412d84:
          movzx EDX,BYTE PTR [EAX+2]
          mov BYTE PTR [EAX+1],BL
          add EAX,16
          and EDX,4294967280
          or EDX,ESI
          mov BYTE PTR [EAX-14],DL
          cmp ECX,EAX
          je L_412db3
L_412d9a:
          movzx EDX,BYTE PTR [EAX+2]
          and EDX,15
          cmp DL,15
          jne L_412d84
          cmp BYTE PTR [EAX+1],255
          jne L_412d84
          add EAX,16
          cmp ECX,EAX
          jne L_412d9a
L_412db3:
          add EBX,1
          add ECX,4096
          cmp EDI,EBX
          jne L_412d74
          jmp L_412d2d
L_412dc5:
          mov ECX,4294967295
          jmp L_412cfa
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
L_451b04:
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
L_451ce4:
          .string "fixing up big block LBA numbers in spare..."
L_451d10:
          .string "fixing up big block controller on small block NAND LBA numbers..."
          .zero 2
L_451d54:
          .string "calculating ECD bytes and assembling raw image..."
          .zero 2
L_451d88:
          .string "attempting to restore NAND MU data to big block unit from dump..."
L_451dca:
          .string "remapping %d blocks\n"
          .zero 1
L_451de0:
          .string "    copying 0x%x bytes of LBA 0x%x to block 0x%x..."
L_451e14:
          .string "zero fill origin..."
L_451e28:
          .string "\n\n***** ERROR: Remapping block 0x%x to block 0x%x is not sane on a NAND with 0x%x blocks!\n"
          .zero 1
L_451e84:
          .string "    Remapping block 0x%x is not required, zerofilling..."
          .zero 3
L_451ec0:
          .string "\n\n***** ERROR: if you had given the same small/big block style NAND donor image I'd be remapping %d bad blocks now...\n"
L_451f37:
          .string "done remapping!\n"
L_451f48:
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
          .long _imgWriteStart - .
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
          .long _imgAdd.constprop.2 - .
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
