# runtime/crt2.s -- mingw-w64 crt2.o, byte match
#
# original placement:
#   .bss           0046f000-0046f01c
#   .data          0044a000-0044a004
#   .eh_frame      00465000-004650c8
#   .rdata$zzz     00463720-0046374c
#   .text          00401000-00401500

.intel_syntax noprefix
.globl L_401010
.globl L_401130

.text
.p2align 4
FUN_401000:
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
L_401010:
          sub ESP,28
          xor EAX,EAX
          cmp WORD PTR [__ImageBase],23117
          mov DWORD PTR [L_479e2c],1
          mov DWORD PTR [L_479e28],1
          mov DWORD PTR [L_479e24],1
          mov DWORD PTR [L_479acc],1
          je L_4010b0
L_401048:
          mov DWORD PTR [L_46f008],EAX
          mov EAX,DWORD PTR [L_479e38]
          test EAX,EAX
          je L_4010a0
          mov DWORD PTR [ESP],2
          call FUN_449278
L_401062:
          mov DWORD PTR [ESP],4294967295
          call FUN_446fd0
          mov EDX,DWORD PTR [L_479e48]
          mov DWORD PTR [L_50ec88],EAX
          mov DWORD PTR [L_50ec8c],EAX
          mov EAX,DWORD PTR [_fmode]
          mov DWORD PTR [EAX],EDX
          call FUN_446cc0
          cmp DWORD PTR [L_44b6bc],1
          je L_401100
          xor EAX,EAX
          add ESP,28
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4010a0:
          mov DWORD PTR [ESP],1
          call FUN_449278
          jmp L_401062
          .byte 0x66
          .byte 0x90
L_4010b0:
          mov EDX,DWORD PTR [__ImageBase+60]
          cmp DWORD PTR [EDX+__ImageBase],17744
          lea ECX,DWORD PTR [EDX+__ImageBase]
          jne L_401048
          movzx EDX,WORD PTR [ECX+24]
          cmp DX,267
          je L_401112
          cmp DX,523
          jne L_401048
          cmp DWORD PTR [ECX+132],14
          jbe L_401048
          mov EDX,DWORD PTR [ECX+248]
          xor EAX,EAX
          test EDX,EDX
          setne AL
          jmp L_401048
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_401100:
          mov DWORD PTR [ESP],OFFSET L_446f50
          call FUN_446f40
          xor EAX,EAX
          add ESP,28
          ret 
L_401112:
          cmp DWORD PTR [ECX+116],14
          jbe L_401048
          mov ECX,DWORD PTR [ECX+232]
          xor EAX,EAX
          test ECX,ECX
          setne AL
          jmp L_401048
          .byte 0x66
          .byte 0x90
L_401130:
          sub ESP,44
          mov EAX,DWORD PTR [L_479e20]
          mov DWORD PTR [ESP+16],OFFSET L_46f000
          mov DWORD PTR [ESP+8],OFFSET L_46f010
          mov DWORD PTR [ESP+4],OFFSET L_46f014
          mov DWORD PTR [ESP],OFFSET L_46f018
          mov DWORD PTR [L_46f000],EAX
          mov EAX,DWORD PTR [L_44b6b0]
          mov DWORD PTR [ESP+12],EAX
          call FUN_449280
          add ESP,44
          ret 
          .byte 0x66
          .byte 0x90
L_401170:
          push EBP
          xor EAX,EAX
          mov ECX,17
          mov EBP,ESP
          push EDI
          push ESI
          lea EDX,DWORD PTR [EBP-92]
          push EBX
          mov EDI,EDX
          sub ESP,124
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,48
          call ___chkstk_ms
          sub ESP,EAX
          lea EAX,DWORD PTR [ESP+27]
          and EAX,4294967280
          mov DWORD PTR [EAX],3435973836
          mov DWORD PTR [EAX+4],3435973836
          mov DWORD PTR [EAX+8],3435973836
          mov DWORD PTR [EAX+12],3435973836
          mov DWORD PTR [EAX+16],3435973836
          mov DWORD PTR [EAX+20],3435973836
          mov DWORD PTR [EAX+24],3435973836
          mov DWORD PTR [EAX+28],3435973836
          and ESP,4294967280
          mov ESI,DWORD PTR [L_479e38]
          test ESI,ESI
          jne L_401470
