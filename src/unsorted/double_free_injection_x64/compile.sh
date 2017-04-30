#!/bin/sh

gcc -g -o ./vul/double_free ./vul/double_free.c
gcc -o ./check/double_free_injection_check ./check/double_free_injection_check.c