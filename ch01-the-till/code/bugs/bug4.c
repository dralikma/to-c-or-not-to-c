#include <stdio.h>

int main(void)
{
    int year_cents = 0;

    for (int day = 0; day < 313; day++)
    {
        year_cents += 8000000;      // $80,000 a day
    }

    printf("Year takings: %d cents\n", year_cents);
    return 0;
}
