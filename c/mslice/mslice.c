/*
 * libmslice.so :
 *  A shared object to hook connect(2) for multiple slices environment
 *  via UERANSIM(nr-ue).
 * 
 * Usage:
 *   Suppose you want to multiple tunnels like below:
 *      destination1: 192.168.100.0/24, tun0 w/local address: 10.1.1.1
 *      destination2: 192.168.200.0/24, tun1 w/local address: 10.1.2.1
 *   You can specify the mappings using MSLICE_TARGETS environment variable.
 * 
 * $ env MSLICE_TARGETS="192.168.100.0/24,10.1.1.1;192.168.200.0/24,10.1.2.1" \
 *       LD_PRELOAD=./libmslice.so SOME_PROGRAM (e.g., curl)
 *
 * Author: Masanori Itoh <masanori.itoh@gmail.com>
 * Status: development started
 * History: 2024/02/10 Started design and implementation
 */
#include <dlfcn.h>

#include <unistd.h>
#include <stdio.h> 
#include <string.h>
#include <time.h>
#include <errno.h>

/* connect(2) */
#include <sys/types.h>
#include <sys/socket.h>

/* getenv()  */
#include <stdlib.h>

/*
 * A function pointer with the same function prototype with connect(2)
 * to save the original connect(2) entry.
 */
ssize_t (*org)(int fd, const void *buf, size_t count) = 0;

__attribute__((constructor))
static void init_hook()
{
	org = (ssize_t(*)(int, const void *, size_t))dlsym(RTLD_NEXT, "connect");
	printf("DEBUG: %s: constructor called! %p\n", __func__, org);
}

__attribute__((destructor))
static void fini_hook()
{
	printf("DEBUG: %s: destructor called!\n", __func__);
}


int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
  int ret = 0;

  printf("DEBUG: %s: hook!\n", __func__);


  
  ret = (int)org(sockfd, addr, addrlen);
  return ret;
}
