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
/* connect(2), bind(2) */
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h> /* getenv()  */
#include <string.h>

static int debug = 0;

#define MAX_DESTINFO 16
static int num_destinfo = 0;
static struct destinfo *destinfos;

struct destinfo {
  struct in_addr dest;
  int size;
  struct in_addr local;
};

unsigned int bitmask(int size)
{
  if (size >= 32) {
    return 0xffffff;
  } else if (size <= 0) {
    return 0x0;
  }
  return htonl(0xffffff << (32 - size));
}

struct destinfo *check(struct in_addr *target)
{
  int i;
  for (i = 0; i < num_destinfo; i++) {
    if (debug) printf("DEBUG: %d: %08x %08x\n",
                      i,
                      (destinfos[i].dest.s_addr & bitmask(destinfos[i].size)),
                      (target->s_addr  & bitmask(destinfos[i].size)));
    if ((destinfos[i].dest.s_addr & bitmask(destinfos[i].size)) ==
        (target->s_addr & bitmask(destinfos[i].size))) {
      if (debug) printf("match !\n");
      return destinfos + i;
    } else {
      if (debug) printf("no match \n");
    }
  }
  return NULL;
}

void show_destinfos()
{
  int i;
  for (i = 0; i < num_destinfo; i++) {
    if (debug) printf("DEBUG: %d: %08x %d %08x\n",
                      i,
                      destinfos[i].dest.s_addr,
                      destinfos[i].size,
                      destinfos[i].local.s_addr);
  }
}

void parse_env()
{
  char *env = getenv("MSLICE_TARGETS");
  char *saveptr1, *str1, *token1;
  char *saveptr2, *str2, *token2;
  char *str3;
  int i, j, netsize;
  char *dest_addr;
  char *local_addr;
  int ret;
  char *debug_env;

  if (env == NULL) {
    return;
  }
  if ((debug_env = getenv("MSLICE_DEBUG")) != NULL) {
    debug = atoi(debug_env);
  }

  destinfos =  malloc(sizeof(struct destinfo) * MAX_DESTINFO);
  memset(destinfos, 0x0, sizeof(struct destinfo) * MAX_DESTINFO);

  if (debug) printf("DEBUG: MSLICE_TARGETS: %s\n", env);

  /* parse MSLICE_TARGETS and build destinfo array */
  for (i = 0, str1 = env; ; i++, str1 = NULL) {
    token1 = strtok_r(str1, ";", &saveptr1);
    if (token1 == NULL || i > MAX_DESTINFO) {
      break;
    }
    if (debug) printf("DEGBUG: %d: %s\n", i, token1);

    for (j = 0, str2 = token1; ; j++, str2 = NULL) {
      token2 = strtok_r(str2, ",", &saveptr2);
      if (debug) printf("DEBUG(token2): %d: %s\n", j, token2);
      if (token2 == NULL || j > 1) {
        break;
      }
      if (j == 0) {
        if ((str3 = strchr(token2, (int)'/')) != NULL) {
          netsize = atoi(str3 + 1);
          if (debug) printf("DEBUG(size): %s (%d)\n", str3 + 1, netsize);
          dest_addr = strndup(token2, str3 - token2);
        } else {
          dest_addr = token2;
          if (debug) printf("DEBUG(dest): %d %s\n", j, dest_addr);
        }
      }
      if (j == 1) {
        local_addr = token2;
        if (debug) printf("DDEBUG(local):  %d: %s\n", j, local_addr);
      }
    }
    if (debug) printf("DEGBUG2: %s/%d -> %s\n", dest_addr, netsize, local_addr);
    ret = inet_aton(dest_addr, &(destinfos[i].dest));
    if (ret <= 0) {
      if (debug) printf("DEBUG3: %s is not valid\n", dest_addr);
      continue;
    }
    ret = inet_aton(local_addr, &(destinfos[i].local));
    if (ret <= 0) {
      if (debug) printf("DEBUG3: %s is not valid\n", local_addr);
      continue;
    }
    destinfos[i].size = netsize;
  }
  num_destinfo = i;
  if (debug) printf("DEBUG: num_destinfo = %d\n", num_destinfo);
}


/*
 * A function pointer with the same function prototype with connect(2)
 * to save the original connect(2) entry.
 */
int (*org)(int sockfd, const struct sockaddr *addr, socklen_t addrlen) = 0;

__attribute__((constructor))
static void init_hook()
{
  parse_env();

  org = (int(*)(int sockfd, const struct sockaddr *addr, socklen_t addrlen))dlsym(RTLD_NEXT, "connect");  
  if (debug) printf("DEBUG: %s: constructor called! %p\n", __func__, org);
}

__attribute__((destructor))
static void fini_hook()
{
  if (debug) printf("DEBUG: %s: destructor called!\n", __func__);
}


int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
  int ret = 0;
  struct sockaddr_in saddr;
  struct sockaddr_in local_saddr;
  socklen_t slen;
  struct destinfo *dinfo = NULL;

  if(debug) printf("DEBUG: %s: hook!\n", __func__);


  if (addr->sa_family != AF_INET) {
    return org(sockfd, addr, addrlen);
  }
  
  ret = getsockname(sockfd, &saddr, &slen);
  if (debug) printf("DEBUG: ret = %d %08x\n", ret, saddr.sin_addr.s_addr);
  dinfo = check((struct in_addr*)&((struct sockaddr_in *)addr)->sin_addr.s_addr);
  /* TODO(thatsdone): call bind(2) if dinfo is not NULL */
  if (dinfo != NULL) {
    if (debug) {
      printf("DEBUG: %08x is in %08x/%d\n",
             ((struct sockaddr_in *)addr)->sin_addr.s_addr,
             dinfo->dest.s_addr,
             dinfo->size);
    }
    local_saddr.sin_family = addr->sa_family;
    local_saddr.sin_addr.s_addr = dinfo->local.s_addr;
    ret = bind(sockfd, &local_saddr, sizeof(struct sockaddr_in));
    if (debug) printf("DEBUG: bind(2) returns %d (%d)\n", ret, errno);
    if (ret < 0) {
      printf("WARNING: bind(2) failed\n");
    }
  }
  return org(sockfd, addr, addrlen);
}
