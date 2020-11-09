convex_hull.o : convex_hull.c
	gcc -c convex_hull.c

exe: convex_hull.o
	gcc convex_hull.o -o exe
	rm convex_hull.o

action : exe
	./exe
	rm exe