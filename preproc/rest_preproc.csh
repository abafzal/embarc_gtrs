#!/bin/csh -f

## Source Freesurfer. 
source /usr/local/freesurfer/nmr-stable53-env
setenv SUBJECTS_DIR /space/will/3/users/EMBARC/Recons/

## Specify root directory. 
set ROOT_DIR = /space/will/3/users/EMBARC/EMBARC-FAST/
cd $ROOT_DIR

## Specify user. 
set USER = aafzal

## Specify parameters.
set SURFACE = fsaverage
set FWHM = 6
#set SUBJECTS = (`cat $ROOT_DIR/scripts/preproc/sessid`)
set SUBJECTS = (CU0092CUMR1R1 CU0087CUMR1R1)
set TASK = rest

foreach SUBJECT ($SUBJECTS)

    ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###
    ## Preprocess.
    ###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~###

    preproc-sess -s $SUBJECT -surface $SURFACE lhrh -mni305 -fwhm $FWHM -per-run -fsd $TASK -nostc -noreg

end
