# crypto/rsa.s -- RSA key generation, PKCS#1 v1.5/OAEP/PSS
#
# original placement:
#   .eh_frame      0046c9a0-0046ce10
#   .rdata         00461ca4-00462438
#   .rdata$zzz     00463cf8-00463d24
#   .text          0043e5e0-00440e20

.intel_syntax noprefix
.globl FUN_43e870
.globl FUN_43e940

.text
.p2align 4
FUN_43e5e0:
          push EBP
          push EDI
          mov EDI,ECX
          push ESI
          push EBX
          mov EBX,EAX
          imul EBP,ECX,3200
          lea EAX,DWORD PTR [EAX+ECX*4-4]
          sub ESP,44
          mov DWORD PTR [ESP+20],EDX
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP+28],5
L_43e605:
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_461ca4
          xor ESI,ESI
          call _printf
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call _mpMakeRandom
          mov EAX,DWORD PTR [ESP+24]
          or DWORD PTR [EAX],3221225472
          or DWORD PTR [EBX],1
          test EBP,EBP
          jg L_43e687
          jmp L_43e6d0
          .byte 0x8d
          .byte 0xb4
          .byte 0x26
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_43e640:
          mov DWORD PTR [ESP],42
          call _putchar
          mov DWORD PTR [ESP+8],200
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call _mpIsPrimeRabin
          test EAX,EAX
          jne L_43e6db
L_43e664:
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],2
          add ESI,1
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EBX
          call _mpShortAdd
          test EAX,EAX
          jne L_43e6d0
          cmp EBP,ESI
          jle L_43e6d0
L_43e687:
          mov DWORD PTR [ESP],46
          call _putchar
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          call _mpIsPrimeShort
          test EAX,EAX
          je L_43e664
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call _mpShortMod
          cmp EAX,1
          jne L_43e640
          mov DWORD PTR [ESP],120
          call _putchar
          jmp L_43e664
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
L_43e6d0:
          sub DWORD PTR [ESP+28],1
          jne L_43e605
L_43e6db:
          add ESP,44
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
          .byte 0x8d
          .byte 0xbc
          .byte 0x27
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
FUN_43e6f0:
          push EBP
          push EDI
          push ESI
          push EBX
          push EAX
          mov EAX,32824
          call FUN_447c00
          sub ESP,EAX
          mov ESI,EDX
          mov EBX,ECX
          mov EAX,DWORD PTR [ESP+EAX*1]
          mov DWORD PTR [ESP+8],32768
          mov DWORD PTR [ESP+4],0
          mov EDI,EAX
          mov DWORD PTR [ESP+28],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _memset
          mov DWORD PTR [ESP],EDI
          call FUN_441410
          test EAX,EAX
          jne L_43e750
          add ESP,32828
          mov EAX,8
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43e750:
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+32852]
          xor EDX,EDX
          div EDI
          cmp EDX,1
          lea EDX,DWORD PTR [EBX+4]
          sbb EAX,-1
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP+36],EAX
          call _malloc
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],ESI
          mov ESI,EAX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+32],EAX
          add EBX,ESI
          call _memcpy
          mov DWORD PTR [ESP],EDI
          lea ESI,DWORD PTR [ESP+48]
          call _malloc
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+40],EBX
          xor EBX,EBX
          test EAX,EAX
          jne L_43e7cb
          jmp L_43e820
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_43e7b0:
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EDI
          add EBX,1
          mov DWORD PTR [ESP+4],EBP
          add ESI,EDI
          call _memcpy
          cmp DWORD PTR [ESP+36],EBX
          je L_43e820
L_43e7cb:
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [EAX],EBX
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          je L_43e7b0
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          add ESP,32828
          mov EAX,14
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
L_43e820:
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+32852]
          mov DWORD PTR [ESP+8],EAX
          lea EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+32848]
          mov DWORD PTR [ESP],EAX
          call _memcpy
          add ESP,32828
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_43e870:
          push EBX
          sub ESP,24
          mov EBX,DWORD PTR [ESP+32]
          test EBX,EBX
          je L_43e930
          mov EAX,DWORD PTR [EBX+4]
          test EAX,EAX
          je L_43e896
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+4],0
L_43e896:
          mov EAX,DWORD PTR [EBX+8]
          test EAX,EAX
          je L_43e8ac
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+8],0
L_43e8ac:
          mov EAX,DWORD PTR [EBX+12]
          test EAX,EAX
          je L_43e8c2
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+12],0
L_43e8c2:
          mov EAX,DWORD PTR [EBX+16]
          test EAX,EAX
          je L_43e8d8
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+16],0
L_43e8d8:
          mov EAX,DWORD PTR [EBX+24]
          test EAX,EAX
          je L_43e8ee
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+24],0
L_43e8ee:
          mov EAX,DWORD PTR [EBX+32]
          test EAX,EAX
          je L_43e904
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+32],0
L_43e904:
          mov EAX,DWORD PTR [EBX+36]
          test EAX,EAX
          je L_43e91a
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+36],0
L_43e91a:
          mov EAX,DWORD PTR [EBX+40]
          test EAX,EAX
          je L_43e930
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [EBX+40],0
L_43e930:
          add ESP,24
          pop EBX
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
FUN_43e940:
          push EBP
          push EDI
          xor EAX,EAX
          push ESI
          push EBX
          sub ESP,860
          mov EBX,DWORD PTR [ESP+880]
          mov ESI,DWORD PTR [ESP+884]
          lea EDI,DWORD PTR [EBX+4]
          mov ECX,EBX
          mov DWORD PTR [EBX],0
          mov DWORD PTR [EBX+40],0
          and EDI,4294967292
          sub ECX,EDI
          add ECX,44
          shr ECX,2
          cmp ESI,4
          rep stosd DWORD PTR ES:[EDI]
          mov EAX,2
          ja L_43e990
L_43e983:
          add ESP,860
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x66
          .byte 0x90
L_43e990:
          cmp ESI,64
          mov EAX,3
          ja L_43e983
          mov EDI,ESI
          mov EAX,ESI
          shr EDI,1
          sub EAX,EDI
          cmp EDI,EAX
          mov DWORD PTR [ESP+20],EAX
          mov EBP,EAX
          mov EAX,ESI
          cmovae EBP,EDI
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+24],EAX
          call _malloc
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+48],EAX
          call _mpSetZero
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+40],EAX
          call _mpSetZero
          mov EAX,DWORD PTR [ESP+888]
          test EAX,EAX
          jne L_43edc3
L_43e9fc:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+52],EAX
          call _mpSetZero
          mov EAX,EDI
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          call _malloc
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+72],EAX
          mov DWORD PTR [ESP+32],EAX
          call _mpSetZero
          mov EDX,DWORD PTR [ESP+20]
          shl EDX,5
          mov ECX,EDX
          shr ECX,3
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+68],ECX
          call _malloc
          mov EDX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+36],EAX
          mov DWORD PTR [ESP+4],EDX
          call _mpSetZero
          mov EDX,EBP
          shl EDX,5
          mov EAX,EDX
          shr EAX,3
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+28],EAX
          call _malloc
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+56],EAX
          call _mpSetZero
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDX
          call _malloc
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+60],EAX
          call _mpSetZero
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDX
          call _malloc
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+64],EAX
          call _mpSetZero
          mov EDX,DWORD PTR [ESP+888]
          mov EAX,DWORD PTR [ESP+32]
          mov ECX,EDI
          call FUN_43e5e0
          cmp EAX,-1
          jne L_43eaf0
