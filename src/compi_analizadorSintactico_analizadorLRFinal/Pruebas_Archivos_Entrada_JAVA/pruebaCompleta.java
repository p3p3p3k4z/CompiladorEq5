int main()�{
//declaraciones de varios tipos de variables
int a,b@;
/*comentario 
de bloque*/
int *aptr, vec[10],categ=2;
int *aVecPtr[3];
float vecFloat[3]={2.3,5.0,3.1},sueldo;
printf("Teclea un numero:");
scanf("%d",&a);
b=a%2;
if(b==0){
	printf("%d el numero es ",a);
}
else
	;

switch(categ){
	case 1: nsueldo=sueldo*1.15;
			break;
	case 2: nsueldo=sueldo*1.10;
			break;
}
for(i=0;i<=n;i++){
	pot=1;
	for(j=0;j<i;j++){
		pot=pot*2;
	}
	suma=suma+1/pot;
}
while(i<=4){
    do{
        printf("Teclea la calificacion %d:",i);
        scanf("%f",&calif);
    }while(calif<0||calif>10);
    suma+=calif;
    i++;
}
}
float suma(float a, float b){
return a+b;
}
