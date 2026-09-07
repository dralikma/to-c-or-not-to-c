// Chapter 2, Part 3: "Finally: a function that takes text"
//
// This is the thing Chapter 1 could not do. char text[] is an array
// parameter, and it needs no length beside it, because a string
// carries its own end marker.
//
// You will also see this written char *text. Same meaning. Chapter 4
// explains the star.

#include <ctype.h>
#include <stdio.h>

void shout(char text[]);

int main(void)
{
    shout("sourdough loaf");
    shout("2 x croissant");
    return 0;
}

void shout(char text[])
{
    for (int i = 0; text[i] != '\0'; i++)
    {
        printf("%c", toupper(text[i]));
    }

    printf("\n");
}