L_43eae1:
          mov EAX,4
          jmp L_43e983
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_43eaf0:
          mov DWORD PTR [ESP],OFFSET L_461cc0
          call FUN_4490d0
          mov ECX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+888]
          mov EAX,DWORD PTR [ESP+36]
          call FUN_43e5e0
          cmp EAX,-1
          je L_43eae1
          mov DWORD PTR [ESP],OFFSET L_461cd3
          call FUN_4490d0
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _mpCompare
          test EAX,EAX
          jle L_43ede3
L_43eb41:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_461ce7
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP],OFFSET L_461cf8
          mov DWORD PTR [ESP+8],EDX
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+32]
          lea ECX,DWORD PTR [ESP+336]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+76],ECX
          mov DWORD PTR [ESP+4],EAX
          call _mpShortSub
          mov EDX,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+8],1
          mov DWORD PTR [ESP+4],EDX
          lea EDX,DWORD PTR [ESP+592]
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+68],EDX
          call _mpShortSub
          mov EDX,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [ESP+32]
          lea ECX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          call _mpMultiply
          lea ECX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],ECX
          mov ECX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],ECX
          call _mpSetEqual
          mov EDX,DWORD PTR [ESP+24]
          mov ECX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_461d09
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],ECX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+76]
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+68],ECX
          lea ECX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+72],EDX
          mov DWORD PTR [ESP],ECX
          call _mpMultiply
          mov ECX,EBP
          mov DWORD PTR [ESP],OFFSET L_461d19
          shl ECX,6
          mov EAX,ECX
          lea ECX,DWORD PTR [ESP+80]
          shr EAX,3
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],ECX
          call FUN_441890
          lea ECX,DWORD PTR [ESP+80]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+12],ESI
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],ECX
          call _mpModInv
          mov ECX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],OFFSET L_461d33
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],EDX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],OFFSET L_461d4d
          mov DWORD PTR [ESP+8],EDX
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+68]
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+4],ECX
          call _mpModInv
          mov ECX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EDX
          mov ECX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EDX
          call _mpModInv
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+12],EBP
          mov EAX,DWORD PTR [ESP+64]
          mov EBP,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EAX
          call _mpModInv
          mov EDX,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_461d68
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_461d75
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],OFFSET L_461d82
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBX],ESI
          mov DWORD PTR [EBX+16],EBP
          mov DWORD PTR [EBX+20],EDI
          mov DWORD PTR [EBX+4],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [EBX+8],ECX
          mov DWORD PTR [EBX+24],EDX
          mov ECX,DWORD PTR [ESP+20]
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [EBX+12],EAX
          mov EAX,DWORD PTR [ESP+60]
          mov DWORD PTR [EBX+28],ECX
          mov DWORD PTR [EBX+32],EDX
          mov DWORD PTR [EBX+36],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [EBX+40],EAX
          mov EAX,1
          jmp L_43e983
L_43edc3:
          mov EAX,DWORD PTR [ESP+888]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _mpSetDigit
          jmp L_43e9fc
L_43ede3:
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+68],EAX
          mov EAX,EDI
          mov EDI,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+36],EAX
          jmp L_43eb41
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
L_43ee20:
          sub ESP,44
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _mpModExp
          mov EAX,1
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
L_43ee60:
          sub ESP,44
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _mpModExp
          mov EAX,1
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
L_43eea0:
          sub ESP,44
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+12]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _mpModExp
          mov EAX,1
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
L_43eee0:
          sub ESP,44
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [EAX]
          mov DWORD PTR [ESP+16],EDX
          mov EDX,DWORD PTR [EAX+4]
          mov DWORD PTR [ESP+12],EDX
          mov EAX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _mpModExp
          mov EAX,1
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
L_43ef20:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+80]
          mov EBX,DWORD PTR [EAX]
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],EAX
          call FUN_441410
          test EAX,EAX
          mov EDX,8
          jne L_43ef50
L_43ef42:
          add ESP,60
          mov EAX,EDX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_43ef50:
          shl EBX,5
          mov ESI,EAX
          shr EBX,3
          lea EDX,DWORD PTR [ESI+ESI*1]
          lea EAX,DWORD PTR [EBX-2]
          sub EAX,EDX
          cmp EAX,DWORD PTR [ESP+92]
          mov EDX,5
          jb L_43ef42
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],OFFSET L_461d91
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+12],EAX
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          mov EDX,14
          jne L_43ef42
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_461da2
          call FUN_441890
          mov EAX,EBX
          mov DWORD PTR [ESP+4],1
          sub EAX,ESI
          lea ECX,DWORD PTR [EAX-1]
          mov DWORD PTR [ESP+32],EAX
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+24],ECX
          call _calloc
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EDI
          mov EBP,EAX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+32]
          sub EAX,DWORD PTR [ESP+92]
          mov EDX,DWORD PTR [ESP+92]
          mov BYTE PTR [EBP+EAX*1-2],1
          mov DWORD PTR [ESP+8],EDX
          lea EAX,DWORD PTR [EBP+EAX*1-1]
          mov EDX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],EDX
          call _memcpy
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_461dbb
          mov DWORD PTR [ESP+8],ECX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+28],EAX
          call FUN_441400
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461dcd
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],ECX
          call _malloc
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+36],EAX
          mov DWORD PTR [ESP],EAX
          mov EDX,DWORD PTR [ESP+28]
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],ECX
          mov ECX,ESI
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+40],EAX
          je L_43f0c8
          mov DWORD PTR [ESP],EDI
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [ESP+40]
          jmp L_43ef42
L_43f0c8:
          mov EAX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],OFFSET L_461de1
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+32]
          mov EDX,DWORD PTR [ESP+24]
          mov ECX,DWORD PTR [ESP+36]
          sub EAX,2
          test EDX,EDX
          je L_43f110
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43f100:
          movzx EDX,BYTE PTR [ECX+EAX*1]
          xor BYTE PTR [EBP+EAX*1],DL
          sub EAX,1
          cmp EAX,-1
          jne L_43f100
L_43f110:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_461df7
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+32],EAX
          mov EDX,EBP
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],ESI
          call FUN_43e6f0
          cmp EAX,1
          je L_43f184
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+24],EAX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [ESP+24]
          jmp L_43ef42
L_43f184:
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461e0f
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP+40],EBX
          mov ECX,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [ESI-1]
          mov EBX,DWORD PTR [ESP+32]
          nop
L_43f1b0:
          movzx EDX,BYTE PTR [EBX+EAX*1]
          xor BYTE PTR [ECX+EAX*1],DL
          sub EAX,1
          cmp EAX,-1
          jne L_43f1b0
          mov EAX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461e27
          mov EBX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EAX
          mov DWORD PTR [ESP+40],EDX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],0
          mov DWORD PTR [ESP],EDX
          call _memset
          mov EDX,DWORD PTR [ESP+104]
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],ESI
          lea EAX,DWORD PTR [EDX+1]
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EDX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EBP
          lea EAX,DWORD PTR [EDX+ESI*1+1]
          mov ESI,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],ESI
          call _memcpy
          mov ESI,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],OFFSET L_461e44
          mov DWORD PTR [ESP+4],ESI
          call FUN_441890
          mov DWORD PTR [ESP],EDI
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [ESP+40]
          jmp L_43ef42
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43f290:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov EAX,DWORD PTR [ESP+108]
          mov EDI,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],OFFSET L_461e66
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EAX,DWORD PTR [EDI]
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP],EAX
          mov EBP,EAX
          call _malloc
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],EAX
          call FUN_441410
          test EAX,EAX
          mov DWORD PTR [ESP+32],8
          jne L_43f300
