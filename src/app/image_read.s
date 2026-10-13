# app/image_read.s -- parsing an existing NAND image: sectors, pairing, LDV, smc.bin
#
# original placement:
#   .bss           00474a20-00478d60
#   .data          0044a5c0-0044a5e0
#   .eh_frame      004676ac-00467fd0
#   .rdata         004521b8-004541f8
#   .rdata$zzz     004639b4-004639e0
#   .text          004136a0-00418240

.intel_syntax noprefix
.globl FUN_4137f0
.globl FUN_414650
.globl FUN_414760
.globl FUN_415ef0
.globl FUN_416840
.globl FUN_417680

.text
.p2align 4
FUN_4136a0:
          push EBP
          push EDI
          mov EBP,ECX
          push ESI
          push EBX
          mov ESI,EAX
          mov EDI,8192
          xor EBX,EBX
          sub ESP,60
          mov DWORD PTR [ESP+40],EDX
          jmp L_4136d2
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4136c0:
          add EBX,1
          add EDI,32
          cmp EBX,256
          je L_4137a0
L_4136d2:
          mov EDX,DWORD PTR [L_44a5d8]
          lea EAX,DWORD PTR [EBX+256]
          shl EAX,5
          cmp BYTE PTR [EDX+EAX*1],0
          je L_4136c0
          add EDX,EDI
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDX
          call FUN_4491d8
          test EAX,EAX
          jne L_4136c0
          mov EAX,DWORD PTR [L_44a5d8]
          shl EBX,5
          mov EDI,DWORD PTR [ESP+40]
          add EAX,EBX
          mov EDX,DWORD PTR [EAX+8216]
          mov EBX,EDX
          mov ECX,EDX
          shr ECX,24
          shl EBX,24
          add EBX,ECX
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add ECX,EBX
          add ECX,EDX
          mov DWORD PTR [EBP],ECX
          movzx ECX,WORD PTR [EAX+8214]
          mov EDX,ECX
          movzx ECX,CH
          shl EDX,8
          and EDX,65280
          add ECX,EDX
          mov DWORD PTR [EDI],ECX
          mov ECX,DWORD PTR [ESP+80]
          test ECX,ECX
          je L_413784
          mov EAX,DWORD PTR [EAX+8220]
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
          mov ECX,DWORD PTR [ESP+80]
          add EAX,EDX
          mov DWORD PTR [ECX],EAX
L_413784:
          mov EDX,DWORD PTR [ESP+84]
          mov EAX,1
          test EDX,EDX
          je L_4137aa
          add ESP,60
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
L_4137a0:
          add ESP,60
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4137aa:
          mov EDX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_4521b8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+44]
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
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
FUN_4137f0:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [L_478d40],0
          test EAX,EAX
          je L_413810
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_413810:
          mov EAX,DWORD PTR [L_479f4c]
          test EAX,EAX
          je L_413821
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_413821:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [L_479f4c],0
          mov EBX,OFFSET L_47a08c
          mov DWORD PTR [L_479f50],0
          mov DWORD PTR [L_479f6c],0
          mov DWORD PTR [L_479f70],0
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_413860:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_41386e
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_41386e:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_413860
          mov EBX,OFFSET L_479ea0
          mov ESI,OFFSET L_479ec0
L_413883:
          mov EAX,DWORD PTR [EBX+580]
          test EAX,EAX
          je L_413895
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_413895:
          mov DWORD PTR [EBX+584],0
          add EBX,8
          cmp ESI,EBX
          jne L_413883
          mov EAX,DWORD PTR [L_47a104]
          test EAX,EAX
          je L_4138b7
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_4138b7:
          add ESP,20
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_4138c0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [L_479f4c]
          mov ESI,DWORD PTR [EBX+112]
          mov EDX,ESI
          mov ECX,ESI
          mov EAX,ESI
          shl EDX,24
          shr ECX,24
          shl EAX,8
          add ECX,EDX
          and EAX,16711680
          shr ESI,8
          lea EDX,DWORD PTR [ECX+EAX*1]
          and ESI,65280
          mov EAX,EDX
          mov EDX,65536
          add EAX,ESI
          mov ESI,DWORD PTR [EBX+100]
          cmove EAX,EDX
          mov DWORD PTR [ESP+4],EAX
          mov EDX,ESI
          mov ECX,ESI
          mov EAX,ESI
          shl EDX,24
          shr ECX,24
          shl EAX,8
          add ECX,EDX
          and EAX,16711680
          lea EDX,DWORD PTR [ECX+EAX*1]
          mov EAX,ESI
          shr EAX,8
          and EAX,65280
          add EAX,EDX
          add EAX,EBX
          mov DWORD PTR [ESP],EAX
          call FUN_401a00
          test EAX,EAX
          mov ESI,EAX
          je L_413993
L_413939:
          cmp BYTE PTR [L_479f15],0
          je L_413a70
L_413946:
          mov EBX,ESI
          mov DWORD PTR [ESP+4],OFFSET L_4522e4
          mov DWORD PTR [ESP],1
          shr EBX,8
          mov DWORD PTR [ESP+8],EBX
          call FUN_433690
          mov DWORD PTR [ESP],EBX
          call FUN_41ade0
          movzx EAX,BYTE PTR [L_479f15]
          test AL,AL
          jne L_413a3b
          mov EDX,ESI
          cmp DL,32
          jbe L_413a60
          mov BYTE PTR [L_479f15],32
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_413993:
          mov EDX,DWORD PTR [EBX+108]
          mov EDI,DWORD PTR [EBX+96]
          mov ESI,EDX
          mov EBX,EDX
          mov ECX,EDX
          shr ESI,24
          shl EBX,24
          shl ECX,8
          add EBX,ESI
          mov ESI,EDI
          and ECX,16711680
          shl ESI,24
          shr EDX,8
          mov EAX,EDI
          add EBX,ESI
          mov ESI,EDI
          and EDX,65280
          shr ESI,24
          shl EAX,8
          add ESI,EBX
          and EAX,16711680
          lea EBX,DWORD PTR [ESI+ECX*1]
          lea ECX,DWORD PTR [EBX+EDX*1]
          lea EDX,DWORD PTR [ECX+EAX*1]
          mov EAX,EDI
          shr EAX,8
          and EAX,65280
          add EAX,EDX
          add EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP],EAX
          call FUN_4017d0
          test EAX,EAX
          mov ESI,EAX
          jne L_413939
          mov EAX,DWORD PTR [L_479ea8]
          lea EDX,DWORD PTR [EAX-6]
          cmp EDX,1
          jbe L_413ab0
          sub EAX,8
          cmp EAX,1
          jbe L_413a92
          mov DWORD PTR [ESP+4],OFFSET L_452260
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EDX,1
L_413a30:
          movzx EAX,BYTE PTR [L_479f15]
          test AL,AL
          je L_413a60
L_413a3b:
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_45230f
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESP,16
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
L_413a60:
          mov BYTE PTR [L_479f15],DL
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_413a70:
          mov EAX,ESI
          mov DWORD PTR [ESP+4],OFFSET L_4522c4
          mov DWORD PTR [ESP],1
          movzx EAX,AL
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          jmp L_413946
L_413a92:
          mov DWORD PTR [ESP+4],OFFSET L_452220
          mov DWORD PTR [ESP],1
          call FUN_433690
          xor EDX,EDX
          jmp L_413a30
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_413ab0:
          mov DWORD PTR [ESP+4],OFFSET L_4521e0
          mov DWORD PTR [ESP],1
          call FUN_433690
          xor EDX,EDX
          jmp L_413a30
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_413ad0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDX,DWORD PTR [L_479f4c]
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
          mov DWORD PTR [ESP+4],OFFSET L_45232c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,ESI
          and AH,247
          cmp EAX,12288
          je L_413cb0
          mov EBX,4096
          mov EDI,4096
L_413b79:
          mov DWORD PTR [ESP+8],12288
          mov DWORD PTR [ESP+4],OFFSET L_45238c
          mov ESI,12288
          mov DWORD PTR [ESP],1
          call FUN_433690
L_413b9a:
          imul EAX,DWORD PTR [L_479f5c],528
          cmp EBX,EAX
          jb L_413c20
L_413ba8:
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_452494
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_45235c
          mov ESI,14336
          mov DWORD PTR [ESP],1
          call FUN_433690
          imul EAX,DWORD PTR [L_479f5c],528
          cmp EBX,EAX
          jae L_413ba8
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_413c20:
          mov DWORD PTR [ESP],ESI
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a0e0+4],EAX
          je L_413d10
          add EBX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [L_47a0e4+4],ESI
          mov DWORD PTR [ESP+4],EBX
          call FUN_4490f8
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_4523bc
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0e4+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call FUN_401730
          test EAX,EAX
          je L_413cd0
          mov DWORD PTR [ESP+4],OFFSET L_4523ec
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call FUN_41add0
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
          mov DWORD PTR [ESP+4],OFFSET L_45242c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0e0+4]
          mov DWORD PTR [ESP],EAX
          call FUN_449140
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
          mov DWORD PTR [ESP+4],OFFSET L_452450
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_413bc4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_413d30:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDX,DWORD PTR [L_479f4c]
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
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a0e8+4],EAX
          je L_414010
          mov DWORD PTR [ESP+12],16384
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_452538
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [L_47a0ec+4],16384
          add EAX,EDI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
          mov EAX,DWORD PTR [L_47a0ec+4]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call FUN_401630
          test EAX,EAX
          je L_413f90
          mov DWORD PTR [ESP+4],OFFSET L_45256c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0e8+4]
          add EAX,16
          mov DWORD PTR [ESP],EAX
          call FUN_41ad90
          cmp ESI,32768
          jne L_413f38
          mov DWORD PTR [ESP],16384
          add EDI,16384
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a0f4],EAX
          je L_414030
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+12],16384
          mov DWORD PTR [ESP+4],OFFSET L_452674
          mov DWORD PTR [ESP],1
          call FUN_433690
          add EDI,DWORD PTR [L_479f4c]
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [L_47a0f8],16384
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDI
          call FUN_4490f8
          mov EAX,DWORD PTR [L_47a0f8]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [ESP],EAX
          call FUN_401630
          test EAX,EAX
          je L_413fd0
          mov DWORD PTR [ESP+4],OFFSET L_4526ac
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0f4]
          add EAX,16
          mov DWORD PTR [ESP],EAX
          call FUN_41adb0
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
          mov DWORD PTR [ESP+4],OFFSET L_45261c
          mov DWORD PTR [ESP],1
          call FUN_433690
L_413f38:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_413f40:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_452508
          mov ESI,16384
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_413da4
L_413f62:
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],OFFSET L_4524dc
          mov EDI,16384
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_4525a8
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0e8+4]
          mov DWORD PTR [ESP],EAX
          call FUN_449140
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
          mov DWORD PTR [ESP+4],OFFSET L_4526f0
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_47a0f4]
          mov DWORD PTR [ESP],EAX
          call FUN_449140
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
          mov DWORD PTR [ESP+4],OFFSET L_4525d0
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_413f38
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_414030:
          mov DWORD PTR [ESP+4],OFFSET L_45271c
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_413f38
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_414050:
          push EBP
          push EDI
          mov EDI,66
          push ESI
          push EBX
          mov ESI,OFFSET L_47a08c
          mov EBX,OFFSET L_474a24+20
          sub ESP,92
          lea EBP,DWORD PTR [ESP+50]
          jmp L_414085
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_414070:
          add EBX,24
          add EDI,1
          add ESI,8
          cmp EBX,OFFSET L_474b10
          je L_414130
