#!/bin/bash
### This file is generated through script 10-generate-config.sh
SASL_PASSWORD=
SEC="-X security.protocol=SASL_SSL -X ssl.ca.location=./data/ca.crt -X sasl.mechanisms=SCRAM-SHA-512 -X sasl.username=cp4waiops-cartridge-kafka-auth-0 -X sasl.password="
BROKER="iaf-system-kafka-bootstrap-cp4waiops.itzroks-aaaaaa.cloud:443"