L_43f2e3:
          mov DWORD PTR [ESP],EBX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43f300:
          mov ESI,EAX
          lea EAX,DWORD PTR [EBP-2]
          mov DWORD PTR [ESP+32],5
          lea EDX,DWORD PTR [ESI+ESI*1]
          sub EAX,EDX
          cmp DWORD PTR [ESP+108],EAX
          ja L_43f2e3
          mov EAX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP],OFFSET L_461d91
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          mov DWORD PTR [ESP+32],14
          jne L_43f2e3
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461da2
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EAX,EBP
          mov DWORD PTR [ESP+4],1
          sub EAX,ESI
          lea ECX,DWORD PTR [EAX-1]
          mov DWORD PTR [ESP+56],EAX
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+48],ECX
          call _calloc
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          mov DWORD PTR [ESP+4],EDX
          call _memcpy
          mov EDX,DWORD PTR [ESP+56]
          sub EDX,DWORD PTR [ESP+108]
          mov ECX,DWORD PTR [ESP+44]
          mov BYTE PTR [ECX+EDX*1-2],1
          lea EAX,DWORD PTR [ECX+EDX*1-1]
          mov EDX,DWORD PTR [ESP+108]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],EDX
          mov EDX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EDX
          call _memcpy
          mov ECX,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_461dbb
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],EDX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+36],EAX
          call FUN_441400
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461dcd
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EDX
          call _malloc
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+52],EAX
          mov ECX,ESI
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],EDX
          mov EDX,DWORD PTR [ESP+36]
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+32],EAX
          je L_43f494
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDX
          call _free
          mov ECX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],ECX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          jmp L_43f2e3
L_43f494:
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],OFFSET L_461de1
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+56]
          mov EDX,DWORD PTR [ESP+48]
          sub EAX,2
          test EDX,EDX
          je L_43f4e3
          mov EDX,DWORD PTR [ESP+44]
          mov ECX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+32],EBX
          nop
          .byte 0x8d,0x74,0x26,0x00   # lea ESI,DWORD PTR [ESI]
L_43f4d0:
          movzx EBX,BYTE PTR [ECX+EAX*1]
          xor BYTE PTR [EDX+EAX*1],BL
          sub EAX,1
          cmp EAX,-1
          jne L_43f4d0
          mov EBX,DWORD PTR [ESP+32]
L_43f4e3:
          mov EDX,DWORD PTR [ESP+44]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_461df7
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov ECX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+56],EAX
          mov DWORD PTR [ESP],EAX
          mov EDX,DWORD PTR [ESP+44]
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],ESI
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+32],EAX
          je L_43f561
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _free
          jmp L_43f2e3
L_43f561:
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461e0f
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESP+56]
          lea EAX,DWORD PTR [ESI-1]
          mov DWORD PTR [ESP+60],EBX
          nop
          .byte 0x8d,0xb4,0x26,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_43f590:
          movzx EBX,BYTE PTR [ECX+EAX*1]
          xor BYTE PTR [EDX+EAX*1],BL
          sub EAX,1
          cmp EAX,-1
          jne L_43f590
          mov EAX,DWORD PTR [ESP+36]
          mov EBX,DWORD PTR [ESP+60]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_461e27
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],0
          call _memset
          mov ECX,DWORD PTR [ESP+36]
          lea EAX,DWORD PTR [EBX+1]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov EDX,DWORD PTR [ESP+48]
          lea EAX,DWORD PTR [EBX+ESI*1+1]
          mov ESI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],ESI
          call _memcpy
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_461e44
          call FUN_441890
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDX
          call _free
          mov DWORD PTR [ESP],ESI
          call _free
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ECX
          call _free
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [EDI+4]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EDI+8]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+120]
          mov DWORD PTR [ESP],EAX
          call _mpModExp
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP],OFFSET L_461e83
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+120]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],EBX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_43f6b0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+80]
          mov EBX,DWORD PTR [ESP+88]
          mov EBP,DWORD PTR [EAX]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_461ea4
          shl EBP,5
          shr EBP,3
          mov DWORD PTR [ESP+8],EBP
          call FUN_441890
          cmp BYTE PTR [EBX],0
          mov EDX,7
          je L_43f6f0
L_43f6e5:
          add ESP,60
          mov EAX,EDX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
L_43f6f0:
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],EAX
          call FUN_441410
          test EAX,EAX
          mov ESI,EAX
          mov EDX,8
          je L_43f6e5
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP],OFFSET L_461ec6
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_43f842
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+8],ESI
          sub EBP,ESI
          mov DWORD PTR [ESP],OFFSET L_461ed7
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov EDI,EAX
          lea EAX,DWORD PTR [EBX+1]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_461ef0
          call FUN_441890
          lea EAX,DWORD PTR [EBP-1]
          mov DWORD PTR [ESP+36],EBP
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+24],EAX
          call _malloc
          lea ECX,DWORD PTR [ESI+1]
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EBP
          add EBX,ECX
          mov DWORD PTR [ESP+40],ECX
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_461f0a
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],ESI
          mov EDX,EBP
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+32],EAX
          je L_43f85b
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov DWORD PTR [ESP],EBX
          call _free
          mov EDX,DWORD PTR [ESP+32]
          jmp L_43f6e5
L_43f842:
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [ESP+24]
          jmp L_43f6e5
L_43f85b:
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_461f22
          call FUN_441890
          lea EAX,DWORD PTR [ESI-1]
L_43f872:
          movzx EDX,BYTE PTR [EDI+EAX*1]
          xor BYTE PTR [EBX+EAX*1],DL
          sub EAX,1
          cmp EAX,-1
          jne L_43f872
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_461f3a
          call FUN_441890
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+32],EAX
          mov EDX,EBX
          mov DWORD PTR [ESP],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],ECX
          mov ECX,ESI
          call FUN_43e6f0
          cmp EAX,1
          je L_43f8ff
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+24],EAX
          mov DWORD PTR [ESP],ECX
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov DWORD PTR [ESP],EBX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [ESP+24]
          jmp L_43f6e5
L_43f8ff:
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],OFFSET L_461f4e
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+24]
          mov ECX,DWORD PTR [ESP+36]
          sub ECX,2
          test EDX,EDX
          mov EDX,DWORD PTR [ESP+44]
          mov EAX,ECX
          je L_43f958
          mov DWORD PTR [ESP+36],EDI
          mov EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+44],EDX
L_43f940:
          movzx EDX,BYTE PTR [EBP+EAX*1]
          xor BYTE PTR [EDI+EAX*1],DL
          sub EAX,1
          cmp EAX,-1
          jne L_43f940
          mov EDI,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [ESP+44]
