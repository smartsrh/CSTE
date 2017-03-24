/*gcc -fno-stack-protector -z execstack -g -o stack_overflow stack_overflow.c 
  dep aslr off
*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<stdbool.h>

#define SIZE 200
#define MAX_LENGTH 216

void jmp_rsp(){
    __asm__("jmpq %rsp");
}

bool read_file(char file_name[],char buf[]){
    FILE *fp;
    int v,length=0;
    if((fp=fopen(file_name,"r"))==NULL){
        printf("open file error!!!\n");
        return false;
    }

   while (fscanf(fp, "\\x%02x", &v) == 1)
    {  
        buf[length++] = v;
        if(length==MAX_LENGTH){
            long long int tmp=(long long int)jmp_rsp+4;
            for(int i=0;i<8;++i){
                v=(tmp%16)+(tmp/16%16)*16;
                buf[length++] = v;
                tmp=tmp/16/16;
            }
        }
    } 
    return true;
    fclose(fp);
}


void printf_file(char file_name[]){
    char buffer[SIZE];
    read_file(file_name,buffer);
    printf("%s",buffer); 
}

int main(int argc,char *argv[]){
    if(access("./output/code_injection_output.txt",0)==0)
        remove("./output/code_injection_output.txt");
    printf_file(argv[1]);
    return 0;
}
