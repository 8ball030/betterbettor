# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:18:57 2018

@author: Tom
"""

    

import requests
import json
import time


base_url = 'https://www.ethcrash.io/game/'



for x in range (22202, 100000):
    try:
        y = str(json.loads(requests.get(base_url+str(x+2)+'.json').content)['game_crash']    )
    except:
        print("wait boi")
        time.sleep(20)
    fd = open('crash_data.csv','a')
    fd.write(y+'\n')
    fd.close()
    time.sleep(1)