# app/log.s -- build.log, verbose levels; called by every app unit
#
# original placement:
#   .bss           004796a0-00479ac0
#   .eh_frame      0046b300-0046b3e8
#   .rdata         0045c684-0045c7e0
#   .rdata$zzz     00463b6c-00463b98
#   .text          00433570-00433800

.intel_syntax noprefix
.globl FUN_433570
.globl FUN_4335a0
.globl FUN_433600
.globl FUN_433610
.globl FUN_433690
.globl FUN_433740
.globl FUN_4337a0

.text
.p2align 4
FUN_433570:
          mov EDX,DWORD PTR [ESP+4]
          mov EAX,EDX
          and EAX,3
          test EDX,EDX
          js L_433590
          cmp EAX,3
          mov EDX,2
          cmove EAX,EDX
          mov DWORD PTR [L_479aa4],EAX
          ret 
          .byte 0x66
          .byte 0x90
L_433590:
          mov DWORD PTR [L_479aa0],1
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_4335a0:
          mov EAX,DWORD PTR [ESP+4]
          cmp AL,50
          ja L_4335f2
          movzx EAX,AL
          jmp DWORD PTR [EAX*4+L_45c6b4]
L_4335b2:
          mov DWORD PTR [L_479aa4],1
          mov DWORD PTR [ESP+4],OFFSET L_45c654
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4335d0:
          mov DWORD PTR [L_479aa4],2
          mov DWORD PTR [ESP+4],OFFSET L_45c66b
          jmp FUN_4490d0
L_4335e7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4335f0:
          repz ret 
L_4335f2:
          mov DWORD PTR [ESP+4],OFFSET L_45c684
          jmp FUN_4490d0
          .byte 0x90
FUN_433600:
          mov EAX,DWORD PTR [L_479aa4]
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_433610:
          sub ESP,28
          mov EAX,DWORD PTR [ESP+32]
          test EAX,EAX
          je L_433684
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP],OFFSET L_4796a0
          call FUN_449080
          mov EDX,OFFSET L_4796a0
L_433630:
          mov ECX,DWORD PTR [EDX]
          add EDX,4
          lea EAX,DWORD PTR [ECX-16843009]
          not ECX
          and EAX,ECX
          and EAX,2155905152
          je L_433630
          mov ECX,EAX
          mov DWORD PTR [ESP+32],OFFSET L_4796a0
          shr ECX,16
          test EAX,32896
          cmove EAX,ECX
          lea ECX,DWORD PTR [EDX+2]
          cmove EDX,ECX
          mov ECX,EAX
          add CL,AL
          sbb EDX,OFFSET L_4796a3
          mov DWORD PTR [EDX+L_4796a0],1735355438
          mov BYTE PTR [EDX+L_4796a4],0
          add ESP,28
          jmp FUN_4490b8
L_433684:
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
FUN_433690:
          push ESI
          push EBX
          sub ESP,532
          lea EAX,DWORD PTR [ESP+552]
          lea ESI,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP+4],512
          mov EBX,DWORD PTR [ESP+544]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+548]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_449030
          cmp DWORD PTR [L_479aa4],EBX
          jae L_433730
L_4336d1:
          cmp EBX,2
          ja L_4336df
          mov EAX,DWORD PTR [L_479aa0]
          test EAX,EAX
          je L_4336f0
L_4336df:
          add ESP,532
          pop EBX
          pop ESI
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4336f0:
          mov DWORD PTR [ESP+4],OFFSET L_45c780
          mov DWORD PTR [ESP],OFFSET L_45c782
          call FUN_449160
          test EAX,EAX
          mov EBX,EAX
          je L_4336df
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_449158
          mov DWORD PTR [ESP],EBX
          call FUN_449190
          add ESP,532
          pop EBX
          pop ESI
          ret 
L_433727:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_433730:
          mov DWORD PTR [ESP],ESI
          call _printf
          jmp L_4336d1
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_433740:
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_45c78c
          mov DWORD PTR [ESP],OFFSET L_45c782
          call FUN_449160
          test EAX,EAX
          je L_433770
          mov DWORD PTR [ESP],EAX
          call FUN_449190
          add ESP,28
          ret 
L_433767:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_433770:
          mov DWORD PTR [ESP+4],OFFSET L_45c782
          mov DWORD PTR [ESP],OFFSET L_45c790
          call _printf
          mov DWORD PTR [L_479aa0],1
          add ESP,28
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
FUN_4337a0:
          mov EAX,DWORD PTR [L_479aa0]
          test EAX,EAX
          jne L_4337bc
          cmp BYTE PTR [L_4796a0],0
          mov DWORD PTR [L_479aa0],1
          jne L_4337c0
L_4337bc:
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_4337c0:
          sub ESP,28
          mov DWORD PTR [ESP+4],OFFSET L_45c7cf
          mov DWORD PTR [ESP],OFFSET L_45c782
          call FUN_449160
          test EAX,EAX
          je L_4337f7
          mov DWORD PTR [ESP],EAX
          call FUN_449190
          mov DWORD PTR [ESP+4],OFFSET L_4796a0
          mov DWORD PTR [ESP],OFFSET L_45c782
          call FUN_4490b0
L_4337f7:
          add ESP,28
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_45c684:
          .string "verbose flag is invalid or default, ignoring"
          .zero 3
L_45c6b4:
          .long L_4335b2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335b2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f2
          .long L_4335f0
          .long L_4335b2
          .long L_4335d0
L_45c780:
          .string "a"
L_45c782:
          .string "build.log"
L_45c78c:
          .string "wb"
          .zero 1
L_45c790:
          .string "could not initialize temp log file at '%s', logging disabled!\n"
L_45c7cf:
          .string "rb"
          .zero 14

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
          .long FUN_433570 - .
          .byte 0x2b
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
          .long FUN_4335a0 - .
          .byte 0x5f
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
          .long FUN_433600 - .
          .byte 0x6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_433610 - .
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x2
          .byte 0x6c
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x45
          .byte 0xb
          .byte 0x43
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_433690 - .
          .byte 0xaa
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
          .byte 0x46
          .byte 0xe
          .byte 0xa0
          .byte 0x4
          .byte 0x2
          .byte 0x4d
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
          .byte 0x49
          .byte 0xb
          .byte 0x74
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
          .byte 0x4a
          .byte 0xb
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_433740 - .
          .byte 0x52
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x20
          .byte 0x63
          .byte 0xa
          .byte 0xe
          .byte 0x4
          .byte 0x4a
          .byte 0xb
          .byte 0x61
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xd4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4337a0 - .
          .byte 0x5b
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x63
          .byte 0xe
          .byte 0x20
          .byte 0x77
          .byte 0xe
          .byte 0x4
          .byte 0x0

.bss
.p2align 5
L_4796a0:
          .zero 3
L_4796a3:
          .zero 1
L_4796a4:
          .zero 1020
L_479aa0:
          .zero 4
L_479aa4:
          .zero 28
