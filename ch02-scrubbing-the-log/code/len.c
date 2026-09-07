// Chapter 2, Part 3: "fgets, properly"
//
// fgets keeps the newline. strlen counts it. "David" comes back as 6,
// and the last character is 10, which is '\n' in ASCII.
//
//     printf 'David\n' | ./len

#include <stdio.h>
#include <string.h>

int main(void)
{
    char line[64];

    if (fgets(line, sizeof line, stdin) == NULL)
    {
        printf("no input\n");
        return 1;
    }

    printf("strlen says %zu\n", strlen(line));
    printf("last char is %d\n", line[strlen(line) - 1]);

    line[strcspn(line, "\n")] = '\0';
    printf("after stripping: strlen says %zu\n", strlen(line));

    return 0;
}
