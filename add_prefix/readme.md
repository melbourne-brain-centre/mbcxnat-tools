The script is a Python program that uses the xnat package to interact with an XNAT server. The script takes 5 command-line arguments:
    -x : The XNAT server
    -u : The XNAT username
    -s : The XNAT source project
    -d : The XNAT destination project
    -p : Prefered prefix to be added/removed while moving XNAT subjects
And it asks for the password in the CLI prompt.
Step 1: After successfull authentication, the script ckecks if both the source and destination projects are available or not. If one of them is not available, the program exits.
Step 2: Originally, the DICOM PatientID is taken as XNAT subject. The program loops through each subjects and reads the DICOM PatientID from 1st scan of the subject.
Step 3: The program shares each subject from the source project to the destination. In this step, if the XNAT subject is same as its DICOM PatientID, we can say that prefix is not added to the XNAT subject label previously. Hence the program changes the XNAT subject label to prefix_PatientID for destination project; in this case PatientID is same as the original XNAT subject label.
If the XNAT subject label doesn't match to its DICOM PatientID, we can say that a prefix is already added to the XNAT subject label previously. Hence, while sharing, the program changes the XNAT subject label to its DICOM PatientID for destination project, as the DICOM PatientID is same as the original XNAT subject label. Hence it resembles as removing the prefix from the XNAT subject label
Step 4: Then the program loops through each XNAT experiment of each XNAT subjects and permanently moves the experiment to its corresponding subject of the destination project.
Step 5: Since a XNAT subject can be permanently moved after all its experiments are moved, the program then permanently moves the XNAT subject from the source project to the destination project, with same labeling rule as mentioned in the Step 3.