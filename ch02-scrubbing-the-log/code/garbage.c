// Chapter 2, Part 3: "What is in an array before you put anything there"
//
// Run it twice. The numbers change. Setting aside memory does not
// clean it, so what you read is whatever the last occupant left.
//
// This program is deliberately not in the test suite, because its
// output is different every time, which is the whole point.

#include <stdio.h>

int main(void)
{
    int scores[3];
    char word[8];

    printf("scores holds: %d %d %d\n", scores[0], scores[1], scores[2]);
    printf("word[0] is:   %d\n", word[0]);

    return 0;
}
