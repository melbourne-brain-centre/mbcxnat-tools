'''
Custom subject archive from a mapping table and deidentification for MBC XNAT

STEPS:
    1. Upload studies to XNAT using storescu or DQR plugin.
    2. Create a mapping file eg. format 
        PROJECT_001,46852
        PROJECT_002,95142
    2. Select the correct project for required studies.
    3. Run the script : eg : python mbc-deident-up.py -t {mapping_file_path} -u {username} -p {password}

TODO:
    1. Select project directly form the script
        error while changing project, 1.8.2.2 not yet supported natively
'''

import xnat as x
import os
import random
import argparse


def create_table(table):
    # Create mapping dictionary from a text file
    mapdic = {}
    with open(table, 'r') as transt_file:
        for line in transt_file:
            tup = line.strip('\n').strip(',').split(',')
            for i in range(len(tup)-1):
                mapdic[tup[i+1]] = tup[0]

    return mapdic


def main():
    '''
        - Get input form user through cli
        - make a dictionary form table
        - connect to xnat instance
        - archive studies based on uid from mapping table
    '''

    #CLI input
    parser = argparse.ArgumentParser(description='Archive and Deident MBC XNAT')
    parser.add_argument('-t', '--table', dest='tname', help='Mapping table')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-p', '--password', dest='pword', help='Password')
    args = parser.parse_args()

    # setting up variables
    dic = {}
    table = args.tname
    uname = args.uname
    pword = args.pword

    # Create a dictionary for subject mapping
    dic = create_table(table)

    # Connect with xnat instance
    with x.connect('https://xnat.thembc.com.au', user=uname, password=pword) as session:
        # Create a new name for subject and experiment
        prearc = session.prearchive.sessions()
        for pas in prearc:
            print(pas)
            work_subject = pas.subject
            try:
                subject_name = dic[work_subject]
                nr = random.randint(0, 99)
                exp_name = f'{subject_name}_{nr}'
                print(f'Study ID : {work_subject}: Subject Name : {subject_name} / Session Name : {exp_name}')
                pas.archive(subject=subject_name, experiment=exp_name)
            except:
                print("Subject not present in Table")


if __name__ == "__main__":
    main()