L_414085:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_414070
          mov EDX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+44],EDX
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [ESI],EAX
          mov EDX,DWORD PTR [ESP+44]
          je L_4141d2
          mov EAX,EDI
          mov DWORD PTR [ESP+8],OFFSET L_44a5d0
          mov DWORD PTR [ESP+4],OFFSET L_452799
          mov DWORD PTR [ESP],EBP
          mov BYTE PTR [L_44a5d6],AL
          call FUN_449098
          mov EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4527a0
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+12],EAX
          call FUN_433690
          mov EAX,DWORD PTR [EBX+16]
          add EAX,DWORD PTR [L_479f4c]
          mov EDX,DWORD PTR [EBX+12]
          mov ECX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+44],EDX
          call FUN_4490f8
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESI+4],EDX
          jmp L_414070
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_414130:
          mov EAX,DWORD PTR [L_479f68]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_479f60]
          mov DWORD PTR [ESP],EAX
          call FUN_412e90
          mov ESI,EAX
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+4],4096
          add EAX,ESI
          mov DWORD PTR [ESP],EAX
          call FUN_410070
          test EAX,EAX
          je L_414255
L_41417f:
          mov EAX,DWORD PTR [L_479f68]
          mov DWORD PTR [ESP+16],0
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_479f60]
          mov DWORD PTR [ESP],EAX
          call FUN_412f60
          mov ESI,EAX
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+4],4096
          add EAX,ESI
          mov DWORD PTR [ESP],EAX
          call FUN_410070
          test EAX,EAX
          je L_4141f3
L_4141ca:
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4141d2:
          mov DWORD PTR [ESP+12],EDX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45276c
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_414070
L_4141f3:
          mov DWORD PTR [ESP+16],4096
          mov DWORD PTR [ESP+12],4096
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_452864
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP],4096
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a0d8+4],EAX
          je L_4142d1
          add ESI,DWORD PTR [L_479f4c]
          mov ECX,1024
          mov EDI,EAX
          rep movsd 
          mov DWORD PTR [L_47a0dc+4],4096
          add ESP,92
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_414255:
          mov DWORD PTR [ESP+16],4096
          mov DWORD PTR [ESP+12],4096
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_4527e4
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP],4096
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a0d4],EAX
          je L_4142b0
          add ESI,DWORD PTR [L_479f4c]
          mov ECX,1024
          mov EDI,EAX
          rep movsd 
          mov DWORD PTR [L_47a0d4+4],4096
          jmp L_41417f
L_4142b0:
          mov DWORD PTR [ESP+8],4096
          mov DWORD PTR [ESP+4],OFFSET L_452824
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_41417f
L_4142d1:
          mov DWORD PTR [ESP+8],4096
          mov DWORD PTR [ESP+4],OFFSET L_4528a4
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_4141ca
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
FUN_414300:
          push EDI
          push ESI
          push EBX
          sub ESP,32
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [L_47a104],0
          sub EAX,-128
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          cmp AX,51786
          je L_414330
L_414326:
          add ESP,32
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_414330:
          mov EBX,DWORD PTR [L_479f4c]
          lea EAX,DWORD PTR [EBX+144]
          lea ESI,DWORD PTR [EBX+128]
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov EDI,EAX
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,140
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov DWORD PTR [ESP+4],OFFSET L_4528e1
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP],1
          mov DWORD PTR [L_47a108],EAX
          call FUN_433690
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_4528fe
          mov DWORD PTR [ESP],1
          call FUN_433690
          cmp EDI,1
          je L_4143d0
L_414398:
          mov EBX,DWORD PTR [L_47a108]
          mov DWORD PTR [ESP],EBX
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a104],EAX
          je L_414326
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
          add ESP,32
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
L_4143d0:
          movzx EAX,BYTE PTR [EBX+151]
          mov DWORD PTR [ESP+20],EAX
          movzx EAX,BYTE PTR [EBX+150]
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EBX+149]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX+148]
          mov DWORD PTR [ESP+4],OFFSET L_452912
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          movzx EAX,BYTE PTR [EBX+157]
          mov DWORD PTR [ESP+28],EAX
          movzx EAX,BYTE PTR [EBX+156]
          mov DWORD PTR [ESP+24],EAX
          movzx EAX,BYTE PTR [EBX+155]
          mov DWORD PTR [ESP+20],EAX
          movzx EAX,BYTE PTR [EBX+154]
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EBX+153]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX+152]
          mov DWORD PTR [ESP+4],OFFSET L_452930
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          lea EAX,DWORD PTR [EBX+158]
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          movzx EAX,AX
          mov DWORD PTR [ESP+4],OFFSET L_452958
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          movzx EAX,BYTE PTR [EBX+163]
          mov DWORD PTR [ESP+20],EAX
          movzx EAX,BYTE PTR [EBX+162]
          mov DWORD PTR [ESP+16],EAX
          movzx EAX,BYTE PTR [EBX+161]
          mov DWORD PTR [ESP+12],EAX
          movzx EAX,BYTE PTR [EBX+160]
          mov DWORD PTR [ESP+4],OFFSET L_45296a
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          jmp L_414398
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
FUN_4144e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDI,DWORD PTR [L_474d20]
          mov EAX,DWORD PTR [ESP+64]
          mov EBX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],1
          mov EBP,EAX
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [EAX*4+L_4c90e8]
          mov EDX,EBX
          add EBP,81032
          shl EDX,14
          add EDX,EDI
          mov ESI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+20],EAX
          call FUN_4491a0
          cmp ESI,16384
          mov DWORD PTR [EBP*4+L_479ea0],EAX
          mov EDX,DWORD PTR [ESP+16]
          jbe L_4145fe
          mov ECX,ESI
          sub ECX,16385
          mov ESI,ECX
          mov DWORD PTR [ESP+28],ECX
          and ESI,4294950912
          lea ECX,DWORD PTR [ESI+16384]
          xor ESI,ESI
          mov DWORD PTR [ESP+16],ECX
          jmp L_414569
L_414562:
          mov EAX,DWORD PTR [EBP*4+L_479ea0]
L_414569:
          add EDX,DWORD PTR [L_479f4c]
          add EAX,ESI
          mov DWORD PTR [ESP+8],16384
          mov DWORD PTR [ESP],EAX
          add ESI,16384
          mov DWORD PTR [ESP+4],EDX
          call FUN_4490f8
          mov EAX,DWORD PTR [L_44a5d8]
          movzx EBX,WORD PTR [EAX+EBX*2]
          mov EAX,EBX
          shl EBX,8
          movzx EAX,AH
          add EBX,EAX
          and EBX,8191
          mov EDX,EBX
          shl EDX,14
          add EDX,EDI
          cmp ESI,DWORD PTR [ESP+16]
          jne L_414562
          mov EAX,DWORD PTR [ESP+28]
          mov EDI,DWORD PTR [ESP+20]
          and EAX,4294950912
          neg EAX
          lea EAX,DWORD PTR [EDI+EAX*1-16384]
          mov DWORD PTR [ESP+20],EAX
L_4145cb:
          mov ECX,DWORD PTR [EBP*4+L_479ea0]
          add EDX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],EAX
          add ECX,ESI
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP],ECX
          call FUN_4490f8
L_4145ea:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+64],EAX
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp FUN_40d120
L_4145fe:
          mov EAX,DWORD PTR [ESP+20]
          test EAX,EAX
          je L_4145ea
          xor ESI,ESI
          mov EAX,DWORD PTR [ESP+20]
          jmp L_4145cb
          .byte 0x66
          .byte 0x90
L_414610:
          cmp DWORD PTR [L_474d24],1
          push ESI
          push EBX
          mov EAX,DWORD PTR [ESP+12]
          mov EDX,DWORD PTR [ESP+16]
          mov ECX,DWORD PTR [ESP+20]
          mov EBX,DWORD PTR [ESP+24]
          mov ESI,DWORD PTR [ESP+28]
          je L_414634
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
L_414634:
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+12],EBX
          pop EBX
          pop ESI
          jmp FUN_4136a0
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
FUN_414650:
          cmp DWORD PTR [L_474d24],1
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
          mov EDX,DWORD PTR [L_44a5d8]
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
          mov DWORD PTR [ESP+4],OFFSET L_452988
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
          add EAX,DWORD PTR [L_474d20]
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+12],EAX
          call FUN_433690
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
FUN_414760:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov ESI,DWORD PTR [L_474d24]
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
          mov EDX,DWORD PTR [L_44a5d8]
          lea EAX,DWORD PTR [EBX+256]
          shl EAX,5
          cmp BYTE PTR [EDX+EAX*1],0
          je L_414790
          add EDX,EBP
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EDX
          call FUN_4491d8
          test EAX,EAX
          jne L_414790
          mov EAX,DWORD PTR [L_44a5d8]
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
          mov EAX,DWORD PTR [L_474d20]
          mov EBX,EDX
          movzx EDX,DH
          shl EBX,8
          and EBX,65280
          mov DWORD PTR [ESP+20],EAX
          add EBX,EDX
          mov EDI,EBX
          shl EDI,14
          add EDI,EAX
          call FUN_4491a0
          mov ECX,DWORD PTR [L_479f4c]
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
          call FUN_4490f8
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
          add EDI,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
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
FUN_414960:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov DWORD PTR [ESP+4],OFFSET L_4529d0
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,50233368
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov ESI,EAX
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,50249752
          mov DWORD PTR [ESP],EAX
          call FUN_420ad0
          mov EBX,EAX
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,50233344
          mov DWORD PTR [ESP],EAX
          call FUN_402a00
          test EAX,EAX
          mov EDI,EAX
          je L_414a50
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_4529f8
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,50249728
          mov DWORD PTR [ESP],EAX
          call FUN_402a00
          test EAX,EAX
          je L_414a7a
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_452a4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          cmp ESI,EBX
          jae L_414a94
L_414a10:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_452a78
          mov EDI,OFFSET L_474b20
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_479f4c]
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
          mov DWORD PTR [ESP+4],OFFSET L_452a24
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,50249728
          mov DWORD PTR [ESP],EAX
          call FUN_402a00
          test EAX,EAX
          jne L_414ad0
L_414a7a:
          mov DWORD PTR [ESP+4],OFFSET L_452aa4
          mov DWORD PTR [ESP],1
          call FUN_433690
          xor EAX,EAX
          test EDI,EDI
          je L_414a44
L_414a94:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_452acc
          mov EDI,OFFSET L_474b20
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_479f4c]
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
          mov DWORD PTR [ESP+4],OFFSET L_452a4c
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_414a10
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_414af0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          call FUN_414960
          test EAX,EAX
          je L_414b7a
          mov ESI,OFFSET L_474b3c
          mov EDI,OFFSET L_474a20
          xor EBX,EBX
          jmp L_414b1e
          .byte 0x66
          .byte 0x90
L_414b10:
          add EBX,1
          add ESI,4
          add EDI,24
          cmp EBX,10
          je L_414b75
L_414b1e:
          mov DWORD PTR [ESP],ESI
          call FUN_420ab0
          movzx EBP,AX
          test BP,BP
          je L_414b10
          lea EAX,DWORD PTR [ESI+2]
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          test AX,AX
          jne L_414b82
          test EBX,EBX
          mov EDX,16384
          jne L_414b82
L_414b47:
          mov DWORD PTR [EDI+8],EBX
          shl EBP,14
          add EBX,1
          mov DWORD PTR [EDI],1
          mov DWORD PTR [EDI+4],1
          add ESI,4
          mov DWORD PTR [EDI+16],EBP
          mov DWORD PTR [EDI+20],0
          add EDI,24
          mov DWORD PTR [EDI-12],EDX
          cmp EBX,10
          jne L_414b1e
