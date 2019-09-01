/*
 * An example system call hook module using LD_PRELOAD.
 * Usage:
 *   $ env LD_PRELOAD=./hook.so SOME_PROGRAM_WHICH_CALLS_write
 *
 * Author: Masanori Itoh <masanori.itoh@gmail.com>
 */
#include <dlfcn.h>

#include <unistd.h>
#include <stdio.h> 
#include <string.h>
#include <time.h>
#include <errno.h>

/*
 * A function pointer with the same function prototype with write(2)
 * to save the original write(2) entry.
 */
ssize_t (*org)(int fd, const void *buf, size_t count) = 0;

__attribute__((constructor))
static void init_hook()
{
	org = (ssize_t(*)(int, const void *, size_t))dlsym(RTLD_NEXT, "write");
	printf("%s: constructor called! %p\n", __func__, org);
}

__attribute__((destructor))
static void fini_hook()
{
	printf("%s: destructor called!\n", __func__);
}

ssize_t write(int fd, const void *buf, size_t count)
{
	int ret;

	/*
	 * Do what you like to do here
	 */ 
	printf("%s: hook!\n", __func__);
	ret = (int)org(fd, buf, count);
	/*
	 * Do what you like to do here
	 */
    return ret;

}

