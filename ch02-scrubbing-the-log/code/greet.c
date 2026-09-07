// Chapter 2, Part 3: "Arguments from the command line"
//
//     ./greet David Malan
//
// argv[0] is always the program's own name, so your arguments start
// at argv[1] and argc is always at least 1.

#include <stdio.h>

int main(int argc, char *argv[])
{
    printf("argc is %d\n", argc);

    for (int i = 0; i < argc; i++)
    {
        printf("argv[%d] is %s\n", i, argv[i]);
    }

    return 0;
}
