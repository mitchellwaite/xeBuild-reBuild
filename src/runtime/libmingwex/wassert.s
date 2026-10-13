# runtime/libmingwex/wassert.s -- byte match (_assert)
#
# original placement:
#   .eh_frame      0046e974-0046ea1c
#   .rdata         004634bc-004635a0
#   .rdata$zzz     00464614-00464640
#   .text          00448600-00448820

.intel_syntax noprefix
.globl __assert

.text
.p2align 4
FUN_448600:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,572
          mov EBX,DWORD PTR [ESP+596]
          mov DWORD PTR [ESP],16384
          mov ESI,DWORD PTR [ESP+592]
          call _malloc
          test EBX,EBX
          mov EBP,EAX
          je L_448710
          cmp WORD PTR [EBX],0
          mov EAX,OFFSET L_4634bc
          cmove EBX,EAX
L_44863a:
          test ESI,ESI
          je L_448705
          cmp WORD PTR [ESI],0
          mov EAX,OFFSET L_4634d0
          cmove ESI,EAX
L_44864e:
          lea EDI,DWORD PTR [ESP+38]
          mov DWORD PTR [ESP+8],260
          mov DWORD PTR [ESP],0
          mov DWORD PTR [ESP+4],EDI
          call DWORD PTR [GetModuleFileNameW]
          sub ESP,12
          test EAX,EAX
          je L_4486f0
L_448672:
          mov EAX,DWORD PTR [ESP+600]
          mov DWORD PTR [ESP+24],ESI
          mov DWORD PTR [ESP+16],EBX
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],OFFSET L_4634d4
          mov DWORD PTR [ESP+4],8191
          mov DWORD PTR [ESP+20],EAX
          mov DWORD PTR [ESP],EBP
          call FUN_4491e8
          mov EAX,DWORD PTR [L_479e38]
          test EAX,EAX
          je L_448737
          mov DWORD PTR [ESP+12],73746
          mov DWORD PTR [ESP+8],OFFSET L_463568
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],0
          call DWORD PTR [MessageBoxW]
          sub ESP,16
          cmp EAX,3
          je L_44871f
          cmp EAX,5
          jne L_44871a
          add ESP,572
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4486e7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4486f0:
          mov DWORD PTR [ESP+4],OFFSET L_4634bc
          mov DWORD PTR [ESP],EDI
          call FUN_449040
          jmp L_448672
L_448705:
          mov ESI,OFFSET L_4634d0
          jmp L_44864e
          .byte 0x90
L_448710:
          mov EBX,OFFSET L_4634bc
          jmp L_44863a
L_44871a:
          call FUN_4491b0
L_44871f:
          mov DWORD PTR [ESP],22
          call FUN_4490c8
          mov DWORD PTR [ESP],3
          call FUN_449248
L_448737:
          mov EAX,DWORD PTR [_iob]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],OFFSET L_46355c
          add EAX,64
          mov DWORD PTR [ESP],EAX
          call FUN_449120
          call FUN_4491b0
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
__assert:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov ECX,DWORD PTR [ESP+64]
          mov ESI,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+28],ECX
          call _strlen
          lea EAX,DWORD PTR [EAX+EAX*1+2]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          call _strlen
          lea EAX,DWORD PTR [EAX+EAX*1+2]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+28]
          mov EBP,EAX
          xor EAX,EAX
          movzx EDX,BYTE PTR [ECX]
          test DL,DL
          je L_4487c1
L_4487b0:
          mov WORD PTR [EBX+EAX*2],DX
          add EAX,1
          movzx EDX,BYTE PTR [ECX+EAX*1]
          test DL,DL
          jne L_4487b0
          add EAX,EAX
L_4487c1:
          movzx EDX,BYTE PTR [ESI]
          xor ECX,ECX
          mov WORD PTR [EBX+EAX*1],CX
          xor EAX,EAX
          test DL,DL
          je L_4487e2
L_4487d0:
          mov WORD PTR [EBP+EAX*2],DX
          add EAX,1
          movzx EDX,BYTE PTR [ESI+EAX*1]
          test DL,DL
          jne L_4487d0
          add EAX,EAX
L_4487e2:
          xor EDX,EDX
          mov WORD PTR [EBP+EAX*1],DX
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EBX
          call FUN_448600
          mov DWORD PTR [ESP],EBX
          call _free
          mov DWORD PTR [ESP+64],EBP
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          jmp _free
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
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_4634bc:
          .string "<"
          .string "u"
          .string "n"
          .string "k"
          .string "n"
          .string "o"
          .string "w"
          .string "n"
          .string ">"
          .zero 2
L_4634d0:
          .string "?"
          .zero 2
L_4634d4:
          .string "A"
          .string "s"
          .string "s"
          .string "e"
          .string "r"
          .string "t"
          .string "i"
          .string "o"
          .string "n"
          .string " "
          .string "f"
          .string "a"
          .string "i"
          .string "l"
          .string "e"
          .string "d"
          .string "!"
          .string "\n"
          .long L_50000a
          .string "r"
          .string "o"
          .string "g"
          .string "r"
          .string "a"
          .string "m"
          .string ":"
          .string " "
          .string "%"
          .string "w"
          .string "s"
          .string "\n"
          .string "F"
          .string "i"
          .string "l"
          .string "e"
          .string ":"
          .string " "
          .string "%"
          .string "w"
          .string "s"
          .string ","
          .long L_4c0020
          .string "i"
          .string "n"
          .string "e"
          .string " "
          .string "%"
          .string "u"
          .string "\n"
          .byte 0xa
          .byte 0x0
          .string "E"
          .string "x"
          .string "p"
          .string "r"
          .string "e"
          .string "s"
          .string "s"
          .string "i"
          .string "o"
          .string "n"
          .string ":"
          .string " "
          .string "%"
          .string "w"
          .string "s"
          .zero 2
L_46355c:
          .string "%"
          .string "w"
          .string "s"
          .string "\n"
          .zero 4
L_463568:
          .string "M"
          .string "i"
          .long L_47006e
          .string "W"
          .string " "
          .string "R"
          .string "u"
          .string "n"
          .string "t"
          .string "i"
          .string "m"
          .string "e"
          .string " "
          .string "A"
          .string "s"
          .string "s"
          .string "e"
          .string "r"
          .string "t"
          .string "i"
          .string "o"
          .string "n"
          .zero 10

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
          .long FUN_448600 - .
          .byte 0x58
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
          .byte 0xd0
          .byte 0x4
          .byte 0x2
          .byte 0x61
          .byte 0xe
          .byte 0xc4
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0xd0
          .byte 0x4
          .byte 0x2
          .byte 0x61
          .byte 0xe
          .byte 0xc0
          .byte 0x4
          .byte 0x43
          .byte 0xe
          .byte 0xd0
          .byte 0x4
          .byte 0x50
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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long __assert - .
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
          .byte 0x43
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xa1
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
