# runtime/libgcc/_chkstk_ms.s -- byte match; assembly, no unwind info
#
# original placement:
#   .text          00447c00-00447c30

.intel_syntax noprefix
.globl ___chkstk_ms

.text
.p2align 4
___chkstk_ms:
          push ECX
          push EAX
          cmp EAX,4096
          lea ECX,DWORD PTR [ESP+12]
          jb L_447c22
L_447c0d:
          sub ECX,4096
          or DWORD PTR [ECX],0
          sub EAX,4096
          cmp EAX,4096
          ja L_447c0d
L_447c22:
          sub ECX,EAX
          or DWORD PTR [ECX],0
          pop EAX
          pop ECX
          ret 
          nop
          nop
          .byte 0x66   # nop
          nop
          .byte 0x66   # nop
          nop