L_4011e2:
          mov EAX,DWORD PTR FS:[24]
          xor ESI,ESI
          mov EBX,DWORD PTR [EAX+4]
          mov EDI,DWORD PTR [Sleep]
          jmp L_401209
L_4011f5:
          cmp EBX,EAX
          je L_401412
          mov DWORD PTR [ESP],1000
          call EDI
          sub ESP,4
L_401209:
          mov EAX,ESI
          lock cmpxchg DWORD PTR [L_50ec90],EBX
          test EAX,EAX
          jne L_4011f5
          mov EAX,DWORD PTR [L_50ec94]
          xor EBX,EBX
          cmp EAX,1
          je L_401425
L_401227:
          mov EAX,DWORD PTR [L_50ec94]
          test EAX,EAX
          je L_401481
          mov DWORD PTR [L_46f004],1
L_40123e:
          mov EAX,DWORD PTR [L_50ec94]
          cmp EAX,1
          je L_40143f
L_40124c:
          test EBX,EBX
          je L_401465
L_401254:
          mov EAX,DWORD PTR [L_46328c]
          test EAX,EAX
          je L_401279
          mov DWORD PTR [ESP+8],0
          mov DWORD PTR [ESP+4],2
          mov DWORD PTR [ESP],0
          call EAX
          sub ESP,12
L_401279:
          call FUN_447180
          mov DWORD PTR [ESP],OFFSET L_447450
          call DWORD PTR [SetUnhandledExceptionFilter]
          sub ESP,4
          mov DWORD PTR [L_479e4c],EAX
          mov DWORD PTR [ESP],OFFSET FUN_401000
          call FUN_4492b0
          call FUN_446fb0
          mov EAX,DWORD PTR [_acmdln]
          mov DWORD PTR [L_479e7c],OFFSET __ImageBase
          mov EAX,DWORD PTR [EAX]
          test EAX,EAX
          je L_401314
          xor ECX,ECX
          jmp L_4012d1
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4012c0:
          test DL,DL
          je L_4012f0
          and ECX,1
          je L_4012f0
          mov ECX,1
L_4012ce:
          add EAX,1
L_4012d1:
          movzx EDX,BYTE PTR [EAX]
          cmp DL,32
          jle L_4012c0
          mov EBX,ECX
          xor EBX,1
          cmp DL,34
          cmove ECX,EBX
          jmp L_4012ce
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4012f0:
          test DL,DL
          jne L_401305
          jmp L_40130f
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_401300:
          cmp DL,32
          jg L_40130f
L_401305:
          add EAX,1
          movzx EDX,BYTE PTR [EAX]
          test DL,DL
          jne L_401300
L_40130f:
          mov DWORD PTR [L_479e78],EAX
L_401314:
          mov EBX,DWORD PTR [L_479e38]
          test EBX,EBX
          je L_401334
          test BYTE PTR [EBP-48],1
          mov EAX,10
          cmovne AX,WORD PTR [EBP-44]
          movzx EAX,AX
          mov DWORD PTR [L_44a000],EAX
L_401334:
          mov EAX,DWORD PTR [L_46f018]
          mov DWORD PTR [EBP-112],EAX
          mov ESI,EAX
          lea EAX,DWORD PTR [EAX*4+4]
          mov DWORD PTR [EBP-116],EAX
          mov DWORD PTR [ESP],EAX
          call _malloc
          test ESI,ESI
          mov DWORD PTR [EBP-108],EAX
          mov EDI,DWORD PTR [L_46f014]
          jle L_4014a4
          xor EBX,EBX
          mov ESI,EDI
L_401365:
          mov EAX,DWORD PTR [ESI+EBX*4]
          mov DWORD PTR [ESP],EAX
          call _strlen
          lea EDI,DWORD PTR [EAX+1]
          mov DWORD PTR [ESP],EDI
          call _malloc
          mov ECX,DWORD PTR [EBP-108]
          mov DWORD PTR [ECX+EBX*4],EAX
          mov ECX,DWORD PTR [ESI+EBX*4]
          add EBX,1
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          cmp DWORD PTR [EBP-112],EBX
          jne L_401365
          mov EAX,DWORD PTR [EBP-116]
          sub EAX,4
