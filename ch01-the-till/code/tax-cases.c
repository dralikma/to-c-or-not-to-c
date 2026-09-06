// Chapter 1: a regression test for the tax rounding rule.
//
// WHY THIS FILE EXISTS
//
// The basket in receipt.c comes to 4948 cents. Its tax works out to
// 408 cents whether you round properly or just let the division
// truncate, because 4948 * 825 is 4082100 and the leftover 2100 is
// below half of 10000. So receipt-expected.txt cannot tell the two
// formulas apart. Delete the "+ 5000" from tax_on and not one test
// would fail.
//
// That is a hole in the test suite, so this program fills it. It runs
// the tax calculation across amounts on both sides of the rounding
// boundary, including $10.00, which sits exactly on it: 1000 * 825 is
// 825000, and the leftover is exactly 5000, which is exactly half.
// Truncating gives 82 cents. Rounding gives 83.
//
// Try it. Delete the "+ 5000" below, run `make test`, and watch this
// catch it. A test suite that cannot catch your own deliberate
// sabotage would not have caught Maria's nephew either.
//
// Uses nothing beyond Chapter 1: functions, loops, and whole numbers.

#include <stdio.h>

const long TAX_BASIS_POINTS = 825;

long tax_on(long amount_cents);
void show(long amount_cents);

int main(void)
{
    printf("%10s %10s\n", "subtotal", "tax");

    show(0);            // nothing owed on nothing
    show(100);          // rounds down
    show(1000);         // exactly on the boundary: 82 or 83?
    show(1212);         // exactly one dollar of tax
    show(4948);         // the basket in receipt.c
    show(5000);
    show(9999);
    show(100000);       // large enough to show the long is doing its job

    return 0;
}

// Sales tax on an amount, rounded to the nearest cent.
long tax_on(long amount_cents)
{
    return (amount_cents * TAX_BASIS_POINTS + 5000) / 10000;
}

// Prints one row of the table: the amount and the tax on it.
void show(long amount_cents)
{
    long t = tax_on(amount_cents);

    printf("%7ld.%02ld %7ld.%02ld\n",
           amount_cents / 100, amount_cents % 100,
           t / 100, t % 100);
}
