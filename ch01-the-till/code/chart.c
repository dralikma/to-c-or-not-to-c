// Chapter 1, Part 3: "A loop inside a loop"
//
// The newline goes AFTER the inner loop but INSIDE the outer one,
// so it happens once per row. Move it inside the inner loop and every
// hash lands on its own line. Move it after the outer loop and the
// whole chart runs together on one line.

#include <stdio.h>

int main(void)
{
    for (int hour = 9; hour < 13; hour++)
    {
        int sales = hour * 2;

        printf("%2d:00 ", hour);

        for (int bar = 0; bar < sales; bar++)
        {
            printf("#");
        }

        printf("\n");
    }

    return 0;
}
