/* fast.c: C port of dsim.py + annealing. fast EVENTS SEED SECS [cl cr cd NODES...]
   EVENTS from expev.py. Prints kendall-0 states with the lowest costs.
   cl = cost per key step toward 0 (lowering frequency), cr = per step away (raising), cd = per dummy. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
typedef long long ll;
#define GMIN (-(1LL<<62))
typedef struct N { ll key; int data; struct N *parent,*child,*left,*right; int degree,mark; } N;
typedef struct { N *min,*root; int n; } H;
static N pool[4000]; static int np;
static N *nn(ll k,int d){N*x=&pool[np++];x->key=k;x->data=d;x->parent=x->child=0;x->left=x->right=x;x->degree=0;x->mark=0;return x;}
static int cmp(N*a,N*b){return a->key<b->key?-1:(a->key>b->key?1:0);}
static void ins_after(N*a,N*b){if(a==a->right){a->right=b;a->left=b;b->right=a;b->left=a;}else{b->right=a->right;a->right->left=b;a->right=b;b->left=a;}}
static void ins_before(N*a,N*b){if(a==a->left){a->right=b;a->left=b;b->right=a;b->left=a;}else{b->left=a->left;a->left->right=b;a->left=b;b->right=a;}}
static N*rem(N*s){N*ret=s==s->left?0:s->left;if(s->parent&&s->parent->child==s)s->parent->child=ret;s->right->left=s->left;s->left->right=s->right;s->parent=0;s->left=s->right=s;return ret;}
static void link_(N*s,N*p){if(!p->child)p->child=s;else ins_before(p->child,s);s->parent=p;p->degree++;s->mark=0;}
static void ins_root(H*h,N*x){if(!h->root){h->root=x;x->left=x->right=x;}else ins_after(h->root,x);}
static void rem_root(H*h,N*x){if(x->left==x)h->root=0;else h->root=rem(x);}
static N*hins(H*h,ll k,int d){N*x=nn(k,d);ins_root(h,x);if(!h->min||x->key<h->min->key)h->min=x;h->n++;return x;}
static void consol(H*h){N*a[66];memset(a,0,sizeof a);while(h->root){N*w=h->root,*x=w;rem_root(h,w);int d=x->degree;while(a[d]){N*y=a[d];if(cmp(x,y)>0){N*t=x;x=y;y=t;}link_(y,x);a[d]=0;d++;}a[d]=x;}h->min=0;for(int i=0;i<65;i++)if(a[i]){ins_root(h,a[i]);if(!h->min||cmp(a[i],h->min)<0)h->min=a[i];}}
static N*xmin(H*h){N*z=h->min;if(!z)return 0;N*x=z->child,*orig=0;while(x&&x!=orig){if(!orig)orig=x;N*y=x->right;x->parent=0;ins_root(h,x);x=y;}rem_root(h,z);h->n--;if(h->n==0)h->min=0;else{h->min=z->right;consol(h);}return z;}
static void cut(H*h,N*x,N*y){rem(x);y->degree--;ins_root(h,x);x->parent=0;x->mark=0;}
static void ccut(H*h,N*y){for(;;){N*z=y->parent;if(!z)return;if(!y->mark){y->mark=1;return;}cut(h,y,z);y=z;}}
static N*rkey(H*h,N*n,ll key);
static void hdel(H*h,N*n){rkey(h,n,GMIN);xmin(h);}
static N*rkey(H*h,N*n,ll key){if(key>n->key){int d=n->data;hdel(h,n);return hins(h,key,d);}ll o=n->key;n->key=key;N*y=n->parent;if(o==key&&o!=GMIN)return n;if(y&&cmp(n,y)<=0){cut(h,n,y);ccut(h,y);}if(cmp(n,h->min)<=0)h->min=n;return n;}
/* events */
typedef struct {int t,a,fl;ll k;} E; /* t: 0 round,1 get,2 visit,3 ins(fl 1=this),4 push,5 chg */
static E pre[3000];static int npre;
#define MB 300
static E g3[MB][80];static int ng3[MB];static E g4[MB][80];static int ng4[MB];
static int want[100],nwant,flex[MB],posw[MB];
static ll base[MB];static int isb[MB];
static ll ovv[MB];static char ovf[MB];
typedef struct{int b;int k;int r;}D;
static H*lh[MB];static N*ln[MB];static char vis[MB];
#define OV(b,k) (ovf[b]?ovv[b]:(k))
static int o4[200],no4;
static void step(E*l,int n,H*th,H*nx,int rn,D*du,int nd){
  for(int i=0;i<n;i++){E*e=&l[i];
    if(e->t==2){vis[e->a]=1;if(ln[e->a]){hdel(lh[e->a],ln[e->a]);ln[e->a]=0;}
      for(int j=0;j<nd;j++)if(du[j].b==e->a&&du[j].r==rn){hins(rn==4?th:nx,du[j].k,-1);}
    }else if(e->t==3){H*h=e->fl?th:nx;if(vis[e->a])continue;if(ln[e->a]){ll k=OV(e->a,e->k);if(ln[e->a]->key!=k)ln[e->a]=rkey(lh[e->a],ln[e->a],k);continue;}lh[e->a]=h;ln[e->a]=hins(h,OV(e->a,e->k),e->a);
    }else if(e->t==4){if(vis[e->a])continue;if(ln[e->a]){if(lh[e->a]!=nx){hdel(lh[e->a],ln[e->a]);ln[e->a]=0;}else continue;}lh[e->a]=nx;ln[e->a]=hins(nx,OV(e->a,e->k),e->a);
    }else if(e->t==5){if(ln[e->a])ln[e->a]=rkey(lh[e->a],ln[e->a],OV(e->a,e->k));}
  }
}
static void sim(D*du,int nd){
  np=0;memset(ln,0,sizeof ln);memset(vis,0,sizeof vis);no4=0;
  static H hs[8];memset(hs,0,sizeof hs);int hi=0;H*heap=&hs[hi++],*nw=0;
  lh[2]=heap;ln[2]=hins(heap,0,2);
  for(int i=0;i<npre;i++){E*e=&pre[i];
    if(e->t==0){if(nw)heap=nw;nw=&hs[hi++];}
    else if(e->t==1){N*z=xmin(heap);ln[z->data]=0;}
    else if(e->t==2){if(ln[e->a]){hdel(lh[e->a],ln[e->a]);ln[e->a]=0;}}
    else if(e->t==3){H*h=e->fl?heap:nw;lh[e->a]=h;ln[e->a]=hins(h,OV(e->a,e->k),e->a);}
    else if(e->t==4){lh[e->a]=nw;ln[e->a]=hins(nw,OV(e->a,e->k),e->a);}
    else if(e->t==5){ln[e->a]=rkey(lh[e->a],ln[e->a],OV(e->a,e->k));}
  }
  heap=nw;nw=&hs[hi++];
  for(int b=0;b<MB;b++)if(ln[b]&&lh[b]!=heap)ln[b]=0;
  while(heap->min){N*z=xmin(heap);int b=z->data;if(b<0)continue;ln[b]=0;if(vis[b])continue;step(g3[b],ng3[b],heap,nw,3,du,nd);}
  heap=nw;H*dm=&hs[hi++];
  for(int b=0;b<MB;b++)if(ln[b]&&lh[b]!=heap)ln[b]=0;
  while(heap->min){N*z=xmin(heap);int b=z->data;if(b<0)continue;ln[b]=0;if(vis[b])continue;o4[no4++]=b;step(g4[b],ng4[b],heap,dm,4,du,nd);}
}
static int kend(void){int o[200],m=0,n=0;for(int i=0;i<no4;i++)if(!flex[o4[i]])o[m++]=posw[o4[i]];for(int i=0;i<m;i++)for(int j=i+1;j<m;j++)if(o[i]>o[j])n++;return n;}
static double rnd(void){return rand()/(RAND_MAX+1.0);}
static int r3b[200],nr3,r4b[200],nr4;static int nodes[100],nnodes;
static double cl=.6,cr=.6,cd=.5;
#define MD 8
int main(int c,char**v){
  FILE*f=fopen(v[1],"r");char s[16];int a,fl;ll k;int cur=0;int mode=0;
  while(fscanf(f,"%15s",s)==1){
    if(!strcmp(s,"PRE")){mode=0;continue;} if(!strcmp(s,"G3")){fscanf(f,"%d",&cur);mode=3;continue;} if(!strcmp(s,"G4")){fscanf(f,"%d",&cur);mode=4;continue;}
    if(!strcmp(s,"W")){while(fscanf(f,"%d",&a)==1&&a>=0){posw[a]=nwant;want[nwant++]=a;}continue;}
    if(!strcmp(s,"F")){while(fscanf(f,"%d",&a)==1&&a>=0)flex[a]=1;continue;}
    fscanf(f,"%d %d %lld",&a,&fl,&k);E e={atoi(s),a,fl,k};
    if(e.t==3||e.t==4){if(!isb[a]){isb[a]=1;base[a]=k;}}
    if(mode==0)pre[npre++]=e;else if(mode==3){g3[cur][ng3[cur]++]=e;if(e.t==2)r3b[nr3++]=a;}else{g4[cur][ng4[cur]++]=e;if(e.t==2)r4b[nr4++]=a;}
  }
  int seed=atoi(v[2]);double secs=atof(v[3]);srand(seed);
  if(c>4)cl=atof(v[4]);if(c>5)cr=atof(v[5]);if(c>6)cd=atof(v[6]);
  for(int i=7;i<c;i++)nodes[nnodes++]=atoi(v[i]);
  { char*ex=getenv("EXCL"); if(ex){ int m=0; for(int i=0;i<nr4;i++){ char t[16]; sprintf(t,",%d,",r4b[i]); if(!strstr(ex,t)) r4b[m++]=r4b[i]; } nr4=m; } }
  D du[MD];int nd=0;
  sim(du,0);int k0=kend();
  double cur_c=k0;time_t t0=time(0);long it=0;double bestc=1e9;
  while(1){
    if((it&1023)==0&&difftime(time(0),t0)>secs)break;it++;
    double T=1.2*(1-((it%400000)/400000.0))+.03;
    int b=-1;char sf=0;ll sv=0;D sd[MD];int snd=nd;memcpy(sd,du,sizeof du);
    double r=rnd();
    if(r<.55){b=nodes[rand()%nnodes];sf=ovf[b];sv=ovv[b];ll x=ovf[b]?ovv[b]:base[b];x+=rnd()<.5?-1:1;if(x>0)x=0;if(x<-9)x=-9;if(x==base[b])ovf[b]=0;else{ovf[b]=1;ovv[b]=x;}}
    else if(r<.75&&nd<MD){D d;if(rnd()<.8){d.b=r4b[rand()%nr4];d.r=4;}else{d.b=r3b[rand()%nr3];d.r=3;}d.k=-(rand()%10);du[nd++]=d;}
    else if(r<.9&&nd){du[rand()%nd]=du[--nd];}
    else if(nd){D d;if(rnd()<.8){d.b=r4b[rand()%nr4];d.r=4;}else{d.b=r3b[rand()%nr3];d.r=3;}d.k=-(rand()%10);du[rand()%nd]=d;}
    sim(du,nd);int kk=kend();
    double cc=kk+cd*nd;for(int i=0;i<nnodes;i++){int n=nodes[i];if(ovf[n]){ll dl=ovv[n]-base[n];cc+=dl<0?-dl*cr:dl*cl;}}
    if(cc<=cur_c||rnd()<exp((cur_c-cc)/T)){cur_c=cc;
      if(kk==0&&cc<bestc){bestc=cc;printf("cost %.2f keys:",cc);for(int i=0;i<nnodes;i++){int n=nodes[i];if(ovf[n])printf(" %d=%lld(%lld)",n,ovv[n],base[n]);}printf(" dum:");for(int i=0;i<nd;i++)printf(" (%d,%d,r%d)",du[i].b,du[i].k,du[i].r);printf("\n");fflush(stdout);}
    }else{if(b>=0){ovf[b]=sf;ovv[b]=sv;}nd=snd;memcpy(du,sd,sizeof du);}
  }
  printf("iters %ld k0 %d best %.2f\n",it,k0,bestc);
  return 0;
}
