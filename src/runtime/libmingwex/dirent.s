# runtime/libmingwex/dirent.s -- byte match
#
# original placement:
#   .eh_frame      0046e810-0046e974
#   .rdata$zzz     004645e8-00464614
#   .text          004481c0-00448600

.intel_syntax noprefix
.globl FUN_4481c0
.globl FUN_448360
.globl FUN_448470

.text
.p2align 4
FUN_4481c0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,316
          mov EBX,DWORD PTR [ESP+336]
          call FUN_449250
          mov DWORD PTR [EAX],0
          test EBX,EBX
          je L_44834c
          cmp BYTE PTR [EBX],0
          je L_448310
          mov DWORD PTR [ESP],EBX
          call DWORD PTR [GetFileAttributesA]
          sub ESP,4
          cmp EAX,-1
          je L_448330
          test AL,16
          je L_448310
          lea EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],260
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EDI
          mov ESI,EDI
          call FUN_449218
L_448224:
          mov EDX,DWORD PTR [ESI]
          add ESI,4
          lea EAX,DWORD PTR [EDX-16843009]
          not EDX
          and EAX,EDX
          and EAX,2155905152
          je L_448224
          mov EDX,EAX
          shr EDX,16
          test EAX,32896
          cmove EAX,EDX
          lea EDX,DWORD PTR [ESI+2]
          mov ECX,EAX
          cmove ESI,EDX
          add CL,AL
          sbb ESI,3
          sub ESI,EDI
          lea EAX,DWORD PTR [ESI+563]
          mov DWORD PTR [ESP],EAX
          call FUN_449108
          test EAX,EAX
          mov EBX,EAX
          je L_44833f
          lea EDX,DWORD PTR [ESI+1]
          lea EBP,DWORD PTR [EAX+556]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+28],EDX
          call FUN_4490f8
          cmp BYTE PTR [EBX+556],0
          je L_4482b4
          movzx EAX,BYTE PTR [EBX+ESI*1+555]
          cmp AL,47
          je L_4482b4
          cmp AL,92
          je L_4482b4
          mov EDX,DWORD PTR [ESP+28]
          mov EDI,92
          mov WORD PTR [EBP+ESI*1],DI
          mov ESI,EDX
L_4482b4:
          mov EAX,42
          xor EDX,EDX
          xor ECX,ECX
          mov WORD PTR [EBP+ESI*1],AX
          mov WORD PTR [EBX+284],DX
          lea EDX,DWORD PTR [EBX+288]
          mov WORD PTR [EBX+286],CX
          xor EAX,EAX
          mov ECX,65
          mov EDI,EDX
          mov DWORD PTR [EBX+548],4294967295
          mov DWORD PTR [EBX+552],0
          mov DWORD PTR [EBX+280],0
          rep stosd DWORD PTR ES:[EDI]
L_4482ff:
          add ESP,316
          mov EAX,EBX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_448310:
          call FUN_449250
          xor EBX,EBX
          mov DWORD PTR [EAX],20
          add ESP,316
          mov EAX,EBX
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
L_448330:
          call FUN_449250
          xor EBX,EBX
          mov DWORD PTR [EAX],2
          jmp L_4482ff
L_44833f:
          call FUN_449250
          mov DWORD PTR [EAX],12
          jmp L_4482ff
L_44834c:
          call FUN_449250
          mov DWORD PTR [EAX],14
          jmp L_4482ff
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_448360:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          call FUN_449250
          mov DWORD PTR [EAX],0
          test EBX,EBX
          je L_44845d
          mov EAX,DWORD PTR [EBX+552]
          test EAX,EAX
          js L_448442
          mov DWORD PTR [ESP+4],EBX
          je L_4483f0
          mov EAX,DWORD PTR [EBX+548]
          mov DWORD PTR [ESP],EAX
          call FUN_449220
          test EAX,EAX
          jne L_448415
          mov EAX,DWORD PTR [EBX+552]
          add EAX,1
          test EAX,EAX
          mov DWORD PTR [EBX+552],EAX
          jle L_448442
L_4483b9:
          lea ESI,DWORD PTR [EBX+20]
          mov DWORD PTR [ESP],ESI
          call FUN_449078
          mov WORD PTR [EBX+286],AX
          lea EAX,DWORD PTR [EBX+288]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_449080
          lea EAX,DWORD PTR [EBX+280]
L_4483e3:
          add ESP,20
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4483f0:
          lea EAX,DWORD PTR [EBX+556]
          mov DWORD PTR [ESP],EAX
          call FUN_449228
          cmp EAX,-1
          mov DWORD PTR [EBX+548],EAX
          je L_448438
          mov DWORD PTR [EBX+552],1
          jmp L_4483b9
L_448415:
          call DWORD PTR [GetLastError]
          cmp EAX,18
          je L_448450
