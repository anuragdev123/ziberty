# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 08:45:42 2021

@author: Nick.P
"""

from pycel import ExcelCompiler
import pickle

excel = ExcelCompiler('zibertyAlgorithm.xlsx')
print(excel.evaluate('Attributes Inputs and Outputs!C3'))

with open('pickledAlgorithmAttributes', 'wb') as f:
    pickle.dump(excel, f)

#########################################################
excel = ExcelCompiler('zibertyAlgorithm.xlsx')
print(excel.evaluate('Packages Inputs and Outputs!K3'))

with open('pickledAlgorithmPackages', 'wb') as f:
    pickle.dump(excel, f)