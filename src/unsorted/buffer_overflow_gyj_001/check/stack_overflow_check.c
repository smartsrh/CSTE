/*
  gcc stack_overflow_check.c -o stack_overflow_check
  
*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void check(){
    FILE* fp; 
    fp=fopen("./output/code_injection_output.txt","r"); 
    if(fp==NULL){
        printf("Fail: File code_injection_output.txt not found!!!\n");
	return; 
    }
    if(fgetc(fp)==EOF){
        printf("Fail: File is empty!!!\n");
	return;
    }
    fseek(fp, 0, SEEK_END);
    int file_size;
    file_size = ftell(fp)+1;
    char *tmp;
    fseek(fp, 0, SEEK_SET);
    tmp =  (char *)malloc(file_size * sizeof(char));
    fread(tmp, file_size, sizeof(char), fp);
    tmp[file_size-1]='\0';
    if(strcmp(tmp,"buffer_overflow_gyj_001 attack succeeded")==0)
        printf("Success: Stack overflow attack succeeded\n");
    else
        printf("Fail: Stack overflow attack failed\n");
    fclose(fp); 
}

int main(){
    check();
    return 0;
}

