// Chapter 1, Part 1: "Making it look like money"
// Same program, but %f becomes %.2f so it reads like a price.

#include <stdio.h>

int main(void)
{
    double loaf = 4.25;
    double coffee = 12.99;
    double oil = 19.99;

    double total = loaf + coffee + oil;

    printf("Total is $%.2f\n", total);

    return 0;
}
