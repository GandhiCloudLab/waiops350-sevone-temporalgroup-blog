#!/usr/bin/env bash

source ./00-config.sh

echo "process started ..... $(date)"

#### Operations Type (TopoDownload,TopoAll,EventsHistoryDownload, EventsHistoryAll)
export OPERATION_TYPE="TopoAll"

cd ../python

python3 main.py

cd ../run

echo "process Completed ..... $(date)"
