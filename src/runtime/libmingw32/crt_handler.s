# runtime/libmingw32/crt_handler.s -- byte match
#
# original placement:
#   .bss           00479e4c-00479e50
#   .eh_frame      0046e2c0-0046e31c
#   .rdata$zzz     00464488-004644b4
#   .text          00447450-00447600

.intel_syntax noprefix
.globl L_447450
.globl L_479e4c

.text
.p2align 4
L_447450:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          mov EAX,DWORD PTR [EBX]
          mov EAX,DWORD PTR [EAX]
          cmp EAX,3221225617
          ja L_4474b0
          cmp EAX,3221225613
          jae L_447520
          cmp EAX,3221225477
          jne L_447560
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],11
          call _signal
          cmp EAX,1
          je L_4475c0
          test EAX,EAX
          je L_4474c9
          mov DWORD PTR [ESP],11
          call EAX
          add ESP,24
          mov EAX,4294967295
          pop EBX
          ret 4
          .byte 0x90
L_4474b0:
          cmp EAX,3221225620
          je L_4474e0
          cmp EAX,3221225622
          je L_44756b
          cmp EAX,3221225619
          je L_447520
L_4474c9:
          mov EAX,DWORD PTR [L_479e4c]
          test EAX,EAX
          je L_44750f
          mov DWORD PTR [ESP+32],EBX
          add ESP,24
          pop EBX
          jmp EAX
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_4474e0:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],8
          call _signal
          cmp EAX,1
          je L_4475a1
L_4474fd:
          test EAX,EAX
          je L_4474c9
          mov DWORD PTR [ESP],8
          call EAX
          mov EAX,4294967295
L_44750f:
          add ESP,24
          pop EBX
          ret 4
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_447520:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],8
          call _signal
          cmp EAX,1
          jne L_4474fd
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],8
          call _signal
          call FUN_446fb0
          mov EAX,4294967295
          jmp L_44750f
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_447560:
          cmp EAX,3221225501
          jne L_4474c9
L_44756b:
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],4
          call _signal
          cmp EAX,1
          je L_4475e0
          test EAX,EAX
          je L_4474c9
          mov DWORD PTR [ESP],4
          call EAX
          add ESP,24
          mov EAX,4294967295
          pop EBX
          ret 4
L_4475a1:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],8
          call _signal
          mov EAX,4294967295
          jmp L_44750f
          .byte 0x90
L_4475c0:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],11
          call _signal
          mov EAX,4294967295
          jmp L_44750f
          .byte 0x66
          .byte 0x90
L_4475e0:
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],4
          call _signal
          mov EAX,4294967295
          jmp L_44750f
          .byte 0x90
          .byte 0x90

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
          .byte 0x40
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_447450 - .
          .byte 0xae
          .byte 0x1
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
          .byte 0x2
          .byte 0x52
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x44
          .byte 0xb
          .byte 0x69
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x46
          .byte 0xb
          .byte 0x72
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x4d
          .byte 0xb
          .byte 0x2
          .byte 0x78
          .byte 0xa
          .byte 0xe
          .byte 0x8
          .byte 0x46
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x43
          .byte 0xb
          .byte 0x0

.bss
.p2align 2
L_479e4c:
          .zero 4
