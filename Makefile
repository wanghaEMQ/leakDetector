main.o: exampleProcess.c liblm.so
	cc -o exampleProcess.o exampleProcess.c -L. -llm -lrt
liblm.so: hook/lm.o
	cc -shared -o liblm.so hook/lm.o -lrt
lm.o: hook/lm.c
	cc -fpic -c hook/lm.c -o hook/lm.o -lrt

clean:
	rm hook/lm.o liblm.so exampleProcess.o
