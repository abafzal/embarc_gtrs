#!/bin/csh -f

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
### Submit Recons for EMBARC Subjects. 
### Usage: 'source recons_submit.csh $subject_id' 
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
## Define paths/variables.
setenv SUBJECTS_DIR /space/will/3/users/EMBARC/Recons
set DICOM_DIR = /space/will/3/users/EMBARC/DICOMs
set DATA_DIR = /space/will/4/users/EMBARC/DATA

set USER = aafzal

# Read Subject ID from user input. 
set SUBJECT = $1

# Find MEMPRAGE
foreach MEMPRAGE (`find $DATA_DIR/$SUBJECT/anat -maxdepth 2 -name $SUBJECT'_mpr**.nii.gz' | cut -d" " -f1`)
    echo $MEMPRAGE
    
    # Organize files.
    #pbsubmit -m $USER -c "recon-all -i $MEMPRAGE -subjid $SUBJECT"

    # Submit job.
    pbsubmit -m $USER -c "recon-all -all -subjid $SUBJECT"

    break
end
