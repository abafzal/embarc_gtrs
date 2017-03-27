import os
import numpy as np
import nibabel as nib
from mne import read_label
from pandas import read_csv
from pandas import read_table

import scipy.io as sio
from pandas import DataFrame
from scipy.stats import pearsonr
from mne.filter import band_pass_filter


## Specify directories and parameters.
fast_dir = '/space/will/3/users/EMBARC/EMBARC-FAST'
fsd = 'rest'
run = '001'

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~## 
### Load cortical labels.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~## 

parc_dir = '/space/lilli/1/users/DARPA-Recons/fscopy/label/yeo114_orig'
lh_labels = [read_label(os.path.join(parc_dir, l)) for l in sorted(os.listdir(parc_dir)) if 'LH' in l]
rh_labels = [read_label(os.path.join(parc_dir, l)) for l in sorted(os.listdir(parc_dir)) if 'RH' in l]

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~## 
### Load subcortical labels.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~## 

## Read Freesurfer Color Lookup Table. 
lh_subcort = dict.fromkeys(['Left-Accumbens-area', 'Left-Thalamus-Proper', 'Left-Caudate', 'Left-Putamen', 'Left-Hippocampus', 'Left-Amygdala'])
rh_subcort = dict.fromkeys(['Right-Accumbens-area', 'Right-Thalamus-Proper', 'Right-Caudate', 'Right-Putamen', 'Right-Hippocampus', 'Right-Amygdala'])

clut = read_table(os.path.join('/space/will/3/users/EMBARC/EMBARC-FAST/scripts/labels', 'FreeSurferColorLUT_truncated.txt'), 
                                              sep=' *', skiprows=4, names=['No', 'Label','R','G','B','A'], engine='python')
clut = clut.loc[np.where(np.in1d(clut.Label,lh_subcort.keys() + rh_subcort.keys()))]

## Load subcortical segmentation.
aseg_obj = nib.load('/space/lilli/1/users/DARPA-Recons/fsaverage/mri.2mm/aseg.mgz')
aseg_dat = aseg_obj.get_data()

for l in lh_subcort.keys(): lh_subcort[l] = np.where(aseg_dat == int(clut.No[clut.Label == l]))
for l in rh_subcort.keys(): rh_subcort[l] = np.where(aseg_dat == int(clut.No[clut.Label == l]))
    
print 'cortical lh: %d,' %len(lh_labels), 'rh: %d\n' %len(rh_labels), 'subcortical lh: %d' %len(lh_subcort), 'subcortical rh: %d' %len(rh_subcort)

## Save list of regions. 
regions = np.array([l.name for l in lh_labels] + lh_subcort.keys() + [l.name for l in rh_labels] + rh_subcort.keys())
np.savetxt(os.path.join(fast_dir, 'scripts', 'subtypes_gt', 'gt_regions'), regions, fmt='%s')

## Define functions and directories.
def zscore(arr): return (arr - arr.mean()) / arr.std()

## Specify directories. 
gt_dir = '/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt'

## Specify subjects.
pps = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_subjects", 'r')]
hcs = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_healthies", 'r')]
subjects = pps + hcs

## Specify regions. 
regions = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_regions", 'r')]
n_regions = len(regions)

for i, subject in enumerate(subjects):
    
    ## print i, subject, 

    ## Load cortical/subcortical data.
    lh_dat = (nib.load(os.path.join(fast_dir, subject, fsd, run, 'fmcpr.sm6.fsaverage.%s.nii.gz' %'lh'))).get_data().squeeze()
    rh_dat = (nib.load(os.path.join(fast_dir, subject, fsd, run, 'fmcpr.sm6.fsaverage.%s.nii.gz' %'rh'))).get_data().squeeze()
    sc_dat = (nib.load(os.path.join(fast_dir, subject, fsd, run, 'fmcpr.sm6.%s.2mm.nii.gz' %('mni305')))).get_data()
    
    ## Drop first 4 volumes. 
    lh_dat = np.delete(lh_dat, np.arange(4), axis=1)
    rh_dat = np.delete(rh_dat, np.arange(4), axis=1)
    sc_dat = np.delete(sc_dat, np.arange(4), axis=3)

    n_times = sc_dat.shape[3]
    n_verts = lh_dat.shape[0]
    
    ## Remove any extra timepoints collected.
    if n_times > 176:
        print 'Removing last %d timepoints for %s' %(n_times-176,subject)
        lh_dat = np.delete(lh_dat, np.arange(176,n_times), axis=1)
        rh_dat = np.delete(rh_dat, np.arange(176,n_times), axis=1)
        sc_dat = np.delete(sc_dat, np.arange(176,n_times), axis=3)
        n_times = sc_dat.shape[3]
            
    elif n_times < 176: 
        print 'Mismatch in number of timepoints. %s, n_times: %d. Missing %d timepoints.' %(subject, n_times, 176-n_times)
        break
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    ### Average by labels.
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 
    mean_dat = np.zeros((n_regions,n_times))
    
    for idx in np.arange(len(lh_labels)):
        mean_dat[idx] = lh_dat[lh_labels[idx].vertices].mean(axis=0)

    for idx,k in zip(np.arange(len(lh_labels), len(lh_labels) + len(lh_subcort)),lh_subcort.keys()):
        x,y,z = lh_subcort[k]
        mean_dat[idx] = sc_dat[x,y,z].mean(axis=0)
        
    for rh_idx, idx in zip(np.arange(len(rh_labels)), np.arange(len(lh_labels) + len(lh_subcort), len(lh_labels) + len(lh_subcort) + len(rh_labels))):
        mean_dat[idx] = rh_dat[rh_labels[rh_idx].vertices].mean(axis=0)

    for idx,k in zip(np.arange(len(lh_labels) + len(lh_subcort) + len(rh_labels), n_regions),rh_subcort.keys()):
        x,y,z = rh_subcort[k]
        mean_dat[idx] = sc_dat[x,y,z].mean(axis=0)
        
    ## Save data averaged by labels. 
    np.savez_compressed(os.path.join(gt_dir, 'raw', '%s_raw' %subject), mean_dat=mean_dat)

print 'Done.'
