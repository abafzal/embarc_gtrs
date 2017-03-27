import os
import numpy as np
import pylab as plt
from scipy.signal import detrend
from sklearn.decomposition import PCA
def demean(arr): return arr - arr.mean()
def rms(arr): return np.sqrt( np.mean( np.power(arr, 2) ) )

mri_dir = '/autofs/space/lilli_002/users/DARPA-ARC'
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
subject = 'hc007'
threshold = 0.5

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Prepare motion data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Read motion data.
mc = os.path.join(mri_dir, subject, 'arc_001', '001', 'fmcpr.mcdat')
mc = np.loadtxt(mc)[:,1:7]

## Invert angular displacement.
copy = mc.copy()
mc[:,:3] = np.deg2rad(mc[:,:3]) 
mc[:,:3] *= 50

## Compute framewise displacement (See Power 2012, 2014).
fd = np.insert( np.abs( np.diff(mc[:,3:], axis=0) ).sum(axis=1), 0, 0 )

## Demean/detrend data.
mc = detrend(copy, axis=0, type='constant')
mc = detrend(mc, axis=0, type='linear')

## Construct basis sets.
mcreg24 = mc.copy()
mcreg24 = np.concatenate([mcreg24, np.roll(mcreg24, -1, 0)], axis=-1)
mcreg24 = np.concatenate([mcreg24, np.power(mcreg24,2)], axis=-1)
    
## Apply PCA.  
pca = PCA(n_components=24)
mcreg24 = pca.fit_transform(mcreg24)   

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Prepare fMRI data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load gray/white matter timeseries.
npz = np.load('motion/%s_arc_qc_data.npz' %subject)
gm_pre = np.apply_along_axis(demean, 1, npz['gm'])

beta, _, _, _ = np.linalg.lstsq(mcreg24, gm_pre.T)
gm_post = gm_pre - np.dot(mcreg24, beta).T

## Compute DVARS.
DVARS = np.zeros((2,fd.shape[0]))
for n, arr in enumerate([gm_pre,gm_post]): DVARS[n,1:] += np.apply_along_axis(rms, 0, np.diff(arr, axis=1))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Plotting
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
fig = plt.figure(figsize=(12,12))
nrow = 10
rowspan = (nrow - 2) / 2

## Plot framewise displacement.
ax = plt.subplot2grid((nrow,1),(0,0))
ax.plot(fd, linewidth=1.5, color='k')
ax.hlines(0.5, 0, fd.shape[0], linestyle='--', color='k', alpha=0.5)
ax.set_xlim(0,fd.shape[0])
ax.set_xticks([])
ax.set_yticks([0.0,0.5,1.0])
ax.set_yticklabels([0.0,0.5,1.0], rotation=90)
ax.set_ylabel('FD (mm)', fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.set_title('Example Subject', fontsize=30)

## Plot grey matter (pre-regression).
ax = plt.subplot2grid((nrow,1),(1,0),rowspan=rowspan)
cbar = ax.imshow(gm_pre, aspect='auto', interpolation='none', origin='lower', cmap='bone', vmin=-50, vmax=50)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylabel('Grey Matter\nPre-Regression', fontsize=18)

# Colobar setup.
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
axColor = plt.axes([0.905, 0.523, 0.015, 0.255])
cbar = plt.colorbar(cbar, cax = axColor, orientation="vertical")
cbar.set_ticks([-50,0,50])
axColor.set_ylabel('BOLD', fontsize=18, rotation=270)

## Plot grey matter (post-regression).
ax = plt.subplot2grid((nrow,1),(1+rowspan,0),rowspan=rowspan)
cbar = ax.imshow(gm_post, aspect='auto', interpolation='none', origin='lower', cmap='bone', vmin=-50, vmax=50)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylabel('Grey Matter\nPost-Regression', fontsize=18)

# Colobar setup.
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height])
axColor = plt.axes([0.905, 0.222, 0.015, 0.255])
cbar = plt.colorbar(cbar, cax = axColor, orientation="vertical")
cbar.set_ticks([-50,0,50])
axColor.set_ylabel('BOLD', fontsize=18, rotation=270)

## Plot DVARS.
ax = plt.subplot2grid((nrow,1),(nrow-1,0))
for arr, label in zip(DVARS, ['Pre','Post']): ax.plot(arr, linewidth=1.5, alpha=0.8, label=label)
ax.legend(loc=2, fontsize=16, frameon=False, borderpad=0.0,  handlelength=1.4, handletextpad=0.2)
ax.set_xlim(0,fd.shape[0])
ax.set_xlabel('Acquisitions', fontsize=18)
ax.set_ylim(20,100)
ax.set_yticks([20,60,100])
ax.set_yticklabels([20,60,100], rotation=90)
ax.set_ylabel('DVARS', fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=12)

plt.subplots_adjust(left=0.05, right=0.90, top=0.95, bottom=0.05, hspace=0.05)
# plt.show()
plt.savefig('plots/FINAL/supp_motion_example.png', dpi=180)
plt.close('all')
print 'Done.'
