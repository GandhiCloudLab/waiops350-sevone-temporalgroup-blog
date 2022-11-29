#!/bin/bash

echo "process started ..... $(date)"

source ./01-config1.sh
source ./02-config2.sh

for myFile in $EVENTS_INFERENCING_FOLDER/*.json; do 
    echo  "Sending the inferencing file to Kafka : $myFile " ; 
    kcat -P $SEC -b $BROKER -t $TOPIC_NAME  -l $myFile
done

# LOG_FILE="../../data/input/events-inferencing/test.json"
# LOG_FILE="../../data/input/events-inferencing/inferencing-events.json"
# kcat $SEC -b $BROKER -P -t $TOPIC_NAME -l $LOG_FILE

echo "process completed ..... $(date)"