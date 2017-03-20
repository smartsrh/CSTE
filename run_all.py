#! /usr/bin/python
# coding:utf-8
try:
    import cmd2 as cmd
except ImportError:
    import cmd

from tools.core import *
from tools.script_tools import *

cases = []
select_cases = []
report_buf = []

root_path=os.path.abspath('.')


class ui(cmd.Cmd):
    prompt = "CSTE>"
    intro = '''简要说明：通过以下命令, 运行指定的漏洞程序
        show                      显示可以利用的所有程序
        select i                  选择第i个要执行的程序
        select i1 i2 ...          选择第i1,i2,i3...个要执行的程序
        select name/path          选择名字或路径下所有程序
        select tag name           选择name类型的程序
        run                       运行选择的漏洞程序,并进行攻击
        run normal                运行选择的漏洞程序,正常运行
        attach i                  附加调试第i个程序
        aslr status               获取ASLR的状态
        aslr on/off/conservative  修改ASLR状态
        help run                  查看相关命令信息
        q                         退出'''

    def do_reload(self, line):
        '''Reload the test cases.'''
        global cases, root_path
        root_path = os.path.abspath('.')
        if 'src' in os.listdir('.'):
            path = root_path + '/src'
        else:
            print "No test cases found please run the script in the CSTE root path."  # TODO auto correct path.
            return True
        cases = list_cases(path)

    def do_show(self, line):
        '''Show all available test cases.
        Format:
        show                            show all
        show [path_name]                show all under the path
        show tag [tag_name]             show all with the tag'''
        global cases,select_cases

        # if tag
        if len(line.split())==2:
            tag = line.split()[1]
            i = 1
            for case in cases:
                if tag in case.tags:
                    print i, ':', case.path.replace(os.path.abspath(root_path+'/src')+'/','')
                i += 1

            pass
        # no arg
        elif len(line.strip()) ==0 :
            i = 1
            for case in cases:
                print i, ':', case.path.replace(os.path.abspath(root_path+'/src')+'/','')
                i += 1
        # path
        else:
            path=line.strip()
            i = 1
            for case in cases:
                if case.path.startswith(os.path.abspath(root_path+'/src/'+path)):
                    print i, ':', case.path.replace(os.path.abspath(root_path+'/src')+'/','')
                i += 1


    def do_guide(self, line):
        print self.intro

    def do_select(self, line):
        '''Select by number/path/tag'''
        global cases,select_cases
        if line[0] in '0123456789':
            indexes = [int(i)-1 for i in line.split()]
            select_cases = [cases[i]  for i in indexes]
        elif line.startswith('tag'):
            select_cases = [case for case in cases if line.split(None,1)[1].strip() in case.tags]
        else:   # path
            select_cases = [case for case in cases if
                case.path.startswith(os.path.abspath(root_path+'/src/'+line.strip()))]
            pass

        print "Now selected %d cases" % len(select_cases)

    def do_run(self, line):
        if line.startswith('normal'):
            attack = False
        else:
            attack = True
        if select_cases:
            for case in select_cases:
                case.run(attack=attack)
        else:
            print "No case selected, run all."
            for case in cases:
                case.run(attack=attack)

    def do_check(self, line):
        '''Check all selected.'''
        if select_cases:
            for case in select_cases:
                ans = case.check()
                report_buf.append(ans)
                print ans
        else:
            print "No case selected, check all."
            for case in cases:
                ans = case.check()
                report_buf.append(ans)
                print ans


    def do_add(self, line):
        '''Add cases after select'''
        print '''Not implement yet.'''

    def do_remove(self, line):
        '''Remove cases after select'''
        print '''Not implement yet.'''

    def do_report(self, line):  # design how to report
        ''''''
        print '''Not implement yet.'''

    def do_aslr(self, line):
        '''Check status/Turn on/Turn off ASLR of system.
Format: aslr status/check/on/off/conservative'''
        if line in ['status', 'frame_check', 'on', 'off', 'conservative']:
            if line[1] in ['h', 't']:
                state = aslr_status()
                if state == 2:
                    print "ASLR: ON\n"
                elif state == 0:
                    print "ASLR: OFF\n"
                elif state == 1:
                    print "ASLR: Conservative ON\n"
                else:
                    print "Invalid Value."
            elif line[1] == 'n':
                aslr_on()
            elif line[1] == 'f':
                aslr_off()
            elif line[1] == 'o':
                aslr_conservative()

        else:
            print colorize('[Error]: ', 'red'), 'Wrong Format.'
            self.do_help('aslr')

    def complete_aslr(self, text, line, begidx, endidx):
        return [i for i in ['status', 'check', 'on', 'off', 'conservative'] if i.startswith(text)]

    def do_attach(self, line):
        '''Run a case and attach it.'''
        print '''Not implement yet.'''

    def do_q(self, line):
        '''Quit.'''
        return True

    def do_info(self, line):
        '''Show info of cases'''
        print '''Not implement yet.'''


CSTEui = ui()

# delete unused command (make command list clear)
for attr in ['do_list', 'do_r', 'do_cmdenvironment', 'do_history', 'do_hi', 'do_save',
             'do_pause', 'do_ed', 'do_edit', 'do_EOF', 'do_eof', 'do_li', 'do_l', 'do_quit']:
    if hasattr(cmd.Cmd, attr): delattr(cmd.Cmd, attr)

CSTEui.do_reload('')
CSTEui.cmdloop()