L_43f958:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP],OFFSET L_461f64
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP+36],ECX
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call FUN_449100
          test EAX,EAX
          mov ECX,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [ESP+44]
          jne L_43f9e4
          mov EAX,DWORD PTR [ESP+32]
          movzx EAX,BYTE PTR [EAX+ESI*1]
          test AL,AL
          jne L_43f9dc
          cmp ESI,ECX
          jae L_43f9e4
          mov DWORD PTR [ESP+24],EDI
          mov DWORD PTR [ESP+36],EBP
          mov EDI,DWORD PTR [ESP+40]
          mov EBP,DWORD PTR [ESP+32]
          jmp L_43f9c9
L_43f9c2:
          cmp EDI,ECX
          jae L_43fa1e
          add EDI,1
L_43f9c9:
          movzx EAX,BYTE PTR [EBP+EDI*1]
          mov ESI,EDI
          test AL,AL
          je L_43f9c2
          mov EDI,DWORD PTR [ESP+24]
          mov EBP,DWORD PTR [ESP+36]
L_43f9dc:
          cmp ESI,ECX
          je L_43f9e4
          sub AL,1
          je L_43fa28
L_43f9e4:
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov EDX,7
          jmp L_43f6e5
L_43fa1e:
          mov EDI,DWORD PTR [ESP+24]
          mov EBP,DWORD PTR [ESP+36]
          jmp L_43f9e4
L_43fa28:
          mov EAX,DWORD PTR [ESP+104]
          sub ECX,ESI
          mov DWORD PTR [ESP+24],EDX
          mov DWORD PTR [EAX],ECX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+100]
          lea EAX,DWORD PTR [EAX+ESI*1+1]
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov ECX,DWORD PTR [ESP+104]
          mov EAX,DWORD PTR [ECX]
          mov ECX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],OFFSET L_461f76
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],ECX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ECX
          call _free
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov EDX,DWORD PTR [ESP+24]
          jmp L_43f6e5
L_43faa7:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43fab0:
          push EBP
          push EDI
          push ESI
          push EBX
          mov EBX,8
          sub ESP,44
          mov ESI,DWORD PTR [ESP+68]
          mov EDI,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],ESI
          call FUN_441410
          test EAX,EAX
          jne L_43fae0
L_43fad0:
          add ESP,44
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
L_43fae0:
          mov EDX,DWORD PTR [EDI]
          lea EAX,DWORD PTR [EAX+EAX*1+2]
          mov EBX,7
          shl EDX,5
          shr EDX,3
          cmp EDX,EAX
          jb L_43fad0
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],OFFSET L_461f91
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EBX,DWORD PTR [EDI]
          mov EAX,EBX
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov DWORD PTR [ESP+16],EBX
          mov EBP,EAX
          mov EAX,DWORD PTR [EDI+4]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [EDI+12]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+4],EAX
          call _mpModExp
          mov EAX,DWORD PTR [EDI]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_461fb0
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+24],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+12],EAX
          call FUN_43f6b0
          mov DWORD PTR [ESP],EBP
          mov EBX,EAX
          call _free
          jmp L_43fad0
          .byte 0x66
          .byte 0x90
L_43fba0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov ESI,DWORD PTR [ESP+96]
          mov EBX,DWORD PTR [ESI]
          shl EBX,5
          shr EBX,3
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],EAX
          call FUN_441410
          mov EDI,EAX
          mov EAX,8
          test EDI,EDI
          jne L_43fbf0
L_43fbd4:
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+36],EAX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_43fbf0:
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [ESP],OFFSET L_461fe9
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],EDI
          call _malloc
          mov DWORD PTR [ESP+36],EAX
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_43fc80
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],OFFSET L_461fff
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+112]
          add EDX,EDI
          lea EAX,DWORD PTR [EDX+2]
          cmp EBX,EAX
          jae L_43fd00
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,13
          jmp L_43fbd4
          .byte 0x90
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_43fc80:
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+40]
L_43fc94:
          cmp EAX,1
          jne L_43fbd4
L_43fc9d:
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+16],EAX
          mov EAX,DWORD PTR [ESI+4]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESI+12]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP],EAX
          call _mpModExp
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP],OFFSET L_4620db
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+116]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],EBP
          call _free
          add ESP,76
          mov EAX,1
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_43fd00:
          mov EAX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+40],EDX
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          mov DWORD PTR [ESP+4],ECX
          call FUN_441400
          mov EDX,DWORD PTR [ESP+112]
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_46201c
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],1
          add EDX,8
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+48],EDX
          call _calloc
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+40],EAX
          add EAX,8
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov ECX,DWORD PTR [ESP+112]
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+44]
          lea EAX,DWORD PTR [EAX+EDI*1+8]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov EDX,DWORD PTR [ESP+48]
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],OFFSET L_462030
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+40]
          mov ECX,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+12],ECX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_43fed4
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP],OFFSET L_462054
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          lea EAX,DWORD PTR [EBX-1]
          mov DWORD PTR [ESP+4],1
          sub EAX,EDI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+48],EAX
          call _calloc
          mov ECX,EBX
          sub ECX,DWORD PTR [ESP+112]
          mov EDX,EAX
          mov DWORD PTR [ESP+56],EDX
          mov EAX,ECX
          mov ECX,DWORD PTR [ESP+112]
          sub EAX,EDI
          mov BYTE PTR [EDX+EAX*1-2],1
          lea EAX,DWORD PTR [EDX+EAX*1-1]
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov EDX,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],OFFSET L_462080
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+52],EAX
          mov DWORD PTR [ESP],EAX
          mov EDX,DWORD PTR [ESP+36]
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],ECX
          mov ECX,EDI
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+60],EAX
          je L_43ff05
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov ESI,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],ESI
          call _free
          mov EDI,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EDI
          call _free
          mov ECX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],ECX
          call _free
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EDX
          call _free
          mov EAX,DWORD PTR [ESP+60]
          jmp L_43fbd4
L_43fed4:
          mov DWORD PTR [ESP+48],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+48]
          jmp L_43fc94
L_43ff05:
          mov EAX,DWORD PTR [ESP+48]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],OFFSET L_462091
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+48]
          mov EAX,ECX
          sub EAX,1
          test ECX,ECX
          je L_43ff53
          mov ECX,DWORD PTR [ESP+56]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+40],EBX
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_43ff40:
          movzx EBX,BYTE PTR [ECX+EAX*1]
          xor BYTE PTR [EDX+EAX*1],BL
          sub EAX,1
          cmp EAX,-1
          jne L_43ff40
          mov EBX,DWORD PTR [ESP+40]
L_43ff53:
          mov EAX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],OFFSET L_4620a6
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],ECX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+52]
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP+8],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+48]
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+8],EDI
          add EAX,EBP
          mov DWORD PTR [ESP+4],ECX
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov BYTE PTR [EBP+EBX*1-1],188
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_4620bd
          call FUN_441890
          jmp L_43fc9d
          .byte 0x90
