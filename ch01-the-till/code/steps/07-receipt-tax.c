// Chapter 1, Part 3: "Giving things names" and "Working out the tax"
//
// The + 5000 is half of 10000. It pushes anything with a remainder of
// half or more up into the next whole cent before the division
// truncates, which is round-half-up done exactly.

#include <stdio.h>

int main(void)
{
    // Sales tax in basis points. A basis point is one hundredth of a
    // percent, so 825 basis points means 8.25 percent.
    const long TAX_BASIS_POINTS = 825;

    long subtotal = 4948;
    long tax = (subtotal * TAX_BASIS_POINTS + 5000) / 10000;

    printf("Tax: $%ld.%02ld\n", tax / 100, tax % 100);

    return 0;
}
