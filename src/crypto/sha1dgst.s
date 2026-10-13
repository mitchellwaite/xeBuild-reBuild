# crypto/sha1dgst.s -- SHA-1 init/block/update/final
#
# original placement:
#   .data          0044b6a0-0044b6a4
#   .eh_frame      0046d92c-0046da18
#   .rdata$zzz     00464144-00464170
#   .text          00442b00-00444fb0

.intel_syntax noprefix
.globl FUN_442b00
.globl FUN_4448d0
.globl FUN_444da0

.text
.p2align 4
FUN_442b00:
          mov EAX,DWORD PTR [ESP+4]
          mov DWORD PTR [EAX],1732584193
          mov DWORD PTR [EAX+4],4023233417
          mov DWORD PTR [EAX+8],2562383102
          mov DWORD PTR [EAX+12],271733878
          mov DWORD PTR [EAX+16],3285377520
          mov DWORD PTR [EAX+20],0
          mov DWORD PTR [EAX+24],0
          mov DWORD PTR [EAX+92],0
          ret 
          .byte 0x8d
          .byte 0x74
          .byte 0x26
          .byte 0x0
FUN_442b40:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,60
          mov EAX,DWORD PTR [ESP+80]
          mov EDI,DWORD PTR [ESP+80]
          mov EBX,DWORD PTR [ESP+84]
          mov EDX,DWORD PTR [EAX]
          mov ESI,DWORD PTR [EAX+4]
          mov EAX,DWORD PTR [EAX+8]
          mov EDI,DWORD PTR [EDI+16]
          mov EBP,EBX
          mov DWORD PTR [ESP+32],EDX
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [ESP+80]
          mov EBX,EDI
          mov EAX,DWORD PTR [EAX+12]
          mov EDX,EAX
          jmp L_442b78
L_442b75:
          add EBP,64