L_414b75:
          mov EAX,DWORD PTR [L_474a20]
L_414b7a:
          add ESP,28
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_414b82:
          test AX,AX
          je L_414b10
          movzx EDX,AX
          jmp L_414b47
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_414b90:
          mov ECX,DWORD PTR [L_479f60]
          push EBX
          mov EDX,DWORD PTR [ESP+8]
          test ECX,ECX
          jne L_414bd5
          mov EAX,DWORD PTR [L_479f64]
          test EAX,EAX
          jne L_414bd0
          movzx ECX,BYTE PTR [EDX+2]
L_414bac:
          movzx EAX,BYTE PTR [EDX+3]
          movzx EBX,BYTE PTR [EDX+4]
          movzx EDX,BYTE PTR [EDX+6]
          shl EBX,16
          shl EAX,8
          or EAX,EBX
          shl EDX,24
          or EAX,EDX
          or EAX,ECX
          pop EBX
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_414bd0:
          movzx ECX,BYTE PTR [EDX]
          jmp L_414bac
L_414bd5:
          movzx ECX,BYTE PTR [EDX+5]
          jmp L_414bac
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
FUN_414be0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EDX,DWORD PTR [L_479f60]
          mov EBX,DWORD PTR [L_479f4c]
          mov EAX,DWORD PTR [L_479f5c]
          test EDX,EDX
          jne L_414e7d
          sub EAX,1152
          mov BYTE PTR [ESP+63],48
          mov DWORD PTR [ESP+56],EAX
L_414c0e:
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],2
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_452af8
          mov DWORD PTR [ESP],2
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],2
          call FUN_433690
          mov EAX,DWORD PTR [EBX+100]
          mov ESI,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+4],OFFSET L_452b20
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
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_452b6c
          mov DWORD PTR [ESP],2
          shl ESI,24
          or EDX,ESI
          or EDX,DWORD PTR [ESP+52]
          lea ESI,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+12],EDX
          call FUN_433690
L_414d91:
          mov EAX,DWORD PTR [L_479f50]
          movzx EAX,BYTE PTR [EAX+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET L_452bc3
          add EBX,1
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          cmp EBX,ESI
          jne L_414d91
          cmp WORD PTR [ESP+60],0
          js L_414e50
          mov DWORD PTR [ESP+4],OFFSET L_452bd3
          mov DWORD PTR [ESP],2
          call FUN_433690
L_414dd9:
          add EDI,1
          add DWORD PTR [ESP+48],512
          add EBP,528
          cmp DWORD PTR [ESP+56],EDI
          mov EBX,ESI
          jne L_414ce0
L_414df6:
          mov DWORD PTR [ESP+4],OFFSET L_44a4e0
          mov DWORD PTR [ESP],2
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_452bc9
          mov DWORD PTR [ESP],2
          call FUN_433690
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
FUN_414e90:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,92
          mov EDX,DWORD PTR [L_479f60]
          mov EBX,DWORD PTR [L_479f4c]
          mov EAX,DWORD PTR [L_479f5c]
          test EDX,EDX
          jne L_415160
          sub EAX,1152
          mov BYTE PTR [ESP+71],48
          mov DWORD PTR [ESP+64],EAX
          call FUN_433600
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
          call FUN_433600
          cmp EAX,2
          je L_4150a0
L_414fa4:
          lea EAX,DWORD PTR [EBX+EBX*2]
          mov ECX,DWORD PTR [ESP+60]
          cmp DWORD PTR [EAX*8+L_474a24],ECX
          jbe L_415010
          mov ECX,DWORD PTR [EAX*8+L_474a20]
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
          mov EAX,DWORD PTR [L_474a20]
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
          lea EAX,DWORD PTR [EDX*8+L_474a20]
          mov DWORD PTR [EDX*8+L_474a20],1
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
          mov DWORD PTR [ESP+4],OFFSET L_452b6c
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
          call FUN_433690
          lea EAX,DWORD PTR [EDI+16]
          mov DWORD PTR [ESP+76],EBX
          mov EBX,EDI
          mov ESI,EAX
L_4150f5:
          mov EDX,DWORD PTR [L_479f50]
          movzx EDX,BYTE PTR [EDX+EBX*1]
          mov DWORD PTR [ESP+4],OFFSET L_452bc3
          add EBX,1
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+8],EDX
          call FUN_433690
          cmp ESI,EBX
          jne L_4150f5
          cmp WORD PTR [ESP+68],0
          mov EBX,DWORD PTR [ESP+76]
          js L_4151a0
          mov DWORD PTR [ESP+4],OFFSET L_452bd3
          mov DWORD PTR [ESP],2
          call FUN_433690
          jmp L_414fa4
L_415143:
          lea EAX,DWORD PTR [EBX+EBX*2]
          add EBP,1
          mov DWORD PTR [EAX*8+L_474a20],0
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
          call FUN_433600
          cmp EAX,2
          jne L_414ecc
L_41517c:
          mov DWORD PTR [ESP+4],OFFSET L_452bd3
          mov DWORD PTR [ESP],2
          call FUN_433690
          call FUN_414be0
          jmp L_414ecc
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4151a0:
          mov DWORD PTR [ESP+4],OFFSET L_452bc9
          mov DWORD PTR [ESP],2
          call FUN_433690
          jmp L_414fa4
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4151c0:
          mov EAX,DWORD PTR [L_479f60]
          mov DWORD PTR [L_474d20],0
          test EAX,EAX
          jne L_4151d4
          ret 
L_4151d4:
          sub ESP,44
          mov EAX,DWORD PTR [L_474a20+20]
          mov EDX,DWORD PTR [L_479f50]
          movzx EDX,BYTE PTR [EDX+EAX*1+8]
          mov EAX,3808
          mov DWORD PTR [ESP+20],3808
          mov DWORD PTR [ESP+4],OFFSET L_452bd8
          mov DWORD PTR [ESP],1
          shl EDX,5
          sub EAX,EDX
          mov DWORD PTR [ESP+16],EDX
          mov ECX,EAX
          mov DWORD PTR [ESP+12],EAX
          shl ECX,14
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [L_474d20],ECX
          call FUN_433690
          add ESP,44
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_415230:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov DWORD PTR [ESP+4],OFFSET L_452c20
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov ECX,DWORD PTR [L_479f68]
          test ECX,ECX
          je L_415282
          call FUN_414960
          test EAX,EAX
          jne L_415402
L_415262:
          mov DWORD PTR [ESP+4],OFFSET L_452d0c
          mov DWORD PTR [ESP],1
          xor EBP,EBP
          call FUN_433690
          add ESP,44
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_415282:
          call FUN_414e90
          mov EBP,EAX
L_415289:
          test EBP,EBP
          je L_415262
          mov DWORD PTR [ESP],OFFSET L_452c47
          call FUN_4490d0
          mov EDX,DWORD PTR [L_479f60]
          mov DWORD PTR [L_474d20],0
          test EDX,EDX
          jne L_4153b0
L_4152b1:
          mov DWORD PTR [ESP+4],OFFSET L_452c5e
          mov DWORD PTR [ESP],1
          mov EBX,OFFSET L_474a20
          call FUN_433690
          mov ESI,1
          jmp L_4152d7
L_4152d1:
          add EBX,24
          add ESI,1
L_4152d7:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_41531d
          cmp ESI,1
          je L_41548a
          mov EAX,DWORD PTR [EBX+8]
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [EBX+12]
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [EBX+16]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EBX+4]
          mov DWORD PTR [ESP+4],OFFSET L_452cbc
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          lea EAX,DWORD PTR [ESI+64]
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
L_41531d:
          cmp ESI,10
          jne L_4152d1
          mov EDX,DWORD PTR [L_474a30]
          add EDX,DWORD PTR [L_479f4c]
          mov EAX,OFFSET L_474d40
          mov EBX,OFFSET L_476d40
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_415340:
          mov EDI,EAX
          mov ESI,EDX
          mov ECX,128
          rep movsd 
          lea ECX,DWORD PTR [EAX+8192]
          lea ESI,DWORD PTR [EDX+512]
          add EDX,1024
          mov EDI,DWORD PTR [EDX-512]
          mov DWORD PTR [EAX+8192],EDI
          mov EDI,DWORD PTR [EDX-4]
          mov DWORD PTR [EAX+8700],EDI
          lea EDI,DWORD PTR [EAX+8196]
          add EAX,512
          and EDI,4294967292
          sub ECX,EDI
          sub ESI,ECX
          add ECX,512
          shr ECX,2
          cmp EBX,EAX
          rep movsd 
          jne L_415340
          mov DWORD PTR [L_474d24],1
          add ESP,44
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4153a7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4153b0:
          mov EAX,DWORD PTR [L_474a20+20]
          mov EDX,DWORD PTR [L_479f50]
          movzx EDX,BYTE PTR [EDX+EAX*1+8]
          mov EAX,3808
          mov DWORD PTR [ESP+20],3808
          mov DWORD PTR [ESP+4],OFFSET L_452bd8
          mov DWORD PTR [ESP],1
          shl EDX,5
          sub EAX,EDX
          mov DWORD PTR [ESP+16],EDX
          mov ECX,EAX
          mov DWORD PTR [ESP+12],EAX
          shl ECX,14
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [L_474d20],ECX
          call FUN_433690
          jmp L_4152b1
L_415402:
          mov ESI,OFFSET L_474b3c
          mov EDI,OFFSET L_474a20
          xor EBX,EBX
          jmp L_41541e
L_415410:
          add EBX,1
          add ESI,4
          add EDI,24
          cmp EBX,10
          je L_415475
L_41541e:
          mov DWORD PTR [ESP],ESI
          call FUN_420ab0
          movzx EBP,AX
          test BP,BP
          je L_415410
          lea EAX,DWORD PTR [ESI+2]
          mov DWORD PTR [ESP],EAX
          call FUN_420ab0
          test AX,AX
          jne L_415480
          test EBX,EBX
          mov EDX,16384
          jne L_415480
L_415447:
          mov DWORD PTR [EDI+8],EBX
          shl EBP,14
          add EBX,1
          mov DWORD PTR [EDI],1
          mov DWORD PTR [EDI+4],1
          add ESI,4
          mov DWORD PTR [EDI+16],EBP
          mov DWORD PTR [EDI+20],0
          add EDI,24
          mov DWORD PTR [EDI-12],EDX
          cmp EBX,10
          jne L_41541e
L_415475:
          mov EBP,DWORD PTR [L_474a20]
          jmp L_415289
L_415480:
          test AX,AX
          je L_415410
          movzx EDX,AX
          jmp L_415447
L_41548a:
          mov EAX,DWORD PTR [L_474a28]
          mov DWORD PTR [ESP+4],OFFSET L_452c70
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [L_474a2c]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [L_474a30]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_474a24]
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          jmp L_4152d1
L_4154c7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4154d0:
          sub ESP,44
          mov DWORD PTR [ESP+4],OFFSET L_452d33
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,DWORD PTR [L_4c9160]
          test EDX,EDX
          je L_4155b1
          cmp BYTE PTR [L_4c8fe4],0
          jne L_4158c0
L_415502:
          cmp EDX,1
          jbe L_4155b1
          cmp BYTE PTR [L_4c8ffa],0
          jne L_415860
L_415518:
          cmp EDX,2
          jbe L_4155b1
          cmp BYTE PTR [L_4c9010],0
          jne L_415800
L_41552e:
          cmp EDX,3
          jbe L_4155b1
          cmp BYTE PTR [L_4c9026],0
          jne L_4157a0
