#include <stdio.h>
#include <malloc.h>

int main()
{
	int * t = malloc(5);
	free(t);
	t = calloc(1, 1);
	t = realloc(t, 2);
	free(t);
}
