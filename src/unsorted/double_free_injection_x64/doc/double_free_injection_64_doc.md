# 程序说明

---

## 1) vul
命名：double_free
漏洞：重复释放漏洞
攻击：代码注入攻击
Shellcode：写文件

本次代码注入攻击是借助 double free 实现的，通过用户编写程序时对申请的同一堆块 double free 的不慎操作获得一个可控指针，篡改 `free@got` 表内容，最终实现将对 free 函数的调用篡改为对 shellcode 的调用。
漏洞程序在课件 double free 部分中所给例子的基础上，稍加改动，漏洞程序主体如下：

```c
p0 = malloc(448);
p1 = malloc(512);
free(p0);
free(p1);
p2 = malloc(768);

memcpy(p2, buf, length);

free(p1); //double free
```

### 对于 double free 以及 unlink 实现细节的绕过：
本次试验攻击模式为单纯的输入数据攻击，随着操作系统安全性的增强，存在防止堆溢出的检测代码，如下：

```c
if (__builtin_expect (FD->bk != P || BK->fd != P, 0))
  malloc_printerr (check_action, "corrupted double-linked list", P, AV);
```
	
   	
其基本含义为：当前堆块的上一堆块中指向下一堆块的指针和当前堆块的下一堆块中指向上一堆块的指针，如果不是指向当前堆块的话，程序就会崩溃退出。
为绕过其检查，需要对注入数据进行特殊构造。已知堆块结构中存在两个指向前后空闲堆块的指针：

```c
struct malloc_chunk* fd;
struct malloc_chunk* bk;
```
	
在注入数据中将两个内存区域分别覆盖为：

```c
p0+16 = &p0-24; //本程序中为0x0000000000601090-24
p0+24 = &p0-16; //本程序中为0x0000000000601090-16
```

即 shellcode 中：

```
\x78\x10\x60\x00\x00\x00\x00\x00
\x80\x10\x60\x00\x00\x00\x00\x00
```

同时，为了绕过 unlink 时对于要释放的堆块大小的检查，在申请的堆块 `p0` , `p1` 的相关位置需覆盖如下数据：

```c
p0 = 0; //十六进制为0x0000000000000000
p0+8 = 448+1; //十六进制为0x00000000000001c1
p1-16 = 448; //十六进制为0x00000000000001c0
p1-8 = 320; //十六进制为0x0000000000000140
```

均可在 shellcode 注入数据的相关位置查看。

这样即可绕过 double free 以及 unlink 的所有相关检查，并可以获得一个可控指针。
之后寻找到 `free@got` 地址 `0x00000000000601018`，将其篡改为 shellcode 地址，本程序为 `p2+32`，那么在用户再次调用 `free(p2)` 时，即转到shellcode的调用，从而实现攻击。

### 对于操作系统相关保护的绕过：
首先，为了绕过 DEP，将 shellcode 所在页改为可执行，代码如下：

```c
mprotect((void *)((uint64_t)p2 & ~4095), 4096, PROT_WRITE|PROT_READ|PROT_EXEC);
```
	
其次，为了绕过ASLR，漏洞程序在构造的过程中对堆块指针进行全局声明，如下：

```c
unsigned char *p0;
unsigned char *p1;
unsigned char *p2;
```

最后，本程序不牵扯栈保护的相关内容。

## 2) input
`input.txt` 此文件为 shellcode，其功能为向 `output`文件夹中的 `double_free_injection_output.txt` 文件中写入字符串 `Double free attack success!`

## 3) output
如果攻击成功会产生 `double_free_injection_output.txt` 文件，文件内容为 `Double free attack success!`
如果攻击失败，将不产生文件，或文件为空

## 4) check
命名：`double_free_injection_check`
获取 `output` 文件夹下 `double_free_injection_output.txt` 文件
如果此文件不存在，或为空，返回失败信息，否则将此文件中的信息返回

## 5) compile.sh  define.json
编译命令和配置信息已经写入 `compile.sh` 和 `define.json` 文件

## 6) shellcode 生成 
用汇编写一段满足攻击要求的程序 `shellcode.asm`
按照如下命令生成 shellcode :
```bash
nasm -f elf64 shellcode.asm -o shellcode.o
ld -s -o shellcode shellcode.o
for i in $(objdump -d shellcode |grep "^ " |cut -f2); do echo -n '\x'$i; done; echo
```