L_442b78:
          mov EAX,DWORD PTR [ESP+32]
          mov EDI,DWORD PTR [EBP]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov ECX,DWORD PTR [ESP+28]
          lea EDI,DWORD PTR [EDI+EAX*1+1518500249]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          xor ECX,EDX
          and ECX,ESI
          xor ECX,EDX
          add EDI,ECX
          add EDI,EBX
          call FUN_449200
          mov ESI,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP],EDI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],30
          mov ECX,EDX
          xor ECX,EBX
          and ECX,DWORD PTR [ESP+32]
          xor ECX,EDX
          mov EDX,DWORD PTR [ESP+36]
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          add EAX,ESI
          lea ESI,DWORD PTR [ECX+EAX*1]
          mov EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP+36],ESI
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [EBP+8]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          xor ECX,EBX
          and ECX,EDI
          xor ECX,EBX
          add ESI,EAX
          add ESI,ECX
          call FUN_449200
          mov EDI,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [EBX+EAX*1+1518500249]
          mov DWORD PTR [ESP+4],30
          add EDI,EAX
          mov EAX,DWORD PTR [ESP+36]
          xor ECX,EDX
          and ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          xor ECX,EDX
          add EDI,ECX
          call FUN_449200
          mov EBX,EAX
          mov EAX,DWORD PTR [EBP+16]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          mov ECX,EDX
          xor ECX,EBX
          and ECX,ESI
          xor ECX,EDX
          mov EDX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          add EAX,DWORD PTR [ESP+36]
          add EAX,ECX
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [EBP+20]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          xor ECX,EBX
          and ECX,EDI
          xor ECX,EBX
          add ESI,EAX
          add ESI,ECX
          call FUN_449200
          mov EDI,DWORD PTR [EBP+24]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [EBX+EAX*1+1518500249]
          mov DWORD PTR [ESP+4],30
          add EDI,EAX
          mov EAX,DWORD PTR [ESP+36]
          xor ECX,EDX
          and ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          xor ECX,EDX
          add EDI,ECX
          call FUN_449200
          mov EBX,EAX
          mov EAX,DWORD PTR [EBP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          mov ECX,EDX
          xor ECX,EBX
          and ECX,ESI
          xor ECX,EDX
          mov EDX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          add EAX,DWORD PTR [ESP+36]
          add EAX,ECX
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [EBP+32]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          xor ECX,EBX
          and ECX,EDI
          xor ECX,EBX
          add ESI,EAX
          add ESI,ECX
          call FUN_449200
          mov EDI,DWORD PTR [EBP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [EBX+EAX*1+1518500249]
          mov DWORD PTR [ESP+4],30
          xor ECX,EDX
          and ECX,DWORD PTR [ESP+36]
          add EDI,EAX
          mov EAX,DWORD PTR [ESP+36]
          xor ECX,EDX
          mov DWORD PTR [ESP],EAX
          add EDI,ECX
          call FUN_449200
          mov EBX,EAX
          mov EAX,DWORD PTR [EBP+40]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          mov ECX,EDX
          xor ECX,EBX
          and ECX,ESI
          xor ECX,EDX
          mov EDX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          add EAX,DWORD PTR [ESP+36]
          add EAX,ECX
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [EBP+44]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          xor ECX,EBX
          and ECX,EDI
          xor ECX,EBX
          add ESI,EAX
          add ESI,ECX
          call FUN_449200
          mov EDI,DWORD PTR [EBP+48]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+28]
          lea EAX,DWORD PTR [EBX+EAX*1+1518500249]
          mov DWORD PTR [ESP+4],30
          add EDI,EAX
          mov EAX,DWORD PTR [ESP+36]
          xor ECX,EDX
          and ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          xor ECX,EDX
          add EDI,ECX
          call FUN_449200
          mov EBX,EAX
          mov EAX,DWORD PTR [EBP+52]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          mov ECX,EDX
          xor ECX,EBX
          and ECX,ESI
          xor ECX,EDX
          mov EDX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          add EAX,DWORD PTR [ESP+36]
          add EAX,ECX
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [ESP+36]
          mov ESI,DWORD PTR [EBP+56]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          xor ECX,EBX
          lea EAX,DWORD PTR [EDX+EAX*1+1518500249]
          and ECX,EDI
          xor ECX,EBX
          add ESI,EAX
          add ESI,ECX
          mov DWORD PTR [ESP+40],ESI
          call FUN_449200
          mov EDX,DWORD PTR [ESP+40]
          mov ESI,DWORD PTR [EBP+60]
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EDX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EBX+EAX*1+1518500249]
          mov DWORD PTR [ESP+4],30
          add ESI,EAX
          mov EAX,DWORD PTR [ESP+36]
          mov ECX,EDX
          xor ECX,EDI
          and ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          xor ECX,EDX
          add ESI,ECX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+52]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [EDX+EBX*1+1518500249]
          mov DWORD PTR [ESP],ECX
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          and EBX,ECX
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+56]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+4],EAX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+36]
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDI+ECX*1+1518500249]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+32]
          xor EDI,EDX
          and EDI,ESI
          xor EDI,EDX
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+60]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+8],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [EDX+ESI*1+1518500249]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+36]
          xor ESI,ECX
          and ESI,EBX
          xor ESI,ECX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+12],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+32]
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [ECX+EBX*1+1518500249]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+28]
          xor EBX,EDX
          and EBX,EDI
          xor EBX,EDX
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+16],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+8]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+20],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [ECX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+24],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [EDX+EBX*1+1859775393]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+16]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+28],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [ECX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+20]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+32],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [EDX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+24]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+36],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [ECX+EBX*1+1859775393]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+28]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+40],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+32]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+44],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [ECX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+36]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+48],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [EDX+EBX*1+1859775393]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+40]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+52],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [ECX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+44]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+56],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [EDX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+48]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+60],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [ECX+EBX*1+1859775393]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+52]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+56]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+4],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [ECX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+60]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+8],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [EDX+EBX*1+1859775393]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+12],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [ECX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+16],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [EDX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+8]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+20],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [ECX+EBX*1+1859775393]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+24],EAX
          mov DWORD PTR [ESP],EBX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDX+EDI*1+1859775393]
          add EAX,EDI
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+16]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+28],EAX
          mov DWORD PTR [ESP],EDI
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ESI,DWORD PTR [ECX+ESI*1+1859775393]
          add EAX,ESI
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov EBX,EAX
          mov EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+20]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+32],EAX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EDX,DWORD PTR [EDX+ECX*1-1894007588]
          mov ECX,EDI
          and ECX,EBX
          add EAX,EDX
          mov EDX,EDI
          or EDX,EBX
          and EDX,DWORD PTR [ESP+36]
          or EDX,ECX
          add EDX,EAX
          mov DWORD PTR [ESP+32],EDX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+24]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [EBP+36],EAX
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+40],EDX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [ECX+EDI*1-1894007588]
          mov EDI,DWORD PTR [ESP+28]
          add EAX,ECX
          mov ECX,EDI
          and EDI,ESI
          or ECX,ESI
          and ECX,EBX
          or ECX,EDI
          lea EDI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+28]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov ESI,EAX
          mov DWORD PTR [EBP+40],EAX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          lea ECX,DWORD PTR [EBX+ESI*1-1894007588]
          mov ESI,DWORD PTR [ESP+32]
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+4],30
          add EAX,ECX
          mov ECX,ESI
          mov EBX,ESI
          mov DWORD PTR [ESP],EDX
          or ECX,EDX
          and ECX,DWORD PTR [ESP+28]
          and EBX,EDX
          or ECX,EBX
          lea EBX,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+32]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+44],EAX
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+ESI*1-1894007588]
          mov ESI,DWORD PTR [ESP+36]
          add EAX,ECX
          mov ECX,ESI
          and ESI,EDI
          or ECX,EDI
          and ECX,DWORD PTR [ESP+32]
          or ECX,ESI
          lea ESI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+36]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+48],EAX
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EDI*1-1894007588]
          mov EDI,DWORD PTR [ESP+28]
          add EAX,ECX
          mov ECX,EDI
          and EDI,EBX
          or ECX,EBX
          and ECX,DWORD PTR [ESP+36]
          or ECX,EDI
          lea EDI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+40]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+52],EAX
          mov DWORD PTR [ESP],EDI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EBX*1-1894007588]
          mov EBX,DWORD PTR [ESP+32]
          add EAX,ECX
          mov ECX,EBX
          and EBX,ESI
          or ECX,ESI
          and ECX,DWORD PTR [ESP+28]
          or ECX,EBX
          lea EBX,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+44]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+56],EAX
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+ESI*1-1894007588]
          mov ESI,DWORD PTR [ESP+36]
          add EAX,ECX
          mov ECX,ESI
          and ESI,EDI
          or ECX,EDI
          and ECX,DWORD PTR [ESP+32]
          or ECX,ESI
          lea ESI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+48]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+60],EAX
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EDI*1-1894007588]
          mov EDI,DWORD PTR [ESP+28]
          add EAX,ECX
          mov ECX,EDI
          and EDI,EBX
          or ECX,EBX
          and ECX,DWORD PTR [ESP+36]
          or ECX,EDI
          lea EDI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+52]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP],EAX
          mov DWORD PTR [ESP],EDI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EBX*1-1894007588]
          mov EBX,DWORD PTR [ESP+32]
          add EAX,ECX
          mov ECX,EBX
          and EBX,ESI
          or ECX,ESI
          and ECX,DWORD PTR [ESP+28]
          or ECX,EBX
          lea EBX,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+56]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+4],EAX
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+ESI*1-1894007588]
          mov ESI,DWORD PTR [ESP+36]
          add EAX,ECX
          mov ECX,ESI
          and ESI,EDI
          or ECX,EDI
          and ECX,DWORD PTR [ESP+32]
          or ECX,ESI
          lea ESI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+60]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+8],EAX
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EDI*1-1894007588]
          mov EDI,DWORD PTR [ESP+28]
          add EAX,ECX
          mov ECX,EDI
          and EDI,EBX
          or ECX,EBX
          and ECX,DWORD PTR [ESP+36]
          or ECX,EDI
          lea EDI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+12],EAX
          mov DWORD PTR [ESP],EDI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EBX*1-1894007588]
          mov EBX,DWORD PTR [ESP+32]
          add EAX,ECX
          mov ECX,EBX
          and EBX,ESI
          or ECX,ESI
          and ECX,DWORD PTR [ESP+28]
          or ECX,EBX
          lea EBX,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+16],EAX
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+ESI*1-1894007588]
          mov ESI,DWORD PTR [ESP+36]
          add EAX,ECX
          mov ECX,ESI
          and ESI,EDI
          or ECX,EDI
          and ECX,DWORD PTR [ESP+32]
          or ECX,ESI
          lea ESI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+8]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+20],EAX
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea ECX,DWORD PTR [EDX+EDI*1-1894007588]
          mov EDI,DWORD PTR [ESP+28]
          add EAX,ECX
          mov ECX,EDI
          and EDI,EBX
          or ECX,EBX
          and ECX,DWORD PTR [ESP+36]
          or ECX,EDI
          lea EDI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+24],EAX
          mov DWORD PTR [ESP],EDI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [EDX+EBX*1-1894007588]
          mov EDX,DWORD PTR [ESP+32]
          add EAX,EBX
          mov EBX,EDX
          and EDX,ESI
          or EBX,ESI
          and EBX,DWORD PTR [ESP+28]
          or EBX,EDX
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+16]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+28],EAX
          mov DWORD PTR [ESP],EBX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EDX,DWORD PTR [ECX+ESI*1-1894007588]
          mov ECX,DWORD PTR [ESP+36]
          add EAX,EDX
          mov EDX,DWORD PTR [ESP+32]
          mov ESI,ECX
          and ECX,EDI
          or ESI,EDI
          and EDX,ESI
          or EDX,ECX
          add EDX,EAX
          mov DWORD PTR [ESP+40],EDX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+20]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+40]
          mov DWORD PTR [EBP+32],EAX
          mov ESI,EAX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EDX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDX+ESI*1-1894007588]
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+36]
          add EAX,EDI
          mov EDI,EDX
          mov ECX,EDX
          or EDI,EBX
          and ECX,EBX
          and EDI,ESI
          or EDI,ECX
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+24]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EBX,EAX
          mov DWORD PTR [EBP+36],EAX
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          lea ESI,DWORD PTR [ESI+EBX*1-1894007588]
          call FUN_449200
          mov EBX,DWORD PTR [ESP+32]
          mov EDX,DWORD PTR [ESP+40]
          add EAX,ESI
          mov DWORD PTR [ESP+4],30
          mov ESI,EBX
          and EBX,EDX
          mov DWORD PTR [ESP],EDX
          or ESI,EDX
          and ESI,DWORD PTR [ESP+28]
          or ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+28]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+40],EAX
          mov DWORD PTR [ESP],ESI
          mov EBX,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EBX,DWORD PTR [ECX+EBX*1-1894007588]
          mov ECX,DWORD PTR [ESP+36]
          add EAX,EBX
          mov EBX,DWORD PTR [ESP+32]
          mov EDX,ECX
          and ECX,EDI
          or EDX,EDI
          and EBX,EDX
          or EBX,ECX
          add EAX,EBX
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EBX,EAX
          mov EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+32]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+44],EAX
          mov EDI,EAX
          mov EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov ECX,ESI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EDI,DWORD PTR [EDX+EDI*1-1894007588]
          add EAX,EDI
          mov EDI,ESI
          or EDI,EBX
          and EDI,DWORD PTR [ESP+36]
          and ECX,EBX
          or EDI,ECX
          add EDI,EAX
          call FUN_449200
          mov ESI,EAX
          mov EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+36]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+48],EAX
          add EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EAX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+32]
          mov EDX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP+36],ESI
          xor ESI,EBX
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [ECX+EAX*1-899497514]
          xor ESI,EDX
          mov DWORD PTR [ESP],EDX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+40]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          lea EDX,DWORD PTR [EBX+EAX*1]
          mov DWORD PTR [EBP+52],EAX
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EDX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+44]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+56],EAX
          add EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+48]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+60],EAX
          add EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+52]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP],EAX
          add EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+56]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+4],EAX
          add EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+60]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+8],EAX
          add EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+12],EAX
          add EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+4]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+16],EAX
          add EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+8]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+20],EAX
          add EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+12]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+24],EAX
          add EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+16]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+28],EAX
          add EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+32]
          xor EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+20]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+32],EAX
          add EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+36]
          xor EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+24]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+36],EAX
          add EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+40]
          xor EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+8]
          xor EAX,DWORD PTR [EBP+28]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+40],EAX
          add EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+36]
          mov EDI,DWORD PTR [ESP+28]
          xor EDI,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EDI,ESI
          add EDI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+36],EAX
          mov EAX,DWORD PTR [EBP+44]
          xor EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+12]
          xor EAX,DWORD PTR [EBP+32]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+44],EAX
          add EAX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+28],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+28]
          mov ESI,DWORD PTR [ESP+32]
          xor ESI,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+28],EAX
          mov EAX,DWORD PTR [EBP+48]
          xor EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP+16]
          xor EAX,DWORD PTR [EBP+36]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+48],EAX
          add EAX,DWORD PTR [ESP+32]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],5
          mov DWORD PTR [ESP+32],EAX
          call FUN_449200
          mov EDX,DWORD PTR [ESP+32]
          mov EBX,DWORD PTR [ESP+36]
          xor EBX,DWORD PTR [ESP+28]
          mov DWORD PTR [ESP],EDI
          mov DWORD PTR [ESP+4],30
          lea EAX,DWORD PTR [EDX+EAX*1-899497514]
          xor EBX,EDI
          add EBX,EAX
          call FUN_449200
          mov DWORD PTR [ESP+32],EAX
          mov EAX,DWORD PTR [EBP+52]
          xor EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+20]
          xor EAX,DWORD PTR [EBP+40]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+36]
          mov DWORD PTR [EBP+52],EAX
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],5
          lea EDI,DWORD PTR [ECX+EAX*1]
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          xor ECX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EDI+EAX*1-899497514]
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+4],30
          xor ECX,ESI
          add EAX,ECX
          mov DWORD PTR [ESP+36],EAX
          call FUN_449200
          mov ESI,EAX
          mov EAX,DWORD PTR [EBP+56]
          xor EAX,DWORD PTR [EBP]
          xor EAX,DWORD PTR [EBP+24]
          xor EAX,DWORD PTR [EBP+44]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+28]
          mov DWORD PTR [EBP+56],EAX
          mov DWORD PTR [ESP+4],5
          lea EDI,DWORD PTR [ECX+EAX*1]
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+32]
          lea EAX,DWORD PTR [EDI+EAX*1-899497514]
          mov DWORD PTR [ESP+40],ESI
          mov DWORD PTR [ESP],EBX
          mov DWORD PTR [ESP+4],30
          xor ECX,ESI
          mov ESI,ECX
          xor ESI,EBX
          add ESI,EAX
          call FUN_449200
          mov DWORD PTR [ESP+44],EAX
          mov EAX,DWORD PTR [EBP+60]
          xor EAX,DWORD PTR [EBP+4]
          xor EAX,DWORD PTR [EBP+28]
          xor EAX,DWORD PTR [EBP+48]
          mov DWORD PTR [ESP+4],1
          mov DWORD PTR [ESP],EAX
          call FUN_449200
          mov DWORD PTR [EBP+60],EAX
          mov DWORD PTR [ESP],ESI
          mov EDI,EAX
          mov DWORD PTR [ESP+4],5
          call FUN_449200
          mov EBX,DWORD PTR [ESP+40]
          mov DWORD PTR [ESP+28],EAX
          xor EBX,DWORD PTR [ESP+44]
          mov EAX,DWORD PTR [ESP+36]
          mov DWORD PTR [ESP+4],30
          mov DWORD PTR [ESP],EAX
          xor EBX,EAX
          call FUN_449200
          mov ECX,DWORD PTR [ESP+80]
          mov EDX,DWORD PTR [ESP+32]
          sub DWORD PTR [ESP+88],64
          mov ECX,DWORD PTR [ECX]
          lea ECX,DWORD PTR [EDX+ECX*1-899497514]
          lea EDX,DWORD PTR [ECX+EDI*1]
          mov ECX,DWORD PTR [ESP+80]
          mov EDI,DWORD PTR [ESP+28]
          add EAX,DWORD PTR [ECX+8]
          add EDI,EDX
          add ESI,DWORD PTR [ECX+4]
          add EDI,EBX
          mov EDX,DWORD PTR [ESP+44]
          mov EBX,DWORD PTR [ESP+40]
          add EDX,DWORD PTR [ECX+12]
          add EBX,DWORD PTR [ECX+16]
          mov DWORD PTR [ESP+32],EDI
          mov DWORD PTR [ECX],EDI
          mov DWORD PTR [ESP+28],EAX
          mov DWORD PTR [ECX+8],EAX
          mov EAX,DWORD PTR [ESP+88]
          mov DWORD PTR [ECX+4],ESI
          mov DWORD PTR [ECX+12],EDX
          mov DWORD PTR [ECX+16],EBX
          test EAX,EAX
          jg L_442b75
          add ESP,60
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
FUN_4448d0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov EAX,DWORD PTR [ESP+72]
          mov ESI,DWORD PTR [ESP+64]
          mov EDI,DWORD PTR [ESP+68]
          test EAX,EAX
          je L_444b05
          mov EAX,DWORD PTR [ESP+72]
          shl EAX,3
          add EAX,DWORD PTR [ESI+20]
          jb L_444d8c
          mov EBX,DWORD PTR [ESI+24]
