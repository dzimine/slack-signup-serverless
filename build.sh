#!/bin/bash

OWD=$(pwd)
for dir in 'record_ac' 'record_db' 'invite_slack' ;
do
  if [ -f $dir/requirements.txt ]; then
    echo "Installing Python dependencies for $dir ..."
    cd $dir
    rm -rf ./site-packages
    pip install -t ./site-packages/ -r ./requirements.txt
    cd $OWD
  fi
done