L_415540:
          cmp EDX,4
          jbe L_4155b1
          cmp BYTE PTR [L_4c903c],0
          jne L_415740
L_415552:
          cmp EDX,5
          jbe L_4155b1
          cmp BYTE PTR [L_4c9052],0
          jne L_4156e0
L_415564:
          cmp EDX,6
          jbe L_4155b1
          cmp BYTE PTR [L_4c9068],0
          jne L_415680
L_415576:
          cmp EDX,7
          jbe L_4155b1
          cmp BYTE PTR [L_4c907e],0
          jne L_415624
L_415588:
          cmp EDX,8
          jbe L_4155b1
          cmp BYTE PTR [L_4c9094],0
          jne L_4155d0
L_415596:
          cmp EDX,9
          jbe L_4155b1
          cmp BYTE PTR [L_4c90aa],0
          je L_4155b1
          cmp DWORD PTR [L_474d24],1
          je L_415920
L_4155b1:
          mov DWORD PTR [ESP+4],OFFSET L_452d4e
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESP,44
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4155d0:
          cmp DWORD PTR [L_474d24],1
          jne L_415596
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9130
          mov ECX,OFFSET L_4c9108
          mov EAX,OFFSET L_4c9094
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415596
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415596
L_415624:
          cmp DWORD PTR [L_474d24],1
          jne L_415588
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c912c
          mov ECX,OFFSET L_4c9104
          mov EAX,OFFSET L_4c907e
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415588
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],7
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415588
L_415680:
          cmp DWORD PTR [L_474d24],1
          jne L_415576
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9128
          mov ECX,OFFSET L_4c9100
          mov EAX,OFFSET L_4c9068
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415576
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],6
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415576
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4156e0:
          cmp DWORD PTR [L_474d24],1
          jne L_415564
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9124
          mov ECX,OFFSET L_4c90fc
          mov EAX,OFFSET L_4c9052
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415564
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415564
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_415740:
          cmp DWORD PTR [L_474d24],1
          jne L_415552
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9120
          mov ECX,OFFSET L_4c90f8
          mov EAX,OFFSET L_4c903c
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415552
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],4
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415552
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4157a0:
          cmp DWORD PTR [L_474d24],1
          jne L_415540
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c911c
          mov ECX,OFFSET L_4c90f4
          mov EAX,OFFSET L_4c9026
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415540
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415540
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_415800:
          cmp DWORD PTR [L_474d24],1
          jne L_41552e
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9118
          mov ECX,OFFSET L_4c90f0
          mov EAX,OFFSET L_4c9010
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_41552e
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_41552e
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_415860:
          cmp DWORD PTR [L_474d24],1
          jne L_415518
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9114
          mov ECX,OFFSET L_4c90ec
          mov EAX,OFFSET L_4c8ffa
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415518
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415518
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4158c0:
          cmp DWORD PTR [L_474d24],1
          jne L_415502
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9110
          mov ECX,OFFSET L_4c90e8
          mov EAX,OFFSET L_4c8fe4
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_415502
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_415502
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_415920:
          lea EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9134
          mov ECX,OFFSET L_4c910c
          mov EAX,OFFSET L_4c90aa
          call FUN_4136a0
          test EAX,EAX
          je L_4155b1
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],9
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          jmp L_4155b1
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
FUN_415970:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov ECX,DWORD PTR [L_479f68]
          test ECX,ECX
          jne L_4159a0
          mov EDX,DWORD PTR [L_479f60]
          test EDX,EDX
          je L_415a70
          mov EBX,67108864
          mov ESI,62783488
          jmp L_4159aa
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4159a0:
          mov EBX,50331648
          mov ESI,50315264
L_4159aa:
          mov DWORD PTR [ESP+4],OFFSET L_452d55
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_4159ce
L_4159c0:
          add ESI,512
          cmp ESI,EBX
          jae L_415a5d
L_4159ce:
          mov EAX,DWORD PTR [L_479f4c]
          add EAX,ESI
          mov DWORD PTR [ESP],EAX
          call FUN_40c210
          test EAX,EAX
          je L_4159c0
          mov DWORD PTR [ESP],1024
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [L_47a0fc],EAX
          mov DWORD PTR [ESP+8],ESI
          je L_415aa5
          mov DWORD PTR [ESP+4],OFFSET L_452d74
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESI,DWORD PTR [L_479f4c]
          mov ECX,DWORD PTR [L_47a0fc]
          lea EDI,DWORD PTR [ECX+4]
          mov EAX,DWORD PTR [ESI]
          and EDI,4294967292
          mov DWORD PTR [ECX],EAX
          mov EAX,DWORD PTR [ESI+1020]
          mov DWORD PTR [ECX+1020],EAX
          sub ECX,EDI
          sub ESI,ECX
          add ECX,1024
          shr ECX,2
          rep movsd 
          mov ESI,EBX
          mov DWORD PTR [L_47a100],1024
          add ESI,512
          cmp ESI,EBX
          jb L_4159ce
L_415a5d:
          mov EAX,DWORD PTR [L_47a0fc]
          test EAX,EAX
          je L_415aca
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_415a70:
          mov EBX,DWORD PTR [L_479f54]
          cmp EBX,16777216
          je L_415ac0
          cmp EBX,67108864
          je L_415ae9
          mov DWORD PTR [ESP+4],OFFSET L_452d55
          mov DWORD PTR [ESP],1
          xor ESI,ESI
          call FUN_433690
          test EBX,EBX
          je L_415a5d
          jmp L_4159ce
L_415aa5:
          mov DWORD PTR [ESP+4],OFFSET L_452db0
          mov DWORD PTR [ESP],1
          mov ESI,EBX
          call FUN_433690
          jmp L_4159c0
L_415ac0:
          mov ESI,16236544
          jmp L_4159aa
L_415aca:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_452e09
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
L_415ae9:
          mov ESI,64995328
          jmp L_4159aa
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
FUN_415b00:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [L_479f60]
          mov EBX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBX
          call FUN_40ff40
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
          mov DWORD PTR [ESP+4],OFFSET L_452e18
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_452e50
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_452e80
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_452eb0
          mov DWORD PTR [ESP],0
          call FUN_433690
          test BYTE PTR [L_479f03],16
          jne L_415d55
L_415c05:
          mov DWORD PTR [ESP+4],OFFSET L_452f44
          mov DWORD PTR [ESP],0
          call FUN_433690
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
          call FUN_40fcc0
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
          mov DWORD PTR [ESP+4],OFFSET L_452edc
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_452f0c
          mov DWORD PTR [ESP],0
          call FUN_433690
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
L_415d90:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EDX,DWORD PTR [L_479f74]
          mov ESI,DWORD PTR [ESP+80]
          mov EDI,DWORD PTR [ESP+84]
          mov EBP,DWORD PTR [ESP+88]
          test EDX,EDX
          je L_415e19
          xor EAX,EAX
          xor EBX,EBX
          jmp L_415dba
L_415db3:
          add EBX,1
          cmp EBX,EDX
          jae L_415e10
L_415dba:
          cmp ESI,DWORD PTR [EBX*4+L_479f78]
          jne L_415db3
          cmp DWORD PTR [EBX*4+L_479ff8],-1
          jne L_415db3
          cmp EDI,EBP
          jge L_415db3
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],OFFSET L_452f7c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [EBX*4+L_479ff8],EDI
          mov EDX,DWORD PTR [L_479f74]
          add EBX,1
          mov EAX,1
          cmp EBX,EDX
          jb L_415dba
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_415e10:
          test EAX,EAX
          jne L_415e63
          cmp EDX,32
          je L_415e6b
L_415e19:
          cmp EDI,-1
          je L_415e47
          add EDX,1
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+4],OFFSET L_452fb8
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,DWORD PTR [L_479f74]
L_415e47:
          mov DWORD PTR [EDX*4+L_479f78],ESI
          mov DWORD PTR [EDX*4+L_479ff8],EDI
          add EDX,1
          mov DWORD PTR [L_479f74],EDX
          mov EAX,1
L_415e63:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_415e6b:
          mov DWORD PTR [ESP+4],OFFSET L_452ffc
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+44],EAX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+44]
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_415e90:
          push ESI
          push EBX
          mov ESI,DWORD PTR [ESP+12]
          mov ECX,DWORD PTR [L_479f74]
          lea EAX,DWORD PTR [ESI-1]
          sub ESI,32
L_415ea2:
          test ECX,ECX
          je L_415ee4
          xor EDX,EDX
          xor EBX,EBX
          jmp L_415ec0
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_415eb0:
          cmp DWORD PTR [EDX*4+L_479f78],EAX
          je L_415ec9
          add EDX,1
          cmp ECX,EDX
          jbe L_415ed7
L_415ec0:
          cmp DWORD PTR [EDX*4+L_479ff8],EAX
          jne L_415eb0
L_415ec9:
          mov EDX,ECX
          mov EBX,1
          add EDX,1
          cmp ECX,EDX
          ja L_415ec0
L_415ed7:
          test EBX,EBX
          je L_415ee4
          sub EAX,1
          cmp EAX,ESI
          jge L_415ea2
          xor EAX,EAX
L_415ee4:
          pop EBX
          pop ESI
          ret 
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_415ef0:
          push EBP
          push EDI
          push ESI
          push EBX
          xor ESI,ESI
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_453049
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_45309c
          add ESI,1
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov ECX,DWORD PTR [L_479f74]
          cmp ESI,ECX
          jb L_415f2e
L_415fbb:
          mov DWORD PTR [ESP+4],OFFSET L_452d4e
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_453064
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESI*4+L_479ff8],EDX
          call FUN_433690
          mov ECX,DWORD PTR [L_479f74]
          jmp L_415f23
L_416009:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4530d4
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESI*4+L_479ff8],4294967291
          mov ECX,DWORD PTR [L_479f74]
          jmp L_415f23
L_416037:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_416040:
          sub ESP,28
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],OFFSET L_44a5c0
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_449100
          test EAX,EAX
          setne AL
          add ESP,28
          movzx EAX,AL
          ret 
          .byte 0x90
FUN_416070:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,28
          mov EBP,DWORD PTR [ESP+48]
          cmp EBP,1
          jle L_4160c0
          mov EDI,DWORD PTR [L_479f50]
          mov ESI,1
          lea EBX,DWORD PTR [EDI+16]
          jmp L_41609a
L_416090:
          add ESI,1
          add EBX,16
          cmp EBP,ESI
          je L_4160c0
L_41609a:
          mov DWORD PTR [ESP+8],3
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          call FUN_449100
          test EAX,EAX
          je L_416090
          add ESP,28
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4160c0:
          add ESP,28
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4160d0:
          sub ESP,28
          mov EAX,DWORD PTR [L_479f54]
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],OFFSET L_44a5c0
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_449100
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
          mov DWORD PTR [ESP+4],OFFSET L_45310c
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_416150:
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
          mov DWORD PTR [ESP+4],OFFSET L_45318c
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          call FUN_415b00
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
          mov DWORD PTR [ESP+4],OFFSET L_453354
          mov DWORD PTR [ESP],1
          call FUN_433690
L_416251:
          mov EBX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [L_479f4c]
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
          mov ECX,DWORD PTR [L_479f4c]
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
          mov DWORD PTR [ESP+4],OFFSET L_452f7c
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDI
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_452fb8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EDI
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_452d4e
          mov DWORD PTR [ESP],1
          call FUN_433690
          test BYTE PTR [L_479f03],64
          je L_4166c5
          mov ECX,DWORD PTR [L_479f74]
          mov EAX,1
          test ECX,ECX
          je L_4165d0
          mov DWORD PTR [ESP+4],OFFSET L_4534b8
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+40],EAX
          call FUN_433690
          mov DWORD PTR [L_479f74],0
          mov EAX,DWORD PTR [ESP+40]
          jmp L_4165d0
          .byte 0x66
          .byte 0x90
