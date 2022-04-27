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
        Work around can be written. Can be done by sending POST request
    
'''

import xnat as x
import os
import argparse
import pydicom
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
    parser = argparse.ArgumentParser(description='Archive and Deident MBC XNAT\nIf there is no table dont put -t\nExample usage python mbc-deident-up.py -p {proj} -u {uname} -s {server_url}')
    parser.add_argument('-p', '--project', dest='nproj', default=None, help='new proj')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-s', '--server', dest='xnat_server', help='Server URL')
    args = parser.parse_args()

    # setting up variables
    new_proj = args.nproj
    uname = args.uname
    
    pword =  getpass("Enter your XNAT password: ")
    xnat_site = args.xnat_server

    if not xnat_site[-1] == "/":
        xnat_site = xnat_site + "/"

    
    print(f"Connecting to {xnat_site} as {uname}")
    # Connect with xnat instance
    with x.connect(xnat_site, user=uname, password=pword) as session:
        print(f"Succesfully connected to {xnat_site}")
        # Select all sessions in prearchive
        prearc = session.prearchive.sessions()
        for eachp in prearc:
            work_subject = eachp.subject
            print(f"Working on {work_subject}")
            org_link = eachp.external_uri()
            temp = org_link.split("/")[4:]
            pre_arc_src = f"/{('/').join(temp)}"
            try:
                session.post(path=f"{xnat_site}data/services/prearchive/move", data={"src":pre_arc_src,"newProject":new_proj})
                print(f"Moved : {work_subject} to project : {new_proj}")
            except:
                print("Project move failed!")
                continue
          
if __name__ == "__main__":
    main()