L_4448fe:
          mov ECX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESI+20],EAX
          lea EBP,DWORD PTR [ESI+28]
          shr ECX,29
          add ECX,EBX
          mov DWORD PTR [ESI+24],ECX
          mov ECX,DWORD PTR [ESI+92]
          test ECX,ECX
          jne L_444b10
L_44491b:
          cmp DWORD PTR [ESP+72],63
          jbe L_4449f6
          mov EAX,DWORD PTR [ESP+72]
          mov EBX,EDI
          mov DWORD PTR [ESP+68],EDI
          sub EAX,64
          mov DWORD PTR [ESP+20],EAX
          and EAX,4294967232
          lea EAX,DWORD PTR [EDI+EAX*1+64]
          mov EDI,ESI
          mov ESI,EAX
L_444942:
          mov EDX,DWORD PTR [EBX]
          add EBX,64
          bswap EDX
          mov DWORD PTR [EDI+28],EDX
          mov EDX,DWORD PTR [EBX-60]
          bswap EDX
          mov DWORD PTR [EDI+32],EDX
          mov EDX,DWORD PTR [EBX-56]
          bswap EDX
          mov DWORD PTR [EDI+36],EDX
          mov EDX,DWORD PTR [EBX-52]
          bswap EDX
          mov DWORD PTR [EDI+40],EDX
          mov EDX,DWORD PTR [EBX-48]
          bswap EDX
          mov DWORD PTR [EDI+44],EDX
          mov EDX,DWORD PTR [EBX-44]
          bswap EDX
          mov DWORD PTR [EDI+48],EDX
          mov EDX,DWORD PTR [EBX-40]
          bswap EDX
          mov DWORD PTR [EDI+52],EDX
          mov EDX,DWORD PTR [EBX-36]
          bswap EDX
          mov DWORD PTR [EDI+56],EDX
          mov EDX,DWORD PTR [EBX-32]
          bswap EDX
          mov DWORD PTR [EDI+60],EDX
          mov EDX,DWORD PTR [EBX-28]
          bswap EDX
          mov DWORD PTR [EDI+64],EDX
          mov EDX,DWORD PTR [EBX-24]
          bswap EDX
          mov DWORD PTR [EDI+68],EDX
          mov EDX,DWORD PTR [EBX-20]
          bswap EDX
          mov DWORD PTR [EDI+72],EDX
          mov EDX,DWORD PTR [EBX-16]
          bswap EDX
          mov DWORD PTR [EDI+76],EDX
          mov EDX,DWORD PTR [EBX-12]
          bswap EDX
          mov DWORD PTR [EDI+80],EDX
          mov EDX,DWORD PTR [EBX-8]
          bswap EDX
          mov DWORD PTR [EDI+84],EDX
          mov EDX,DWORD PTR [EBX-4]
          bswap EDX
          mov DWORD PTR [EDI+88],EDX
          mov DWORD PTR [ESP+8],64
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],EDI
          call FUN_442b40
          cmp ESI,EBX
          jne L_444942
          mov EAX,DWORD PTR [ESP+20]
          mov ESI,EDI
          mov EDI,DWORD PTR [ESP+68]
          and DWORD PTR [ESP+72],63
          and EAX,4294967232
          lea EDI,DWORD PTR [EDI+EAX*1+64]
