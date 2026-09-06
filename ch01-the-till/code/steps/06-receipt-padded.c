// Chapter 1, Part 3: "Now break it on purpose"
//
// At $4.02 each, the version above prints "$8.4" because %ld prints
// the number 4 as a single character. %02ld pads it to two digits
// with a leading zero.

#include <stdio.h>

int main(void)
{
    long loaves = 2 * 402;

    printf("Two loaves cost $%ld.%02ld\n", loaves / 100, loaves % 100);

    return 0;
}
