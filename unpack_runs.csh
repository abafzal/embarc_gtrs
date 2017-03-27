#!/bin/csh -f

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
### Unpack runs using dcmunpack. 
### Usage: 'source unpack_runs.csh $subject_id $anat_run $eor1_run'  
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#echo $1
#echo $2
#echo $3

set ROOT_DIR = /space/will/3/users/EMBARC/EMBARC-FAST
set DICOM_DIR = /space/will/3/users/EMBARC/DICOMs
set DATA_DIR = /space/will/4/users/EMBARC/DATA

# Point to user-specified subject. 
set SUBJ = $1
set ANAT_RUN = $2
set EOR1_RUN = $3

echo $SUBJ
if (-d $DICOM_DIR/$SUBJ) then 
    #echo $DICOM_DIR/$SUBJ
    foreach FOLD (`find $DICOM_DIR/$SUBJ -maxdepth 1 -type d -name 'embarc_CU_'{$SUBJ}'**'`)
        echo Unpacking $FOLD
	    pbsubmit -m aafzal -c "dcmunpack -src $FOLD -targ $DATA_DIR/$SUBJ/. -run $ANAT_RUN anat nii {$SUBJ}_mpr00{$ANAT_RUN}.nii -run $EOR1_RUN bold nii {$SUBJ}_bld00{$EOR1_RUN}_rest.nii"
        endif
    end
else
    echo ERROR: Cannot find {$DICOM_DIR}/{$SUBJ} Directory. 
    break
endif 
