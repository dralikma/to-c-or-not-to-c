// Chapter 1, Part 3: "Getting out early with break" and
// "Skipping one pass with continue".
//
// while (true) needs <stdbool.h> in C17, because true is not a
// keyword until C23 and this book pins -std=c17. Leave the header
// out and gcc says: 'true' undeclared.

#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    long lost = 0;    // cents the old till has thrown away
    int day = 0;

    while (true)
    {
        day++;
        lost += 400;             // 400 baskets, one cent each

        if (lost >= 100000)      // $1000
        {
            break;
        }
    }

    printf("The loss passes $1000 on day %d\n", day);

    // continue abandons only the current pass, not the whole loop.
    int trading_days = 0;

    for (int d = 1; d <= 14; d++)
    {
        if (d % 7 == 0)
        {
            continue;            // every seventh day the shop is shut
        }

        trading_days++;
    }

    printf("Trading days in a fortnight: %d\n", trading_days);

    return 0;
}
