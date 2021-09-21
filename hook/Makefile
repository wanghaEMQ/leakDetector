main.o: main.c liblm.so
	cc -o main.o main.c -L. -llm -lrt
liblm.so: lm.o
	cc -shared -o liblm.so lm.o -lrt
lm.o: lm.c
	cc -fpic -c lm.c -o lm.o -lrt

clean:
	rm lm.o liblm.so main.o
