#/bin/bash -f

matlab=/Applications/MATLAB_R2018a.app/bin/matlab
basedir=/Volumes/jacobprince_external/TarrLab/Projects/Project-BIDS/git/
outputdir="$basedir"/heudiconv
sourcedata="$basedir"/sourcedata
bidsdir=/Volumes/jacobprince_external/TarrLab/Projects/Project-BIDS/git/BIDS/

echo $sourcedata

for dir in $sourcedata
do
    for subdir in "$dir"/*
    do
        if [[ -d $subdir ]]
        then
            echo $subdir
            subname=$(basename $subdir)
            echo $subname
            $matlab -nodisplay -nosplash -nojvm -r "renameDicomSeries('${sourcedata}/$subname'); quit;"

            #generate heuristic file
            # docker run --rm -it \
            # -v $basedir:/base \
            # nipy/heudiconv:latest \
            # -d /base/sourcedata/{subject}/*/*.dcm \
            # -s $subname \
            # -f /base/heudiconv/heuristics/convertall.py \
            # -c none \
            # -o /base/heudiconv/ \
            # --overwrite
            # # #
            # docker run --rm -it -v $basedir:/base nipy/heudiconv:latest \
            # -d /base/sourcedata/{subject}/*/*.dcm \
            # -o /base/BIDS-test/ -f /base/heudiconv/heuristics/heuristic.py \
            # -s $subname -ss 001 -c dcm2niix -b --overwrite

            # $matlab -nodisplay -nosplash -nojvm -r "bids_fill_fmap_jsons('$bidsdir','$subname',0,{'pictures','rest'}); quit;"

        fi
    done
done

echo "done"