'''
Custom subject archive from a mapping table and deidentification for MBC XNAT
'''

import xnat as x
import os
import sys
import random
import argparse


def create_table(table):
    # Create mapping dictionary
    mapdic = {}
    with open(table, 'r') as transt_file:
        for line in transt_file:
            tup = line.strip('\n').strip(',').split(',')
            for i in range(len(tup)-1):
                mapdic[tup[i+1]] = tup[0]

    return mapdic


def main():
    #CLI input
    parser = argparse.ArgumentParser(description='Archive and Deident MBC XNAT')
    parser.add_argument('-t', '--table', dest='tname', help='Mapping table')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-p', '--password', dest='pword', help='Password')
    args = parser.parse_args()

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
