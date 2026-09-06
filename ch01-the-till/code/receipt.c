// receipt.c
// Prints one receipt for the Sourdough & Co till.
// All money is held as a whole number of cents in a long.

#include <stdio.h>

// Sales tax in basis points. A basis point is one hundredth of a
// percent, so 825 basis points means 8.25 percent.
const long TAX_BASIS_POINTS = 825;

// Prototypes. The bodies are at the bottom of the file.
long line_total(int quantity, long unit_cents);
long tax_on(long amount_cents);
long share_of(long total_cents, int parts, int which);
void print_money(long cents);

int main(void)
{
    long subtotal = 0;

    printf("SOURDOUGH & CO\n");
    printf("--------------------------------\n");

    long loaves = line_total(2, 425);
    printf("%-22s", "2 x Sourdough loaf");
    print_money(loaves);
    printf("\n");
    subtotal += loaves;

    // The 3-for-$8.00 deal does not divide evenly into three prices,
    // so split it into parts that add up to exactly 800 cents.
    for (int i = 0; i < 3; i++)
    {
        long part = share_of(800, 3, i);
        printf("%-22s", "1 x Croissant (3/8)");
        print_money(part);
        printf("\n");
        subtotal += part;
    }

    long coffee = line_total(1, 1299);
    printf("%-22s", "1 x Coffee beans 250g");
    print_money(coffee);
    printf("\n");
    subtotal += coffee;

    long oil = line_total(1, 1999);
    printf("%-22s", "1 x Olive oil 500ml");
    print_money(oil);
    printf("\n");
    subtotal += oil;

    long tax = tax_on(subtotal);
    long total = subtotal + tax;

    printf("--------------------------------\n");

    printf("%-22s", "Subtotal");
    print_money(subtotal);
    printf("\n");

    printf("%-22s", "Tax 8.25%");
    print_money(tax);
    printf("\n");

    printf("%-22s", "TOTAL");
    print_money(total);
    printf("\n");

    return 0;
}

// The cost of `quantity` items at `unit_cents` each.
long line_total(int quantity, long unit_cents)
{
    return quantity * unit_cents;
}

// Sales tax on an amount, rounded to the nearest cent.
long tax_on(long amount_cents)
{
    return (amount_cents * TAX_BASIS_POINTS + 5000) / 10000;
}

// One share of total_cents split into `parts` shares, where `which`
// counts from 0. The first few shares get the leftover cents, one
// each, so that all the shares together add up to exactly total_cents.
long share_of(long total_cents, int parts, int which)
{
    long base = total_cents / parts;
    long remainder = total_cents % parts;

    if (which < remainder)
    {
        return base + 1;
    }

    return base;
}

// Prints an amount as dollars and cents. Does not print a newline,
// so the caller decides what comes next on the line.
void print_money(long cents)
{
    if (cents < 0)
    {
        printf("-$%6ld.%02ld", -cents / 100, -cents % 100);
    }
    else
    {
        printf("$%6ld.%02ld", cents / 100, cents % 100);
    }
}
