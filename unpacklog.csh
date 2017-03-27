#!/bin/csh -f

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
### Create unpacklogs for EMBARC Subjects. 
### Usage: 'source unpacklog.csh $subject_id' 
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

set ROOT_DIR = /space/will/3/users/EMBARC/EMBARC-FAST
set DICOM_DIR = /space/will/3/users/EMBARC/DICOMs

# Point to user-specified subject. 
set SUBJ = $1

echo $SUBJ
if (-d $DICOM_DIR/$SUBJ) then 
    #echo $DICOM_DIR/$SUBJ
    foreach FOLD (`find $DICOM_DIR/$SUBJ -maxdepth 1 -type d -name 'embarc_CU_'{$SUBJ}'**'`)
        if (-f $DICOM_DIR/$SUBJ/$SUBJ.unpacklog) then 
     	    break 
	else
	    echo Unpacking $FOLD
	    pbsubmit -m aafzal -c "unpacksdcmdir -src $FOLD -targ $DICOM_DIR/$SUBJ/ -scanonly $DICOM_DIR/$SUBJ/$SUBJ.unpacklog"
        endif
    end
else
    break
endif 

