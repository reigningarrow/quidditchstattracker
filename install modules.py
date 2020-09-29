# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:52:00 2020

@author: Sam
"""


import subprocess
import sys
import time
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    
modules=['pandas','numpy','tkinter','scipy','matplotlib','os','time','jinja2','openpyxl']
for module in modules:
    try:
        install(module)
    except:
        print(f'Can\'t install {module}')
    time.sleep(1)