L_43ffc0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,76
          mov ESI,DWORD PTR [ESP+96]
          mov EDI,DWORD PTR [ESP+116]
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_4620db
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EBP,DWORD PTR [ESI]
          mov EAX,EBP
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov DWORD PTR [ESP+16],EBP
          mov EBX,EAX
          mov EAX,DWORD PTR [ESI+4]
          mov DWORD PTR [ESP+12],EAX
          mov EAX,DWORD PTR [ESI+8]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],EAX
          call _mpModExp
          mov EAX,DWORD PTR [ESI]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_4620e8
          shl EAX,5
          shr EAX,3
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+100]
          mov EDI,DWORD PTR [ESI]
          mov DWORD PTR [ESP],EAX
          call FUN_441410
          test EAX,EAX
          jne L_440060
L_44004b:
          mov DWORD PTR [ESP],EBX
          call _free
          mov EAX,10
L_440058:
          add ESP,76
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_440060:
          mov ESI,EAX
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [ESP],OFFSET L_462111
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov DWORD PTR [ESP+12],EAX
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+108]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+104]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_440102
          shl EDI,5
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          shr EDI,3
          mov DWORD PTR [ESP],OFFSET L_462125
          call FUN_441890
          mov DWORD PTR [ESP+8],EDI
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],OFFSET L_462141
          call FUN_441890
          mov EAX,DWORD PTR [ESP+112]
          add EAX,ESI
          mov DWORD PTR [ESP+40],EAX
          add EAX,2
          cmp EDI,EAX
          jb L_4400f5
          cmp BYTE PTR [EBX+EDI*1-1],188
          lea EAX,DWORD PTR [EDI-1]
          je L_440133
L_4400f5:
          mov DWORD PTR [ESP],EBP
          call _free
          jmp L_44004b
L_440102:
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+40],EAX
          call _free
          mov EAX,DWORD PTR [ESP+40]
L_440112:
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+40],EAX
          call _free
          mov EAX,DWORD PTR [ESP+40]
          cmp EAX,11
          setne AL
          movzx EAX,AL
          add EAX,9
          jmp L_440058
L_440133:
          sub EAX,ESI
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+44],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+4],EBX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+56],EAX
          mov DWORD PTR [ESP+8],ECX
          call _memcpy
          mov EDX,DWORD PTR [ESP+56]
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_46215d
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov DWORD PTR [ESP],ESI
          call _malloc
          mov ECX,DWORD PTR [ESP+44]
          mov EDX,EAX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+48],EDX
          lea EAX,DWORD PTR [EBX+ECX*1]
          mov DWORD PTR [ESP+4],EAX
          call _memcpy
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP],OFFSET L_462172
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],ECX
          call _malloc
          mov ECX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP+52],EAX
          mov DWORD PTR [ESP],EAX
          mov EDX,DWORD PTR [ESP+48]
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP+4],ECX
          mov ECX,ESI
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+60],EAX
          je L_44021a
          mov EDX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EDX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EDX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EDX
          call _free
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+60]
          jmp L_440112
L_44021a:
          mov EAX,DWORD PTR [ESP+44]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],OFFSET L_462180
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+44]
          mov EAX,ECX
          sub EAX,1
          test ECX,ECX
          je L_440263
          mov ECX,DWORD PTR [ESP+56]
          mov EDX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+60],EBX
          nop
L_440250:
          movzx EBX,BYTE PTR [ECX+EAX*1]
          xor BYTE PTR [EDX+EAX*1],BL
          sub EAX,1
          cmp EAX,-1
          jne L_440250
          mov EBX,DWORD PTR [ESP+60]
L_440263:
          mov EAX,DWORD PTR [ESP+44]
          mov DWORD PTR [ESP],OFFSET L_462193
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          sub EDI,DWORD PTR [ESP+112]
          mov EAX,DWORD PTR [ESP+52]
          mov EDX,EDI
          sub EDX,ESI
          cmp BYTE PTR [EAX+EDX*1-2],1
          je L_4402c3
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _free
          jmp L_44004b
L_4402c3:
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP+44],EDX
          add EAX,8
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+40],EAX
          call _calloc
          mov EDI,EAX
          lea EAX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov ECX,DWORD PTR [ESP+52]
          mov EDX,DWORD PTR [ESP+44]
          lea EAX,DWORD PTR [EDI+ESI*1+8]
          mov DWORD PTR [ESP],EAX
          lea EDX,DWORD PTR [ECX+EDX*1-1]
          mov ECX,DWORD PTR [ESP+112]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],ECX
          call _memcpy
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_4621a4
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+12],EBP
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_440395
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_4621c4
          call FUN_441890
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call FUN_449100
          test EAX,EAX
          jne L_44004b
          mov DWORD PTR [ESP],EBX
          call _free
          mov EAX,9
          jmp L_440058
L_440395:
          mov DWORD PTR [ESP+40],EAX
          mov EAX,DWORD PTR [ESP+48]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+56]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+52]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov EAX,DWORD PTR [ESP+40]
          jmp L_440112
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4403e0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EAX
          call FUN_441410
          test EAX,EAX
          mov EDX,8
          jne L_440410
L_4403fc:
          add ESP,44
          mov EAX,EDX
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_440410:
          mov EBX,EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP],OFFSET L_461fe9
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov DWORD PTR [ESP+12],EAX
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+68]
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_440491
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_461fff
          call FUN_441890
          mov EBP,DWORD PTR [ESP+76]
          add EBP,EBX
          lea EAX,DWORD PTR [EBP+2]
          cmp EAX,DWORD PTR [ESP+84]
          jbe L_4404b0
          mov DWORD PTR [ESP],EDI
          call _free
          mov EDX,13
          jmp L_4403fc
L_440491:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+20],EAX
          call _free
          mov EDX,DWORD PTR [ESP+20]
          jmp L_4403fc
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_4404b0:
          mov EAX,DWORD PTR [ESP+76]
          add EBP,8
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP],EAX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],ECX
          call FUN_441400
          mov EAX,DWORD PTR [ESP+76]
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_46201c
          mov DWORD PTR [ESP+20],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EBP
          call _calloc
          mov ESI,EAX
          mov DWORD PTR [ESP+28],EAX
          add EAX,8
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EDX,DWORD PTR [ESP+76]
          mov ECX,DWORD PTR [ESP+20]
          lea EAX,DWORD PTR [ESI+EBX*1+8]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_462030
          call FUN_441890
          mov EAX,DWORD PTR [ESP+64]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_441480
          test EAX,EAX
          jne L_440640
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_462054
          call FUN_441890
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],1
          sub EAX,1
          sub EAX,EBX
          mov DWORD PTR [ESP],EAX
          mov EBP,EAX
          call _calloc
          mov ESI,EAX
          mov EAX,DWORD PTR [ESP+84]
          sub EAX,DWORD PTR [ESP+76]
          mov ECX,DWORD PTR [ESP+76]
          sub EAX,EBX
          mov BYTE PTR [ESI+EAX*1-2],1
          mov DWORD PTR [ESP+8],ECX
          lea EAX,DWORD PTR [ESI+EAX*1-1]
          mov ECX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov DWORD PTR [ESP+8],EBP
          mov DWORD PTR [ESP+4],ESI
          mov DWORD PTR [ESP],OFFSET L_462080
          call FUN_441890
          mov DWORD PTR [ESP],EBP
          mov DWORD PTR [ESP+24],EBP
          call _malloc
          mov EBP,EAX
          mov EAX,DWORD PTR [ESP+24]
          mov ECX,EBX
          mov DWORD PTR [ESP],EBP
          mov EDX,EDI
          mov DWORD PTR [ESP+4],EAX
          mov EAX,DWORD PTR [ESP+64]
          call FUN_43e6f0
          cmp EAX,1
          je L_44066d
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+24],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov ECX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],ECX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov DWORD PTR [ESP],ESI
          call _free
          mov EDX,DWORD PTR [ESP+24]
          jmp L_4403fc
          .byte 0x66
          .byte 0x90
