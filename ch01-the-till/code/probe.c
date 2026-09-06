// Chapter 1, Part 2: the scratchpad you add to as you read.
// Everything the chapter tells you to add, assembled in order.

#include <stdio.h>

int main(void)
{
    // "Looking inside a variable"
    printf("0.1     is stored as %.20f\n", 0.1);
    printf("0.2     is stored as %.20f\n", 0.2);
    printf("0.1+0.2 is stored as %.20f\n", 0.1 + 0.2);
    printf("0.5     is stored as %.20f\n", 0.5);
    printf("0.25    is stored as %.20f\n", 0.25);

    // "The errors pile up"
    double tenths = 0.1 + 0.1 + 0.1 + 0.1 + 0.1
                    + 0.1 + 0.1 + 0.1 + 0.1 + 0.1;

    printf("ten tenths     = %.20f\n", tenths);
    printf("off by         = %.20f\n", 1.0 - tenths);

    // "float is worse than double"
    float f = 19.99f;
    printf("19.99 in a float = %.20f\n", f);

    // "Whole numbers run out too"
    int dollars = 1073741824;
    printf("one billion doubled = %d\n", dollars * 2);

    // "Whole-number division throws away the part you wanted"
    printf("7 / 2 = %d\n", 7 / 2);
    printf("1 / 3 = %d\n", 1 / 3);
    printf("7 %% 2 = %d\n", 7 % 2);
    printf("8 %% 3 = %d\n", 8 % 3);

    // "Casting"
    int a = 1;
    int b = 3;
    printf("%f\n", (double) a / b);

    return 0;
}
