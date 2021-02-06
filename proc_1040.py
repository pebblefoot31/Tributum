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

#read_tax_table is a "hard function"
def read_tax_table(income_tax):

    return 6322

def proc_sched_b(dict_sched_b):
    """
    This function processes Part1 Interest and Part2 Ordinary Dividends of the Sched B document.
    """
    items = dict_sched_b["Part1_Interest"]["i1"]
    i_2 = 0
    for i in items:
        i_2 += int(i.split("=")[1].strip())
    dict_sched_b["Part1_Interest"]["i_2"] = i_2
    dict_sched_b["Part1_Interest"]["i3"] = 0
    dict_sched_b["Part1_Interest"]["i4"] = dict_sched_b["Part1_Interest"]["i_2"]\
                                            -dict_sched_b["Part1_Interest"]["i3"]

    items = dict_sched_b["Part2_Ordinary_Dividends"]["i5"]
    i_6 = 0
    for i in items:
        i_6 += int(i.split("=")[1].strip())

    dict_sched_b["Part2_Ordinary_Dividends"]["i_6"] = i_6

    return dict_sched_b

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

#the 'if' condition determines if we need the file containing schedule B
    if d_1040["Main"]["i2a"] > 0 or d_1040["Main"]["i3a"] > 0:
        d_sched_b = toml.load("sched_B.c1.toml")
         #this line processes sched B file with the function proc_sched_b
        d_sched_b = proc_sched_b(d_sched_b)
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
    print(d_1040["Main"]["i9"])

#processing line 10 of f1040
    d_1040["Main"]["i10c"] = d_1040["Main"]["i10a"] + d_1040["Main"]["i10b"]

#processing line 11 of f1040
    d_1040["Main"]["i11"] = d_1040["Main"]["i9"] - d_1040["Main"]["i10c"]

#processing line 12 of f1040
    if d_1040["Filing_Status"] == "Single" or\
                                    d_1040["Filing_Status"] == "Married Filing Separately" or\
                                    d_1040["Filing_Status"] == "MFS":
        d_1040["Main"]["i12"] = 12400

    elif d_1040["Filing_Status"] == "Married filing jointly" or\
                                    d_1040["Filing_Status"] == "Qualified widow" or\
                                    d_1040["Filing_Status"] == "QW":
        d_1040["Main"]["i12"] = 24800

    elif d_1040["Filing_Status"] == "Head of Household" or\
                                    d_1040["Filing_Status"] == "HOH":
        d_1040["Main"]["i12"] = 18650

    print(d_1040["Main"]["i12"])

#processing line 14 and 15 of f1040
    d_1040["Main"]["i14"] = d_1040["Main"]["i12"] + d_1040["Main"]["i13"]

    d_1040["Main"]["i15"] = d_1040["Main"]["i11"] - d_1040["Main"]["i14"]
    if d_1040["Main"]["i15"] <= 0:
        d_1040["Main"]["i15"] = 0

    if d_1040["Main"]["i15"] <= 100000:
       d_1040["Main"]["i16"] = read_tax_table(d_1040["Main"]["i15"])
    else:
        print("To do for income greater than 100k")

    #creates and opens new file that we will dump the processed values into in 'write' mode
    outfile = open("f1040.c1.processed.toml",'w')
    #toml.dump is a function that takes arguments in this format: (content, location).
    #It comes with the toml package we installed
    toml.dump(d_1040, outfile)
    outfile.close()#closing processed file



if __name__ == "__main__":

    start()