L_440640:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+24],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+20]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EDX,DWORD PTR [ESP+24]
          jmp L_4403fc
L_44066d:
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_462091
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+24]
          mov EDX,DWORD PTR [ESP+20]
          mov EAX,ECX
          sub EAX,1
          test ECX,ECX
          je L_4406b0
          .byte 0x8d,0xb6,0x00,0x00,0x00,0x00   # lea ESI,DWORD PTR [ESI]
L_4406a0:
          movzx ECX,BYTE PTR [ESI+EAX*1]
          xor BYTE PTR [EBP+EAX*1],CL
          sub EAX,1
          cmp EAX,-1
          jne L_4406a0
L_4406b0:
          mov ESI,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_4620a6
          mov DWORD PTR [ESP+20],EDX
          mov DWORD PTR [ESP+8],ESI
          call FUN_441890
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          add EAX,ESI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov EAX,DWORD PTR [ESP+80]
          mov ECX,DWORD PTR [ESP+84]
          mov BYTE PTR [EAX+ECX*1-1],188
          mov EAX,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP+8],ECX
          mov DWORD PTR [ESP],OFFSET L_4620bd
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+20]
          jmp L_4403fc
          .byte 0x8d
          .byte 0xb6
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8d,0xbf,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_440730:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov ESI,DWORD PTR [ESP+80]
          mov DWORD PTR [ESP],ESI
          call FUN_441410
          mov EBX,EAX
          mov EAX,8
          test EBX,EBX
          jne L_440760
L_44074e:
          add ESP,60
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_440760:
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],OFFSET L_462111
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov DWORD PTR [ESP+12],EAX
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+84]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441480
          test EAX,EAX
          jne L_440810
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_462125
          call FUN_441890
          mov EAX,DWORD PTR [ESP+100]
          mov DWORD PTR [ESP],OFFSET L_462141
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EBP,DWORD PTR [ESP+92]
          add EBP,EBX
          lea EAX,DWORD PTR [EBP+2]
          cmp DWORD PTR [ESP+100],EAX
          jb L_4407fb
          mov EAX,DWORD PTR [ESP+100]
          mov ECX,DWORD PTR [ESP+96]
          mov EDX,DWORD PTR [ESP+100]
          sub EAX,1
          cmp BYTE PTR [ECX+EDX*1-1],188
          je L_440825
L_4407fb:
          mov DWORD PTR [ESP],EDI
          call _free
          mov EAX,12
          jmp L_44074e
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440810:
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+28],EAX
          call _free
          mov EAX,DWORD PTR [ESP+28]
          jmp L_44074e
L_440825:
          sub EAX,EBX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+28],EAX
          call _malloc
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+40],EAX
          mov DWORD PTR [ESP+8],ECX
          mov ECX,DWORD PTR [ESP+96]
          mov DWORD PTR [ESP+4],ECX
          call _memcpy
          mov EDX,DWORD PTR [ESP+40]
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],OFFSET L_46215d
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov DWORD PTR [ESP],EBX
          call _malloc
          mov EDX,DWORD PTR [ESP+28]
          add EDX,DWORD PTR [ESP+96]
          mov ECX,EAX
          mov DWORD PTR [ESP],ECX
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+32],ECX
          mov DWORD PTR [ESP+4],EDX
          call _memcpy
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP],OFFSET L_462172
          mov DWORD PTR [ESP+4],ECX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EAX
          call _malloc
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+36],EAX
          mov ECX,EBX
          mov DWORD PTR [ESP],EAX
          mov EAX,ESI
          mov DWORD PTR [ESP+4],EDX
          mov EDX,DWORD PTR [ESP+32]
          call FUN_43e6f0
          cmp EAX,1
          mov DWORD PTR [ESP+44],EAX
          je L_44090f
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ECX
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EDX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+44]
          jmp L_44074e
L_44090f:
          mov EAX,DWORD PTR [ESP+28]
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],OFFSET L_462180
          mov DWORD PTR [ESP+8],EAX
          mov DWORD PTR [ESP+4],EDX
          call FUN_441890
          mov ECX,DWORD PTR [ESP+28]
          mov EAX,ECX
          sub EAX,1
          test ECX,ECX
          je L_440957
          mov ECX,DWORD PTR [ESP+40]
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+44],EBX
L_440944:
          movzx EBX,BYTE PTR [ECX+EAX*1]
          xor BYTE PTR [EDX+EAX*1],BL
          sub EAX,1
          cmp EAX,-1
          jne L_440944
          mov EBX,DWORD PTR [ESP+44]
L_440957:
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],OFFSET L_462193
          mov DWORD PTR [ESP+8],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],EAX
          call FUN_441890
          mov EDX,DWORD PTR [ESP+100]
          sub EDX,DWORD PTR [ESP+92]
          mov EAX,DWORD PTR [ESP+36]
          sub EDX,EBX
          cmp BYTE PTR [EAX+EDX*1-2],1
          je L_4409be
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,12
          jmp L_44074e
L_4409be:
          lea EAX,DWORD PTR [EBP+8]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP+44],EDX
          mov DWORD PTR [ESP],EAX
          mov DWORD PTR [ESP+28],EAX
          call _calloc
          mov EBP,EAX
          lea EAX,DWORD PTR [EAX+8]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call _memcpy
          mov ECX,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [ESP+44]
          lea EAX,DWORD PTR [EBP+EBX*1+8]
          mov DWORD PTR [ESP],EAX
          lea EDX,DWORD PTR [ECX+EDX*1-1]
          mov ECX,DWORD PTR [ESP+92]
          mov DWORD PTR [ESP+4],EDX
          mov DWORD PTR [ESP+8],ECX
          call _memcpy
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],OFFSET L_4621a4
          mov DWORD PTR [ESP+8],EAX
          call FUN_441890
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+12],EDI
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],EAX
          call FUN_441480
          test EAX,EAX
          jne L_440a7e
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],OFFSET L_4621c4
          call FUN_441890
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],EAX
          call FUN_449100
          test EAX,EAX
          setne AL
          movzx EAX,AL
          add EAX,11
          jmp L_44074e
L_440a7e:
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EDI
          call _free
          mov EAX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP],EAX
          call _free
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call _free
          mov DWORD PTR [ESP],EBP
          call _free
          mov EAX,DWORD PTR [ESP+28]
          jmp L_44074e
          .byte 0x90
L_440ac0:
          mov EAX,DWORD PTR [ESP+4]
          cmp EAX,14
          ja L_440bb0
          jmp DWORD PTR [EAX*4+L_4623f8]
L_440ad4:
          mov DWORD PTR [ESP+4],OFFSET L_4623a8
          jmp FUN_4490d0
L_440ae1:
          mov DWORD PTR [ESP+4],OFFSET L_4621eb
          jmp FUN_4490d0
          .byte 0x66
          .byte 0x90
