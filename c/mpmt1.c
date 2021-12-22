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
#include <wait.h>


int use_thread = 1;

void *worker(void *arg)
{
	struct timeval tv, tv_save;
	long ts, ts_save;
	long duration = *(long *)arg;
	pthread_t tid = 0;
	pid_t pid = 0;
	if (use_thread) {
		tid = pthread_self();
		printf("%s: TID: %lu running: %ld (us)\n",
		       __func__, tid, *(long *)arg);
	} else {
		pid = getpid();
		printf("%s: PID: %d running: %ld (us)\n",
		       __func__, pid, *(long *)arg);
	}

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
	if (use_thread) {
		pthread_exit(0);
	} else {
		exit(0);
	}
}
		
#define MAX_CONTEXT 16

int main(int argc, char **argv)
{
	int i, ret, opt;
	pthread_t th[MAX_CONTEXT];
	pthread_t tid;
	pid_t pr[MAX_CONTEXT];
	pid_t pid;

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
				printf("Multi thread mode,\n");
				use_thread = 1; //thread
			} else if (*optarg == 'p' || *optarg == 'P') {
				printf("Multi process mode,\n");
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
	
	printf("%s: PID: %d. Creating workers.\n", __func__, getpid());

	for (i = 0; i < num_context; i++) {
		if (use_thread) {
			ret = pthread_create(&th[i], NULL, worker, (void *)&duration);
			printf("%s: pthread_create retruned %d\n", __func__, ret);
		} else {
			pid = fork();
			switch (pid) {
			case 0:
				/* child */
				printf("child: fork returnd %d.\n", pid);
				worker((void *)&duration);
				break;
			case -1:
				/* failure */
				printf("fork returnd %d\n", pid);
				exit(-1);
				break;
			default:
				/* parent */
				printf("parent: fork returnd %d\n", pid);
				pr[i] = pid;
			}
		}
	}

	printf("%s: PID: %d. Waiting for completion of workers.\n", __func__, getpid());

	for (i = 0; i < num_context; i++) {
		if (use_thread) {
			ret = pthread_join(th[i], (void **)NULL);
			printf("%s: pthread_join for %d retruned %d / %lu\n",
			       __func__, i, ret, (unsigned long)0);
		} else {
			int wstatus;
			ret = waitpid(pr[i], &wstatus, 0);
			printf("%s: waitpid for %d retruned %d / %d\n",
			       __func__, i, ret, wstatus);
			;
		}
	}
}
