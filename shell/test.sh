#!/bin/bash
set -ex
tmpDir="/home/tmp$(date +%Y%m%d%H%M%s)"
NODE_1='1.1.1.1'
NODE_2='2.2.2.2'
CONTROLLER_IP='4.4.4.4'
MYSQL_IP='3.3.3.3'

# 创建数据库


# 获取vmanager-deploy
# mkdir -p $tmpDir
# sudo mount -t cifs -o username=,password= //10.43.42.219/vnfoversion/vManagerV6.16.10/PAAS/vmanager-deploy $tmpDir
# rm -rf /home/vmanager && rm -f /home/vmanager.tar.gz
# cp -rf $tmpDir/vmanager.tar.gz /home
# tar -xvzf $tmpDir/vmanager.tar.gz
# umount $tmpDir && rm -rf $tmpDir

# 替换ip地址
sed -i "s/120.0.0.18/$NODE_1/g" `grep 120.0.0.18 -rl /home/vmanager/vmanager-deploy`
sed -i "s/120.0.0.17/$NODE_2/g" `grep 120.0.0.17 -rl /home/vmanager/vmanager-deploy`
sed -i "s/10.62.97.241/$CONTROLLER_IP/g" `grep 10.62.97.241 -rl /home/vmanager/vmanager-deploy`
sed -i "s/mysql_ip: $CONTROLLER_IP/mysql_ip: $MYSQL_IP/g" `grep mysql_ip: -rl /home/vmanager/vmanager-deploy`
sed -i "s/3306/5432/g" `grep 3306 -rl /home/vmanager/vmanager-deploy`

# 替换tosca-yaml-parser
rm -rf /home/vmanager/app/tosca-yaml-parser.tar
ftp -nv 10.74.151.103 <<!FTPRUN 
user zenap zenap.123 
prompt 
bin 
cd /zenap/zenap-modelparser/v20161019/zenap-modelparser-docker-img
lcd /home/vmanager/app/
mget tosca-yaml-parser.tar

cd /zenap/zenap-modeldesign/modeldesign-nfv-paas/latest/install-package
lcd /home/tools
bye 
!FTPRUN 

# 安装modeldesign

