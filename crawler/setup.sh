#!/bin/bash

# Must run from src/crawler with sudo permissions

mkdir /opt/sbig
mkdir /opt/sbig/logs
mkdir /opt/sbig/jobs

cp -r base_backup /opt/sbig/jobs
cp -r recover_backup /opt/sbig/jobs
