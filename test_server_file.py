#!/usr/bin/env python

import time

class Change_log():

    def Change_log():
        f=open("change_log.txt","w+")

        rl = f.readlines()
        print("Initlization:",rl)
        change_log = []
        for line in rl:
            change_log.append(line)
            print(line)
        f.close()
        
    def add_log():
        et=time.localtime() #entry time
        ed=time.asctime(et) #entry date
        msg= ed+": " + msg+"\n"
        change_log.append(msg)
        f=open(file,"w+")
        for change in change_log:
            f.write(change)
        f.close()
        
    def show(change_log):
        for line in change_log:
            print(line)
            
    def get_last(change_log):
        last=change_log.pop()
        change_log.append(last)
        return last
