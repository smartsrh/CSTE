/*
  gcc stack_overflow_check.c -o stack_overflow_check
  
*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

void check(){
    FILE* fp; 
    fp=fopen("./output/double_free_injection_output.txt","r"); 
    if(fp==NULL){
        printf("Fail: File double_free_injection_output.txt not found!!!\n");
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
    if(strcmp(tmp,"Double free attack success!")==0)
        printf("Success: double free injection attack succeeded\n");
    else
        printf("Fail: double free injection attack failed\n");
    fclose(fp); 
}

int main(){
    check();
    return 0;
}