L_4449f6:
          mov EAX,DWORD PTR [ESP+72]
          mov EDX,DWORD PTR [ESP+72]
          mov DWORD PTR [ESI+92],EAX
          sar EAX,2
          and EDX,3
          test EAX,EAX
          je L_444d5d
          mov EBX,DWORD PTR [EDI]
          cmp EAX,1
          bswap EBX
          mov DWORD PTR [EBP],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+4]
          cmp EAX,2
          bswap EBX
          mov DWORD PTR [EBP+4],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+8]
          cmp EAX,3
          bswap EBX
          mov DWORD PTR [EBP+8],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+12]
          cmp EAX,4
          bswap EBX
          mov DWORD PTR [EBP+12],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+16]
          cmp EAX,5
          bswap EBX
          mov DWORD PTR [EBP+16],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+20]
          cmp EAX,6
          bswap EBX
          mov DWORD PTR [EBP+20],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+24]
          cmp EAX,7
          bswap EBX
          mov DWORD PTR [EBP+24],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+28]
          cmp EAX,8
          bswap EBX
          mov DWORD PTR [EBP+28],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+32]
          cmp EAX,9
          bswap EBX
          mov DWORD PTR [EBP+32],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+36]
          cmp EAX,10
          bswap EBX
          mov DWORD PTR [EBP+36],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+40]
          cmp EAX,11
          bswap EBX
          mov DWORD PTR [EBP+40],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+44]
          cmp EAX,12
          bswap EBX
          mov DWORD PTR [EBP+44],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+48]
          cmp EAX,13
          bswap EBX
          mov DWORD PTR [EBP+48],EBX
          je L_444adc
          mov EBX,DWORD PTR [EDI+52]
          cmp EAX,15
          bswap EBX
          mov DWORD PTR [EBP+52],EBX
          jne L_444adc
          mov EBX,DWORD PTR [EDI+56]
          bswap EBX
          mov DWORD PTR [EBP+56],EBX
