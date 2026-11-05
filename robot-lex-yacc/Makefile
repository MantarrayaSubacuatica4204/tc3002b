# Makefile - Intérprete robot/dron (LEX + YACC)
# Autor: Jaime Trujillo Ruiz

CC     = gcc
CFLAGS = -Wall -Wextra -g

OBJS = robot.tab.o lex.yy.o main.o

robot: $(OBJS)
	$(CC) $(CFLAGS) -o robot $(OBJS) -lm

robot.tab.c robot.tab.h: robot.y
	bison -d -Wall robot.y -o robot.tab.c

lex.yy.c: robot.l robot.tab.h
	flex robot.l

robot.tab.o: robot.tab.c
	$(CC) $(CFLAGS) -c robot.tab.c

lex.yy.o: lex.yy.c robot.tab.h
	$(CC) $(CFLAGS) -c lex.yy.c

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

clean:
	rm -f robot $(OBJS) robot.tab.c robot.tab.h lex.yy.c

.PHONY: clean
