# CMU_heudiconv pipeline 
### Enables conversion of a series of DICOM folders to BIDS format.
#### Author: Jacob Prince (TarrLab @ CMU - jacob.samuel.prince@gmail.com)

##### Software requirements:
- UNIX (Mac OSX or Linux)
- Docker
- MATLAB ([R2018a?] or later)

##### To run the pipeline, the user will execute the `heudiconv/commands.sh` file. Beforehand, there are several critical setup steps:
(1) Within the `heudiconv/commands.sh` file, the user must supply:
- a set of paths, atop the `/heudiconv/commands.sh` file:
    - `matlabpath`: path to matlab installation (e.g. `Applications/MATLAB_R2018a.app/bin/matlab`)
    - `basedir`: path to top level project directory
    - `sourcedatadir`: path to directory containing all folders of DICOM data (e.g. `~/basedir/sourcedata`)

(2) Within the sourcedatadir, the user must supply:
- at least one subject of data in DICOM format, containing any number of scan sessions.

(3) Within the heudiconv/heuristics folder,
- a heuristic file informing the converter which DICOM folder corresponds to what scan (see `heuristics/example_heuristic.py` for an example)
- The DICOM folders in `sourcedata/sub-${sub_id}` can be the poorly named '1', '2', ... folders from [? server].

This repository provides the necessary template code to run the heudiconv procedure, which efficiently converts DICOM files into BIDS format using a set of functions within the heudiconv Docker container. As such, Docker must be running in order for the pipeline to execute. In addition, the user must have a working version of MATLAB (R2018a or later?), and have set the path to the MATLAB installation correctly (see below) in order to execute the relevant functions automatically when the pipeline is run.

"Heudiconv" stands for "heuristic" + "conversion", referring to the fact that the user needs to supply a "heuristic file" specifying how the outputted BIDS folders will be formatted. This file is located at `heudiconv/heuristics/heuristic.py`. The heuristic file specifies which DICOM folders to process (and which, if any, to ignore), as well as the specific naming scheme that is relevant for a particular study, that will hopefully enable all dataset users to understand which folders contain data from particular scan sessions. The user has full control over all the naming parameters specified in the `heuristic.py` file, and as such, it is up to the user to specify naming schemes that conform to the BIDS specification. After this pipeline is run, issues with naming can be easily diagnosed by running a quick BIDS-validator tool (https://bids-standard.github.io/bids-validator/). If the BIDS-validatior reveals that some folders in the output directory are named incorrectly with respect to the BIDS standard, it may be necessary to delete or otherwise remove the outputted `BIDS` folder AND the hidden `.heudiconv` folder that are created during the execution of this pipeline, and to start over from scratch.

**IMPORTANT: especially for first-time users, it is expected that it will take more than 1 attempt to successfully format a `heuristic.py` file such that the output BIDS folder passes BIDS-validation. As such, it is STRONGLY advised to first run this pipeline using a DICOM files from a single subject, and to ensure that all outputs are reasonable before proceeding to a full-scale conversion of the remaining subjects. This may even include proceeding beyond BIDS conversion to run subsequent preprocessing routines (e.g. fmriprep) to verify that the DICOM conversion worked as expected. This pipeline template has been written for converting data from the [scanner?]. It may require user modification if used to convert DICOMs from other scan sites.**
