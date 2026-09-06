// Chapter 1, Part 3: "Closing the loop on Maria"
//
// Two different bugs are visible in this output at the same time.
//
//   The $4.00 is the ROUNDING POLICY bug. One cent per basket, 400
//   baskets. Nothing to do with binary fractions.
//
//   The 0.0000000001 is the FLOATING POINT PRECISION bug. 400
//   additions of a value the machine cannot hold exactly.
//
// The whole-number version has neither. Counts do not drift.

#include <stdio.h>

int main(void)
{
    long correct_cents = 0;
    double naive_dollars = 0.0;

    for (int basket = 0; basket < 400; basket++)
    {
        correct_cents += 5357;      // what the books say each basket is worth
        naive_dollars += 53.56;     // what the old till actually charged
    }

    printf("Books say:      $%ld.%02ld\n", correct_cents / 100, correct_cents % 100);
    printf("Till took:      $%.2f\n", naive_dollars);
    printf("Till took, raw: $%.10f\n", naive_dollars);
    printf("Short by:       $%.2f\n", correct_cents / 100.0 - naive_dollars);

    return 0;
}