L_416450:
          mov EDI,EAX
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],OFFSET L_4533a8
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EDI
          mov EBP,EDI
          mov DWORD PTR [ESP+4],OFFSET L_4533ec
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_416251
L_416491:
          mov ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBX
          xor EBX,EBX
          mov DWORD PTR [ESP+4],OFFSET L_4531b4
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],ESI
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_452f7c
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_4531e8
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
          jmp L_4163d0
L_416579:
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+4],OFFSET L_453248
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+8],EDI
          call FUN_433690
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_4532b0
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_4163d0
L_4165ba:
          mov DWORD PTR [ESP+4],OFFSET L_452ffc
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_453310
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+8],EAX
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_452f7c
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_453150
          mov DWORD PTR [ESP],0
          call FUN_433690
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
          call FUN_415ef0
          mov DWORD PTR [ESP+4],OFFSET L_4534e9
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_453538
          add EBX,1
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call FUN_433690
          cmp DWORD PTR [L_479f74],EBX
          ja L_416703
L_416741:
          mov DWORD PTR [ESP+4],OFFSET L_4534fc
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_453510
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+12],EAX
          call FUN_433690
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
          mov DWORD PTR [ESP],OFFSET L_44a5c0
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [ESP+4],EAX
          call FUN_449100
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+40]
          je L_416822
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [ESP],EAX
          call FUN_416070
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+40]
          jne L_416263
          mov DWORD PTR [ESP+4],OFFSET L_453420
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+40],EAX
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_453474
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EAX,DWORD PTR [ESP+40]
          jmp L_4165d0
L_416822:
          mov DWORD PTR [ESP+4],OFFSET L_45310c
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_4165d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
FUN_416840:
          push EDI
          push ESI
          mov EDX,1041204193
          push EBX
          sub ESP,1040
          mov ECX,DWORD PTR [L_478d40]
          mov EAX,ECX
          imul EDX
          mov EAX,ECX
          sar EAX,31
          sar EDX,24
          sub EDX,EAX
          imul EDX,EDX,69206016
          cmp ECX,EDX
          jne L_416a10
          cmp ECX,69206016
          jle L_4169f0
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],OFFSET L_47ad4c
          mov DWORD PTR [ESP],EBX
          call FUN_449080
          mov EDX,EBX
L_416892:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_416892
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
          mov DWORD PTR [ESP+4],OFFSET L_4535a7
          mov DWORD PTR [ESP],EBX
          call FUN_449160
          test EAX,EAX
          mov ESI,EAX
          je L_416a70
          mov DWORD PTR [ESP+8],2
          mov DWORD PTR [ESP+4],69206016
          mov DWORD PTR [ESP],EAX
          call FUN_449138
          test EAX,EAX
          jne L_416a40
          mov EAX,DWORD PTR [L_478d40]
          lea EDI,DWORD PTR [EAX-69206016]
          mov DWORD PTR [ESP],EDI
          call FUN_449108
          test EAX,EAX
          mov EBX,EAX
          je L_416a90
          mov DWORD PTR [ESP+4],OFFSET L_453649
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [L_478d40]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP],EBX
          sub EAX,69206016
          mov DWORD PTR [ESP+4],EAX
          call FUN_449148
          mov DWORD PTR [ESP],ESI
          call FUN_449190
          mov DWORD PTR [ESP+4],OFFSET L_453664
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,DWORD PTR [ESP+1060]
          test EAX,EAX
          je L_4169af
          mov EAX,DWORD PTR [L_478d40]
          mov DWORD PTR [ESP+4],EBX
          sub EAX,69206016
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+1060]
          mov DWORD PTR [ESP],EAX
          call FUN_434960
L_4169af:
          mov EAX,DWORD PTR [ESP+1056]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [L_478d40]
          sub EAX,69206016
          mov DWORD PTR [ESP+4],EAX
          call FUN_449118
          mov DWORD PTR [ESP],EBX
          call FUN_449140
          add ESP,1040
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
L_4169f0:
          mov DWORD PTR [ESP+4],OFFSET L_453594
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
L_416a06:
          add ESP,1040
          pop EBX
          pop ESI
          pop EDI
          ret 
L_416a10:
          mov DWORD PTR [ESP+8],69206016
          mov DWORD PTR [ESP+4],OFFSET L_45355c
          mov DWORD PTR [ESP],0
          call FUN_433690
          add ESP,1040
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_416a40:
          mov DWORD PTR [ESP+8],69206016
          mov DWORD PTR [ESP+4],OFFSET L_4535e4
L_416a50:
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP],ESI
          call FUN_449190
          add ESP,1040
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          ret 
L_416a70:
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_4535ac
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416a06
          .byte 0x90
L_416a90:
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],OFFSET L_453610
          jmp L_416a50
          .byte 0x66
          .byte 0x90
FUN_416aa0:
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
          mov DWORD PTR [ESP+4],OFFSET L_4537b4
          mov DWORD PTR [ESP],0
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_453760
          mov DWORD PTR [ESP],1
          sar EDX,12
          mov EDI,EDX
          sub EDI,EBX
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_45378c
          mov DWORD PTR [ESP],1
          mov EBX,EDI
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_4536e0
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_4536b8
          mov DWORD PTR [ESP],1
          call FUN_433690
          cmp EBX,69206015
          jle L_416cb0
          mov DWORD PTR [L_479f60],1
          mov DWORD PTR [L_479f64],1
          mov EAX,1
          jmp L_416ae7
L_416c22:
          mov DWORD PTR [ESP+4],OFFSET L_453694
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_4536b8
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          mov DWORD PTR [ESP+4],OFFSET L_4536b8
          mov DWORD PTR [ESP],1
          mov EBX,EDI
          call FUN_433690
          mov DWORD PTR [L_479f64],1
          mov DWORD PTR [ESP+28],1
          jmp L_416b40
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_416cb0:
          mov DWORD PTR [ESP+4],OFFSET L_453708
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416ae7
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_416cd0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,732
          mov EDI,DWORD PTR [ESP+756]
          mov EBP,DWORD PTR [ESP+752]
          mov DWORD PTR [ESP],EDI
          call FUN_4224d0
          mov DWORD PTR [ESP+8],EBP
          mov ESI,EDX
          mov DWORD PTR [ESP+12],EAX
          mov DWORD PTR [ESP+16],EDX
          mov DWORD PTR [ESP+4],OFFSET L_453810
          mov EBX,EAX
          mov DWORD PTR [ESP],1
          call FUN_433690
          cmp ESI,0
          jle L_416f70
L_416d1d:
          lea EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],128
          mov DWORD PTR [ESP],EAX
          call FUN_449148
          mov DWORD PTR [ESP],EDI
          call FUN_4490a8
          movzx EDX,WORD PTR [ESP+64]
          mov EAX,EDX
          movzx EDX,DH
          shl EAX,8
          and EAX,65280
          add EAX,EDX
          cmp EAX,65359
          jne L_416db0
          mov EAX,DWORD PTR [ESP+72]
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
          cmp ESI,0
          jg L_416dd9
          jge L_416dd5
L_416d8e:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4538ac
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_416db0:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45386c
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
L_416dca:
          add ESP,732
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_416dd5:
          cmp EBX,EAX
          jb L_416d8e
L_416dd9:
          mov EAX,DWORD PTR [ESP+76]
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
          cmp ESI,0
          mov DWORD PTR [ESP+44],EAX
          jg L_416e34
          jge L_416e30
L_416e0b:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4538ec
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
L_416e27:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_416e30:
          cmp EBX,EAX
          jb L_416e0b
L_416e34:
          mov EAX,DWORD PTR [ESP+160]
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
          add EDX,EAX
          cmp EDX,32768
          ja L_417100
          mov EAX,DWORD PTR [ESP+164]
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
          add EDX,EAX
          cmp ESI,0
          jl L_4170e0
          jle L_4170d0
L_416ea3:
          cmp DWORD PTR [ESP+44],EDX
          ja L_4170e0
          movzx EDX,WORD PTR [ESP+168]
          mov EAX,EDX
          movzx EDX,DH
          shl EAX,8
          and EAX,65280
          add EAX,EDX
          cmp EAX,2
          je L_416ee1
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4539b4
          mov DWORD PTR [ESP],0
          call FUN_433690
L_416ee1:
          movzx EDX,WORD PTR [ESP+170]
          mov EAX,EDX
          movzx EDX,DH
          shl EAX,8
          and EAX,65280
          add EAX,EDX
          cmp EAX,1810
          je L_416f17
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453a0c
          mov DWORD PTR [ESP],0
          call FUN_433690
L_416f17:
          mov EAX,DWORD PTR [ESP+172]
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
          cmp ESI,0
          jg L_416fb4
          jge L_416fb0
L_416f48:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453a68
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
L_416f67:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_416f70:
          jl L_416f7e
          cmp EBX,17301503
          ja L_416d1d
L_416f7e:
          mov DWORD PTR [ESP+12],EBX
          mov DWORD PTR [ESP+16],ESI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453828
          mov DWORD PTR [ESP],0
          call FUN_433690
          add ESP,732
          xor EAX,EAX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_416fb0:
          cmp EBX,EAX
          jb L_416f48
L_416fb4:
          mov EAX,DWORD PTR [ESP+176]
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
          cmp ESI,0
          jg L_417008
          jge L_417004
L_416fe5:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453aac
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
L_417004:
          cmp EBX,EAX
          jb L_416fe5
L_417008:
          mov EAX,DWORD PTR [ESP+180]
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
          add EDX,EAX
          jne L_417120
L_417038:
          mov EDX,DWORD PTR [ESP+184]
          mov ECX,EDX
          mov EAX,EDX
          shr EAX,24
          shl ECX,24
          add ECX,EAX
          mov EAX,EDX
          shr EDX,8
          shl EAX,8
          and EDX,65280
          and EAX,16711680
          add EAX,ECX
          add EDX,EAX
          and DH,247
          cmp EDX,12288
          jne L_417140
          mov EAX,DWORD PTR [ESP+188]
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
          cmp ESI,0
          jg L_417168
          jge L_417160
L_4170aa:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453b98
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4170d0:
          cmp EBX,EDX
          jae L_416ea3
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4170e0:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_45396c
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
          .byte 0x90
L_417100:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453928
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
          .byte 0x90
L_417120:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453af4
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_417038
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_417140:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_453b48
          mov DWORD PTR [ESP],0
          call FUN_433690
          xor EAX,EAX
          jmp L_416dca
          .byte 0x90
L_417160:
          cmp EBX,EAX
          jb L_4170aa
L_417168:
          cmp ESI,0
          jle L_417261
L_417171:
          lea EBP,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+12],0
          mov DWORD PTR [ESP+4],50331648
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP],EDI
          call FUN_448af0
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],4
          mov DWORD PTR [ESP],EBP
          call FUN_449148
          mov DWORD PTR [ESP],EDI
          call FUN_4490a8
          mov DWORD PTR [ESP],EBP
          call FUN_420ad0
          cmp EAX,1481916742
          je L_417273
          lea EBP,DWORD PTR [ESP+192]
          mov DWORD PTR [ESP],EDI
          call FUN_4490a8
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],528
          mov DWORD PTR [ESP],EBP
          call FUN_449148
          mov DWORD PTR [ESP],EDI
          call FUN_4490a8
          lea EAX,DWORD PTR [ESP+704]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],EAX
          call FUN_40fc30
          test EAX,EAX
          je L_41728e
          cmp ESI,0
          jle L_4172a9
