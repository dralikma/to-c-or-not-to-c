#include <stdio.h>

int main(void)
{
    int tax = 408;
    int total = 5356;

    int percent = (tax / total) * 100;

    printf("Tax is %d%% of the bill\n", percent);
    return 0;
}
