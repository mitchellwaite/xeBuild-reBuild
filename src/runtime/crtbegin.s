# runtime/crtbegin.s -- gcc crtbegin.o, byte match
#
# original placement:
#   .bss           0046f01c-0046f040
#   .data          0044a004-0044a008
#   .eh_frame      004650c8-00465130
#   .rdata         0044c000-0044c064
#   .rdata$zzz     0046374c-00463778
#   .text          00401500-00401630

.intel_syntax noprefix
.globl L_401500

.text
.p2align 4
L_401500:
          push EBP
          mov EBP,ESP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov ESI,DWORD PTR [GetModuleHandleA]
          mov DWORD PTR [ESP],OFFSET L_44c000
          call ESI
          sub ESP,4
          test EAX,EAX
          je L_4015e0
          mov EBX,EAX
          mov DWORD PTR [ESP],OFFSET L_44c000
          call DWORD PTR [LoadLibraryA]
          mov EDX,DWORD PTR [GetProcAddress]
          sub ESP,4
          mov DWORD PTR [L_479e80],EAX
          mov DWORD PTR [ESP+4],OFFSET L_44c013
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [EBP-28],EDX
          call EDX
          sub ESP,8
          mov EDI,EAX
          mov EDX,DWORD PTR [EBP-28]
          mov DWORD PTR [ESP+4],OFFSET L_44c029
          mov DWORD PTR [ESP],EBX
          call EDX
          sub ESP,8
          mov DWORD PTR [L_44a004],EAX
L_40156d:
          test EDI,EDI
          je L_401582
          mov DWORD PTR [ESP+4],OFFSET L_46f01c
          mov DWORD PTR [ESP],OFFSET L_4650c8
          call EDI
L_401582:
          mov EAX,DWORD PTR [L_44b6d4]
          test EAX,EAX
          je L_4015c3
          mov DWORD PTR [ESP],OFFSET L_44c041
          call ESI
          sub ESP,4
          test EAX,EAX
          mov EDX,0
          je L_4015b6
          mov DWORD PTR [ESP+4],OFFSET L_44c04f
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [GetProcAddress]
          sub ESP,8
          mov EDX,EAX
L_4015b6:
          test EDX,EDX
          je L_4015c3
          mov DWORD PTR [ESP],OFFSET L_44b6d4
          call EDX
L_4015c3:
          mov DWORD PTR [ESP],OFFSET L_401600
          call FUN_446bf0
          lea ESP,DWORD PTR [EBP-12]
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_4015d7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4015e0:
          mov DWORD PTR [L_44a004],0
          mov EDI,0
          .byte 0xe9; .long L_40156d-.-4   # jmp L_40156d
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
L_401600:
          push EBP
          mov EBP,ESP
          sub ESP,24
          mov EAX,DWORD PTR [L_44a004]
          test EAX,EAX
          je L_401618
          mov DWORD PTR [ESP],OFFSET L_4650c8
          call EAX
L_401618:
          mov EAX,DWORD PTR [L_479e80]
          test EAX,EAX
          je L_40162d
          mov DWORD PTR [ESP],EAX
          call DWORD PTR [FreeLibrary]
          sub ESP,4
L_40162d:
          leave 
          ret 
          .byte 0x90

.data
.p2align 2
L_44a004:
          .zero 4

.section .rdata,"dr"
.p2align 2
L_44c000:
          .string "libgcc_s_dw2-1.dll"
L_44c013:
          .string "__register_frame_info"
L_44c029:
          .string "__deregister_frame_info"
L_44c041:
          .string "libgcj-16.dll"
L_44c04f:
          .string "_Jv_RegisterClasses"
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
L_4650c8:
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
          .byte 0x2c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_401500 - .
          .byte 0xf4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x42
          .byte 0xd
          .byte 0x5
          .byte 0x46
          .byte 0x87
          .byte 0x3
          .byte 0x86
          .byte 0x4
          .byte 0x83
          .byte 0x5
          .byte 0x2
          .byte 0xca
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
          .byte 0x4a
          .byte 0xb
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x4c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_401600 - .
          .byte 0x2f
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x41
          .byte 0xe
          .byte 0x8
          .byte 0x85
          .byte 0x2
          .byte 0x42
          .byte 0xd
          .byte 0x5
          .byte 0x6b
          .byte 0xc5
          .byte 0xc
          .byte 0x4
          .byte 0x4
          .byte 0x0
          .byte 0x0

.bss
.p2align 2
L_46f01c:
          .zero 36