L_440af0:
          mov DWORD PTR [ESP+4],OFFSET L_462204
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b00:
          mov DWORD PTR [ESP+4],OFFSET L_462228
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b10:
          mov DWORD PTR [ESP+4],OFFSET L_46224c
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b20:
          mov DWORD PTR [ESP+4],OFFSET L_462276
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b30:
          mov DWORD PTR [ESP+4],OFFSET L_462291
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b40:
          mov DWORD PTR [ESP+4],OFFSET L_4622ae
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b50:
          mov DWORD PTR [ESP+4],OFFSET L_4622cc
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b60:
          mov DWORD PTR [ESP+4],OFFSET L_4622f2
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b70:
          mov DWORD PTR [ESP+4],OFFSET L_462310
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b80:
          mov DWORD PTR [ESP+4],OFFSET L_462330
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440b90:
          mov DWORD PTR [ESP+4],OFFSET L_46235c
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440ba0:
          mov DWORD PTR [ESP+4],OFFSET L_46238a
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440bb0:
          mov DWORD PTR [ESP+4],OFFSET L_4623e6
          jmp FUN_4490d0
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_440bc0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,1772
          mov EAX,DWORD PTR [ESP+1792]
          mov DWORD PTR [ESP+4],OFFSET L_462434
          mov EBP,DWORD PTR [ESP+1796]
          mov DWORD PTR [ESP],EAX
          call FUN_449160
          test EAX,EAX
          je L_440cdc
          lea EBX,DWORD PTR [ESP+30]
          lea EDI,DWORD PTR [ESP+32]
          mov ESI,EAX
          xor EAX,EAX
          mov DWORD PTR [ESP+30],0
          mov DWORD PTR [ESP+1756],0
          mov ECX,EBX
          sub ECX,EDI
          add ECX,1730
          shr ECX,2
          rep stosd DWORD PTR ES:[EDI]
          xor EDI,EDI
L_440c20:
          mov DWORD PTR [ESP],ESI
          call FUN_449188
          test EAX,EAX
          jne L_440cd4
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+8],ESI
          mov DWORD PTR [ESP+4],346
          call FUN_449168
          mov DWORD PTR [ESP],EBX
          add EBX,346
          call _strlen
          imul EDX,EDI,346
          lea ECX,DWORD PTR [ESP+1760]
          add EDI,1
          add EDX,ECX
          cmp EDI,5
          mov BYTE PTR [EAX+EDX*1-1731],0
          jne L_440c20
          mov DWORD PTR [ESP],ESI
          lea EBX,DWORD PTR [ESP+24]
          call FUN_449190
          lea EAX,DWORD PTR [ESP+376]
          mov DWORD PTR [ESP],EAX
          call FUN_4491a8
          mov DWORD PTR [EBP],EAX
          lea EAX,DWORD PTR [ESP+722]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441330
          test EAX,EAX
          mov DWORD PTR [EBP+4],EAX
          je L_440cdc
          lea EAX,DWORD PTR [ESP+1068]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441330
          test EAX,EAX
          mov DWORD PTR [EBP+8],EAX
          sete AL
          add ESP,1772
          movzx EAX,AL
          pop EBX
          neg EAX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_440cd4:
          mov DWORD PTR [ESP],ESI
          call FUN_449190
L_440cdc:
          add ESP,1772
          mov EAX,4294967295
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
L_440cf0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,2108
          mov EAX,DWORD PTR [ESP+2128]
          mov DWORD PTR [ESP+4],OFFSET L_462434
          mov ESI,DWORD PTR [ESP+2132]
          mov DWORD PTR [ESP],EAX
          call FUN_449160
          test EAX,EAX
          je L_440e0a
          lea EDX,DWORD PTR [ESP+20]
          mov EBX,EAX
          mov ECX,519
          xor EAX,EAX
          xor EBP,EBP
          mov EDI,EDX
          rep stosd DWORD PTR ES:[EDI]
          mov EDI,EDX
L_440d35:
          mov DWORD PTR [ESP],EBX
          call FUN_449188
          test EAX,EAX
          jne L_440e02
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+8],EBX
          mov DWORD PTR [ESP+4],346
          call FUN_449168
          mov DWORD PTR [ESP],EDI
          add EDI,346
          call _strlen
          imul EDX,EBP,346
          lea ECX,DWORD PTR [ESP+2096]
          add EBP,1
          add EDX,ECX
          cmp EBP,5
          mov BYTE PTR [EAX+EDX*1-2077],0
          jne L_440d35
          mov DWORD PTR [ESP],EBX
          lea EBX,DWORD PTR [ESP+16]
          call FUN_449190
          lea EAX,DWORD PTR [ESP+366]
          mov DWORD PTR [ESP],EAX
          call FUN_4491a8
          mov DWORD PTR [ESI],EAX
          lea EAX,DWORD PTR [ESP+712]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441330
          test EAX,EAX
          mov DWORD PTR [ESI+4],EAX
          je L_440e0a
          lea EAX,DWORD PTR [ESP+1058]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441330
          test EAX,EAX
          mov DWORD PTR [ESI+8],EAX
          je L_440e0a
          lea EAX,DWORD PTR [ESP+1404]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],EAX
          call FUN_441330
          test EAX,EAX
          mov DWORD PTR [ESI+12],EAX
          sete AL
          add ESP,2108
          movzx EAX,AL
          pop EBX
          neg EAX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_440e02:
          mov DWORD PTR [ESP],EBX
          call FUN_449190
L_440e0a:
          add ESP,2108
          mov EAX,4294967295
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90
          .byte 0x90

.section .rdata,"dr"
.p2align 2
L_461ca4:
          .string "making rand of 0x%x digits\n"
L_461cc0:
          .string "\nfirst prime found"
L_461cd3:
          .string "\nsecond prime found"
L_461ce7:
          .string "Key Gen: prime p"
L_461cf8:
          .string "Key Gen: prime q"
L_461d09:
          .string "Key Gen Modulus"
L_461d19:
          .string "Key Gen Phi(n)=(p-1)(q-1)"
L_461d33:
          .string "Key Gen Public Exponent e"
L_461d4d:
          .string "Key Gen Private Exponent d"
L_461d68:
          .string "CRT value dP"
L_461d75:
          .string "CRT value dQ"
L_461d82:
          .string "CRT value qInv"
L_461d91:
          .string "OAEP Encoding: L"
L_461da2:
          .string "OAEP Encoding: Hash of L"
L_461dbb:
          .string "OAEP Encoding: DB"
L_461dcd:
          .string "OAEP Encoding: seed"
L_461de1:
          .string "OAEP Encoding: dbMask"
L_461df7:
          .string "OAEP Encoding: maskedDB"
L_461e0f:
          .string "OAEP Encoding: seedMask"
L_461e27:
          .string "OAEP Encoding: maskedSeed"
          .zero 3
L_461e44:
          .string "OAEP Encoding: Encoded Message em"
L_461e66:
          .string "RSAOAEP Encrypt: Plaintext m"
L_461e83:
          .string "RSAOAEP Encrypt: Ciphertext c"
          .zero 3
L_461ea4:
          .string "OAEP Decoding: Encoded Message em"
L_461ec6:
          .string "OAEP Decoding: L"