L_41721f:
          mov DWORD PTR [ESP+4],OFFSET L_453c9c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,69206016
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_417240:
          mov DWORD PTR [ESP+4],OFFSET L_453d18
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+44],EAX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+44]
          jmp L_416dca
L_417261:
          jl L_41726f
          cmp EBX,50331648
          ja L_417171
L_41726f:
          mov EAX,EBX
          jmp L_417240
L_417273:
          mov DWORD PTR [ESP+4],OFFSET L_453bdc
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,50331648
          jmp L_417240
L_41728e:
          mov DWORD PTR [ESP+4],OFFSET L_453c28
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EAX,50331648
          jmp L_417240
L_4172a9:
          jl L_41726f
          cmp EBX,69206016
          ja L_41721f
          mov EAX,EBX
          jmp L_417240
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_4172c0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov ESI,DWORD PTR [L_479f4c]
          mov EAX,DWORD PTR [ESI+8]
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
          cmp EBX,DWORD PTR [L_479f54]
          jae L_4173c0
          lea EDI,DWORD PTR [ESI+EBX*1]
          movzx EAX,WORD PTR [EDI]
          rol AX,8
          and AX,17407
          cmp AX,17218
          je L_417330
          mov DWORD PTR [ESP+4],OFFSET L_453d78
          mov DWORD PTR [ESP],1
          call FUN_433690
L_417326:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_417330:
          lea EAX,DWORD PTR [ESI+EBX*1+16]
          mov DWORD PTR [ESP],EAX
          call FUN_41ac70
          mov EAX,DWORD PTR [EDI+12]
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          lea ECX,DWORD PTR [ECX+EDX*1+15]
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          and EAX,4294967280
          add EBX,EAX
          test BYTE PTR [EDI+6],8
          je L_417419
          cmp EBX,DWORD PTR [L_479f54]
          jae L_417520
          mov EDX,DWORD PTR [L_479f4c]
          lea EDI,DWORD PTR [EDX+EBX*1]
          movzx EAX,WORD PTR [EDI]
          rol AX,8
          and AX,17407
          cmp AX,17218
          je L_4173e0
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_453dec
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4173c0:
          mov DWORD PTR [ESP+4],OFFSET L_453d3c
          mov DWORD PTR [ESP],1
          call FUN_433690
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
L_4173e0:
          lea EAX,DWORD PTR [EDX+EBX*1+16]
          mov DWORD PTR [ESP],EAX
          call FUN_41aca0
          mov EAX,DWORD PTR [EDI+12]
          mov ECX,EAX
          mov EDX,EAX
          shr EDX,24
          shl ECX,24
          lea ECX,DWORD PTR [ECX+EDX*1+15]
          mov EDX,EAX
          shr EAX,8
          shl EDX,8
          and EAX,65280
          and EDX,16711680
          add EDX,ECX
          add EAX,EDX
          and EAX,4294967280
          add EBX,EAX
L_417419:
          cmp EBX,DWORD PTR [L_479f54]
          jae L_417500
          mov EDX,DWORD PTR [L_479f4c]
          lea EDI,DWORD PTR [EDX+EBX*1]
          movzx EAX,WORD PTR [EDI]
          rol AX,8
          and AX,17407
          cmp AX,17220
          je L_417460
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_453e64
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_417460:
          lea EAX,DWORD PTR [EDX+EBX*1+16]
          mov DWORD PTR [ESP],EAX
          call FUN_41acd0
          mov EDI,DWORD PTR [EDI+12]
          mov EDX,EDI
          mov EAX,EDI
          shl EDX,24
          shr EAX,24
          lea ECX,DWORD PTR [EDX+EAX*1+15]
          mov EAX,EDI
          shr EDI,8
          shl EAX,8
          and EDI,65280
          and EAX,16711680
          lea EDX,DWORD PTR [ECX+EAX*1]
          lea EAX,DWORD PTR [EDX+EDI*1]
          and EAX,4294967280
          add EBX,EAX
          cmp EBX,DWORD PTR [L_479f54]
          jae L_4174e0
          mov EDX,DWORD PTR [L_479f4c]
          movzx EAX,WORD PTR [EDX+EBX*1]
          rol AX,8
          and AX,17407
          cmp AX,17221
          je L_417540
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_453edc
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4174e0:
          mov DWORD PTR [ESP+4],OFFSET L_453ea4
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_417500:
          mov DWORD PTR [ESP+4],OFFSET L_453e2c
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_417520:
          mov DWORD PTR [ESP+4],OFFSET L_453db0
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_417540:
          lea EAX,DWORD PTR [EDX+EBX*1+16]
          mov DWORD PTR [ESP],EAX
          call FUN_41ad00
          mov EAX,DWORD PTR [ESI+100]
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
          cmp EBX,DWORD PTR [L_479f54]
          jae L_41762c
          mov EDX,DWORD PTR [L_479f4c]
          lea ESI,DWORD PTR [EDX+EBX*1]
          movzx EAX,WORD PTR [ESI]
          rol AX,8
          and AX,17407
          cmp AX,17222
          je L_4175b5
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_453f54
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
L_4175b5:
          lea EAX,DWORD PTR [EDX+EBX*1+32]
          mov DWORD PTR [ESP],EAX
          call FUN_41ad30
          mov EDX,DWORD PTR [ESI+12]
          mov ECX,EDX
          mov EAX,EDX
          shl ECX,24
          shr EAX,24
          lea EAX,DWORD PTR [ECX+EAX*1+15]
          mov ECX,EDX
          shr EDX,8
          shl ECX,8
          and EDX,65280
          and ECX,16711680
          add EAX,ECX
          add EAX,EDX
          and EAX,4294967280
          add EBX,EAX
          cmp EBX,DWORD PTR [L_479f54]
          jae L_417660
          mov EDX,DWORD PTR [L_479f4c]
          movzx EAX,WORD PTR [EDX+EBX*1]
          rol AX,8
          and AX,17407
          cmp AX,17223
          je L_417645
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],OFFSET L_453fcc
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
L_41762c:
          mov DWORD PTR [ESP+4],OFFSET L_453f1c
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
L_417645:
          lea EAX,DWORD PTR [EDX+EBX*1+16]
          mov DWORD PTR [ESP],EAX
          call FUN_41ad60
          mov DWORD PTR [L_479ec0],0
          jmp L_417326
L_417660:
          mov DWORD PTR [ESP+4],OFFSET L_453f94
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417326
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_417680:
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
          call FUN_449080
L_4176a9:
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [L_478d40],0
          test EAX,EAX
          je L_4176c4
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_4176c4:
          mov EAX,DWORD PTR [L_479f4c]
          test EAX,EAX
          je L_4176d5
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_4176d5:
          mov EBX,OFFSET L_47a08c
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [L_479f4c],0
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
          call FUN_449140
L_41771e:
          add ESI,8
          cmp ESI,OFFSET L_47a0e0+4
          jne L_417710
          mov ESI,OFFSET L_479ea0
          mov EDI,ESI
L_417730:
          mov EAX,DWORD PTR [EDI+580]
          test EAX,EAX
          je L_417742
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417742:
          mov DWORD PTR [EDI+584],0
          add EDI,8
          cmp EDI,OFFSET L_479ec0
          jne L_417730
          mov EAX,DWORD PTR [L_47a104]
          test EAX,EAX
          je L_417768
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417768:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_454009
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP+4],OFFSET L_4535a7
          mov DWORD PTR [ESP],EBP
          call FUN_449160
          test EAX,EAX
          mov EDI,EAX
          je L_417d8b
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],EBP
          call FUN_416cd0
          test EAX,EAX
          mov ECX,EAX
          je L_417b20
          cmp EAX,50331648
          mov DWORD PTR [L_478d40],EAX
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
          call FUN_449108
          test EAX,EAX
          mov DWORD PTR [ESP+28],EAX
          mov ECX,DWORD PTR [ESP+36]
          je L_417db0
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP+4],OFFSET L_454114
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+36],ECX
          call FUN_433690
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_449148
          mov DWORD PTR [ESP],EDI
          call FUN_449190
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_452d4e
          mov DWORD PTR [ESP],1
          call FUN_433690
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
          call FUN_449108
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [L_479f4c],EAX
          mov DWORD PTR [ESP+32],EAX
          call FUN_449108
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
          call FUN_4490f0
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],255
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f0
          mov DWORD PTR [ESP+4],OFFSET L_45417c
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov ECX,DWORD PTR [ESP+32]
          mov EDI,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EDI
          call FUN_416aa0
          test EAX,EAX
          je L_417d6c
          mov EAX,DWORD PTR [L_479f68]
          test EAX,EAX
          jne L_417a70
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_416150
          test EAX,EAX
          mov EDI,EAX
          jne L_417c40
L_417966:
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [L_478d40],0
          test EAX,EAX
          je L_417981
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417981:
          mov EAX,DWORD PTR [L_479f4c]
          test EAX,EAX
          je L_417992
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417992:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [L_479f4c],0
          mov DWORD PTR [L_479f50],0
          mov DWORD PTR [L_479f6c],0
          mov DWORD PTR [L_479f70],0
L_4179c4:
          mov EAX,DWORD PTR [EBX]
          test EAX,EAX
          je L_4179d2
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_4179d2:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_4179c4
L_4179dd:
          mov EAX,DWORD PTR [ESI+580]
          test EAX,EAX
          je L_4179ef
          mov DWORD PTR [ESP],EAX
          call FUN_449140
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
          call FUN_449140
L_417a17:
          mov EAX,DWORD PTR [ESP+28]
L_417a1b:
          mov DWORD PTR [ESP],EAX
          call FUN_449140
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
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP],EAX
          call FUN_4490f8
          mov EAX,DWORD PTR [L_479f4c]
          mov DWORD PTR [ESP+8],14
          mov DWORD PTR [ESP],OFFSET L_44a5c0
          add EAX,16
          mov DWORD PTR [ESP+4],EAX
          call FUN_449100
          test EAX,EAX
          jne L_417c40
          mov DWORD PTR [ESP+4],OFFSET L_45310c
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_417966
L_417ada:
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_454098
L_417aea:
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov DWORD PTR [ESP],EDI
          xor EDI,EDI
          call FUN_449190
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
          mov DWORD PTR [ESP+4],OFFSET L_454044
          jmp L_417aea
          .byte 0x90
L_417b20:
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [L_478d40],0
          test EAX,EAX
          je L_417b3b
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417b3b:
          mov EAX,DWORD PTR [L_479f4c]
          test EAX,EAX
          je L_417b4c
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417b4c:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [L_479f4c],0
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
          call FUN_449140
L_417b8e:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_417b80
L_417b99:
          mov EAX,DWORD PTR [ESI+580]
          test EAX,EAX
          je L_417bab
          mov DWORD PTR [ESP],EAX
          call FUN_449140
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
          call FUN_449080
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
          call FUN_413d30
          call FUN_413ad0
          call FUN_415970
          call FUN_4138c0
          call FUN_415230
          test EAX,EAX
          je L_417c78
          mov EAX,DWORD PTR [L_479f00]
          test EAX,536870912
          je L_417f27
L_417c6d:
          test EAX,67108864
          je L_417dd7
L_417c78:
          call FUN_4172c0
          jmp L_417a17
L_417c82:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_454138
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov EAX,DWORD PTR [L_479f50]
          mov DWORD PTR [L_478d40],0
          test EAX,EAX
          je L_417cb5
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417cb5:
          mov EAX,DWORD PTR [L_479f4c]
          test EAX,EAX
          je L_417cc6
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417cc6:
          mov DWORD PTR [L_479f74],0
          mov DWORD PTR [L_479f4c],0
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
          call FUN_449140
