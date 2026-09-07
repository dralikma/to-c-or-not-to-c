// Chapter 2, Part 3: ctype, and the 32 that runs the alphabet.

#include <ctype.h>
#include <stdio.h>

int main(void)
{
    printf("'a' is %d, 'A' is %d, apart by %d\n", 'a', 'A', 'a' - 'A');
    printf("toupper('d') gives %c\n", toupper('d'));
    printf("'d' - 32 gives %c\n", 'd' - 32);
    printf("isalpha('7') = %d   isdigit('7') = %d   isspace(' ') = %d\n",
           isalpha('7') != 0, isdigit('7') != 0, isspace(' ') != 0);

    return 0;
}
