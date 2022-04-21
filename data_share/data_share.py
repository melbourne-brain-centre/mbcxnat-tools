import xnat as x
import argparse
import sys
from getpass import getpass


def check_projects(session, src_p, dest_p):
    """
        Check if user provided projects are available
    """
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


def main():
    #CLI input
    parser = argparse.ArgumentParser(description="Share subjects and exps between projects on XNAT\nExample usage > python data_share.py -x {server} -u {uname} -s {src_pro} -d {dest_proj}")
    parser.add_argument('-x', '--server', dest='server', help='Xnat server')
    parser.add_argument('-u', '--username', dest='uname', help='Username for MBC XNAT')
    parser.add_argument('-s', '--source', dest='source', help='Source Project ID')
    parser.add_argument('-d', '--dest', dest='dest', help='Destination Project ID')
    args = parser.parse_args()

    # Setting up variables
    server = args.server
    if not server[-1] == "/":
        server = server + "/"
    uname = args.uname
    src_p = args.source
    dest_p = args.dest
    pword = getpass("Enter your XNAT password: ")

    # Generate API URL
    def uri_generator(is_sub, sub_data, exp_data=None):
        """
            Generate API URL for subject or experiments
        """
        if is_sub:
            api_url = f"{server}data/projects/{src_p}/subjects/{sub_data.label}/projects/{dest_p}?label={sub_data.label}"
            return api_url

        if not is_sub:
            api_url = f"{server}data/projects/{src_p}/subjects/{sub_data.label}/experiments/{exp_data.label}/projects/{dest_p}?label={exp_data.label}&primary=true"
            return api_url

    print(f"Connecting to {server} as {uname}")
    with x.connect(server, user=uname, password=pword) as session:
        print(f"Succesfully connected to {server}")
        check_projects(session, src_p, dest_p)

        sub_count, exp_count = 0,0

        src_proj = session.projects[src_p]
        all_subjects = src_proj.subjects

        for each_sub in all_subjects.values():
            all_exps = each_sub.experiments.values()
            api_path_sub = uri_generator(is_sub=True, sub_data=each_sub)
            try:
                session.put(path=api_path_sub)
                print(f"{each_sub.label} : SUBJECT SHARING SUCCESFUL")
                sub_count += 1
            except:
                print(f"{each_sub.label} : SUBJECT SHARING FAILED")
                continue

            for each_exp in all_exps:
                api_path_exp = uri_generator(is_sub=False, sub_data=each_sub, exp_data=each_exp)
                try:
                    session.put(path=api_path_exp)
                    print(f"{each_exp.label} : EXPERIMENT SHARING SUCCESFUL")
                    exp_count += 1
                except:
                    print(f"{each_exp.label} : EXPERIMENT SHARING FAILED")
                    continue

        with x.connect(server, user=uname, password=pword) as session:
            src_proj = session.projects[src_p]
            all_subjects = src_proj.subjects
            for each_sub in all_subjects.values():
                api_path_sub = uri_generator(is_sub=True, sub_data=each_sub)
                api_path_sub = f"{api_path_sub}&primary=true"
                #print(api_path_sub)
                try:
                    session.put(path=api_path_sub)
                    print(f"{each_sub.label} : SUBJECT SHARING SUCCESFUL")
                except Exception as e:
                    print(f"{each_sub.label} : SUBJECT SHARING SUCCESFUL")

        print(f"Subjects shared : {sub_count}\nExperiments shared : {exp_count}")


if __name__ == "__main__":
    main()
