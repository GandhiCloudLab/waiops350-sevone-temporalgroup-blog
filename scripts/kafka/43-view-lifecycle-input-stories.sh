#!/bin/bash

echo "process started ..... $(date)"

source ./01-config1.sh
source ./02-config2.sh

TOPIC_NAME1=cp4waiops-cartridge.lifecycle.input.stories

kcat $SEC -b $BROKER -C -t $TOPIC_NAME1

echo "process completed ..... $(date)"
