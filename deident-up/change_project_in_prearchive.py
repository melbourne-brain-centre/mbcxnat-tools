'''
@birendra
Change project of xnat sessions form prearchive
'''

import xnat as x
import os
import argparse
from getpass import getpass

def connect_xnat(xnat_site,uname,pword,new_proj):
    # Connect with xnat instance
    with x.connect(xnat_site, user=uname, password=pword) as session:
        transfer_success, transfer_fail = 0,0
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
    parser = argparse.ArgumentParser(description='Change project in prearchive -t\nExample usage python mbc-deident-up.py -p {proj} -u {uname} -s {server_url}')
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
    ts, tf = connect_xnat(xnat_site,uname,pword,new_proj)
    print(f"Transfer Success : {ts}\nTransfer Fail : {tf}")

          
if __name__ == "__main__":
    main()
