// Chapter 1, Part 1: "Now build Maria's actual basket"
//
// This is the BROKEN till. It compiles with no warnings at the
// strictest settings we have, and it is wrong.
//
// Add up the seven item lines by hand. They come to 49.49.
// The program prints a total of 49.48.

#include <stdio.h>

int main(void)
{
    double loaf = 4.25;
    double croissant = 8.00 / 3;
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
