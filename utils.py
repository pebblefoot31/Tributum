#!/usr/bin/env python3
"""
Functions for processing form 1040
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
def read_tax_table(filing_status, income_tax):

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

