# crypto/hash.s -- hash-id size table, SHA-1 one-shot wrappers
#
# original placement:
#   .eh_frame      0046d03c-0046d0f0
#   .rdata         00462600-00462620
#   .rdata$zzz     00463e2c-00463e58
#   .text          00441400-00441540

.intel_syntax noprefix
.globl FUN_441400
.globl FUN_441410
.globl FUN_441480

.text
.p2align 4
FUN_441400:
          jmp L_441850
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
FUN_441410:
          mov EAX,DWORD PTR [ESP+4]
          lea EDX,DWORD PTR [EAX-1]
          xor EAX,EAX
          cmp EDX,4
          ja L_441425
          mov EAX,DWORD PTR [EDX*4+L_462600]
L_441425:
          repz ret 
L_441427:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_441430:
          push EBX
          sub ESP,120
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          call FUN_442b00
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+128]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4448d0
          mov EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_444da0
          add ESP,120
          xor EAX,EAX
          pop EBX
          ret 
          .byte 0x90
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_441480:
          push EBX
          sub ESP,120
          cmp DWORD PTR [ESP+128],2
          jne L_4414d2
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          call FUN_442b00
          mov EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4448d0
          mov EAX,DWORD PTR [ESP+140]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_444da0
          xor EAX,EAX
L_4414cd:
          add ESP,120
          pop EBX
          ret 
L_4414d2:
          mov EAX,4294967295
          jmp L_4414cd
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_4414e0:
          push EBX
          sub ESP,120
          cmp DWORD PTR [ESP+128],2
          jne L_441532
          lea EBX,DWORD PTR [ESP+16]
          mov DWORD PTR [ESP],EBX
          call FUN_442b00
          mov EAX,DWORD PTR [ESP+136]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+132]
          mov DWORD PTR [ESP+4],EAX
          call FUN_4448d0
          mov EAX,DWORD PTR [ESP+140]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          call FUN_444da0
          xor EAX,EAX
L_44152d:
          add ESP,120
          pop EBX
          ret 
L_441532:
          mov EAX,4294967295
          jmp L_44152d
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 5
L_462600:
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x14
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
          .byte 0x40
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
          .long FUN_441400 - .
          .byte 0x5
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
          .long FUN_441410 - .
          .byte 0x17
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
          .byte 0x44
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_441430 - .
          .byte 0x48
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
          .byte 0x80
          .byte 0x1
          .byte 0x2
          .byte 0x40
          .byte 0xe
          .byte 0x8
          .byte 0x43
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x68
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_441480 - .
          .byte 0x59
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
          .byte 0x80
          .byte 0x1
          .byte 0x2
          .byte 0x4c
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
          .byte 0x0
          .byte 0x0
          .byte 0x24
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x90
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long L_4414e0 - .
          .byte 0x59
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
          .byte 0x80
          .byte 0x1
          .byte 0x2
          .byte 0x4c
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
          .byte 0x0
          .byte 0x0