L_444adc:
          shl EAX,2
          add EDI,EAX
L_444ae1:
          cmp EDX,2
          lea EBX,DWORD PTR [EDI+EDX*1]
          je L_444c25
          cmp EDX,3
          je L_444c35
          cmp EDX,1
          je L_444c15
          xor EDX,EDX
L_444b01:
          mov DWORD PTR [EBP+EAX*1],EDX
L_444b05:
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_444b10:
          mov EAX,ECX
          sar EAX,2
          mov EBX,EAX
          mov DWORD PTR [ESP+20],EAX
          mov EAX,ECX
          add ECX,DWORD PTR [ESP+72]
          and EAX,3
          cmp ECX,63
          mov DWORD PTR [ESP+24],ECX
          jbe L_444be0
          lea ECX,DWORD PTR [EBP+EBX*4]
          cmp EAX,2
          mov EBX,DWORD PTR [ECX]
          je L_444d64
          cmp EAX,3
          je L_444b69
          cmp EAX,1
          je L_444b53
          movzx EBX,BYTE PTR [EDI]
          add EDI,1
          shl EBX,24
L_444b53:
          movzx EDX,BYTE PTR [EDI]
          lea EAX,DWORD PTR [EDI+1]
          shl EDX,16
          or EBX,EDX
L_444b5e:
          lea EDI,DWORD PTR [EAX+1]
          movzx EAX,BYTE PTR [EAX]
          shl EAX,8
          or EBX,EAX
