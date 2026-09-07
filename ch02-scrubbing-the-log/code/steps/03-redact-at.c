// Chapter 2, Part 1: "Now hide the addresses"
//
// The naive attempt. Replaces the @ and nothing else, which leaves
// hana.k*example.com on the page. Still an email address. Still a
// breach. This is the program that motivates the whole chapter.

#include <stdio.h>

int main(void)
{
    char line[1024];

    while (fgets(line, sizeof line, stdin) != NULL)
    {
        for (int i = 0; line[i] != '\0'; i++)
        {
            if (line[i] == '@')
            {
                line[i] = '*';
            }
        }

        printf("%s", line);
    }

    return 0;
}
