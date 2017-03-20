#! /usr/bin/python
#coding:utf-8
import sys, os, json, subprocess

'''Tools for VRL script'''

def new_terminal(command):
    '''Return a new command, execute old command in a new terminal, when old command stop, leave in the terminal.'''
    cmd_bash = command + '; exec bash'
    e_command = "'bash -c \""+cmd_bash+"\"'"
    return "gnome-terminal -e "+e_command

def new_terminal_exit(command):
    '''Return a new command, execute old command in a new terminal, when old command stop, exit the terminal.'''
    return "gnome-terminal -e '"+command+"'"


def aslr_status():
    p = subprocess.Popen("cat /proc/sys/kernel/randomize_va_space",stdout=subprocess.PIPE,shell= True)
    ans = p.stdout.read()
    return int(ans[0])

def aslr_on():
    if aslr_status() == 2:
        print 'ASLR is already ON\n'
        return
    print 'ASLR>>ON, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=2",\
                                           stdin=subprocess.PIPE,shell= True)
    p.wait()

def aslr_off():
    if aslr_status() == 0:
        print 'ASLR is already OFF\n'
        return
    print 'ASLR>>OFF, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=0", \
                                           stdin=subprocess.PIPE,shell= True)
    p.wait()

def aslr_conservative():
    if aslr_status() == 1:
        print 'ASLR is already Conservative\n'
        return
    print 'ASLR>>Conservative, may need password.\n'
    p = subprocess.Popen(r"sudo sysctl -w kernel.randomize_va_space=1", \
                                           stdin=subprocess.PIPE,shell= True)
    p.wait()

def print_line(str, padding='='):
    '''Print str expanded to a whole line.'''
    try:
        import commands
        _output = commands.getoutput('resize')
        columns = int(_output.split(';')[0].split('=')[-1])
    except:
        columns = 80
    _length = columns
    _str = str.center(_length,padding)
    print _str


def pidof(file_name):
    '''Same as bash, return a list of pid number.'''
    p = subprocess.Popen(r"pidof " + str(file_name), stdout=subprocess.PIPE, shell= True)
    lst = p.stdout.read().split()
    lst = [int(i) for i in lst]
    return lst

def gdb(file_name='',pid=0, path='', sudo=True):
    '''Open a gdb.'''
    _cmd = ''
    if sudo: _cmd += 'sudo '
    _cmd += 'gdb '
    if file_name: _cmd += file_name + ' ' + str(pid)
    if path:
        os.chdir(path)
        sys.path.append(path)
        os.system(new_terminal_exit(_cmd))
        sys.path.remove(path)
    else:
        os.system(new_terminal_exit(_cmd))

colorcodes =    {'bold':{True:'\x1b[1m',False:'\x1b[22m'},
                 'cyan':{True:'\x1b[36m',False:'\x1b[39m'},
                 'blue':{True:'\x1b[34m',False:'\x1b[39m'},
                 'red':{True:'\x1b[31m',False:'\x1b[39m'},
                 'magenta':{True:'\x1b[35m',False:'\x1b[39m'},
                 'green':{True:'\x1b[32m',False:'\x1b[39m'},
                 'yellow':{True:'\x1b[33m',False:'\x1b[39m'},
                 'white':{True:'\x1b[37m',False:'\x1b[39m'},
                 'black':{True:'\x1b[30m',False:'\x1b[39m'},
                 'underline':{True:'\x1b[4m',False:'\x1b[24m'}}
def colorize(val, color, prompt=False):
    '''Given a string (``val``), returns that string wrapped in UNIX-style
       special characters that turn on (and then off) text color and style.
       ``color`` should be one of the supported strings (or styles):
       red/blue/green/cyan/magenta/black/white/yellow, bold, underline
       If used in prompt, prompt=True to fix the display bug.'''
    if color:
        if prompt:
            return '\001'+colorcodes[color][True]+'\002' + val + '\001'+colorcodes[color][False]+'\002'
        else:
            return colorcodes[color][True]+ val +colorcodes[color][False]
    return val