L_417d0e:
          add EBX,8
          cmp EBX,OFFSET L_47a0e0+4
          jne L_417d00
L_417d19:
          mov EAX,DWORD PTR [ESI+580]
          test EAX,EAX
          je L_417d2b
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417d2b:
          mov DWORD PTR [ESI+584],0
          add ESI,8
          cmp ESI,OFFSET L_479ec0
          jne L_417d19
          mov EAX,DWORD PTR [L_47a104]
          test EAX,EAX
          je L_417d51
          mov DWORD PTR [ESP],EAX
          call FUN_449140
L_417d51:
          mov EAX,DWORD PTR [ESP+28]
          xor EDI,EDI
          mov DWORD PTR [ESP],EAX
          call FUN_449140
          add ESP,1100
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_417d6c:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4541b0
          xor EDI,EDI
          mov DWORD PTR [ESP],0
          call FUN_433690
          jmp L_417a17
L_417d8b:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_454025
          mov DWORD PTR [ESP],1
          call FUN_433690
          add ESP,1100
          mov EAX,EDI
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_417db0:
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_4540dc
          mov DWORD PTR [ESP],0
          call FUN_433690
          mov DWORD PTR [ESP],EDI
          xor EDI,EDI
          call FUN_449190
          jmp L_417a23
L_417dd7:
          mov DWORD PTR [ESP+4],OFFSET L_452d33
          mov DWORD PTR [ESP],1
          call FUN_433690
          mov EDX,DWORD PTR [L_4c9160]
          test EDX,EDX
          je L_417f0e
          cmp BYTE PTR [L_4c8fe4],0
          je L_417e0f
          cmp DWORD PTR [L_474d24],1
          je L_417f77
L_417e0f:
          cmp EDX,1
          jbe L_417f0e
          cmp BYTE PTR [L_4c8ffa],0
          je L_417e2e
          cmp DWORD PTR [L_474d24],1
          je L_4180b3
L_417e2e:
          cmp EDX,2
          jbe L_417f0e
          cmp BYTE PTR [L_4c9010],0
          je L_417e4d
          cmp DWORD PTR [L_474d24],1
          je L_418102
L_417e4d:
          cmp EDX,3
          jbe L_417f0e
          cmp BYTE PTR [L_4c9026],0
          je L_417e6c
          cmp DWORD PTR [L_474d24],1
          je L_418151
L_417e6c:
          cmp EDX,4
          jbe L_417f0e
          cmp BYTE PTR [L_4c903c],0
          je L_417e8b
          cmp DWORD PTR [L_474d24],1
          je L_4181a0
L_417e8b:
          cmp EDX,5
          jbe L_417f0e
          cmp BYTE PTR [L_4c9052],0
          je L_417ea6
          cmp DWORD PTR [L_474d24],1
          je L_4181ef
L_417ea6:
          cmp EDX,6
          jbe L_417f0e
          cmp BYTE PTR [L_4c9068],0
          je L_417ec1
          cmp DWORD PTR [L_474d24],1
          je L_417fc6
L_417ec1:
          cmp EDX,7
          jbe L_417f0e
          cmp BYTE PTR [L_4c907e],0
          je L_417edc
          cmp DWORD PTR [L_474d24],1
          je L_418015
L_417edc:
          cmp EDX,8
          jbe L_417f0e
          cmp BYTE PTR [L_4c9094],0
          je L_417ef7
          cmp DWORD PTR [L_474d24],1
          je L_418064
L_417ef7:
          cmp EDX,9
          jbe L_417f0e
          cmp BYTE PTR [L_4c90aa],0
          je L_417f0e
          cmp DWORD PTR [L_474d24],1
          je L_417f3b
L_417f0e:
          mov DWORD PTR [ESP+4],OFFSET L_452d4e
          mov DWORD PTR [ESP],1
          call FUN_433690
          jmp L_417c78
L_417f27:
          call FUN_414300
          call FUN_414050
          mov EAX,DWORD PTR [L_479f00]
          jmp L_417c6d
L_417f3b:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9134
          mov ECX,OFFSET L_4c910c
          mov EAX,OFFSET L_4c90aa
          call FUN_4136a0
          test EAX,EAX
          je L_417f0e
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],9
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          jmp L_417f0e
L_417f77:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9110
          mov ECX,OFFSET L_4c90e8
          mov EAX,OFFSET L_4c8fe4
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417e0f
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417e0f
L_417fc6:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9128
          mov ECX,OFFSET L_4c9100
          mov EAX,OFFSET L_4c9068
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417ec1
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],6
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417ec1
L_418015:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c912c
          mov ECX,OFFSET L_4c9104
          mov EAX,OFFSET L_4c907e
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417edc
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],7
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417edc
L_418064:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9130
          mov ECX,OFFSET L_4c9108
          mov EAX,OFFSET L_4c9094
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417ef7
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],8
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417ef7
L_4180b3:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9114
          mov ECX,OFFSET L_4c90ec
          mov EAX,OFFSET L_4c8ffa
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417e2e
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],1
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417e2e
L_418102:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9118
          mov ECX,OFFSET L_4c90f0
          mov EAX,OFFSET L_4c9010
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417e4d
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],2
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417e4d
L_418151:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c911c
          mov ECX,OFFSET L_4c90f4
          mov EAX,OFFSET L_4c9026
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417e6c
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],3
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417e6c
L_4181a0:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9120
          mov ECX,OFFSET L_4c90f8
          mov EAX,OFFSET L_4c903c
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417e8b
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],4
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417e8b
L_4181ef:
          lea EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],OFFSET L_4c9124
          mov ECX,OFFSET L_4c90fc
          mov EAX,OFFSET L_4c9052
          call FUN_4136a0
          test EAX,EAX
          mov EDX,DWORD PTR [L_4c9160]
          je L_417ea6
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP],5
          mov DWORD PTR [ESP+4],EAX
          call FUN_4144e0
          mov EDX,DWORD PTR [L_4c9160]
          jmp L_417ea6
          .byte 0x90
          .byte 0x90

.data
.p2align 5
L_44a5c0:
          .string "zeropair image"
          .zero 1
L_44a5d0:
          .ascii "Mobile"
L_44a5d6:
          .string "A"
L_44a5d8:
          .long L_474d40
          .zero 4

.section .rdata,"dr"
.p2align 3
L_4521b8:
          .string "%s found in sector 0x%x size 0x%x..."
          .zero 3
L_4521e0:
          .string "Did not find a LDV value to use, setting it to 0 for devkit!\n"
          .zero 2
L_452220:
          .string "Did not find a LDV value to use, setting it to 0 for testkit!\n"
          .zero 1
L_452260:
          .string "***** WARNING: could not find a non-zero CF LDV to use, setting it to 1 but that may be incorrect!\n"
L_4522c4:
          .string "setting LDV from image to %d\n"
          .zero 2
L_4522e4:
          .string "setting pairing data from image to 0x%06x\n"
L_45230f:
          .string "LDV was already set to %d\n"
          .zero 2
L_45232c:
          .string "smc.bin should not be at 0x%x, trying 0x1000\n"
          .zero 2
L_45235c:
          .string "smc.bin should not be 0x%x bytes, using 0x3800\n"
L_45238c:
          .string "smc.bin should not be 0x%x bytes, using 0x3000\n"
L_4523bc:
          .string "decrypting SMC at address 0x%x of size 0x%x\n"
          .zero 3
L_4523ec:
          .string "SMC decrypted OK, will use if no external smc.bin is provided\n"
          .zero 1
L_45242c:
          .string "SMC did not decrypt, discarding it\n"
L_452450:
          .string "Wasn't able to alloc 0x%x bytes memory for SMC bin, not using...\n"
          .zero 2
L_452494:
          .string "SMC at 0x%x of size 0x%x is not sane, skipping smc.bin in NAND image\n"
          .zero 2
L_4524dc:
          .string "KeyVault cannot be at 0x0, trying 0x4000\n"
          .zero 2
L_452508:
          .string "KeyVault cannot be 0x%x bytes, using 0x4000\n"
          .zero 3
L_452538:
          .string "decrypting KeyVault at address 0x%x of size 0x%x\n"
          .zero 2
L_45256c:
          .string "keyvault decrypted OK, will use if no kv.bin is provided\n"
          .zero 2
L_4525a8:
          .string "keyvault decrypt failed, discarding\n"
          .zero 3
L_4525d0:
          .string "Wasn't able to alloc 0x4000 bytes memory for KeyVault bin, not using...\n"
          .zero 3
L_45261c:
          .string "KeyVault at address 0x%x of size 0x4000 is not sane, skipping KeyVault in NAND image\n"
          .zero 2
L_452674:
          .string "decrypting alt KeyVault at address 0x%x of size 0x%x\n"
          .zero 2
L_4526ac:
          .string "alt KeyVault decrypted OK, will use if no kv_alt.bin is provided\n"
          .zero 2
L_4526f0:
          .string "alt KeyVault decrypt failed, discarding\n"
          .zero 3
L_45271c:
          .string "Wasn't able to alloc 0x4000 bytes memory for alt KeyVault bin, not using...\n"
          .zero 3
L_45276c:
          .string "Unable to allocate memory for %s 0x%x bytes\n"
L_452799:
          .string "%s.dat"
L_4527a0:
          .string "extracting %s from page 0x%x (offset 0x%x), size %d (0x%x) bytes\n"
          .zero 2
L_4527e4:
          .string "Statistics.settings found at offset 0x%x, size %d (0x%x) bytes\n"
L_452824:
          .string "Unable to allocate memory for Statistics.settings 0x%x bytes\n"
          .zero 2
L_452864:
          .string "Manufacturing.data found at offset 0x%x, size %d (0x%x) bytes\n"
          .zero 1
L_4528a4:
          .string "Unable to allocate memory for Manufacturing.data 0x%x bytes\n"
L_4528e1:
          .string "netKd info found, size 0x%x\n"
L_4528fe:
          .string "    version : 0x%x\n"
L_452912:
          .string "    xbox IP : %d.%d.%d.%d\n"
          .zero 3
L_452930:
          .string "    xbox MAC: %02x:%02x:%02x:%02x:%02x\n"
L_452958:
          .string "    port    : %d\n"
L_45296a:
          .string "    host IP : %d.%d.%d.%d\n"
          .zero 3
L_452988:
          .string "sector: 0x%04x offset: 0x%08x size: 0x%08x timestamp: 0x%08x name: %s\n"
          .zero 1
L_4529d0:
          .string "attempting to find valid anchor block\n"
          .zero 1
L_4529f8:
          .string "anchor block v %d at 0x2fe8000 is valid\n"
          .zero 3
L_452a24:
          .string "anchor block at 0x2fe8000 is invalid\n"
          .zero 2
L_452a4c:
          .string "anchor block v %d at 0x2fec000 is valid\n"
          .zero 3
L_452a78:
          .string "anchor block v %d at 0x2fec000 is selected\n"
L_452aa4:
          .string "anchor block at 0x2fec000 is invalid\n"
          .zero 2
L_452acc:
          .string "anchor block v %d at 0x2fe8000 is selected\n"
L_452af8:
          .string "Showing all pages with mobile info:\n"
          .zero 3
L_452b20:
          .string "starting mobile scan at page 0x%x (offset 0x%x) of 0x%x pages (0x%x total)\n"
L_452b6c:
          .string "mobile%c.dat ver %02d offset 0x%08x (dump:0x%08x) count 0x%02x len 0x%04x page 0x%08x "
