import redcap

def main():
    """
     This script dumps all data from a project to a csv file
    """
    api_key = "FB93AC90D673406ACFCD35F39075E7F1"
    api_url = "https://test-mbctrials.unimelb.edu.au/api/"
    project = redcap.Project(api_url, api_key)
    data_dump = project.export_records(format='df')
    data_dump.to_csv('form_redcap.csv',index=True)

if __name__ == '__main__':
    main()
