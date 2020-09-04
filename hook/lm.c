#include <stdio.h>
#include <malloc.h>

extern void *__libc_malloc(size_t size);
extern void __libc_free(void *p);
extern void *__libc_calloc(size_t nitems, size_t size);
extern void *__libc_realloc(void *p, size_t size);

int malloc_hook_active = 1;
int free_hook_active = 1;
int calloc_hook_active = 1;
int realloc_hook_active = 1;

void*
my_malloc_hook (size_t size, void *caller)
{
	void *result;

	// deactivate hooks for logging
	malloc_hook_active = 0;

	result = malloc(size);

	// do logging
	fprintf(stdout, "malloc,%p,%ld\n", result, size);

	// reactivate hooks
	malloc_hook_active = 1;

	return result;
}

void*
my_calloc_hook (size_t nitems, size_t size, void *caller)
{
	void *result;

	// deactivate hooks for logging
	calloc_hook_active = 0;

	result = calloc(nitems, size);

	// do logging
	fprintf(stdout, "calloc,%p,%ld\n", result, size);

	// reactivate hooks
	calloc_hook_active = 1;

	return result;
}

void*
my_realloc_hook (void *ptr, size_t size, void *caller)
{
	void *result;

	// deactivate hooks for logging
	realloc_hook_active = 0;

	result = realloc(ptr, size);

	// do logging
	fprintf(stdout, "realloc,%p,%ld\n", result, size);

	// reactivate hooks
	malloc_hook_active = 1;

	return result;
}

void
my_free_hook (void *p, void *caller)
{
	// deactivate hooks for logging
	free_hook_active = 0;

	// do logging
	fprintf(stdout, "free,%p\n", p);

	free(p);

	// reactivate hooks
	free_hook_active = 1;

	return;
}

void*
malloc (size_t size)
{
	void *caller = __builtin_return_address(0);
	if (malloc_hook_active)
		return my_malloc_hook(size, caller);
	return __libc_malloc(size);
}

void*
calloc (size_t nitems, size_t size)
{
	void *caller = __builtin_return_address(0);
	if (calloc_hook_active)
		return my_calloc_hook(nitems, size, caller);
	return __libc_calloc(nitems, size);
}

void*
realloc (void *p, size_t size)
{
	void *caller = __builtin_return_address(0);
	if (realloc_hook_active)
		return my_realloc_hook(p, size, caller);
	return __libc_realloc(p, size);
}

void
free (void *p)
{
	void *caller = __builtin_return_address(0);
	if (free_hook_active)
		return my_free_hook(p, caller);
	return __libc_free(p);
}

