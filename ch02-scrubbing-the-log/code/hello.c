// Chapter 2, Part 2: the program you take apart stage by stage.
//
//     gcc -std=c17 -E hello.c > hello.i      preprocess
//     gcc -std=c17 -S hello.c -o hello.s     compile to assembly
//     gcc -std=c17 -c hello.c -o hello.o     assemble
//     gcc hello.o -o hello                   link

#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
