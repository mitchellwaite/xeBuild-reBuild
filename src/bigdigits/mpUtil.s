# bigdigits/mpUtil.s -- digit alloc/free, hex print, random fill, string conversion
#
# original placement:
#   .eh_frame      0046d598-0046d814
#   .rdata         00462900-00462960
#   .rdata$zzz     00464094-004640c0
#   .text          004421a0-004425d0

.intel_syntax noprefix
.globl FUN_4421a0
.globl FUN_4421f0
.globl FUN_4423a0

.text
.p2align 4
FUN_4421a0:
          mov EAX,DWORD PTR [ESP+4]
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+4],EAX
          jmp FUN_449108
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
L_4421c0:
          mov EDX,DWORD PTR [ESP+4]
          mov EAX,EDX
          shr EAX,5
          and EDX,31
          mov EDX,DWORD PTR [ESP+8]
          lea ECX,DWORD PTR [EAX+1]
          cmovne EAX,ECX
          mov DWORD PTR [EDX],EAX
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+4],EAX
          jmp FUN_449108
L_4421e7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_4421f0:
          mov EAX,DWORD PTR [ESP+4]
          test EAX,EAX
          je L_442200
          jmp FUN_449140
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_442200:
          repz ret 
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
L_442210:
          push ESI
          push EBX
          sub ESP,20
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [ESP+32]
          test EAX,EAX
          je L_44223f
          lea EBX,DWORD PTR [EAX-1]
L_442224:
          mov EAX,DWORD PTR [ESI+EBX*4]
          mov DWORD PTR [ESP],OFFSET L_462900
          sub EBX,1
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490e0
          cmp EBX,-1
          jne L_442224
L_44223f:
          add ESP,20
          pop EBX
          pop ESI
          ret 
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
L_442250:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EDI,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [ESP+32]
          test EDI,EDI
          je L_4422a0
          lea ESI,DWORD PTR [EAX+EDI*4-4]
          xor EBX,EBX
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_442270:
          mov EAX,DWORD PTR [ESI]
          add EBX,1
          mov DWORD PTR [ESP],OFFSET L_462900
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490e0
          cmp EDI,EBX
          je L_4422a0
          test BL,7
          jne L_44229a
          mov DWORD PTR [ESP],10
          call FUN_4490d8
L_44229a:
          sub ESI,4
          jmp L_442270
          .byte 0x90
L_4422a0:
          mov DWORD PTR [ESP+32],10
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          jmp FUN_4490d8
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
L_4422c0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EAX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+32]
          lea EBX,DWORD PTR [EAX-1]
          jmp L_4422e0
L_4422d3:
          lea ESI,DWORD PTR [EBX-1]
          mov EAX,DWORD PTR [EDI+ESI*4+4]
          test EAX,EAX
          jne L_4422f5
          mov EBX,ESI
L_4422e0:
          cmp EBX,-1
          jne L_4422d3
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4422f0:
          mov EBX,ESI
          sub ESI,1
L_4422f5:
          mov EAX,DWORD PTR [EDI+EBX*4]
          mov DWORD PTR [ESP],OFFSET L_462900
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490e0
          test EBX,EBX
          jne L_4422f0
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_442320:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EAX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+32]
          lea EBX,DWORD PTR [EAX-1]
          jmp L_442340
L_442333:
          lea EAX,DWORD PTR [EBX-1]
          mov EDX,DWORD PTR [EDI+EAX*4+4]
          test EDX,EDX
          jne L_442360
          mov EBX,EAX
L_442340:
          cmp EBX,-1
          jne L_442333
L_442345:
          mov DWORD PTR [ESP+32],10
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          jmp FUN_4490d8
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_442360:
          xor ESI,ESI
L_442362:
          mov EAX,DWORD PTR [EDI+EBX*4]
          mov DWORD PTR [ESP],OFFSET L_462900
          add ESI,1
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490e0
          test EBX,EBX
          je L_442345
          test ESI,7
          jne L_442390
          mov DWORD PTR [ESP],10
          call FUN_4490d8
L_442390:
          sub EBX,1
          jmp L_442362
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
FUN_4423a0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov ESI,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+32]
          test ESI,ESI
          je L_4423d2
          xor EBX,EBX
L_4423b4:
          mov DWORD PTR [ESP+4],4294967295
          mov DWORD PTR [ESP],0
          call _spPseudoRand
          mov DWORD PTR [EDI+EBX*4],EAX
          add EBX,1
          cmp ESI,EBX
          jne L_4423b4
