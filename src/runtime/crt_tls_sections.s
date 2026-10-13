# runtime/crt_tls_sections.s -- .CRT initializer tables and .tls directory
#
# original placement:
#   .CRT           00510000-00510034
#   .tls           00511000-00511020

.intel_syntax noprefix
.globl L_510000
.globl L_510008
.globl L_51000c
.globl L_510018
.globl L_510030

.section .CRT,"dw"
.p2align 2
L_510000:
          .zero 4
          .long L_401130
L_510008:
          .zero 4
L_51000c:
          .zero 4
          .long L_401010
          .long L_446cb0
L_510018:
          .zero 8
L_510020:
          .long FUN_446e60
          .long L_446e10
          .zero 8
L_510030:
          .zero 4

.section .tls,"dw"
.p2align 2
L_511000:
          .zero 4
.globl __tls_used
__tls_used:
          .long L_511000
          .long L_51101c
          .long L_479e30
          .long L_510020
          .zero 8
L_51101c:
          .zero 4
