// Chapter 1, Part 1: "Your first calculation"
// Three variables, one expression, one placeholder.

#include <stdio.h>

int main(void)
{
    double loaf = 4.25;
    double coffee = 12.99;
    double oil = 19.99;

    double total = loaf + coffee + oil;

    printf("Total is %f\n", total);

    return 0;
}
