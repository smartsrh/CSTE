#!/bin/sh

gcc -fno-stack-protector -z execstack -g -o ./vul/stack_overflow ./vul/stack_overflow.c 
gcc -o ./check/stack_overflow_check ./check/stack_overflow_check.c

