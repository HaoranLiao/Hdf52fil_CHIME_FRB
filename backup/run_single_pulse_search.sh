#1/bin/bash

i=1
while IFS='' read -r line || [[ -n "$line" ]]; do

    IN_FILE_NAME="${line%.*}_p0.fil"
    OUT_FILE_ROOT="${line%.*}_p0"
    MASK_NAME="${OUT_FILE_ROOT}_rfifind.mask"
    OUT_FILE_NAME="${OUT_FILE_ROOT}_DM0.00"

    if [ $i -gt 1 ]
    then
        break
    fi

    echo "Reading: $IN_FILE_NAME"

    rfifind -noclip -time 1.0 -o $OUT_FILE_ROOT $IN_FILE_NAME

    echo "Apply Mask: $MASK_NAME"

    prepdata -nobary -o $OUT_FILE_NAME -dm 0.0 -mask $MASK_NAME -numout 530000 $IN_FILE_NAME 
    #single_pulse_search.py $NAME.dat
    echo "Done: $OUT_FILE_NAME"

    i=$(( $i + 1 ))

done < $1

