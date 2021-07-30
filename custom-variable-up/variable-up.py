'''
Add custom variables to XNAT subjects from a csv file 

STEPS:
    1. Make sure custom variables are set up properly through front-end or xml file
    2. CSV file must contain dident-id in the first column named 'subject'
    3. All variable names must match with csv column names 
    4. eg : python variable-up.py -f {csv_file_path} -u {username} -p {password}

TODO:
    1. Add dynamic dynamic variable selection and project selection
    2. Merge with redcap form completly autimatic workflow
'''

import xnat as x
import pandas as pd 
import argparse


def main():
    '''
        - Get input form user through cli
        - make a dictionary form table
        - connect to xnat instance
        - archive studies based on uid from mapping table
    '''

    #CLI input
    parser = argparse.ArgumentParser(description='Archive and Deident MBC XNAT')
    parser.add_argument('-f', '--csv_file', dest='cfile', help='CSV file')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-p', '--password', dest='pword', help='Password')
    args = parser.parse_args()

    # setting up variables
    csv_file = args.cfile
    uname = args.uname
    pword = args.pword

    # reading the csv file and cleaning up
    df = pd.read_csv(csv_file)
    df.columns = [x.lower() for x in df.columns]
    df.set_index(keys='Subject', inplace=True)


    # Connect with xnat instance
    with x.connect('https://xnat.thembc.com.au', user= uname, password= pword) as session:
        xnat_project = session.projects['XNAT_DTEST']
        for case in xnat_project.subjects.values():
            print(case)
            to_find = case.label
            case.fields['volume'] = df.loc[to_find,['volume']]
            case.fields['ara_scale'] = df.loc[to_find,['ara_scale']]
            case.fields['nra_scale'] = df.loc[to_find,['nra_scale']]
            case.fields['qc_check'] = df.loc[to_find,['qc_check']]
            print(case.fields)


if __name__ == "__main__":
    main()