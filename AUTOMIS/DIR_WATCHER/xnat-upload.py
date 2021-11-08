'''
Custom subject archive and deidentification for MBC XNAT
'''

import xnat as x
import os
import argparse
import pydicom
import random


def main():
    '''
        - Get input form user through cli
        - make a dictionary form table
        - connect to xnat instance
        - upload to prearchive
        - archive using appropriate labels
    '''

    #CLI input
    parser = argparse.ArgumentParser(description='Archive and Deident MBC XNAT')
    parser.add_argument('-x', '--xnat', dest='xnat', help='XNAT')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-p', '--password', dest='pword', help='Password')
    parser.add_argument('-s', '--zip', dest='zipp', help='Zipp file')
    args = parser.parse_args()

    # setting up variables
    uname = args.uname
    pword = args.pword
    source_z = args.zipp
    server = args.xnat

    # Connect with xnat instance
    with x.connect(server, user=uname, password=pword) as session:
        # Upload to prearchive
        print("Uploading to prearchive")
        session.services.import_(source_z, project='TP_MXBAT', destination='/prearchive')
        # Select all sessions in prearchive
        prearc = session.prearchive.sessions()
        for eachp in prearc:
            work_subject = eachp.subject
            print(f"Now Archiving {work_subject}")
            scan = eachp.scans
            # Get date and time from each session
            for sd in scan:
                ds = sd.read_dicom()
                studytime, sep, tail = (ds.StudyTime).partition('.')
                label = f'{ds.StudyDate}T{studytime}'
                # print(label)
                break

            # Archive each session with appropriate subject label 
            try:
                nr = random.randint(0, 99)
                exp_name = f'{work_subject}_{label}_{nr}'
                print(f'Study ID : {work_subject}: Subject Name : {work_subject} / Session Name : {exp_name}')
                eachp.archive(subject=work_subject, experiment=exp_name)
            except:
                print("Subject not present in Table")


if __name__ == "__main__":
    main()
