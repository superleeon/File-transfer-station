#!/bin/bash
set -ex 
sudo mount -t cifs -o username=,password= //10.43.42.219/vnfoversion/vManagerV6.16.10/PAAS/vmanager-deploy /home
tar -xvzf vmanager.tar.gz
cd /home/vmanager/vmanager-deploy

