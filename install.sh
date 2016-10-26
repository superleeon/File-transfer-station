#!/bin/bash
set -ex

docker exec -it mysql bash <<eof
# 创建数据库
export TERM=linux

mysql -uroot -pcloud      #以root用户登录mysql数据库(root用户默认密码是cloud)

GRANT ALL PRIVILEGES ON *.* TO 'vmanager'@'%' IDENTIFIED BY 'U_tywg_2016' WITH GRANT OPTION;      #创建vmanager用户，并给vmanager用户所有权限(用户名和密码,最好不要改动，因为拷贝过来的vmanager文件中好多地方用的就是这个用户名密码，如果改了，就要改vmanager文件中的配置了)

quit       #退出mysql

mysql -uvmanager -pU_tywg_2016      #以vmanager用户登录数据库

CREATE DATABASE if not exists vmanager;

GRANT ALL ON vmanager.*  TO 'vmanager'@'%';

CREATE DATABASE if not exists vmanager_m ;

GRANT ALL ON vmanager_m.*  TO 'vmanager'@'%';

commit;

show databases;
exit;
eof
# 获取vmanager-deploy
tmpDir = "/home/tmp$(date +%Y%m%d%H%M%s)"
mkdir -p $tmpDir
sudo mount -t cifs -o username=,password= //10.43.42.219/vnfoversion/vManagerV6.16.10/PAAS/vmanager-deploy $tmpDir
rm -rf /home/vmanager && rm -f /home/vmanager.tar.gz
cp -rf $tmpDir/vmanager.tar.gz /home
tar -xvzf $tmpDir/vmanager.tar.gz
unount $tmpDir
rm -rf $tmpDir

# 修改配置文件IP
# deplot-tmp.sh
# 插入ftp服务器信息到数据库