L_461ed7:
          .string "OAEP Decoding: Hash of L"
L_461ef0:
          .string "OAEP Decoding: maskedSeed"
L_461f0a:
          .string "OAEP Decoding: maskedDB"
L_461f22:
          .string "OAEP Decoding: seedMask"
L_461f3a:
          .string "OAEP Decoding: seed"
L_461f4e:
          .string "OAEP Decoding: dbMask"
L_461f64:
          .string "OAEP Decoding: DB"
L_461f76:
          .string "OAEP Decoding: Plaintext m"
L_461f91:
          .string "RSAOAEP Decrypt: Ciphertext"
          .zero 3
L_461fb0:
          .string "RSAOAEP Decrypt: OAEP-Encoded Message (After Decryption)"
L_461fe9:
          .string "PSS Encoding: Message"
L_461fff:
          .string "PSS Encoding: Hashed Message"
L_46201c:
          .string "PSS Encoding: Salt"
          .zero 1
L_462030:
          .string "PSS Encoding: Message to be encoded"
L_462054:
          .string "PSS Encoding: Hash of Message to be encoded"
L_462080:
          .string "PSS Encoding: DB"
L_462091:
          .string "PSS Encoding: dbMask"
L_4620a6:
          .string "PSS Encoding: maskedDB"
L_4620bd:
          .string "PSS Encoding: Encoded Message"
L_4620db:
          .string "Signature"
          .zero 3
L_4620e8:
          .string "PSS-Encoded Message (Before Verificaton)"
L_462111:
          .string "PSS Verify: Message"
L_462125:
          .string "PSS Verify: Hash of Message"
L_462141:
          .string "PSS Verify: Encoded Message"
L_46215d:
          .string "PSS Verify: maskedDB"
L_462172:
          .string "PSS Verify: H"
L_462180:
          .string "PSS Verify: dbMask"
L_462193:
          .string "PSS Verify: DB"
          .zero 2
L_4621a4:
          .string "PSS Verify: Message to encoded"
          .zero 1
L_4621c4:
          .string "PSS Verify: Hash of Message to encoded"
L_4621eb:
          .string "Job Done Successfully!!!"
L_462204:
          .string "Wow!!! Modulus Length Too Short."
          .zero 3
L_462228:
          .string "Sorry!!! Modulus Length Too Long."
          .zero 2
L_46224c:
          .string "Failed To Generate A Prime. Try It Again."
L_462276:
          .string "Sorry!!! Message Too Long."
L_462291:
          .string "Sorry!!! OAEP Label Too Long"
L_4622ae:
          .string "Sorry!!! Decryption Error."
          .zero 3
L_4622cc:
          .string "Sorry!!! Hash Function Not Available."
L_4622f2:
          .string "Good!!! Signature Is Valid."
          .zero 2
L_462310:
          .string "Sorry!!! Signature Is Invalid."
          .zero 1
L_462330:
          .string "Good!!! PSS-Encoded Message Is Consistent."
          .zero 1
L_46235c:
          .string "Sorry!!! PSS-Encoded Message Is Inconsistent."
L_46238a:
          .string "Sorry!!! PSS Encoding Error"
          .zero 2
L_4623a8:
          .string "Sorry!!! Hash Function Error. Maybe Hash Input Limit Exceeded"
L_4623e6:
          .string "Unkown Error!!!"
          .zero 2
L_4623f8:
          .long L_440bb0
          .long L_440ae1
          .long L_440af0
          .long L_440b00
          .long L_440b10
          .long L_440b20
          .long L_440b30
          .long L_440b40
          .long L_440b50
          .long L_440b60
          .long L_440b70
          .long L_440b80
          .long L_440b90
          .long L_440ba0
          .long L_440ad4
L_462434:
          .string "r"
          .zero 2

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
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x1c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_43e5e0 - .
          .byte 0x5
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
          .byte 0x4f
          .byte 0xe
          .byte 0x40
          .byte 0x2
          .byte 0xe9
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
          .byte 0x6c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x58
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_43e6f0 - .
          .byte 0x76
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
          .byte 0x41
          .byte 0xe
          .byte 0x18
          .byte 0x4c
          .byte 0xe
          .byte 0xd0
          .byte 0x80
          .byte 0x2
          .byte 0x7b
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
          .byte 0x4b
          .byte 0xb
          .byte 0x2
          .byte 0xbf
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
          .byte 0x48
          .byte 0xb
          .byte 0x7c
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
          .byte 0x20
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xc8
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_43e870 - .
          .byte 0xc5
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
          .byte 0x2
          .byte 0xbf
          .byte 0xe
          .byte 0x8
          .byte 0x41
          .byte 0xc3
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xec
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_43e940 - .
          .byte 0xd2
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
          .byte 0x46
          .byte 0xe
          .byte 0xf0
          .byte 0x6
          .byte 0x7d
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
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x2c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43ee20 - .
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x74
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x44
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43ee60 - .
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x74
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x5c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43eea0 - .
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x74
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x14
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x74
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43eee0 - .
          .byte 0x38
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x43
          .byte 0xe
          .byte 0x30
          .byte 0x74
          .byte 0xe
          .byte 0x4
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x8c
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43ef20 - .
          .byte 0x67
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
          .byte 0x50
          .byte 0x5e
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
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x1
          .byte 0x0
          .byte 0x0
          .long L_43f290 - .
          .byte 0x16
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
          .byte 0x2
          .byte 0x5b
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
          .byte 0xa1
          .byte 0x3
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
          .byte 0x20
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long FUN_43f6b0 - .
          .byte 0xf7
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
          .byte 0x50
          .byte 0x71
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
          .byte 0x42
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x60
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_43fab0 - .
          .byte 0xee
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
          .byte 0x48
          .byte 0xe
          .byte 0x40
          .byte 0x57
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
          .byte 0x0
          .byte 0x54
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xa0
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_43fba0 - .
          .byte 0x1f
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
          .byte 0x2
          .byte 0x40
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
          .byte 0x2
          .byte 0xfc
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xf8
          .byte 0x2
          .byte 0x0
          .byte 0x0
          .long L_43ffc0 - .
          .byte 0x16
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
          .byte 0x2
          .byte 0x94
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
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x38
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_4403e0 - .
          .byte 0x44
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
          .byte 0x58
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x78
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_440730 - .
          .byte 0x8f
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
          .byte 0x50
          .byte 0x5a
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
          .byte 0x4b
          .byte 0xb
          .byte 0x0
          .byte 0x0
          .byte 0x10
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb8
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_440ac0 - .
          .byte 0xfd
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xcc
          .byte 0x3
          .byte 0x0
          .byte 0x0
          .long L_440bc0 - .
          .byte 0x2c
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
          .byte 0x80
          .byte 0xe
          .byte 0x3
          .byte 0x0
          .byte 0x1
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x4e
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
          .byte 0x50
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x20
          .byte 0x4
          .byte 0x0
          .byte 0x0
          .long L_440cf0 - .
          .byte 0x2a
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
          .byte 0x10
          .byte 0x2
          .byte 0xfe
          .byte 0xa
          .byte 0xe
          .byte 0x14
          .byte 0x44
          .byte 0xc3
          .byte 0xe
          .byte 0x10
          .byte 0x43
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
          .byte 0x4e
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
