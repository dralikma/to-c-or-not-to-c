// Chapter 2, Part 3: arrays, and #define for the size.
//
// const cannot size an array in C, which Chapter 1 warned about.
// #define can, because it is a text substitution done before the
// compiler ever looks. Prove it:  gcc -std=c17 -E scores.c | tail -20

#include <stdio.h>

#define N 3

int main(void)
{
    int scores[N] = {72, 73, 33};

    for (int i = 0; i < N; i++)
    {
        printf("Score %d is %d\n", i, scores[i]);
    }

    printf("Average: %f\n", (scores[0] + scores[1] + scores[2]) / 3.0);

    return 0;
}
