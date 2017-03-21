#! /usr/bin/python
# coding:utf-8
import os
import subprocess
import json
import time
from script_tools import new_terminal_exit,new_terminal


class Case():
    '''Class of test cases
        path: abs path
        intro: introduction  (optional)
        run_vul: cmd
        run_exp: cmd         (optional)
        run_check: cmd
        compile: cmd
        aslr: bool
        dep: bool
        stack: bool          (optional)
        tag: tags
        release: bool
    '''
    def __init__(self,abs_path):
        self.path = abs_path
        self.load_info()

    def load_info(self):
        '''Load info file'''
        try:
            with open (self.path+'/define.json','r') as f:
                self.define_data = json.load(f)
        except Exception, e:
            print "Loading %s failed, please check the define.json format." % self.path
        

    def check_define(self,warnings=False):
        '''Check info file and config file.'''
        # required
        return True  # Succeed

    def run(self, input_name=None):
        if not self.check_define():
            print '[Error]: Failed check the info file. Stop.'
            return

        if self.define_data["attack_model"]=="data":
            if not input_name: input_name = self.define_data["default_attack_name"]

            for attack in self.define_data["attack_class"]:
                if attack["name"]==input_name:
                    input_file = attack["path"]

            os.chdir(self.path)
            os.popen(new_terminal_exit(self.define_data['vul_path']+' '+input_file))

        else:
            print "Not supported yet"

    def compile(self,dep=None,stack=None):  # TODO did compile finish? we may run it in current process to make sure.
        if "compile" in self.define_data.keys:
            os.chdir(self.path)
            os.popen(self.define_data["compile"])

    def check(self):
        '''Return check answer.'''
        p = subprocess.Popen(self.define_data["check_path"], stdout=subprocess.PIPE, shell= True)
        res = p.stdout.read().strip()
        return res



def list_cases(path):
    '''Find all cases in the path'''
    lst = []
    case_lst = []
    def find(path):
        if 'define.json' in os.listdir(path) and os.path.isfile(path+'/define.json'):
            lst.append(path)
        else:
            for sub_path in os.listdir(path):
                if not os.path.isfile(sub_path):
                    find(path+'/'+sub_path)
    find(path)
    for i in lst:
        case = Case(i)
        case_lst.append(case)
    return case_lst



if __name__=='__main__':
    c = Case("/home/readm/CSTE/src/sample")
    #c.run()
    #c.check_define(check_optional=True)
    #print list_cases('/home/readm/CSTE/src')