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

    field = create_key(os.path.join('sub-{subject}','field', 'sub-{subject}_fieldname'))

    info = {field: []}

    for idx, s in enumerate(seqinfo):
        if 'name' in s.dcm_dir_name.lower():
            info[field] = [s.series_id]

    for key,val in info.items():
        print('found {} scans for sequence {}'.format(len(val), key))
    return info
