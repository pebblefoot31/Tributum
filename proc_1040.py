#!/usr/bin/env python3
"""
Program for processing form 1040
"""

import utils
import toml

def start():
    """
    This is the main function.
    """
    d_1040 = toml.load("f1040.c1.toml")

    #print(d_1040)

    #print(d_1040["Dependents"]["Dep1"])

    #print(d_1040["Dep1"]["FN_LN"])

    #print(d_1040["Address"]["Street"])

    #print(utils.deps(d_1040))

#the 'if' condition determines if we need the file containing schedule B
    if d_1040["Main"]["i2a"] > 0 or d_1040["Main"]["i3a"] > 0:
        d_sched_b = toml.load("sched_B.c1.toml")
         #this line processes sched B file with the function proc_sched_b
        d_sched_b = utils.proc_sched_b(d_sched_b)
        #creates and opens new file that we will dump the processed values into in 'write' mode
        outfile = open("sched_B.c1.processed.toml",'w')
        #toml.dump is a function that takes arguments in this format: (content, location).
        #It comes with the toml package we installed
        toml.dump(d_sched_b, outfile)
        outfile.close()#closing processed file
        d_1040["Main"]["i2b"] = d_sched_b["Part1_Interest"]["i4"]
        #updating main 1040 document with the processed values from sched B
        print(d_1040["Main"]["i2b"])#just to see if the program worked

    d_1040["Main"]["i9"] = d_1040["Main"]["i1"]\
                            +d_1040["Main"]["i2b"]\
                            +d_1040["Main"]["i3b"]\
                            +d_1040["Main"]["i4b"]\
                            +d_1040["Main"]["i5b"]\
                            +d_1040["Main"]["i6b"]\
                            +d_1040["Main"]["i7"]\
                            +d_1040["Main"]["i8"]

    #processing line 10 of f1040
    d_1040["Main"]["i10c"] = d_1040["Main"]["i10a"] + d_1040["Main"]["i10b"]

    #processing line 11 of f1040
    d_1040["Main"]["i11"] = d_1040["Main"]["i9"] - d_1040["Main"]["i10c"]

    #processing line 12 of f1040
    if d_1040["Filing_Status"] == "S" or\
                                    d_1040["Filing_Status"] == "MFS":
        d_1040["Main"]["i12"] = 12400

    elif d_1040["Filing_Status"] == "MFJ" or\
                                    d_1040["Filing_Status"] == "QW":
        d_1040["Main"]["i12"] = 24800

    elif d_1040["Filing_Status"] == "HOH":
        d_1040["Main"]["i12"] = 18650

    #processing line 14 and 15 of f1040
    d_1040["Main"]["i14"] = d_1040["Main"]["i12"] + d_1040["Main"]["i13"]

    d_1040["Main"]["i15"] = d_1040["Main"]["i11"] - d_1040["Main"]["i14"]
    if d_1040["Main"]["i15"] <= 0:
        d_1040["Main"]["i15"] = 0

    if d_1040["Main"]["i15"] <= 100000:
       d_1040["Main"]["i16"] = utils.read_tax_table(d_1040["Filing_Status"], d_1040["Main"]["i15"])
    else:
        print("To do for income greater than 100k")

    d_1040["Main"]["i17"] = 0 #line 3 of schedule 2.

    d_1040["Main"]["i18"] = d_1040["Main"]["i16"] + d_1040["Main"]["i17"]
    
    d_1040["Main"]["i19"] = int(utils.deps(d_1040)) * 2000
    print(d_1040["Main"]["i19"])#for confirmation

    #d_1040["Main"]["i20"] = 0 #amount from sched 7 line 3

    d_1040["Main"]["i21"] = d_1040["Main"]["i19"] + d_1040["Main"]["i20"]

    d_1040["Main"]["i22"] = d_1040["Main"]["i18"] - d_1040["Main"]["i21"]
    if d_1040["Main"]["i22"] <= 0:
        d_1040["Main"]["i22"] == 0

    #d_1040["Main"]["i23"] = 0 
    d_1040["Main"]["i24"] = d_1040["Main"]["i22"] + d_1040["Main"]["i23"] 
    d_1040["Main"]["i25a"] = 8637
    #d_1040["Main"]["i25b"] = 0
    #d_1040["Main"]["i25c"] = 0
    d_1040["Main"]["i25d"] = d_1040["Main"]["i25a"]\
                            +d_1040["Main"]["i25b"]\
                            +d_1040["Main"]["i25c"]

    #d_1040["Main"]["i26"] = 0
    #d_1040["Main"]["i27"] = 0
    #d_1040["Main"]["i28"] = 0
    #d_1040["Main"]["i29"] = 0 
    #d_1040["Main"]["i30"] = 0
    #d_1040["Main"]["i31"] = 0 
    d_1040["Main"]["i32"] = d_1040["Main"]["i27"]\
                            +d_1040["Main"]["i28"]\
                            +d_1040["Main"]["i29"]\
                            +d_1040["Main"]["i30"]\
                            +d_1040["Main"]["i31"]

    d_1040["Main"]["i33"] = d_1040["Main"]["i25d"]\
                            +d_1040["Main"]["i26"]\
                            +d_1040["Main"]["i23"] 

    if d_1040["Main"]["i33"] > d_1040["Main"]["i24"]:
        d_1040["Main"]["i34"] = d_1040["Main"]["i33"] - d_1040["Main"]["i24"]
    else:
        d_1040["Main"]["i34"] = 0

    d_1040["Amount_you_owe"]["i37"] = d_1040["Main"]["i24"] - d_1040["Main"]["i33"]


    #creates and opens new file that we will dump the processed values into in 'write' mode
    outfile = open("f1040.c1.processed.toml",'w')
    
    #toml.dump is a function that takes arguments in this format: (content, location).
    #It comes with the toml package we installed
    toml.dump(d_1040, outfile)
    outfile.close()#closing processed file


if __name__ == "__main__":

    start()
