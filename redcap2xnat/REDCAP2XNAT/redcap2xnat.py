import xnat as x
import numpy as np
import pandas as pd
import redcap as red
import config
from getpass import getpass


def get_redcap_data(api_key, api_url):
    project = red.Project(api_url, api_key)
    return project.export_records(format='df')

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
    #Setting up variables
    api_key = config.API_KEY
    api_url = config.API_URL

    x_proj = config.XNAT_PROJ
    x_uname = config.XNAT_UNAME
    x_website = config.XNAT_SERVER
    table = config.TABLE
    
    x_pwd = pword =  getpass("Enter your XNAT password: ")

    # get data form redcap
    print("Connecting to REDCap")
    df = get_redcap_data(api_key, api_url)
    print("Data succesfully obtained from REDCap")
    # create table
    dic = create_table(table)
    
    # setting up dataframe
    print("Setting up dataframe")
    df["index"] = df.index.astype(str)
    def pandas_func(temp_var):
        return dic[temp_var]
    df["index"] = df["index"].apply(pandas_func)
    df.set_index("index",inplace=True)

    variables =  list(df.columns)
    
    print(f"Connecting to xnat as {x_uname}")
    with x.connect(x_website, user=x_uname, password=x_pwd) as session:
        print("Succesfully connected to XNAT")
        print(f"Working on {x_proj} project")
        # List out projects and let user select
        all_projects = session.projects
        xnat_project = session.projects[x_proj]

        # Loop each subject in the project
        for case in xnat_project.subjects.values():
            print(case)

            # Loop over and assign values from csv to required custom variable
            to_find = case.label
            for cvar in variables:
                case.fields[cvar] = df.loc[to_find,[cvar]]
            print(case.fields)
    

if __name__ == "__main__":
    main()
