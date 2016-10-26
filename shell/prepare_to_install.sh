#!/bin/bash
set -ex
# 获取配置变量
tmpDir="/home/tmp$(date +%Y%m%d%H%M%s)"
mysql=$(docker ps -a|grep mysql)
mysql=${mysql#*,}
MYSQL_IP=${mysql%:*}
CONTROLLER_IP=$1
MASTER=$(grep 'k8s_ip' -r /root/common/com_vars.yml | awk '{print $3}' | awk -F '}' '{print $1}')
NODE_2=$(ssh ubuntu@$MASTER "kubectl get node" | tail -1 | awk '{print $1}')
# 配置数据库

rm -rf /home/tools /home/vmanager
mkdir -p $tmpDir && mkdir -p /home/tools
# 下载所部署所需要的tar包(vmanager-deploy, modeldesign, jdk,暂时存放在ftp服务器)
ftp -nv 10.62.57.171 <<FTPIT 
user root root
bin
prompt 
cd /vManagerDeploy
lcd $tmpDir
mget *.tar.gz
quit

FTPIT

mv $tmpDir/vmanager_deploy.tar.gz /home
cd /home
tar -xvzf vmanager_deploy.tar.gz
# 替换ip地址
sed -i "s/192.167.1.31/$NODE_2/g" `grep 192.167.1.31 -rl /home/vmanager/vmanager-deploy`
sed -i "s/10.62.100.169/$CONTROLLER_IP/g" `grep 10.62.100.169 -rl /home/vmanager/vmanager-deploy`
sed -i "s/mysql_ip: 192.167.1.28/mysql_ip: $MYSQL_IP/g" `grep mysql_ip: -rl /home/vmanager/vmanager-deploy`

# 执行部署脚本,安装vmanager
./upgrade.sh

# 安装jdk
if ["$JAVA_HOME" == ""]
then
	cd $tmpDir
	tar -xvzf $tmpDir/jdk-8u60-linux-x64.tar.gz 
	mv jdk1.8.0_60 /usr/lib/jvm
	echo -e "export JAVA_HOME=/usr/lib/jvm/ \nexport JRE_HOME=\${JAVA_HOME}/jre\nexport CLASSPATH=.:\${JAVA_HOME}/lib:\${JRE_HOME}/lib\nexport PATH=\${JAVA_HOME}/bin:\$PATH" > /etc/profile
	source /etc/profile 
fi

# 安装modeldesigan
if []
then
	cd $tmpDir
	mv modeldesign-nfv-standalone-5.10.20.B4-SNAPSHOT-linux.gtk.x86_64.tar.gz /home/tools
	cd /home/tools
	tar -xvzf modeldesign-nfv-standalone-5.10.20.B4-SNAPSHOT-linux.gtk.x86_64.tar.gz
	cd modeldesign
	sed -i 's/8088/8089/g' /home/tools/modeldesign/setenv.sh
	nohup ./run.sh &
	sleep 3
	./stop.sh
	sed -i 's/10.62.99.90/10.62.100.149/g' /home/tools/modeldesign/.extract/webapps/winery/WEB-INF/repository_conf.properties
	sed -i 's/port_nfv=5000/port_nfv=10080/g' /home/tools/modeldesign/.extract/webapps/winery/WEB-INF/repository_conf.properties
	nohup ./run.sh &
fi


