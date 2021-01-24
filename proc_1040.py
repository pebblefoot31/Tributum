#!/usr/bin/env python3
"""
Programs for processing form 1040
"""

import toml

def deps(dict_1040):
    """
    A function to calculate no. of dependents.
    This currently goes up to 4 dependents.
    """
    dep_count = 0
    #while
    counter = 1
    while counter <= 4 and dict_1040["Dep" + str(counter)]["FN_LN"] != "":
        counter += 1
        dep_count += 1

    return dep_count

def proc_sched_B(dict_sched_B):
    items = dict_sched_B["Part1_Interest"]["i1"]
    i2 = 0
    for i in items:
        i2 += int(i.split("=")[1].strip())
    dict_sched_B["Part1_Interest"]["i2"] = i2
    dict_sched_B["Part1_Interest"]["i3"] = 0
    dict_sched_B["Part1_Interest"]["i4"] = dict_sched_B["Part1_Interest"]["i2"]-dict_sched_B["Part1_Interest"]["i3"]

    items = dict_sched_B["Part2_Ordinary_Dividends"]["i5"]
    i6 = 0
    for i in items:
        i6 += int(i.split("=")[1].strip())

    dict_sched_B["Part2_Ordinary_Dividends"]["i6"] = i6
    
    return dict_sched_B

def start():
    """
    This is the main function.
    """
    d_1040 = toml.load("f1040.c1.toml")

    #print(d_1040)

    #print(d_1040["Dependents"]["Dep1"])

    #print(d_1040["Dep1"]["FN_LN"])

    #print(d_1040["Address"]["Street"])

    #print(deps(d_1040))

    if d_1040["Main"]["i2a"] > 0 or d_1040["Main"]["i3a"] > 0:
        d_sched_B = toml.load("sched_B.c1.toml")
        d_tmp = proc_sched_B(d_sched_B)

    d_sched_B = d_tmp
    outfile = open("sched_B.c1.processed.toml",'w')
    toml.dump(d_sched_B, outfile)
    d_1040["Main"]["i2b"] = d_sched_B["Part1_Interest"]["i4"]
    print(d_1040["Main"]["i2b"])

if __name__ == "__main__":

    start()
