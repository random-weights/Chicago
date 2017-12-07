__author__ = 'Lakshmi SaiRam Thubati'
__copyright__ = "Copyright 2017, SIE507"
__version__ = "1.0"
__date__ = "12/06/2017"


import re
import pandas as pd
import matplotlib.pyplot as plt
import os.path

ls_type = []                            # global variable to access in subsequent functions
len_ls_type = 0
raw_fname = "test_data.csv"


def en_code():

    '''
    Extract all unique Crimes and write them to text file
    useful for the purpose of encoding
    '''

    print("------------Encoding in progress.....")

    set_type = set()                #unlike list, set will hold only unique values.
    count = 0

    with open(raw_fname) as fh:
        for line in fh:
            count += 1
            line = line.replace("\n",'')
            ls_line = line.split(',')
            print("\r Processing: ".format(count)+str(count),end = '')
            if len(ls_line) != 23:
                pass
            else:
                set_type.add(ls_line[5])

    #update the global variables, this new values will be used by subsequent programs
    global ls_type
    global len_ls_type
    ls_type = list(set_type)
    len_ls_type = len(ls_type)

    #write all unique crime_types to a text file.
    file_type = open('crime_type.txt','a')
    for item in ls_type:
        print(item,file = file_type)
    file_type.close()

    print("\n -----------Encoding finished!! Unique crimes identified: {0}".format(len(ls_type)))


def compress():
    # compressed and filtered data will be written to this file
    file_compressed = open('crimes_compressed.csv','a')

    print("\n ----------Compressing the original File....")

    count = 0
    # used to extract only date. In the raw csv date and time are mixed together
    reg_exp = re.compile(r'\d{2}/\d{2}/\d{4}')

    with open(raw_fname) as fh:
        for line in fh:
            count += 1
            line = line.replace("\n", '')
            ls_line = line.split(',')
            print("\r Processing: ".format(count) + str(count), end='')

            if len(ls_line) != 23:
                # because some lines in csv file are corrupt and not in proper format
                pass

            else:
                #extracting only date
                result = reg_exp.search(ls_line[2])
                date_str = result.group()

                #the index of string in ls_type list is taken as encoded value
                en_value = ls_type.index(ls_line[5])

                print(ls_line[0]+','+date_str+','+str(en_value)+','+ls_line[19]+','+ls_line[20],file =file_compressed)

    file_compressed.close()
    print("\n ----------Compression done. New file created")


def splits():
    """
    This program creates 32 different files. Each file contains data about particular crime

    """

    print("\n ----------Splitting compressed file to many files.....")

    # No. of files = no.of distinct crimes = length of ls_type list
    save_path = 'split_files/'                                      ## creating split files in another folder to avoid clutter
    ls_fname = [os.path.join(save_path)+str(i)+'.csv' for i in range(0,len_ls_type)]

    # Create file handlers to all files and keep them open
    ls_fhandler = [open(fname,'a') for fname in ls_fname ]

    count = 0

    # iterate through compressed crimes and seperate lines into individual files based on crime type
    with open('crimes_compressed.csv') as fh:
        for line in fh:
            line = line.replace('\n','')                            ## replace new line char with empty
            ls_line = line.split(',')                               ## split line into a list
            fh_index = int(ls_line[2])                              ## since same encoding rule is enforced.
            print(line,file = ls_fhandler[fh_index])                ## write line to designated file
            count += 1
            print("\r Finished: ".format(count)+str(count),end = '')

    #close all open file handlers
    for fh in ls_fhandler:
        fh.close()

    print("\n ----------Splitting finished. {0} seperate files created".format(len(ls_fname)))


def main():

    en_code()

    compress()

    splits()

    print("\n----------Plotting and saving Images.")

    fname = 'crimes_compressed.csv'

    #import compressed csv into pandas dataframe
    df = pd.read_csv(fname, sep=',', header=None)

    #give names to columns
    df.columns = ['ID', 'DATE', 'PTYPE', "LAT", "LON"]

    #convert string in date column to a datetime object
    df.DATE = pd.to_datetime(df.DATE)

    df2 = df[['DATE', 'PTYPE']]                 # we are taking only date and type of crime. Plotting on a map will be done in arcgis
    df2.set_index('DATE', inplace=True)         # set date as index to each row
    df2 = df2.sort_index(ascending=True)        # sort the whole data frame based on date.

    #initializing plot parameters
    plt.figure(figsize=(12, 7))
    plt.ylabel("No. of Crimes")
    plt.xlabel("Year-month")

    # for loop is to plot for different type of crimes separately
    for i in range(len_ls_type):
        month_crimes = df2[df2.PTYPE == i].resample("M").count()  # Aggregate based on month
        month_crimes["2001":"2014"]["PTYPE"].plot()
        plt.savefig(os.path.join('plots/')+ls_type[i]+".png", bbox_inches='tight')
        plt.gcf().clear()


main()