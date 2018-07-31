# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 21:50:54 2018

@author: Tom
"""

import os
import random

dir_path = os.path.dirname(os.path.realpath(__file__)) +"\crash_data.csv"
file = open(dir_path)
data = [line for line in open(dir_path)]

def getCrash():    
    return int(data[random.randint(0, len(data)-1)].strip())