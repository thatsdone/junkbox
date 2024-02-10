SRCS=mslice.c
SONAME=libmslice.so
CFLAGS=-Wall -D_GNU_SOURCE -fPIC
DLFAGS=-g
LFLAGS=-Wl,'--no-as-needed' -shared -ldl
# Note: '--no-as-needed' must be in front of -ldl
#
all:
	gcc  $(CFLAGS) $(DFLAGS) ${LFLAGS} $(SRCS) -o $(SONAME)

clean:
	/bin/rm -f *~ *.so *.o core
