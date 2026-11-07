#include <stdlib.h>
#include <string.h>
extern int f(int);
extern int g(void);
extern void (*fp)(int);
extern int *gp(int);
extern double d;
int x, y;
/* indirect call in an arm */
void p_indir(int a) { if (a) fp(1); else x = 2; }
/* goto */
void p_goto(int a) { if (a) goto out; f(1); out: x = 1; }
/* const return (2 vs computed) */
int p_const(int a) { if (a) return 7; return f(a); }
/* null return */
int *p_null(int a) { if (a) return 0; return gp(a); }
/* negative return */
int p_neg(int a) { if (a) return -1; return f(a); }
/* noreturn from the header */
void p_exit(int a) { if (a) exit(1); f(2); }
void p_abort(int a) { if (a) abort(); f(2); }
/* cold from header? (none expected in mingw) */
/* loop guard: loop entry test whose bound is not modified */
void p_guard(int n) { int i; if (n > x) { for (i = 0; i < n; i++) f(i); } }
/* fp compare */
void p_fp(void) { if (d == 1.5) f(1); else x = 1; }
/* continue */
void p_cont(int n) { int i; for (i = 0; i < n; i++) { if (f(i)) continue; x++; } }
/* pure call (no side effects): strlen */
void p_pure(const char *s) { if (x) y = strlen(s); else y = 1; }
/* positive/negative compare */
void p_pos(int a) { if (a > 0) x = 1; else y = 1; }
void p_neg1(int a) { if (a == -1) x = 1; else y = 1; }
/* compare of two non-constants */
void p_two(int a, int b) { if (a == b) x = 1; else y = 1; }
void p_lt2(int a, int b) { if (a < b) x = 1; else y = 1; }
/* loop iv compare */
void p_ivc(void) { int i; for (i = 0; i < 100; i++) { if (i == 50) f(0); x++; } }
