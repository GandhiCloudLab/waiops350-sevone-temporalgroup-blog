#!/bin/bash

#### SevOne - Access Parameters
export SEVONE_URL="http://aaaaa.com"
export SEVONE_USER="bbbbb"
export SEVONE_PWD="cccccc"

#### WAIOps Topology File Observer - Access Parameters
export WAIOPS_TOPO_URL="https://aaaa/1.0/file-observer/files"
export WAIOPS_TOPO_USER="aiops-topology-cp4waiops-user"
export WAIOPS_TOPO_PWD=""
export WAIOPS_TOPO_TENENT_ID="cfd95b7e-3bc7-4006-a4a8-a73a79c71255"

#### SevOne - Topology Filter Parameters
export SEVONE_DEVICE_IDS=3,9
export SEVONE_TOPO_HOPS=2
export SEVONE_GROUP_IDS=13,11

#### SevOne - Topology Filter Secondary Parameters 
export SEVONE_DEVICE_NAMES=
export SEVONE_SOURCE_IDS=

#### Event History - Parameters
export SEVONE_EVENT_HISTORY_DAYS=5
export MAX_NORMALIZED_EVENTS_PER_FILE=500

#### WAIOps Topology File Observer Job Parameters
export WAIOPS_TOPO_JOB_ID="filejob1"
export WAIOPS_TOPO_JOB_FILE_NAME="filejob1.txt"
export WAIOPS_TOPO_JOB_PROVIDER="filejob1"
export WAIOPS_TOPO_JOB_DATA_CENTER="filejob1-dc"

#### Debug Log (true/false)
export LOG_DEBUG=false

#### Folders
export INPUT_FOLDER="../../data/input/"
export OUTPUT_FOLDER="../../data/output/"

#### Operations Type (TopoDownload,TopoAll,EventsHistoryDownload, EventsHistoryAll)
export OPERATION_TYPE="TopoDownload"