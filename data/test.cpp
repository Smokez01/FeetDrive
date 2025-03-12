#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main()
{
    int Tag=15;
    int Monat= 8;
    int Jahr=2006;
    char oben[]="  /\\_/\\";
    char mitte[]=" (=^.^=)";
    char unten[]="  (\")(\")_/";

    printf(" Mateja Stojanovic\n 3CHEL\n 18\n");
    printf(" %d %d %d\n",Tag, Monat, Jahr);
    printf("%s\n",oben);
    printf("%s\n",mitte);
    printf("%s\n", unten);
    printf("%3.2f\n", sqrt(36));
    printf("%2.1f\n", pow(15,2));
    return 0;
}