L_4013a2:
          mov ESI,DWORD PTR [EBP-108]
          mov DWORD PTR [ESI+EAX*1],0
          mov DWORD PTR [L_46f014],ESI
          call FUN_446c90
          mov EAX,DWORD PTR [__initenv]
          mov EDX,DWORD PTR [L_46f010]
          mov DWORD PTR [EAX],EDX
          mov EAX,DWORD PTR [L_46f010]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [L_46f014]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [L_46f018]
          mov DWORD PTR [ESP],EAX
          call FUN_4492c0
          mov ECX,DWORD PTR [L_46f008]
          mov DWORD PTR [L_46f00c],EAX
          test ECX,ECX
          je L_4014ab
          mov EDX,DWORD PTR [L_46f004]
          test EDX,EDX
          jne L_40140a
          call FUN_449260
          mov EAX,DWORD PTR [L_46f00c]
L_40140a:
          lea ESP,DWORD PTR [EBP-12]
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_401412:
          mov EAX,DWORD PTR [L_50ec94]
          mov EBX,1
          cmp EAX,1
          jne L_401227
L_401425:
          mov DWORD PTR [ESP],31
          call FUN_449268
          mov EAX,DWORD PTR [L_50ec94]
          cmp EAX,1
          jne L_40124c
L_40143f:
          mov DWORD PTR [ESP+4],OFFSET L_510008
          mov DWORD PTR [ESP],OFFSET L_510000
          call FUN_449210
          test EBX,EBX
          mov DWORD PTR [L_50ec94],2
          jne L_401254
L_401465:
          xchg DWORD PTR [L_50ec90],EBX
          jmp L_401254
L_401470:
          mov DWORD PTR [ESP],EDX
          call DWORD PTR [GetStartupInfoA]
          sub ESP,4
          jmp L_4011e2
L_401481:
          mov DWORD PTR [L_50ec94],1
          mov DWORD PTR [ESP+4],OFFSET L_510018
          mov DWORD PTR [ESP],OFFSET L_51000c
          call FUN_449210
          jmp L_40123e
L_4014a4:
          xor EAX,EAX
          jmp L_4013a2
L_4014ab:
          mov DWORD PTR [ESP],EAX
          call FUN_449198
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4014c0:
          sub ESP,12
          mov DWORD PTR [L_479e38],1
          call FUN_446cd0
          add ESP,12
          jmp L_401170
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
.globl __EntryPoint
__EntryPoint:
L_4014e0:
          sub ESP,12
          mov DWORD PTR [L_479e38],0
          call FUN_446cd0
          add ESP,12
          jmp L_401170
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop

.data
.p2align 2
L_44a000:
          .byte 0xa
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
          .long FUN_401000 - .
          .byte 0x2
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
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_401010 - .
          .byte 0x1e
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x85
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x71
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_401130 - .
          .byte 0x3e
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x7a
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_401170 - .
          .byte 0x43
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x49
          .byte 0xd
          .byte 0x5
          .byte 0x46
          .byte 0x87
          .byte 0x3
          .byte 0x86
          .byte 0x4
          .byte 0x83
          .byte 0x5
          .byte 0x3
          .byte 0x8e
          .byte 0x2
          .byte 0xa
          .byte 0xc3
          .byte 0x41
          .byte 0xc6
          .byte 0x41
          .byte 0xc7
          .byte 0x41
          .byte 0xc5
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x9c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4014c0 - .
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x52
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4014e0 - .
          .byte 0x1a
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x10
          .byte 0x52
          .byte 0xe
          .byte 0x4
          .byte 0x0

.bss
.p2align 2
L_46f000:
          .zero 4
L_46f004:
          .zero 4
L_46f008:
          .zero 4
L_46f00c:
          .zero 4
L_46f010:
          .zero 4
L_46f014:
          .zero 4
L_46f018:
          .zero 4