L_4423d2:
          add ESP,16
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4423e0:
          push EDI
          push ESI
          push EBX
          sub ESP,16
          mov EBX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBX
          call FUN_4491a0
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          call FUN_449078
          cmp EBX,EAX
          cmova EBX,EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX],EBX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_4490f8
          add ESP,16
          mov EAX,ESI
          pop EBX
          pop ESI
          pop EDI
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_442430:
          push ESI
          push EBX
          sub ESP,20
          mov ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],1
          lea EAX,DWORD PTR [ESI+1]
          mov DWORD PTR [ESP],EAX
          call FUN_4491a0
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_4490f8
          add ESP,20
          mov EAX,EBX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_442470:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EBP,DWORD PTR [ESP+64]
          mov EBX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],EBP
          call FUN_449078
          mov EDI,EAX
          and EDI,1
          jne L_442520
          mov ESI,EAX
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBX
          call FUN_4491a0
          mov EDX,ESI
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [EBX+EBX*1]
          shr EDX,1
          cmp EBX,EDX
          cmovb ESI,EAX
          mov EAX,DWORD PTR [ESP+72]
          test ESI,ESI
          mov DWORD PTR [EAX],ESI
          je L_442511
          .byte 0x66   # nop
          nop
L_4424c0:
          mov DWORD PTR [ESP],EBP
          mov EBX,EDI
          call FUN_449078
          sub EAX,EDI
          shr EBX,1
          add EBX,DWORD PTR [ESP+28]
          movzx ECX,BYTE PTR [EBP+EAX*1-1]
          lea EDX,DWORD PTR [ECX-49]
          xor ECX,ECX
          cmp DL,53
          ja L_4424eb
          movzx EDX,DL
          movzx ECX,BYTE PTR [EDX+L_462920]
L_4424eb:
          movzx EAX,BYTE PTR [EBP+EAX*1-2]
          xor EDX,EDX
          sub EAX,49
          cmp AL,53
          ja L_442506
          movzx EAX,AL
          movzx EDX,BYTE PTR [EAX+L_462920]
          shl EDX,4
L_442506:
          add EDI,2
          add ECX,EDX
          cmp ESI,EDI
          mov BYTE PTR [EBX],CL
          ja L_4424c0
L_442511:
          mov EAX,DWORD PTR [ESP+28]
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_442520:
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+28],0
          mov DWORD PTR [EAX],0
          mov EAX,DWORD PTR [ESP+28]
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_442540:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],1
          mov EDI,DWORD PTR [ESP+64]
          lea EAX,DWORD PTR [EDX+EDX*1+1]
          mov DWORD PTR [ESP+28],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_4491a0
          mov EDX,DWORD PTR [ESP+28]
          mov EBP,EAX
          test EDX,EDX
          je L_4425a3
          lea EBX,DWORD PTR [EDX-1]
          mov ESI,EAX
          .byte 0x8d,0x76,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_442580:
          movzx EAX,BYTE PTR [EDI+EBX*1]
          mov DWORD PTR [ESP],ESI
          sub EBX,1
          mov DWORD PTR [ESP+4],OFFSET L_462906
          add ESI,2
          mov DWORD PTR [ESP+8],EAX
          call FUN_449098
          cmp EBX,-1
          jne L_442580
L_4425a3:
          add ESP,44
          mov EAX,EBP
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4425b0:
          xor EAX,EAX
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
L_4425c0:
          xor EAX,EAX
          ret 
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

.section .rdata,"dr"
.p2align 5
L_462900:
          .string "%08x "
L_462906:
          .string "%02X"
          .zero 21
L_462920:
          .byte 0x1
          .byte 0x2
          .byte 0x3
          .byte 0x4
          .byte 0x5
          .byte 0x6
          .byte 0x7
          .byte 0x8
          .byte 0x9
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0xb
          .byte 0xc
          .byte 0xd
          .byte 0xe
          .byte 0xf
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa
          .byte 0xb
          .byte 0xc
          .byte 0xd
          .byte 0xe
          .byte 0xf
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
          .long FUN_4421a0 - .
          .byte 0x13
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4421c0 - .
          .byte 0x27
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4421f0 - .
          .byte 0x12
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
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_442210 - .
          .byte 0x35
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
          .byte 0x6d
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x84
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_442250 - .
          .byte 0x63
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
          .byte 0x55
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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4422c0 - .
          .byte 0x53
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
          .byte 0x62
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
          .byte 0x5f
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
          .byte 0x34
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xfc
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_442320 - .
          .byte 0x75
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
          .byte 0x6a
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
          .byte 0x4d
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x34
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long FUN_4423a0 - .
          .byte 0x39
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
          .byte 0x6f
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
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x68
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_4423e0 - .
          .byte 0x4c
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
          .byte 0x40
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
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_442430 - .
          .byte 0x3a
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
          .byte 0x70
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
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_442470 - .
          .byte 0xce
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
          .byte 0x59
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_442540 - .
          .byte 0x6d
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
          .byte 0x5f
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
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_4425b0 - .
          .byte 0x3
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
          .byte 0x6c
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_4425c0 - .
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
