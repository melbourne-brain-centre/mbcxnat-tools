# ADD prefix to subjects while sharing data ot the QC project

import xnat
import argparse
import sys
from getpass import getpass
def check_projects(session, src_p, dest_p):
    try:
        temp = session.projects[src_p]
        print(f"Source project : {src_p} available!")
    except:
        print(f"Source project : {src_p} not found!\nTry again.")
        sys.exit()
    try:
        temp = session.projects[dest_p]
        print(f"Destination project : {dest_p} available!")
    except:
        print(f"Destination project : {dest_p} not found!\nTry again.")
        sys.exit()
if __name__ == '__main__':
    # CLI Input
    parser = argparse.ArgumentParser(description="Share subjects and experiment with prefix")
    parser.add_argument('-x', '--server', dest='server', help='Xnat server')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-s', '--source', dest='source', help='Source Project ID')
    parser.add_argument('-d', '--dest', dest='dest', help='Destination Project ID')
    parser.add_argument('-p', '--prefix', dest='prefix', help='Prefix')
    args = parser.parse_args()
    server = args.server
    if not server[-1] == "/":
        server = server + "/"
    uname = args.uname
    src_p = args.source
    dest_p = args.dest
    prefix = args.prefix
    pword = getpass("Enter your XNAT password: ")
    with xnat.connect(server, user=uname, password=pword) as session:
        check_projects(session, src_p, dest_p)
        src_project = session.projects[src_p]
        for each_sub in src_project.subjects.values():
            pid = None
            for each_exp in each_sub.experiments.values():
                for scan in each_exp.scans.values():
                    ds = scan.dicom_dump()
                    for tag in ds:
                        if tag['tag1'] == '(0010,0020)': pid = tag['value']
                    if pid != None: break
                if pid != None: break
            print()
            
            print(f'Sharing from {src_p} to {dest_p}')
            if pid == each_sub.label: subject = f'{prefix}_{each_sub.label}'
            else: subject = pid
            try:
                session.put(path=f'{server}data/projects/{src_p}/subjects/{each_sub.label}/projects/{dest_p}?label={subject}')
                print(f'Subject Sharing Successful. {each_sub.label} --> {subject}')
            except:
                print(f'Subject Sharing Failed!')
            for each_exp in each_sub.experiments.values():
                try:
                    session.put(path=f'{server}data/projects/{src_p}/subjects/{each_sub.label}/experiments/{each_exp.label}/projects/{dest_p}?label={each_exp.label}&primary=true')
                    print(f'Experiment {each_exp.label} permantly moved.')
                except:
                    print(f'Experiment {each_exp.label} sharing failed')
            try:
                session.put(path=f'{server}data/projects/{src_p}/subjects/{each_sub.label}/projects/{dest_p}?label={subject}&primary=true')
                print(f'Subject permantly moved. {each_sub.label} --> {subject}')
            except:
                print(f'Subject permantly moved. {each_sub.label} --> {subject}')
