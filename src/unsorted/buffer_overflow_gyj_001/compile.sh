#!/bin/sh

gcc -fno-stack-protector -z execstack -g -o stack_overflow stack_overflow.c 

