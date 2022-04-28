'''
@birendra
Change project of xnat sessions form prearchive
'''
import xnat as x
import os
import sys
import argparse
from getpass import getpass


def check_projects(session, new_proj):
    # Check if user provided project is available
    try:
        temp = session.projects[new_proj]
        print(f"Source project : {new_proj} available!")
    except:
        print(f"Source project : {new_proj} not found!\nTry again.")
        print(f"Only these projects available to current user are:")
        for i, each in enumerate(session.projects):
            print(f"\t{i+1}. {each}")
        print(f"Select one of them.")
        sys.exit()


def connect_xnat(xnat_site,uname,pword,new_proj):
    # Connect with xnat instance
    with x.connect(xnat_site, user=uname, password=pword) as session:
        check_projects(session, new_proj)
        transfer_success, transfer_fail = 0,0
        print(f"Succesfully connected to {xnat_site}")
        # Select all sessions in prearchive
        prearc = session.prearchive.sessions()

        # Check if there are prearchive sessions
        if len(prearc) == 0:
            print("No sessions in prearchive.\nCheck again")
            sys.exit()

        # Loop through prearchive
        for eachp in prearc:
            work_subject = eachp.subject
            print(f"Working on {work_subject}")

            # Generate URL links
            org_link = eachp.external_uri()
            temp = org_link.split("/")[4:]
            pre_arc_src = f"/{('/').join(temp)}"

            # Send the  POST request
            try:
                session.post(path=f"{xnat_site}data/services/prearchive/move", data={"src":pre_arc_src,"newProject":new_proj})
                print(f"Moved : {work_subject} to project : {new_proj}")
                transfer_success += 1
            except:
                print("Project move failed!")
                transfer_fail += 1
                continue

        return transfer_success, transfer_fail


def main():
    '''
        - Get input form user through cli
        - connect to xnat instance
        - change projects
    '''

    #CLI input
    parser = argparse.ArgumentParser(description='Change project in prearchive -t\nExample usage: python change_project_in_prearchive.py -p {proj} -u {uname} -s {server_url}')
    parser.add_argument('-p', '--project', dest='nproj', help='Destination project')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-s', '--server', dest='xnat_server', help='Server URL')
    args = parser.parse_args()

    # setting up variables
    new_proj = args.nproj
    uname = args.uname
    
    pword =  getpass("Enter your XNAT password: ")
    xnat_site = args.xnat_server

    # Url format check
    if not xnat_site[-1] == "/":
        xnat_site = xnat_site + "/"
    
    # Conect to xnat server
    print(f"Connecting to {xnat_site} as {uname}")
    ts, tf = connect_xnat(xnat_site,uname,pword,new_proj)
    print(f"Transfer Success : {ts}\nTransfer Fail : {tf}")

          
if __name__ == "__main__":
    main()
