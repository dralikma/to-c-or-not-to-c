// Chapter 1, Part 3: getchar, single quotes, and "a char is a number".
//
// The chapter shows the if without an else. This version has one so
// that the program can be tested automatically.

#include <stdio.h>

int main(void)
{
    printf("%d %d %d\n", 'A', 'a', 'y');

    // The same variable printed twice. %c shows the character,
    // %d shows the number. Nothing about the byte changes.
    char grade = 'A';
    printf("%c is stored as the number %d\n", grade, grade);
    printf("Add 32 and you get %c\n", grade + 32);

    printf("Print receipt? (y/n) ");

    int answer = getchar();

    if (answer == 'y' || answer == 'Y')
    {
        printf("Printing.\n");
    }
    else
    {
        printf("Not printing.\n");
    }

    return 0;
}
