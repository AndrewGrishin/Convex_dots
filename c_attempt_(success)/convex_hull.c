#include <stdio.h>
#include <stdlib.h>

struct {
    double x,y;
} typedef Dot;

int direction(Dot p, Dot q, Dot r){
    double number = (q.y - p.y) * (r.x - q.x) - 
                    (q.x - p.x) * (r.y - q.y);
    if (number == 0) return 0;
    return (number > 0) ? 1 : 2; 
}

void jarvisMarch(Dot* array, int size){
    int l = 0;

    for (int i = 0; i < size; i++){
        if (array[l].x > array[i].x)
            l = i;
    }
    
    int p = l, q;

    do
    {
        printf("Dot -> %lf, %lf\n",array[p].x,array[p].y);
        q = (p + 1) % size;
        for (int i = 0; i < size; i++){
            if (direction(array[p],array[i],array[q]) == 2) 
                q = i;
        }
        p = q;
    } while (p != l);
    
    
}

Dot initialize(double x, double y){
    Dot a = {x,y};
    return a;
}

int main()
{
    Dot *array = (Dot*)malloc(sizeof(Dot) * 11);
    array[0] = initialize(1,4); 
    array[1] = initialize(6,12);
    array[2] = initialize(9,8);
    array[3] = initialize(3,5.5);
    array[4] = initialize(1,1);
    array[5] = initialize(1,7);
    array[6] = initialize(4,0);
    array[7] = initialize(11,3);
    array[8] = initialize(6,7);
    array[9] = initialize(18,4);
    array[10] = initialize(6,2);
    jarvisMarch(array,11);
    free(array);
    return 0;
}