L_444b69:
          lea EAX,DWORD PTR [EDI+1]
          mov DWORD PTR [ESP+28],EAX
          movzx EAX,BYTE PTR [EDI]
          or EAX,EBX
          mov EBX,DWORD PTR [ESP+20]
          mov DWORD PTR [ECX],EAX
          cmp EBX,14
          jg L_444d76
          mov EAX,15
          sub EAX,EBX
          mov EDX,EAX
          xor EAX,EAX
          nop
L_444b90:
          mov EBX,DWORD PTR [EDI+EAX*4+1]
          bswap EBX
          mov DWORD PTR [ECX+EAX*4+4],EBX
          add EAX,1
          cmp EAX,EDX
          jne L_444b90
          mov EAX,DWORD PTR [ESP+20]
          mov ECX,DWORD PTR [ESP+28]
          shl EAX,2
          neg EAX
          lea EDI,DWORD PTR [ECX+EAX*1+60]
L_444bb2:
          mov EAX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+8],64
          mov DWORD PTR [ESP+4],EBP
          mov DWORD PTR [ESP],ESI
          sub EAX,64
          mov DWORD PTR [ESP+72],EAX
          call FUN_442b40
          mov DWORD PTR [ESI+92],0
          jmp L_44491b
          .byte 0x8d
          .byte 0x76
          .byte 0x0
L_444be0:
          mov DWORD PTR [ESI+92],ECX
          mov ECX,DWORD PTR [ESP+72]
          add ECX,EAX
          cmp ECX,3
          ja L_444c41
          lea EBX,DWORD PTR [EBP+EBX*4]
          cmp EAX,1
          mov ECX,DWORD PTR [EBX]
          je L_444d6b
          cmp EAX,2
          je L_444d4e
          test EAX,EAX
          je L_444d24
L_444c0e:
          mov DWORD PTR [EBX],ECX
          jmp L_444b05
L_444c15:
          xor ESI,ESI
L_444c17:
          movzx EDX,BYTE PTR [EBX-1]
          shl EDX,24
          or EDX,ESI
          jmp L_444b01
L_444c25:
          xor ESI,ESI
L_444c27:
          movzx EDX,BYTE PTR [EBX-1]
          sub EBX,1
          shl EDX,16
          or ESI,EDX
          jmp L_444c17
L_444c35:
          movzx ESI,BYTE PTR [EBX-1]
          lea EBX,DWORD PTR [EDI+2]
          shl ESI,8
          jmp L_444c27
L_444c41:
          mov ESI,DWORD PTR [ESP+24]
          mov ECX,ESI
          and ESI,3
          mov DWORD PTR [ESP+24],ESI
          mov ESI,DWORD PTR [ESP+20]
          sar ECX,2
          cmp EAX,2
          lea ESI,DWORD PTR [EBP+ESI*4]
          mov DWORD PTR [ESP+28],ESI
          mov ESI,DWORD PTR [ESI]
          je L_444d6f
          cmp EAX,3
          je L_444c93
          cmp EAX,1
          je L_444c7d
          movzx EAX,BYTE PTR [EDI]
          add EDI,1
          shl EAX,24
          mov ESI,EAX
