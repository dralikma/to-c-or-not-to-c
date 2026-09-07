#include <stdio.h>
#include <string.h>

int main(void)
{
    char word[3] = {'H', 'i', '!'};

    printf("The word is %s and it is %zu characters\n", word, strlen(word));

    return 0;
}
