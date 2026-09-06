// Chapter 1, Part 3: the -Wfloat-equal demonstration.
//
// Build it twice and compare:
//     gcc -std=c17 -Wall -Wextra -Wpedantic              -o feq feq.c
//     gcc -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -o feq feq.c
//
// The house flags say nothing. The extra flag names the problem.

#include <stdio.h>

int main(void)
{
    double tenths = 0.1 + 0.1 + 0.1 + 0.1 + 0.1
                    + 0.1 + 0.1 + 0.1 + 0.1 + 0.1;

    if (tenths == 1.0)
    {
        printf("balanced\n");
    }
    else
    {
        printf("OFF\n");
    }

    return 0;
}