L_452bc3:
          .string "%02x "
L_452bc9:
          .string "(DELETE)\n"
L_452bd3:
          .string "\n"
          .zero 3
L_452bd8:
          .string "bigblock file system offset set to 0x%x fsb: %x meta: %x lbaend: %x\n"
          .zero 3
L_452c20:
          .string "Scanning for mobile data and fsroot..."
L_452c47:
          .string "done! fsroot found ok!"
L_452c5e:
          .string "Mobiles found:\n"
          .zero 2
L_452c70:
          .string "    fsroot      version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n"
L_452cbc:
          .string "    mobile%c.dat version %02d found at offset 0x%08x len 0x%04x page 0x%08x\n"
          .zero 3
L_452d0c:
          .string "\n\n***** ERROR! Could not find fsroot!\n"
L_452d33:
          .string "seeking security files...\n"
L_452d4e:
          .string "done!\n"
L_452d55:
          .string "seeking smc config in dump..."
          .zero 1
L_452d74:
          .string "found at offset 0x%x! Using if no smc config is provided.\n"
          .zero 1
L_452db0:
          .string "found at offset 0x%x! Unable to allocate 0x400 bytes of memory for smc config, skipping\n"
L_452e09:
          .string "not found!\n"
          .zero 3
L_452e18:
          .string "\n\n****************  WARNING  *************************\n"
L_452e50:
          .string "  nanddump.bin has NAND memory unit data, make\n"
L_452e80:
          .string "  sure you back up any important data off the\n"
          .zero 1
L_452eb0:
          .string "  internal MU before flashing a new image!\n"
L_452edc:
          .string "\n  xeBuild will attempt to keep this data, but\n"
L_452f0c:
          .string "  many things could cause it to be invalid/corrupt.\n"
          .zero 3
L_452f44:
          .string "****************************************************\n\n"
          .zero 1
L_452f7c:
          .string "block 0x%x was remapped to block 0x%x at remap instance %d\n"
L_452fb8:
          .string "block 0x%x was remapped to block 0x%x, entering remap instance %d\n"
          .zero 1
L_452ffc:
          .string "MAX REMAPS of 32 exceeded, remapping disabled and image rejected as faulty!\n"
L_453049:
          .string "cleaning up stray remaps\n"
          .zero 1
L_453064:
          .string "block 0x%x had no remap, assigning remap block 0x%x\n"
          .zero 3
L_45309c:
          .string "block 0x%x had no remap, and I could not assign one!\n"
          .zero 2
L_4530d4:
          .string "block 0x%x had no need of remap, it's in the wear area\n"
L_45310c:
          .string "\n\n***** ERROR: nanddump.bin is a ZEROPAIR/XELL image, discarding\n"
          .zero 2
L_453150:
          .string "UNEXPECTED DUMP PARSE ERROR: %d pages cannot divide by %d!\n"
L_45318c:
          .string "parsing dump into user and spare...\n"
          .zero 3
L_4531b4:
          .string "bad block at 0x%x (raw offset 0x%x), block ignored\n"
L_4531e8:
          .string "***** WARNING: nanddump.bin has a bad LBA at block 0x%x (raw offset 0x%x), block LBA ignored\n"
          .zero 2
L_453248:
          .string "***** WARNING: nanddump.bin has a mixed controller LBA at block 0x%x (raw offset 0x%x), block ignored\n"
          .zero 1
L_4532b0:
          .string "               this is likely caused by previously using jaspersb on a jasper type console!\n"
          .zero 3
L_453310:
          .string "ECD error at block 0x%x (raw offset 0x%x), block will be remapped\n"
          .zero 1
L_453354:
          .string "copying nanddump data from block 0x%x to block 0x%x for file extraction integrity\n"
          .zero 1
L_4533a8:
          .string "***** WARNING: ignoring possible remap of block 0x%x to block 0x%x\n"
L_4533ec:
          .string "               this dump may have some bad data!\n"
          .zero 2
L_453420:
          .string "\n\n***** ERROR: nanddump.bin has mixed LBA in the same block which usually occurs\n"
          .zero 2
L_453474:
          .string "             due to an improper nandpro write method, discarding\n"
          .zero 2
L_4534b8:
          .string "Discarding remap data as NOREMAP was specified!\n"
L_4534e9:
          .string "--remap summary--\n"
L_4534fc:
          .string "-----------------\n"
          .zero 1
L_453510:
          .string "%d: source: 0x%04x dest: (NONE/BAD)\n"
          .zero 3
L_453538:
          .string "%d: source: 0x%04x dest: 0x%04x\n"
          .zero 3
L_45355c:
          .string "size is not a multiple of %d bytes, not copying data..\n"
L_453594:
          .string "no data to copy..\n"
L_4535a7:
          .string "rb"
          .zero 2
L_4535ac:
          .string "could not re-open '%s' for reading, not copying data..\n"
L_4535e4:
          .string "could not seek to 0x%x, not copying data..\n"
L_453610:
          .string "could not allocate 0x%x byte buffer, not copying data..\n"
L_453649:
          .string "reading nanddump.bin...\n"
          .zero 2
L_453664:
          .string "writing nanddump.bin MU area to output file..."
          .zero 1
L_453694:
          .string "\tNAND dump is from a mmc machine\n"
          .zero 2
L_4536b8:
          .string "\tNAND dump uses big block controller\n"
          .zero 2
L_4536e0:
          .string "\tNAND dump is from a big block machine\n"
L_453708:
          .string "***** WARNING: NAND dump too small to be from a big block machine, discarding dump!\n"
          .zero 3
L_453760:
          .string "\tNAND dump is from a small block machine\n"
          .zero 2
L_45378c:
          .string "\tNAND dump uses small block controller\n"
L_4537b4:
          .string "***** WARNING: NAND dump does not appear to have a good block at block 0, discarding dump!\n"
L_453810:
          .string "%s file size: 0x%llx\n"
          .zero 2
L_453828:
          .string "******* ERROR loading '%s', file size 0x%llx is not large enough\n"
          .zero 2
L_45386c:
          .string "******* ERROR loading '%s', flash header magic is incorrect\n"
          .zero 3
L_4538ac:
          .string "******* ERROR loading '%s', flash header Entry is too large\n"
          .zero 3
L_4538ec:
          .string "******* ERROR loading '%s', flash header Size is too large\n"
L_453928:
          .string "******* ERROR loading '%s', flash header KeyVaultSize is too large\n"
L_45396c:
          .string "******* ERROR loading '%s', flash header SysUpdateAddr is malformed\n"
          .zero 3
L_4539b4:
          .string "******* ERROR loading '%s', flash header SysUpdateCount is not 2, continuing anyway\n"
          .zero 3
L_453a0c:
          .string "******* ERROR loading '%s', flash header KeyVaultVersion is not 0x0712, continuing anyway\n"
          .zero 1
L_453a68:
          .string "******* ERROR loading '%s', flash header KeyVaultAddr is too large\n"
L_453aac:
          .string "******* ERROR loading '%s', flash header FileSystemAddr is too large\n"
          .zero 2
L_453af4:
          .string "******* ERROR loading '%s', flash header SmcConfigAddr is not 0, continuing anyway\n"
L_453b48:
          .string "******* ERROR loading '%s', flash header SmcBootSize is not 0x3000 or 0x3800\n"
          .zero 2
L_453b98:
          .string "******* ERROR loading '%s', flash header SmcBootAddr is too large\n"
          .zero 1
L_453bdc:
          .string "FATX magic found, truncating load size to 0x3000000 bytes for mmc consoles\n"
L_453c28:
          .string "First page does not contain a valid ECC, assuming this is an mmc dump and truncating load size to 0x3000000 bytes!\n"
L_453c9c:
          .string "First page contains a valid ECC, assuming this is a big block flash overdump and truncating load size to 0x4200000 bytes\n"
          .zero 2
L_453d18:
          .string "nanddump header checks passed OK!\n"
          .zero 1
L_453d3c:
          .string "**** Warning: error getting CB/CBA Nonce offset, aborting!\n"
L_453d78:
          .string "**** Warning: error getting CB/CBA Nonce, aborting!\n"
          .zero 3
L_453db0:
          .string "**** Warning: error getting CBB Nonce offset, aborting!\n"
          .zero 3
L_453dec:
          .string "**** Warning: error getting CBB Nonce, offset 0x%x aborting!\n"
          .zero 2
L_453e2c:
          .string "**** Warning: error getting CD Nonce offset, aborting!\n"
L_453e64:
          .string "**** Warning: error getting CD Nonce, offset 0x%x aborting!\n"
          .zero 3
L_453ea4:
          .string "**** Warning: error getting CE Nonce offset, aborting!\n"
L_453edc:
          .string "**** Warning: error getting CE Nonce, offset 0x%x aborting!\n"
          .zero 3
L_453f1c:
          .string "**** Warning: error getting CF Nonce offset, aborting!\n"
L_453f54:
          .string "**** Warning: error getting CF Nonce, offset 0x%x aborting!\n"
          .zero 3
L_453f94:
          .string "**** Warning: error getting CG Nonce offset, aborting!\n"
L_453fcc:
          .string "**** Warning: error getting CG Nonce, offset 0x%x aborting!\n"
L_454009:
          .string "\n------ Checking %s ------\n"
L_454025:
          .string "NAND dump not found at '%s'\n"
          .zero 2
L_454044:
          .string "NAND dump '%s' is not a correct raw (with ecc) dump size (0x%x bytes), ignoring\n"
          .zero 3
L_454098:
          .string "NAND dump '%s' is not a correct dump size (0x%x bytes), ignoring\n"
          .zero 2
L_4540dc:
          .string "******* ERROR loading '%s', unable to allocate memory\n"
          .zero 1
L_454114:
          .string "Loading NAND dump (0x%x bytes)..."
          .zero 2
L_454138:
          .string "******* ERROR loading '%s', unable to allocate user/spare memory\n"
          .zero 2
L_45417c:
          .string "Detecting NAND controller type from dump data...\n"
          .zero 2
L_4541b0:
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
          .long FUN_4136a0 - .
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
          .long FUN_4137f0 - .
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
          .long FUN_4138c0 - .
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
          .long FUN_413ad0 - .
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
          .long FUN_413d30 - .
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
          .long FUN_414050 - .
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
          .long FUN_414300 - .
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
          .long FUN_4144e0 - .
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
          .long L_414610 - .
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
          .long FUN_414650 - .
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
          .long FUN_414760 - .
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
          .long FUN_414960 - .
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
          .long L_414af0 - .
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
          .long L_414b90 - .
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
          .long FUN_414be0 - .
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
          .long FUN_414e90 - .
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
          .long L_4151c0 - .
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
          .long FUN_415230 - .
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
          .long L_4154d0 - .
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
          .long FUN_415970 - .
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
          .long FUN_415b00 - .
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
          .long L_415d90 - .
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
          .long L_415e90 - .
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
          .long FUN_415ef0 - .
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
          .long L_416040 - .
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
          .long FUN_416070 - .
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
          .long L_4160d0 - .
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
          .long FUN_416150 - .
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
          .long FUN_416840 - .
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
          .long FUN_416aa0 - .
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
          .long FUN_416cd0 - .
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
          .long FUN_4172c0 - .
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
          .long FUN_417680 - .
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
L_474a20:
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
L_474b20:
          .zero 28
L_474b3c:
          .zero 484
L_474d20:
          .zero 4
L_474d24:
          .zero 28
L_474d40:
          .zero 8192
L_476d40:
          .zero 8192
L_478d40:
          .zero 32
