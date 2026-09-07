// Chapter 2, Part 3: "A string is an array of characters"
//
// One array, printed three ways. Look at the fourth number: you put
// three characters in and position 3 holds 0. That is the null
// terminator, and it is how anything knows where text ends.

#include <stdio.h>

int main(void)
{
    char word[10] = "Hi!";

    printf("as a string:  %s\n", word);
    printf("as numbers:   %d %d %d %d\n", word[0], word[1], word[2], word[3]);
    printf("as chars:     %c %c %c\n", word[0], word[1], word[2]);

    return 0;
}
