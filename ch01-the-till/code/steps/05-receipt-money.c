// Chapter 1, Part 3: "Printing a count as money"
// Division gives the dollars, remainder gives the cents.

#include <stdio.h>

int main(void)
{
    long loaves = 2 * 425;

    printf("Two loaves cost $%ld.%ld\n", loaves / 100, loaves % 100);

    return 0;
}
