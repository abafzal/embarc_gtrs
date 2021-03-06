#!/bin/csh -f

###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
## Unzip and Rename functional files to f.nii.
###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###

## Specify root directory. 
set ROOT_DIR = /space/will/3/users/EMBARC/EMBARC-FAST/
cd $ROOT_DIR

set SUBJECTS = (`cat $ROOT_DIR/scripts/preproc/sessid`)
set FSD = rest
set RUN = 001

foreach SUBJECT ($SUBJECTS)
   
    echo $SUBJECT 
 
    ## Unzip files (keep original zipped file). 
    set FILE = $SUBJECT/$FSD/$RUN/$SUBJECT'_reorient.nii.gz'
    if !(-f $SUBJECT/$FSD/$RUN/f.nii) then 
	echo Unzipping $SUBJECT
	gunzip -c $FILE > $SUBJECT/$FSD/$RUN/f.nii
    else
	echo $SUBJECT/f.nii already exists.
    endif

end
