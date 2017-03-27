import fnmatch, os, sys
from mne.io import Raw
from numpy import abs, diff
from pandas import read_csv

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Find all motion files.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
root_dir = '/space/will/3/users/EMBARC/EMBARC-FAST/'

pps = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_subjects", 'r')]
hcs = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_healthies", 'r')]
matches = pps + hcs

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Iteratively Calculate stats.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
tasks = ['rest']
run = 1

with open('motion.csv','w') as f:
    f.write(' '.join(['subjid','cohort','abs_mean','abs_max','rel_mean','rel_max'])+'\n')
    for match in sorted(matches):
        for task in tasks:
	    if os.path.isdir(os.path.join(root_dir,match, task)):
		## Get metadata.
            	subjid = match
            	motion_file = os.path.join(root_dir,match,task,'%03d' %run,'fmcpr.mcdat')
            	if os.path.isfile(motion_file):
                    ## Load data.
                    motion = read_csv(motion_file, sep=' *', header=None, engine='python')

                    ## Compute absolute statistics.
                    abs_mean = motion[9].mean()
                    abs_max  = motion[9].max()
                    rel_mean = abs(diff(motion[9])).mean()
                    rel_max = abs(diff(motion[9])).max()
	   	    if match in pps: cohort = 1
	            elif match in hcs: cohort = 2
                    f.write('%s %s %0.3f %0.3f %0.3f %0.3f\n' %(subjid,str(cohort), abs_mean,abs_max,rel_mean,rel_max))
                else:
                    f.write('%s %s %03d\n' %(subjid,task, run))
                
