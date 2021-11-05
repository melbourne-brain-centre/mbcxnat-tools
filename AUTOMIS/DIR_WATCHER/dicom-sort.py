'''
    - Sort DICOM studies based on 'PatientName', 'PatientID', 'Modality'
    - Rewritten in python 3 using pydicom by @brokaha
'''


def replace_oddities(text):
    '''
        replace characrers that match a key in a dict with the associated value
        return the changed text
    '''
    rep_dic = {
        '      ': '_',
        '   ': '_',
        ' ': '_',
        '^': '_',
        '/': '_',
        '__': '_',
        '  ': '_',
        '\\': '_',
        '*': '',
        ':': '',
        ',': '',
        ';': '',
        ']': '',
        '[': '',
        '(': '',
        ')': ''
    }
    rc = re.compile('|'.join(map(re.escape, rep_dic)))

    def translate(match):
        return rep_dic[match.group(0)]

    return rc.sub(translate, text)


def start_sort(input_file,targetdir,file,order_list):
    '''
        - take input_file, targetdir and order of sorting
        - place nondicom files in a seperate directory
        - make corrections to string names where necessary
        - create a directory position and file names
        - copy to required destination
    '''
    global dupfiles
    # Tag and argument lists for making sort order 
    tag_list = ['PatientName', 'PatientID', 'Modality','StudyDate' ,'StudyTime', 'SeriesNumber', 'SeriesDescription', 'InstanceNumber', 'InstitutionName', 'SeriesInstanceUID','SliceThickness']
    tag_arg = []

    # Check if dicom file
    try:
        ds = pydicom.read_file(input_file)
    except Exception as e:
        # If not dicom file then move to nondicom directory
        print(f"NOT dicom file : {input_file}")
        nondicom = f'{targetdir}/nondicom'
        if not os.path.exists(nondicom):
            os.mkdir(nondicom)
        if not os.path.isfile(f'{nondicom}/{file}'):
            shutil.copyfile(input_file, f'{nondicom}/{file}')
        print(f'PATH : {nondicom}/{file}')
        return

    # Making corrections to required strings
    # Removing unwanted wildcard characrers
    try:
        patName = str(ds.PatientName)
        patName = patName.replace(" ", "_")
        patName = patName.replace("^", "_")
    except:
        patName = 'NA_PName'

    try:
        patId = str(ds.PatientID)
        patId = patId.replace(" ", "_")
        patId = patId.replace("^", "_")
    except:
        patId = 'NA_PID'

    try:
        seriesName = str(ds.SeriesDescription)
        seriesName = replace_oddities(seriesName)
    except:
        seriesName = "NASeriesDescription"

    try:
        instNumber = ds.InstanceNumber
    except:
        instNumber = "NA_IN"

    # Creating argument order list
    try:
        for i in range(len(tag_list)):
            try:
                tag_arg.append((getattr(ds, tag_list[i])))
            except:
                tag_arg.append('NA')
    except Exception as e:
            print(e)
    
    # making a dict zipping tag list and args
    file_info = dict(zip(tag_list, tag_arg))
    
    # creating path for according to the sorting order
    order_level = ''
    for i in order_list:
        if i == 'PatientName':
            order_level += f'{patName}/'
            continue
        if i == 'PatientID':
            order_level += f'{patId}/'
            continue
        order_level += f'{file_info[i]}/'
    
    # Creating file name and directory path
    file_name = f'{patName}_{patId}_{file_info["Modality"]}_{str(file_info["StudyDate"])}T{str(file_info["StudyTime"])}_{str(file_info["SeriesNumber"])}_{str(file_info["SeriesInstanceUID"])}_{str(file_info["InstanceNumber"])}'
    folder_position = f'{targetdir}/{order_level}{str(file_info["StudyDate"])}T{str(file_info["StudyTime"])}/{str(file_info["SeriesNumber"])}_{seriesName}/'

    # Making the directory if absent
    if not os.path.exists(folder_position):
        os.makedirs(folder_position)

    # Placing files in the desired destination directory
    if not os.path.isfile(f'{folder_position}/{file_name}'):
        ds.save_as(f'{folder_position}/{file_name}')
        # Verbose output
        print(f'******************* SUCCESS *******************\nORDER : {order_level}\nINPUT : {input_file}\nDESTINATION : {folder_position}\n')
    
    """
    else:
        # handelling duplicate files
        print("Duplicate......")
       
        d_fname = str(file_name+'~')
        if os.path.isfile(f'{folder_position}/{d_fname}'):
            d_fname += str(int_list[0])
            int_list.pop(0)
        ds.save_as(f'{folder_position}/{d_fname}')
        print(f'******************* DUPLICATE *******************\nORDER : {order_level}\nINPUT : {d_fname}\nDESTINATION : {folder_position}\n')
        dupfiles += 1
    """


def main():
    '''
        - get required input form the user
        - setup required variables
        - initiate the sort process
    '''

    # Global for duplicates
    global int_list, dupfiles
    dupfiles = 0

    # Parser Arguments
    # Getting input form user throuch CLI
    parser = argparse.ArgumentParser(description='example usage: python py3_sort.py -s ./foo -t ./bar -o im')
    parser.add_argument('-s', '--source', dest='source', help='source data')
    parser.add_argument('-t', '--target', dest='target',
                        help='target destination')
    parser.add_argument('-o', '--sort order', dest="order",
                        help='i> PatientID ,n> PatientName ,m> Modality')
    args = parser.parse_args()

    # Check in source dir exists
    if not os.path.exists(args.source):
        sys.exit(f"Source dir {args.source} doesnot exist!")

    # pretty variables
    sourcedir = args.source
    targetdir = args.target

    # Making the order list for sorting process
    order_list_dic = {'i': 'PatientID', 'n': 'PatientName', 'm': 'Modality'}
    order_list = []
    for letter in args.order.lower():
        if letter in order_list_dic:
            order_list.append(order_list_dic[letter])

    # Test Print
    print(f'SOURCE_DIR : {sourcedir}\nTARGET_DIR : {targetdir}\nORDER : {order_list}')

    # Start the sorting process for every file in source dir
    # Count total files in sourcedir
    sfcount, dfcount = 0, 0
    for root, dirs, files in os.walk(sourcedir):
        int_list = [x for x in range(1,10000)]
        sfcount += len(files)
        for each in files:
            start_sort(os.path.join(root, each),targetdir,each,order_list)

    # Counting total files in targetdir
    for root, dirs, files in os.walk(targetdir):
        dfcount += len(files)
    
    # Total duplicate files
    print(f'Total Duplicate files : {dupfiles}')

    # sanity check to verify no change in I/O file number
    print(f'Total input files : {sfcount}\nTotal output files : {dfcount}\nDiffrence = {abs(sfcount - dfcount)}')


if __name__ == '__main__':
    # Import necessary libraries
    try:
        import sys # access system
        import os # access filesystem
        import re # regular expressions
        import argparse # argument parser CLI
        import shutil # copy and move file
        import pydicom # DICOM library

    except ImportError as e:
        print('Libraries missing')
        print(e)
        sys.exit()

    except Exception as e:
        print("Libraries are present. Other Error")
        print(e)
        sys.exit()
    # Script entry point
    main()