L_444c7d:
          movzx EBX,BYTE PTR [EDI]
          lea EAX,DWORD PTR [EDI+1]
          shl EBX,16
          or ESI,EBX
L_444c88:
          lea EDI,DWORD PTR [EAX+1]
          movzx EAX,BYTE PTR [EAX]
          shl EAX,8
          or ESI,EAX
L_444c93:
          movzx EDX,BYTE PTR [EDI]
          mov EAX,DWORD PTR [ESP+20]
          lea EBX,DWORD PTR [EDI+1]
          add EAX,1
          or ESI,EDX
          mov EDX,DWORD PTR [ESP+28]
          cmp ECX,EAX
          mov DWORD PTR [EDX],ESI
          jle L_444cdb
          mov ESI,DWORD PTR [ESP+20]
          shl ESI,2
          sub EDI,ESI
          mov EDX,EDI
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
L_444cc0:
          mov ESI,DWORD PTR [EDX+EAX*4-3]
          bswap ESI
          mov DWORD PTR [EBP+EAX*4],ESI
          add EAX,1
          cmp ECX,EAX
          jne L_444cc0
          mov EDX,EAX
          sub EDX,DWORD PTR [ESP+20]
          lea EBX,DWORD PTR [EBX+EDX*4-4]
L_444cdb:
          mov ECX,DWORD PTR [ESP+24]
          test ECX,ECX
          je L_444b05
          cmp ECX,2
          lea ESI,DWORD PTR [EBX+ECX*1]
          je L_444d83
          cmp ECX,3
          jne L_444d7f
          movzx ECX,BYTE PTR [ESI-1]
          add EBX,2
          shl ECX,8
L_444d06:
          movzx EDX,BYTE PTR [EBX-1]
          lea ESI,DWORD PTR [EBX-1]
          shl EDX,16
          or ECX,EDX
L_444d12:
          movzx EDX,BYTE PTR [ESI-1]
          shl EDX,24
          or EDX,ECX
          mov DWORD PTR [EBP+EAX*4],EDX
          jmp L_444b05
L_444d24:
          movzx ECX,BYTE PTR [EDI]
          lea EAX,DWORD PTR [EDI+1]
          shl ECX,24
          sub DWORD PTR [ESP+72],1
          je L_444c0e
L_444d38:
          lea EDI,DWORD PTR [EAX+1]
          movzx EAX,BYTE PTR [EAX]
          shl EAX,16
          or ECX,EAX
          cmp DWORD PTR [ESP+72],1
          je L_444c0e
L_444d4e:
          movzx EAX,BYTE PTR [EDI]
          shl EAX,8
          or ECX,EAX
          mov DWORD PTR [EBX],ECX
          jmp L_444b05
L_444d5d:
          xor EAX,EAX
          jmp L_444ae1
L_444d64:
          mov EAX,EDI
          jmp L_444b5e
L_444d6b:
          mov EAX,EDI
          jmp L_444d38
L_444d6f:
          mov EAX,EDI
          jmp L_444c88
L_444d76:
          mov EDI,DWORD PTR [ESP+28]
          jmp L_444bb2
L_444d7f:
          xor ECX,ECX
          jmp L_444d12
L_444d83:
          mov EBX,ESI
          xor ECX,ECX
          jmp L_444d06
L_444d8c:
          mov ECX,DWORD PTR [ESI+24]
          lea EBX,DWORD PTR [ECX+1]
          jmp L_4448fe
L_444d97:
          mov ESI,ESI
          .byte 0x8d,0xbc,0x27,0x00,0x00,0x00,0x00   # lea EDI,DWORD PTR [EDI]
FUN_444da0:
          push EBP
          push EDI
          push ESI
          push EBX
          sub ESP,44
          mov ESI,DWORD PTR [ESP+68]
          mov EBX,DWORD PTR [ESP+64]
          mov EDX,DWORD PTR [ESI+92]
          lea EDI,DWORD PTR [ESI+28]
          mov EAX,EDX
          mov ECX,EDX
          sar EAX,2
          and ECX,3
          mov DWORD PTR [ESP+16],EAX
          shl EAX,2
          mov DWORD PTR [ESP+24],EAX
          add EAX,EDI
          cmp ECX,2
          mov DWORD PTR [ESP+20],EAX
          mov EAX,DWORD PTR [EAX]
          je L_444f94
          cmp ECX,3
          mov EBP,OFFSET L_44b6a0
          je L_444e24
          cmp ECX,1
          je L_444f83
          movzx EAX,BYTE PTR [L_44b6a0]
          movzx EBP,BYTE PTR [L_44b6a1]
          mov ECX,OFFSET L_44b6a1
          shl EAX,24
L_444e04:
          add ECX,1
          mov DWORD PTR [ESP+28],ECX
          mov ECX,EBP
          movzx EBP,CL
          shl EBP,16
          or EAX,EBP
