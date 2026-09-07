// redact.c
// Reads a web server log on standard input, replaces every email
// address with X, and writes the result to standard output.
//
//     ./redact < access.log > clean.log

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

// Longer than any line the server writes. Chapter 4 removes this limit.
#define MAX_LINE 1024

bool is_address_char(char c);
void redact_line(char line[]);

int main(void)
{
    char line[MAX_LINE];

    while (fgets(line, sizeof line, stdin) != NULL)
    {
        redact_line(line);
        printf("%s\n", line);
    }

    return 0;
}

// True for characters that can appear inside an email address, not
// counting the @ itself. Anything else marks the edge of one.
bool is_address_char(char c)
{
    return isalnum(c) || c == '.' || c == '_' || c == '-' || c == '+';
}

// Finds every email address in the line and overwrites it with X.
// Changes the caller's array directly, because an array parameter is a
// way in rather than a copy.
void redact_line(char line[])
{
    int n = strlen(line);

    for (int i = 0; i < n; i++)
    {
        if (line[i] != '@')
        {
            continue;
        }

        // Walk left from the @ until the character before us is not
        // part of an address.
        int start = i;
        while (start > 0 && is_address_char(line[start - 1]))
        {
            start--;
        }

        // Walk right the same way. The null terminator is not an
        // address character, so this stops at the end of the line.
        int end = i;
        while (is_address_char(line[end + 1]))
        {
            end++;
        }

        for (int j = start; j <= end; j++)
        {
            line[j] = 'X';
        }

        // Carry on scanning after this address, not inside it. Line 7
        // of the sample log has two.
        i = end;
    }
}
