// Chapter 2, Part 1: "Reading it, one line at a time"
//
// This is the version with the bug. fgets keeps the newline that was
// already at the end of the line, and printf adds a second one, so
// every line comes out with a blank line after it.
//
//     ./01-echo < ../data/access.log | cat -A | head -4

#include <stdio.h>

int main(void)
{
    char line[1024];

    while (fgets(line, sizeof line, stdin) != NULL)
    {
        printf("%s\n", line);
    }

    return 0;
}
