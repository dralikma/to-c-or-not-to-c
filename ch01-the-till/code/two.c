// Chapter 1, Part 3: "Failed fix number two: just round everything"
//
// Needs the maths library:
//     gcc -std=c17 -Wall -Wextra -Wpedantic -g -o two two.c -lm
// Leave off -lm and you get a LINKER error, not a compiler error.

#include <stdio.h>
#include <math.h>

int main(void)
{
    double price = 2.675;

    printf("printf rounds it to   %.2f\n", price);
    printf("round() rounds it to  %.2f\n", round(price * 100) / 100);

    return 0;
}
