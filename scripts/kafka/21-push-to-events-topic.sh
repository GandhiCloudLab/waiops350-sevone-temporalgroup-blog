#!/bin/bash

echo "process started ..... $(date)"

source ./01-config1.sh
source ./02-config2.sh

for myFile in $EVENTS_HISTORY_FOLDER/*.json; do 
    echo  "Sending the file to Kafka : $myFile " ; 
    kcat -P $SEC -b $BROKER -t $TOPIC_NAME  -l $myFile
done

echo "process completed ..... $(date)"
