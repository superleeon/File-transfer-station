#!/bin/bash
set -ex
CONTROLLER_IP=$1

# 获取配置变量
bashDir=$(pwd)
tmpDir="/home/tmp$(date +%Y%m%d%H%M%S)"
mysql=$(docker ps -a|grep mysql)
mysql=${mysql#*, }
MYSQL_IP=${mysql%:*}
MASTER=$(grep 'k8s_ip' -r /root/common/com_vars.yml | awk '{print $3}' | awk -F '}' '{print $1}')
NODE_2=$(ssh ubuntu@$MASTER "kubectl get node" | tail -1 | awk '{print $1}')
# 配置数据库
sudo docker exec -i mysql bash -c "export TERM=linux;mysql -uroot -pcloud -e \"grant all privileges on *.* to 'vmanager'@'%' identified by 'U_tywg_2016' with grant option;\""
echo -e "drop database if exists vmanager;\ncreate database vmanager;\ngrant all on vmanager.* to 'vmanager'@'%';\ndrop database if exists vmanager_m;\ncreate database vmanager_m;\ngrant all on vmanager_m.* to 'vmanager'@'%';" > /tmp/mysql.txt
sudo docker cp /tmp/mysql.txt mysql:/home/mysql.txt

sudo docker exec -i mysql bash -c "export TERM=linux;mysql -uvmanager -pU_tywg_2016 < /home/mysql.txt"

# 下载vmanager部署脚本
rm -rf /home/vmanager && rm -f /home/vmanager_deploy.tar.gz
mkdir -p $tmpDir && mkdir -p /home/tools
cd $tmpDir
wget -q http://10.63.240.72/vmanager_deploy.tar.gz

mv $tmpDir/vmanager_deploy.tar.gz /home
cd /home
tar -xzf vmanager_deploy.tar.gz
# 替换ip地址
sed -i "s/192.167.1.31/$NODE_2/g" `grep 192.167.1.31 -rl /home/vmanager/vmanager-deploy`
sed -i "s/10.62.100.169/$CONTROLLER_IP/g" `grep 10.62.100.169 -rl /home/vmanager/vmanager-deploy`
sed -i "s/mysql_ip: 192.167.1.28/mysql_ip: $MYSQL_IP/g" `grep mysql_ip: -rl /home/vmanager/vmanager-deploy`

# 执行部署脚本,安装vmanager
cd $bashDir
./upgrade.sh

# 安装jdk
jdk=$((type java) || true)
if [ "$jdk" = "" ]
then
	echo "jdk is not exist.install now."
	cd $tmpDir
	wget -q http://10.63.240.72/jdk-8u60-linux-x64.tar.gz
	tar -xzf $tmpDir/jdk-8u60-linux-x64.tar.gz 
	mv jdk1.8.0_60 /usr/lib/jvm
	echo -e "export JAVA_HOME=/usr/lib/jvm/ \nexport JRE_HOME=\${JAVA_HOME}/jre\nexport CLASSPATH=.:\${JAVA_HOME}/lib:\${JRE_HOME}/lib\nexport PATH=\${JAVA_HOME}/bin:\$PATH" >> /etc/profile
	source /etc/profile 
fi

# 安装modeldesign
modeldesign="$(ps -ef|grep modeldesign|grep 8089||true)"
if [ "$modeldesign" = "" ]
then
	rm -rf /home/tools && mkdir /home/tools
	cd $tmpDir
	wget -q http://10.63.240.72/modeldesign-nfv-standalone-5.10.20.B4-SNAPSHOT-linux.gtk.x86_64.tar.gz
	mv modeldesign-nfv-standalone-5.10.20.B4-SNAPSHOT-linux.gtk.x86_64.tar.gz /home/tools
	cd /home/tools
	tar -xzf modeldesign-nfv-standalone-5.10.20.B4-SNAPSHOT-linux.gtk.x86_64.tar.gz
	cd modeldesign
	sed -i "s/8088/8089/g" /home/tools/modeldesign/setenv.sh
	nohup ./run.sh &
	sleep 10
	./stop.sh
	sed -i "s/10.62.99.90/$CONTROLLER_IP/g" /home/tools/modeldesign/.extract/webapps/winery/WEB-INF/repository_conf.properties
	sed -i "s/port_nfv=5000/port_nfv=10080/g" /home/tools/modeldesign/.extract/webapps/winery/WEB-INF/repository_conf.properties
	nohup ./run.sh &
fi

rm -rf $tmpDir