L_444e15:
          mov ECX,DWORD PTR [ESP+28]
          lea EBP,DWORD PTR [ECX+1]
          movzx ECX,BYTE PTR [ECX]
          shl ECX,8
          or EAX,ECX
L_444e24:
          movzx ECX,BYTE PTR [EBP]
          or EAX,ECX
          mov ECX,DWORD PTR [ESP+20]
          mov DWORD PTR [ECX],EAX
          mov EAX,DWORD PTR [ESP+16]
          add EAX,1
          cmp EDX,55
          jle L_444f75
          cmp EAX,15
          jg L_444e6d
          mov EAX,DWORD PTR [ESP+16]
          mov ECX,DWORD PTR [ESP+24]
          mov DWORD PTR [ESP+4],0
          shl EAX,2
          lea EDX,DWORD PTR [ESI+ECX*1+32]
          neg EAX
          add EAX,60
          mov DWORD PTR [ESP],EDX
          mov DWORD PTR [ESP+8],EAX
          call FUN_4490f0
L_444e6d:
          mov DWORD PTR [ESP+8],64
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          call FUN_442b40
          xor EAX,EAX
L_444e83:
          lea EDX,DWORD PTR [EAX*4]
          mov ECX,4
          mov DWORD PTR [ESP+4],0
          neg EDX
          add EDX,56
          cmp EAX,13
          lea EAX,DWORD PTR [ESI+EAX*4+28]
          cmovg EDX,ECX
          mov DWORD PTR [ESP+8],EDX
          mov DWORD PTR [ESP],EAX
          call FUN_4490f0
L_444eb2:
          mov EAX,DWORD PTR [ESI+24]
          mov DWORD PTR [ESI+84],EAX
          mov EAX,DWORD PTR [ESI+20]
          mov DWORD PTR [ESI+88],EAX
          mov DWORD PTR [ESP+4],EDI
          mov DWORD PTR [ESP],ESI
          mov DWORD PTR [ESP+8],64
          call FUN_442b40
          mov EAX,DWORD PTR [ESI]
          mov EDX,EAX
          mov BYTE PTR [EBX+3],AL
          shr EDX,24
          mov BYTE PTR [EBX],DL
          mov EDX,EAX
          shr EDX,16
          mov BYTE PTR [EBX+1],DL
          mov EDX,EAX
          shr EDX,8
          mov BYTE PTR [EBX+2],DL
          mov EAX,DWORD PTR [ESI+4]
          mov EDX,EAX
          mov BYTE PTR [EBX+7],AL
          shr EDX,24
          mov BYTE PTR [EBX+4],DL
          mov EDX,EAX
          shr EDX,16
          mov BYTE PTR [EBX+5],DL
          mov EDX,EAX
          shr EDX,8
          mov BYTE PTR [EBX+6],DL
          mov EAX,DWORD PTR [ESI+8]
          mov EDX,EAX
          mov BYTE PTR [EBX+11],AL
          shr EDX,24
          mov BYTE PTR [EBX+8],DL
          mov EDX,EAX
          shr EDX,16
          mov BYTE PTR [EBX+9],DL
          mov EDX,EAX
          shr EDX,8
          mov BYTE PTR [EBX+10],DL
          mov EAX,DWORD PTR [ESI+12]
          mov EDX,EAX
          mov BYTE PTR [EBX+15],AL
          shr EDX,24
          mov BYTE PTR [EBX+12],DL
          mov EDX,EAX
          shr EDX,16
          mov BYTE PTR [EBX+13],DL
          mov EDX,EAX
          shr EDX,8
          mov BYTE PTR [EBX+14],DL
          mov EAX,DWORD PTR [ESI+16]
          mov EDX,EAX
          mov BYTE PTR [EBX+19],AL
          shr EDX,24
          mov BYTE PTR [EBX+16],DL
          mov EDX,EAX
          shr EDX,16
          mov BYTE PTR [EBX+17],DL
          mov EDX,EAX
          shr EDX,8
          mov BYTE PTR [EBX+18],DL
          mov DWORD PTR [ESI+92],0
          add ESP,44
          pop EBX
          pop ESI
          pop EDI
          pop EBP
          ret 
L_444f75:
          cmp EAX,13
          jle L_444e83
          jmp L_444eb2
L_444f83:
          movzx EBP,BYTE PTR [L_44b6a0]
          mov ECX,OFFSET L_44b6a0
          jmp L_444e04
L_444f94:
          mov DWORD PTR [ESP+28],OFFSET L_44b6a0
          jmp L_444e15
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

.data
.p2align 2
L_44b6a0:
          .byte 0x80
L_44b6a1:
          .zero 3

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
          .long FUN_442b00 - .
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x30
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_442b40 - .
          .byte 0x85
          .byte 0x1d
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
          .byte 0x3
          .byte 0x79
          .byte 0x1d
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
          .byte 0x0
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0x70
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_4448d0 - .
          .byte 0xc7
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
          .byte 0x40
          .byte 0x3
          .byte 0x31
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
          .byte 0x44
          .byte 0xb
          .byte 0x3c
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .byte 0xb0
          .byte 0x0
          .byte 0x0
          .byte 0x0
          .long FUN_444da0 - .
          .byte 0x1
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
          .byte 0x3
          .byte 0xc9
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
