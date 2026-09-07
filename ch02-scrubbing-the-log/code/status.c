// Chapter 2, Part 3: "Saying no properly"
//
//     ./status        -> Usage line, exit 1
//     ./status Ali    -> greeting,   exit 0
//
// Check the number with: echo $?

#include <stdio.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s NAME\n", argv[0]);
        return 1;
    }

    printf("Hello, %s\n", argv[1]);
    return 0;
}
