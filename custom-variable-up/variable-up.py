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
import numpy as np
import pandas as pd 
import argparse
from getpass import getpass

def get_user_project(all_projects):
    '''
        Let user select the project form a list of all projects
    '''
    proj_list = []
    for proj in all_projects:
        proj_list.append(proj)
        print(proj)
    
    user_input = ''
    while user_input not in proj_list:
        user_input = input('Select the correct project : ').upper()
        
    print(f'Selected project : {user_input}')
    return user_input


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
    parser.add_argument('-s', '--xnat_server', dest='x_serv', help='XNAT URL')
    args = parser.parse_args()

    # setting up variables
    csv_file = args.cfile
    xnat_server = args.x_serv
    uname = args.uname
    pword = getpass("Enter your XNAT password: ")

    # reading the csv file and cleaning up
    df = pd.read_csv(csv_file)
    df.columns = [x.lower() for x in df.columns]
    df.set_index(keys='subject', inplace=True)
    variables =  list(df.columns)

    # Connect with xnat instance
    with x.connect(xnat_server, user=uname, password=pword) as session:
        # List out projects and let user select
        all_projects = session.projects
        user_project = get_user_project(all_projects)
        xnat_project = session.projects[user_project]

        # Loop each subject in the project
        for case in xnat_project.subjects.values():
            print(case)

            # Loop over and assign values from csv to required custom variable
            to_find = case.label
            for cvar in variables:
                case.fields[cvar] = df.loc[to_find,[cvar]]


if __name__ == "__main__":
    main()
