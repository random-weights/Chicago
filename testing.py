__author__ = 'Lakshmi SaiRam Thubati'
__copyright__ = "Copyright 2017, SIE507"
__version__ = "1.0"
__date__ = "12/06/2017"

'''
This file is used to generate random test data from original raw csv.
Do not run if you don't have original raw CSV
'''

import pandas as pd

def main():

    test_size = 5000
    fname = 'Crimes.csv'

    df = pd.read_csv(fname,nrows=test_size)
    df.to_csv("test_data.csv",header=None,index=False)

main()