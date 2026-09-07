// Chapter 2, Part 3: "Getting at one character of one argument"
//
// argv is an array of strings. A string is an array of characters. So
// argv is an array of arrays, and two sets of brackets get you one
// character of one argument.
//
//     ./argvchars 13     -> key is all digits, exit 0
//     ./argvchars 1x3    -> refused,           exit 1
//
// You need exactly this in the Caesar exercise.

#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s KEY\n", argv[0]);
        return 1;
    }

    printf("argv[1] is        %s\n", argv[1]);
    printf("argv[1][0] is     %c\n", argv[1][0]);

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Key must be all digits. '%c' is not.\n", argv[1][i]);
            return 1;
        }
    }

    printf("Key is all digits.\n");
    return 0;
}
