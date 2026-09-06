// Chapter 1, Part 3: "Reading a number from a person"
//
// Two things worth understanding rather than copying:
//
//   &quantity  is the ADDRESS of the variable. Every argument in C is
//              a copy, so scanf cannot be handed the variable itself.
//              It has to be told where the variable lives.
//
//   != 1       scanf returns how many values it successfully read.
//              Ask for one, get 1 back, and it worked. Checking this
//              is the habit; most tutorials throw it away and then
//              carry on with an uninitialised variable.
//
// Do NOT wrap this in a retry loop yet. See the Trap in the chapter.

#include <stdio.h>

int main(void)
{
    int quantity;

    printf("Quantity: ");

    if (scanf("%d", &quantity) != 1)
    {
        printf("That is not a number.\n");
        return 1;
    }

    printf("Selling %d.\n", quantity);
    return 0;
}
