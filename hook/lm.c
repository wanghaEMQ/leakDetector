#include <stdio.h>
#include <malloc.h>
#include <errno.h>
#include <mqueue.h>
#include <string.h>

#define MSG_MAX_SIZE (31)
#define MSG_SIZE (16)
#define MSG_SIZE_EX (31)
#define MQ_NAME "/leakdetector"

extern void *__libc_malloc(size_t size);
extern void __libc_free(void *p);
extern void *__libc_calloc(size_t nitems, size_t size);
extern void *__libc_realloc(void *p, size_t size);

static int malloc_hook_active = 1;
static int free_hook_active = 1;
static int calloc_hook_active = 1;
static int realloc_hook_active = 1;

void*
dl_malloc_hook (size_t size, void *caller)
{
	void *result;

	// deactivate hooks
	malloc_hook_active = 0;

	result = malloc(size);

	mqd_t mq = mq_open(MQ_NAME, O_WRONLY);
	char buf[MSG_SIZE];
	sprintf(buf, "%p,1", result);
	mq_send(mq, buf, MSG_SIZE, 0);

	// reactivate hooks
	malloc_hook_active = 1;

	return result;
}

void*
dl_calloc_hook (size_t nitems, size_t size, void *caller)
{
	void *result;

	// deactivate hooks
	calloc_hook_active = 0;

	result = calloc(nitems, size);

	mqd_t mq = mq_open(MQ_NAME, O_WRONLY);
	char buf[MSG_SIZE];
	sprintf(buf, "%p,1", result);
	mq_send(mq, buf, MSG_SIZE, 0);

	// reactivate hooks
	calloc_hook_active = 1;

	return result;
}

void*
dl_realloc_hook (void *ptr, size_t size, void *caller)
{
	void *result;

	// deactivate hooks
	realloc_hook_active = 0;

	result = realloc(ptr, size);

	mqd_t mq = mq_open(MQ_NAME, O_WRONLY);
	char buf[MSG_SIZE_EX];
	sprintf(buf, "%p,%p,2", ptr, result);
	mq_send(mq, buf, MSG_SIZE_EX, 0);

	// reactivate hooks
	malloc_hook_active = 1;

	return result;
}

void
dl_free_hook (void *p, void *caller)
{
	// deactivate hooks
	free_hook_active = 0;

	mqd_t mq = mq_open(MQ_NAME, O_WRONLY);
	char buf[MSG_SIZE];
	sprintf(buf, "%p,0", p);
	mq_send(mq, buf, MSG_SIZE, 0);

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
		return dl_malloc_hook(size, caller);
	return __libc_malloc(size);
}

void*
calloc (size_t nitems, size_t size)
{
	void *caller = __builtin_return_address(0);
	if (calloc_hook_active)
		return dl_calloc_hook(nitems, size, caller);
	return __libc_calloc(nitems, size);
}

void*
realloc (void *p, size_t size)
{
	void *caller = __builtin_return_address(0);
	if (realloc_hook_active)
		return dl_realloc_hook(p, size, caller);
	return __libc_realloc(p, size);
}

void
free (void *p)
{
	void *caller = __builtin_return_address(0);
	if (free_hook_active)
		return dl_free_hook(p, caller);
	return __libc_free(p);
}

