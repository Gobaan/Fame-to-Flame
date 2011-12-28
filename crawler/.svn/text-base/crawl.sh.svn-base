#!/bin/bash

# Heritrix location
HERITRIX=/opt/heritrix-1.14.3/bin/heritrix

# Where job files are
JOBS=/opt/sbig/jobs
START_JOB=base
START_TEMPLATE_JOB=base_backup
CRAWL_JOB=recover
CRAWL_TEMPLATE_JOB=recover_backup

# Log directory
LOGS=/opt/sbig/logs

# Make sure setup script has been run
if [ ! -d $JOBS ]; then
  echo "Please run setup.sh first"
  exit
fi

function run_crawl {
  $HERITRIX --nowui $1

  # Check every minute until timeout
  for i in `seq 1 $2`; do
    # We can Ctrl-c out of the script while sleeping and
    # not worry about weird behaviour
    # Wait for the crawl job to run
    sleep 60

    # Check if heritrix is done yet
    if [ `ps aux | grep heritrix | grep -v grep | wc -l` -eq 0 ]; then
      return
    fi
    echo "tick"
  done

  echo Heritrix is still running after timeout - killing
  kill `ps a | grep heritrix | grep -v grep | cut -c1-5`
  return
}


rm -r $JOBS/$START_JOB
cp -r $JOBS/$START_TEMPLATE_JOB $JOBS/$START_JOB

# Run the starter job
run_crawl $JOBS/$START_JOB/order.xml 2

echo "Done running starter job"

# Keep running the crawler
while true; do
  # Reset the directory
  rm -r $JOBS/$CRAWL_JOB
  cp -r $JOBS/$CRAWL_TEMPLATE_JOB $JOBS/$CRAWL_JOB

  # Rn the crawl
  run_crawl $JOBS/$CRAWL_JOB/order.xml 5

  echo Crawl finished, performing cleanup

  # Generate timestamp yyyy.mm.dd-HH.MM for log file
  timestamp=`date +%Y.%m.%d-%k.%M`

  # Backup the log
  python handle_logs.py $JOBS/$CRAWL_JOB/logs/crawl.log
  cp $JOBS/$CRAWL_JOB/logs/crawl.log $LOGS/crawl.$timestamp.log

  # Move recover.gz so we pick up where we left off
  cp $JOBS/$CRAWL_JOB/logs/recover.gz $JOBS/$START_JOB/logs
done
