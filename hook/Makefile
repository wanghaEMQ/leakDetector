main.o: main.c liblm.so
	cc -o main.o main.c -L. -llm
liblm.so: lm.o
	cc -shared -o liblm.so lm.o
lm.o: lm.c
	cc -fpic -c lm.c -o lm.o

clean:
	rm lm.o liblm.so main.o
