import os, subprocess, re

root_dir = '/space/will/3/users/EMBARC/EMBARC-FAST/'
os.chdir(root_dir)
matches = []
for folder in os.listdir(root_dir):
    if os.path.isfile( os.path.join( root_dir, folder, 'subjectname' ) ): 
        matches.append(os.path.join(root_dir,folder))
pps = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_subjects", 'r')]
hcs = [line.strip() for line in open("/space/will/3/users/EMBARC/EMBARC-FAST/scripts/subtypes_gt/gt_healthies", 'r')]
matches = pps + hcs

runs = ['rest']

info = ''
with open(os.path.join(root_dir, 'scripts', 'preproc', 'qc_values.csv'), 'w') as f:
    f.write(' '.join(['cohort','subjid','reg_qc'])+'\n')
    for match in sorted(matches):
        for run in runs:
	    subjid = os.path.basename(match)
	    cmd = 'tkregister-sess -s %s -fsd %s -per-run -bbr-sum' %(subjid,run)
	    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, )
	    output, _ = proc.communicate()
	
	    output = re.sub(' +', ' ',output)
	    if output.startswith('ERROR'):
		output = ' '.join([subjid, '001']) + ' \n'
	    output = output.split(' ')
	    if match in pps: cohort = 1
	    elif match in hcs: cohort = 2
	    output.insert(1, str(cohort))
	    output.pop(2)
	    info = [s for s in output]
	    info = ' '.join(info) 
            	
	    f.write(info)
