S F X E P T A V H R W L C D U G O Z Q B N Y I J K M
id ; , struct { } ( ) malloc printf scanf getchar putchar #include stdio.h stdlib.h return void int float char double bool scanf printf + * / % if else == >= <= != && || ++ -- += -= *= /= %= - > < for return while do break switch case default :
S->N D F D
N->#include <stdio.h> ;
N->λ
D->struct id { X X }
D->λ
F->λ
F->E struct id { X X }
X->E U T id ( P ) { W }
X->T id ( P ) { W }
X->λ
U->static
U->λ
E->public
E->private
E->protected
E->λ
P->λ
P->T R id M
M->, P
M->λ
R->[ nint ] R
R->[ ]
R->λ
T->float
T->int
T->void
T->double
T->char
T->bool
A->T V
A->λ
W->E U T V
V->id L ; W
V->H id ; W
V->H id = malloc ( sizeof ( T ) ) ; W
V->H id = { I } ; W
I->C
I->C , I
H->[ ] H
H->λ
Y->[ nint ] Y
Y->λ
W->scanf ( "%d" , &id ) ; W
W->G ( Y varcadena R ) ; W
Y->id + Y
Y->id , Y
R->+ id R
R->+ C R
R->, C R
R->, id R
W->id L ; W
W->if ( Q ) { W } W
W->if ( Q ) { W } else { W } W
W->for ( T id = C ; Q ; id ++ ) { W } W
W->for ( T id = C ; Q ; id -- ) { W } W
W->while ( Q ) { W } W
W->do { W } while ( Q ) ; W
W->switch ( id ) { B } W
B->case C : W B
B->default : W
B->λ
W->break ; W
W->λ
W->return C ; W
W->return id ; W
W->return Q ; W
W->return L ; W
W->id ++ ; W
W->id -- ; W
Q->id Q
Q->Z id Q
Q->Z C Q
Q->C Q
Q->λ
Z->==
Z->!=
Z->||
Z->&&
Z->>=
Z-><=
Z->>
Z-><
K->scanf
K->scanf
K->scanf
K->scanf
K->getchar
L->= id . K ( )
L->, id L
L->= C L
L->C L
L->id L
L->+= L
L->-= L
L->= id L
L->O id L
L->O C L
L->= C L
O->+
O->*
O->/
O->%
L->λ
C->nint
C->varcadena
C->literalcar
C->nfloat
C->true
C->false
G->printf
G->printf
G->printf
