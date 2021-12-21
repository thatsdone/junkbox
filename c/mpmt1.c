/*
 * mpmt1.c: A stupid simple example of C threading and multiprocessing.
 * C Language pthread version of below:
 *     https://github.com/thatsdone/junkbox/blob/master/python/mpmt1.py
 *
 * STATUS:
 *  Under development
 * License:
 *   Apache License, Version 2.0
 * History:
 *   2021/12/21 v0.1 Initial version based on:
 * Author:
 *   Masanori Itoh <masanori.itoh@gmail.com>
 * BUILD:
 *   * `$ gcc -o mpmt1 mpmt1.c -lpthread`
 * TODO:
 *   * Use pthread_attr (affinity etc.)
 *   * Write multi process version.
 */
#include <sys/types.h>
#include <sys/time.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *worker(void *arg)
{
	struct timeval tv, tv_save;
	long ts, ts_save;
	long duration = *(long *)arg;
	pthread_t tid = pthread_self();
	printf("%s: TID: %lu running: %ld (us)\n", __func__, tid, *(long *)arg);
	gettimeofday(&tv_save, NULL);
	ts_save = tv_save.tv_sec * 1000 * 1000 + tv_save.tv_usec;
	while (1) {
		gettimeofday(&tv, NULL);
		ts = tv.tv_sec * 1000 * 1000 + tv.tv_usec;
		if ((ts - ts_save) > duration) {
			printf("%s: TID: %lu Expired!\n", __func__, tid);
			break;
		}
	}
	pthread_exit(0);
}
		
#define MAX_CONTEXT 16

int main(int argc, char **argv)
{
	int i, ret, opt, use_thread = 1;
	pthread_t th[MAX_CONTEXT];
	pthread_t tid;

	int num_context = 4;
	long duration = 5 * 1000 * 1000;
	
	while ((opt = getopt(argc, argv, "n:d:m:")) != -1) {
		switch (opt) {
		case 'n':
			num_context = atoi(optarg);
			if (num_context > MAX_CONTEXT) {
				printf("%s: -n too big. %d\n", argv[0], num_context);
				exit(-1);
			}
			break;
		case 'd':
			duration = atol(optarg) * 1000 * 1000;
			break;
		case 'm':
			if (*optarg == 't' || *optarg == 'T') {
				printf("DEBUG: optarg: %s\n", optarg);
				use_thread = 1; //thread
			} else if (*optarg == 'p' || *optarg == 'P') {
				printf("Multi process mode, Not implemented yet.\n");
				exit(-1);
				use_thread = 0; //process
			} else {
				printf("Unknown -m value : %s\n", optarg);
				exit(-1);
			}
			break;
               default: /* '?' */
                   fprintf(stderr, "Usage: %s [-n NUM_CONTEXT] [-d DURATION] [-m MODE]\n",
                           argv[0]);
                   exit(-1);
               }
           }
	
	printf("%s: PID: %d\n", __func__, getpid());

	for (i = 0; i < num_context; i++) {
		ret = pthread_create(&th[i], NULL, worker, (void *)&duration);
		printf("%s: pthread_create retruned %d\n", __func__, ret);
	}
	for (i = 0; i < num_context; i++) {
		ret = pthread_join(th[i], (void **)NULL);
		printf("%s: pthread_join for %d retruned %d / %lu\n", __func__, i, ret, (unsigned long)0);
	}

}
