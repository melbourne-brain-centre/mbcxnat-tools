# mbcxnat-tools
Tools developed by MBC for XNAT administration 
*WORK IN PROGRESS*
---
### deident-up
Archive and deidentify data from xnat prearchive while generating formatted experiment labels.

Setup in XNAT
- Enable custom Dicom routing for Subject to `(0010,0020):(.*)` and Session to `(0010,0010):(.*)`
- Use the Xnat Anonymization script provided in deident-up/xnat_annon in the required project.
- Change the project for required subjects from the prearchive menu
- Uploading user must have required privileges for archiving data

Usage
- `python mbc-deident-up.py -u {xnat_username} -s {server_url} -t {mapping_table}`
- Only provide the -t tag if you want to change the id of the subject. A mapping table needs to be created which links the current uid to the required uid. A sample is provided on deident-up/sample_table.txt
- The subject will then be archived and the experiments will have the following label pattern: sub_name+studydate+studytime+modality ie XNATSUB001_20200101T123000_MR

## custom-variable-up
Upload data to XNAT custom variables.

Setup in XNAT
- Create all the fiels that are present in the spreadsheet
- The fields name must match exactly in xnat and spreadsheet

Usage
- `python variable-up.py -f {csv file path} -u {xnat-user} -s {server-url}` 

## redcap2xnat 
- dump variables form REDCap and upload to XNAT subjects. *initial commit*


## Transfer ownership
Transfer ownership of all subjects and experiments between projects

Usage
- `python transfer_ownership.py  -x {SITE_URL} -u {USER_NAME} -s {SOURCE_PROJ_ID} -d {DEST_PROJ_ID}`
- Still in the testing phase. Only use temporary/dumb data.

## ADD prefix
Add prefix to subjects while transfering data between the QC and main projects
