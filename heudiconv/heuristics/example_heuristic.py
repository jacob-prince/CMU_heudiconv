import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    """
    create keys for all the different sequences
    this is telling it the eventual path from the BIDS-formatted experiment directory
    note organization into different sub folders: anat, func, fmap, dwi

    also note there is no session format here, a session formatted floc key would look like:
    floc = create_key(os.path.join('sub-{subject}', 'func', 'ses-{session}', 'sub-{subject}_ses-{session}_task-floc_run-{item:02d}_bold'))

    """
    #localizer = create_key(os.path.join('sub-{subject}','anat', 'sub-{subject}_acq-localizer_run-{item:02d}'))
    #saggital = create_key(os.path.join('sub-{subject}', 'anat', 'sub-{subject}_acq-trufisag_run-{item:02d}'))
    t1w = create_key(os.path.join('sub-{subject}', 'anat', 'sub-{subject}_T1w'))
    t2w = create_key(os.path.join('sub-{subject}', 'anat', 'sub-{subject}_T2w'))

    math = create_key(os.path.join('sub-{subject}', 'func', 'sub-{subject}_task-math_run-{item:02d}_bold'))
    faces = create_key(os.path.join('sub-{subject}', 'func', 'sub-{subject}_task-faces_run-{item:02d}_bold'))
    values = create_key(os.path.join('sub-{subject}', 'func', 'sub-{subject}_task-values_run-{item:02d}_bold'))

    fmap_mag = create_key(os.path.join('sub-{subject}', 'fmap', 'sub-{subject}_acq-AP_magnitude'))
    fmap_diff = create_key(os.path.join('sub-{subject}', 'fmap', 'sub-{subject}_acq-AP_phasediff'))

    #info = {localizer: [], saggital: [], t1w:[], t2w: [], math: [], faces: [], values: [], fmap: []}
    info = {t1w:[], t2w: [], math: [], faces: [], values: [], fmap_mag: [], fmap_diff: []}

    for idx, s in enumerate(seqinfo):
        #if 'localizer' in s.dcm_dir_name.lower():
        #    info[localizer].append(s.series_id)
        #if 'trufi' in s.dcm_dir_name.lower():
        #    info[saggital].append(s.series_id)
        if 't1' in s.dcm_dir_name.lower():
            info[t1w].append(s.series_id)
        if 'math' in s.dcm_dir_name.lower():
            info[math].append(s.series_id)
        if 'faces' in s.dcm_dir_name.lower():
            info[faces].append(s.series_id)
        if 'values' in s.dcm_dir_name.lower():
            info[values].append(s.series_id)
        if 't2' in s.dcm_dir_name.lower():
            info[t2w].append(s.series_id)
        if '5_fieldmap' in s.dcm_dir_name.lower():
            info[fmap_mag].append(s.series_id)
        if '6_fieldmap' in s.dcm_dir_name.lower():
            info[fmap_diff].append(s.series_id)

    for key,val in info.items():
        print('found {} scans for sequence {}'.format(len(val), key))
    return info
