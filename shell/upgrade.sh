#!/bin/bash
set -ex
serviceDir="/service"
umount $serviceDir && rm -rf $serviceDir && mkdir -p $serviceDir
sudo mount -t cifs -o username=,password= //10.43.42.219/vnfoversion/vManagerV6.16.10/PAAS/service $serviceDir

workspace="/home/code"
versionDir="$workspace/version"
rm -rf $workspace && mkdir -p $versionDir
cp -rf $serviceDir/NFVO $versionDir
cp -rf $serviceDir/VNFM $versionDir

cd /home/vmanager/vmanager-deploy
./autodeploy.sh

#升级表结构
node2=$(cat config|grep "NODE_2=")
node2=${node2#NODE_2=}
ssh ubuntu@${node2} << eof
sudo docker exec ns-o python /home/vmanager/server/manage.py makemigrations && \
sudo docker exec ns-o python /home/vmanager/server/manage.py migrate &&  \
sudo docker exec nf-m python /home/vmanager/server/manage.py makemigrations && \
sudo docker exec nf-m python /home/vmanager/server/manage.py migrate
eof


