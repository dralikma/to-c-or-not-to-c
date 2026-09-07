#include <stdio.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s NAME\n", argv[0]);
        return 1;
    }

    if (argv[1] == "Ali")
    {
        printf("Hello, boss\n");
    }
    else
    {
        printf("Hello, stranger\n");
    }

    return 0;
}
