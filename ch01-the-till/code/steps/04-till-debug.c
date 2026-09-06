// Chapter 1, Part 1: "What you have just found"
// The broken till with one temporary line that shows what the
// program is really holding for the croissant price.

#include <stdio.h>

int main(void)
{
    double loaf = 4.25;
    double croissant = 8.00 / 3;
    printf("[debug] croissant = %.20f\n", croissant);
    double coffee = 12.99;
    double oil = 19.99;

    double total = loaf + loaf
                   + croissant + croissant + croissant
                   + coffee + oil;

    printf("SOURDOUGH & CO\n");
    printf("\n");
    printf("Sourdough loaf        $%.2f\n", loaf);
    printf("Sourdough loaf        $%.2f\n", loaf);
    printf("Croissant             $%.2f\n", croissant);
    printf("Croissant             $%.2f\n", croissant);
    printf("Croissant             $%.2f\n", croissant);
    printf("Coffee beans 250g     $%.2f\n", coffee);
    printf("Olive oil 500ml       $%.2f\n", oil);
    printf("\n");
    printf("TOTAL                 $%.2f\n", total);

    return 0;
}
