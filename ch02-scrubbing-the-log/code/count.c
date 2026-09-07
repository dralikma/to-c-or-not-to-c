// Chapter 2, Part 2: "Finding your own loop"
//
//     gcc -std=c17 -S count.c -o count.s
//
// Then look for the label, the comparison, and the jump backwards.
// There is no loop instruction. A loop is a jump.

#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 3; i++)
    {
        printf("%d\n", i);
    }

    return 0;
}
