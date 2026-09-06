// Chapter 1, Part 2: "How big is a box, and what fits in it?"
//
// The output of this program depends on the machine it runs on,
// which is the whole point of running it rather than being told.
// It is deliberately left out of the automatic tests for that reason.

#include <stdio.h>
#include <limits.h>
#include <float.h>

int main(void)
{
    printf("char   %zu byte   %d to %d\n", sizeof(char), CHAR_MIN, CHAR_MAX);
    printf("int    %zu bytes  %d to %d\n", sizeof(int), INT_MIN, INT_MAX);
    printf("long   %zu bytes  %ld to %ld\n", sizeof(long), LONG_MIN, LONG_MAX);
    printf("float  %zu bytes  about %d significant digits\n", sizeof(float), FLT_DIG);
    printf("double %zu bytes  about %d significant digits\n", sizeof(double), DBL_DIG);

    return 0;
}
