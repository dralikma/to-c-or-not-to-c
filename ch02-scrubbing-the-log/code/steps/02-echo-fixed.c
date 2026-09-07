// Chapter 2, Part 1: the same thing with the extra newline removed.
// Output should be byte-identical to the input:
//
//     ./02-echo-fixed < ../data/access.log | diff - ../data/access.log

#include <stdio.h>

int main(void)
{
    char line[1024];

    while (fgets(line, sizeof line, stdin) != NULL)
    {
        printf("%s", line);
    }

    return 0;
}
