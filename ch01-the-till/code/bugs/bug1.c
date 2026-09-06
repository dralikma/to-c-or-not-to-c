#include <stdio.h>

int main(void)
{
    long takings = 4948;
    printf("Small day: %d cents\n", takings);

    takings = 9000000000L;
    printf("Big day:   %d cents\n", takings);

    return 0;
}
