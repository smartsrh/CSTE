#! /usr/bin/python
# coding:utf-8
import os
import subprocess
import json
import time
from script_tools import new_terminal_exit, aslr_on, aslr_off


class Case():
    '''Class of test cases
    '''

    def __init__(self, abs_path):
        self.path = abs_path
        self.load_info()

    def load_info(self):
        '''Load info file'''
        try:
            with open(self.path + '/define.json', 'r') as f:
                self.define_data = json.load(f)
        except Exception, e:
            print "Loading %s failed, please check the define.json format." % self.path

    def check_define(self, warnings=False):
        '''Check info file and config file.'''
        # required
        return True  # Succeed

    def run_all(self, attack_type=[], attack_mode=True, check=True):
        check_return = []
        if attack_mode:
            if attack_type:
                for a in self.define_data["attack_class"]:
                    if a['type'] in attack_type:
                        self.run(input_name=a['name'], auto_aslr=True)
                        if check: check_return.append(self.check())
            else:  # all attack
                for a in self.define_data["attack_class"]:
                    self.run(input_name=a['name'], auto_aslr=True)
                    if check: check_return.append(self.check())
        else:
            for a in self.define_data["normal_class"]:
                self.run(input_name=a['name'], auto_aslr=True)
                if check: check_return.append(self.check())
        return check_return

    def run(self, attack=True, input_name=None, auto_aslr=True):
        if not self.check_define():
            print '[Error]: Failed check the info file. Stop.'
            return
        _class = 'attack_class' if attack else 'normal_class'
        if self.define_data["attack_model"] == "data":
            if not input_name: input_name = self.define_data["default_attack_name"]
            input_file = ''
            for attack in self.define_data[_class]:
                if attack["name"] == input_name:

                    if auto_aslr == True and _class == 'attack_class':
                        if attack["security_bypass"]["aslr"]:
                            aslr_on()
                        else:
                            aslr_off()

                    input_file = attack["path"]
                    break

            if input_file:
                os.chdir(self.path)
                os.popen(new_terminal_exit(self.define_data['vul_path'] + ' ' + input_file))
            else:
                print "Attack %s not found." % input_name

        else:
            print "Not supported yet"

    def compile(self, dep=None, stack=None):  # TODO did compile finish? we may run it in current process to make sure.
        if "compile" in self.define_data.keys():
            os.chdir(self.path)
            os.popen(self.define_data["compile"])

    def check(self):
        '''Return check answer.'''
        p = subprocess.Popen(self.define_data["check_path"], stdout=subprocess.PIPE, shell=True)
        res = p.stdout.read().strip()
        return res


def list_cases(path):
    '''Find all cases in the path'''
    lst = []
    case_lst = []

    def find(path):
        if 'define.json' in os.listdir(path) and os.path.isfile(path + '/define.json'):
            lst.append(path)
        else:
            for sub_path in os.listdir(path):
                if not os.path.isfile(sub_path):
                    find(path + '/' + sub_path)

    find(path)
    for i in lst:
        case = Case(i)
        case_lst.append(case)
    return case_lst


if __name__ == '__main__':
    c = Case("/home/readm/CSTE/src/unsorted/buffer_overflow_gyj_001")
    # print 'cd'
    # c.check_define()
    # print 'c'
    # c.compile()
    # print 'r'
    # c.run()
    # print 'c'
    # print c.check()