L_448420:
          mov EAX,DWORD PTR [EBX+548]
          mov DWORD PTR [ESP],EAX
          call FUN_449230
          mov DWORD PTR [EBX+548],4294967295
L_448438:
          mov DWORD PTR [EBX+552],4294967295
L_448442:
          add ESP,20
          xor EAX,EAX
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_448450:
          call FUN_449250
          mov DWORD PTR [EAX],0
          jmp L_448420
L_44845d:
          call FUN_449250
          mov DWORD PTR [EAX],14
          xor EAX,EAX
          jmp L_4483e3
          .byte 0x90
FUN_448470:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          call FUN_449250
          mov DWORD PTR [EAX],0
          test EBX,EBX
          je L_4484af
          mov EAX,DWORD PTR [EBX+548]
          xor ESI,ESI
          cmp EAX,-1
          je L_44849f
          mov DWORD PTR [ESP],EAX
          call FUN_449230
          mov ESI,EAX
L_44849f:
          mov DWORD PTR [ESP],EBX
          call FUN_449140
L_4484a7:
          add ESP,20
          mov EAX,ESI
          pop EBX
          pop ESI
          ret 
L_4484af:
          call FUN_449250
          mov ESI,4294967295
          mov DWORD PTR [EAX],14
          jmp L_4484a7
L_4484c1:
          jmp FUN_4484d0
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
FUN_4484d0:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          call FUN_449250
          mov DWORD PTR [EAX],0
          test EBX,EBX
          je L_448513
          mov EAX,DWORD PTR [EBX+548]
          cmp EAX,-1
          je L_4484fa
          mov DWORD PTR [ESP],EAX
          call FUN_449230
L_4484fa:
          mov DWORD PTR [EBX+548],4294967295
          mov DWORD PTR [EBX+552],0
L_44850e:
          add ESP,24
          pop EBX
          ret 
L_448513:
          call FUN_449250
          mov DWORD PTR [EAX],14
          jmp L_44850e
L_448520:
          push EBX
          sub ESP,8
          mov EBX,DWORD PTR [ESP+16]
          call FUN_449250
          mov DWORD PTR [EAX],0
          test EBX,EBX
          je L_448542
          mov EAX,DWORD PTR [EBX+552]
L_44853d:
          add ESP,8
          pop EBX
          ret 
L_448542:
          call FUN_449250
          mov DWORD PTR [EAX],14
          mov EAX,4294967295
          jmp L_44853d
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
L_448560:
          push ESI
          push EBX
          sub ESP,20
          mov EBX,DWORD PTR [ESP+32]
          mov ESI,DWORD PTR [ESP+36]
          call FUN_449250
          mov DWORD PTR [EAX],0
          test EBX,EBX
          je L_4485ed
          cmp ESI,-1
          jl L_4485e0
          je L_4485b0
          mov DWORD PTR [ESP],EBX
          call FUN_4484d0
          jmp L_44859c
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_448590:
          mov DWORD PTR [ESP],EBX
          call FUN_448360
          test EAX,EAX
          je L_4485d7
L_44859c:
          cmp ESI,DWORD PTR [EBX+552]
          jg L_448590
          add ESP,20
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4485b0:
          mov EAX,DWORD PTR [EBX+548]
          cmp EAX,-1
          je L_4485c3
          mov DWORD PTR [ESP],EAX
          call FUN_449230
L_4485c3:
          mov DWORD PTR [EBX+548],4294967295
          mov DWORD PTR [EBX+552],4294967295
L_4485d7:
          add ESP,20
          pop EBX
          pop ESI
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4485e0:
          call FUN_449250
          mov DWORD PTR [EAX],22
          jmp L_4485d7
L_4485ed:
          call FUN_449250
          mov DWORD PTR [EAX],14
          jmp L_4485d7
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          nop
          nop

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
          .byte 0x5c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4481c0 - .
          .byte 0x99
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
          .byte 0x2
          .byte 0x6c
          .byte 0xe
          .byte 0xcc
          .byte 0x2
          .byte 0x43
          .byte 0xe
          .byte 0xd0
          .byte 0x2
          .byte 0x3
          .byte 0xc
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
          .byte 0x45
          .byte 0xb
          .byte 0x53
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
          .byte 0x47
          .byte 0xb
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x7c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_448360 - .
          .byte 0xf
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
          .byte 0x20
          .byte 0x2
          .byte 0x81
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
          .byte 0x48
          .byte 0xb
          .byte 0x2
          .byte 0x55
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
          .byte 0x47
          .byte 0xb
          .byte 0x28
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_448470 - .
          .byte 0x51
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
          .byte 0x75
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xe4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4484d0 - .
          .byte 0x50
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
          .byte 0x7d
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_448520 - .
          .byte 0x34
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
          .byte 0x10
          .byte 0x5c
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x41
          .byte 0xb
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_448560 - .
          .byte 0x9a
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
          .byte 0x42
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
          .byte 0x6a
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
          .byte 0x0
