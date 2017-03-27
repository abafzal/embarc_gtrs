#!/bin/csh -f

## Source Freesurfer.
source /usr/local/freesurfer/nmr-stable53-env
setenv SUBJECTS_DIR /space/will/3/users/EMBARC/Recons/

## Specify root directory.
set ROOT_DIR = /autofs/space/will_003/users/EMBARC/EMBARC-FAST

## Specify subjects. 
#set SUBJECTS = (`cat /space/will/3/users/EMBARC/EMBARC-FAST/scripts/preproc/sessid`)
set SUBJECTS = (CU0106CUMR1R1)
set FSD = rest

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
### Configure nuisance variables.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#fcseed-config -wm -fcname wm.dat -fsd $FSD -pca -cfg wm.config
#fcseed-config -vcsf -fcname vcsf.dat -fsd $FSD -pca -cfg vcsf.config

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
### Create nuissance regressors.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

foreach SUBJECT ($SUBJECTS)
   
    fcseed-sess -s $SUBJECT -cfg wm.config
    fcseed-sess -s $SUBJECT -cfg vcsf.config

end
