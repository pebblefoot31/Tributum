#!/usr/bin/env python3

import toml

def deps(d):
    count = 0
    #while
    x = 0
    while x < 4:
        x += 1
        if d["Dep" + str(x)]["FN_LN"] != "":
            count += 1
    
    return(count)

def start():
    d_1040 = toml.load("f1040.toml")

    #print(d_1040)

    #print(d_1040["Dependents"]["Dep1"])

    print(d_1040["Dep1"]["FN_LN"])

    print(d_1040["Address"]["Street"])

    print(deps(d_1040))



if __name__ == "__main__":

    start()


    

