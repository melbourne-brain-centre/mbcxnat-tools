'''
Custom subject archive from a mapping table and deidentification for MBC XNAT

STEPS:
    1. Upload studies to XNAT using storescu or DQR plugin.
    2. Create a mapping file eg. format 
        PROJECT_001,46852
        PROJECT_002,95142
    2. Select the correct project for required studies.
    3. Run the script : eg : python mbc-deident-up.py -t {mapping_file_path} -u {username} 
       If table not required : python mbc-deident-up.py -u {username}
       If table is not provided patientid will be used to create subjects
    4. Enter your password
TODO:
    1. Select project directly form the script
        error while changing project, 1.8.2.2 not yet supported natively
    
'''

import xnat as x
import os
import argparse
import pydicom
import random
from getpass import getpass


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
    parser = argparse.ArgumentParser(description='Archive and Deident MBC XNAT\nIf there is no table dont put any arguments')
    parser.add_argument('-t', '--table', dest='tname', default=None, help='Mapping table')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    # parser.add_argument('-p', '--password', dest='pword', help='Password')
    args = parser.parse_args()

    # setting up variables
    dic = {}
    table = args.tname
    uname = args.uname
    
    #pword =  getpass("Enter your XNAT password: ")
    pword = "MBCrmh2020#"
    xnat_site = 'https://dev-xnat.thembc.com.au'
    

    # Create a dictionary for subject mapping
    if table:
        print("yes")
        dic = create_table(table)
    
    print(f"Connecting to {xnat_site} as {uname}")
    # Connect with xnat instance
    with x.connect(xnat_site, user=uname, password=pword) as session:
        print(f"Succesfully connected to {xnat_site}")
        # Select all sessions in prearchive
        prearc = session.prearchive.sessions()
        for eachp in prearc:
            work_subject = eachp.subject
            print(f"Now Archiving {work_subject}")
            # Getting dicom tags
            scan = eachp.scans
            for sd in scan:
                ds = sd.read_dicom()
                studytime, sep, tail = (ds.StudyTime).partition('.')
                modality = ds.Modality
                label = f'{ds.StudyDate}T{studytime}_{modality}'
                break
            
            # Archiving 
            try:
                if table:
                    subject_name = dic[work_subject]
                else:
                    subject_name = work_subject
                # nr = random.randint(0, 99)
                exp_name = f'{subject_name}_{label}'
                print(f'Study ID : {work_subject}: Subject Name : {subject_name} / Session Name : {exp_name}')
                eachp.archive(subject=subject_name, experiment=exp_name, overwrite="append")
            except Exception as E:
                # print(E)
                # It always throws an exception msg even when archiving is sucesful
                # Be aware and always check for issues on the prearchive page
                # In case of errors click on details for theat particular case to get more info 
                print("Subject Archived")


if __name__ == "__main__":
    main()
