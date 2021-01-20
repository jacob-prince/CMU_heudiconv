#/bin/bash -f

matlabpath=/Applications/MATLAB_R2018a.app/bin/matlab # path to matlab installation
basedir=/Volumes/jacobprince_external/TarrLab/Projects/Project-BIDS/take7 # path to top level project directory
sourcedatadir="$basedir"/sourcedata # path to directory containing all folders of DICOM data

echo $sourcedatadir

for dir in $sourcedatadir # iterate through folders containing DICOM data
do
    for subdir in "$dir"/* # iterate through subdirectories (each should contain data from 1 subject)
    do
        if [[ -d $subdir ]] # if subject is member of "includes" [todo], run heudiconv [reminder to include info about weird folder order in documentation]
        then
            echo $subdir
            subname=$(basename $subdir)
            echo $subname

            # run matlab function to automatically rename DICOM folders to reflect their contents
            $matlabpath -nodisplay -nosplash -nojvm -r "renameDicomSeries('${sourcedata}/$subname'); quit;"

            # run setup routine to generate heudiconv ....
            docker run --rm -it \
            -v $basedir:/base \
                nipy/heudiconv:latest \
            -d /base/sourcedata/{subject}/*/*.dcm \
            -s $subname \
            -f /base/heudiconv/heuristics/convertall.py \
            -c none \
            -o /base/heudiconv/ \
            --overwrite

            # run heudiconv conversion using dcm2niix helpers and user-defined heuristic.py file
            # [todo make functional for multiple sessions]
            docker run --rm -it \
            -v $basedir:/base \
                nipy/heudiconv:latest \
            -d /base/sourcedata/{subject}/*/*.dcm \
            -s $subname -ss 01 \
            -f /base/heudiconv/heuristics/heuristic.py \
            -c dcm2niix -b \
            -o /base/BIDS/ \
            --overwrite

            # to address known issues conforming to BIDS specification, run MATLAB routine
            # to (1) add "IntendedFor" field to fmap json files and (2) add CogAtlasID fields to func json files
            # $matlabpath -nodisplay -nosplash -nojvm -r "bids_fill_fmap_jsons('$bidsdir','$subname',0,{'pictures','rest'}); quit;"

        fi
    done
done

echo "done"