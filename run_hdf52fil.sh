#!/bin/bash

i=1
while IFS='' read -r line || [[ -n "$line" ]]; do
    if [ $i -gt 1 ]
    then
	break
    fi 
    echo "Reading: $line"
    python /home/presto/workspace/hdf52fil_chimefrb/hdf52fil_chimefrb.py $line
    echo "Done: ${line%.*}_p0.fil"
    i=$(( $i + 1 ))
done < $1
