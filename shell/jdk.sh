#!/bin/bash
set -ex

tmpDir=/home/tmp2016102600351477413315
java=$JAVA_HOME
if [$java=""]
then
        cd $tmpDir
        tar -xvzf $tmpDir/jdk-8u60-linux-x64.tar.gz
        mv jdk1.8.0_60 /usr/lib/jvm
        echo -e "export JAVA_HOME=/usr/lib/jvm/ \nexport JRE_HOME=\${JAVA_HOME}/jre\nexport CLASSPATH=.:\${JAVA_HOME}/lib:\${JRE_HOME}/lib\nexport PATH=\${JAVA_HOME}/bin:\$PATH" > /etc/profile
        source /etc/profile
else
	echo "jdk is already exist."
fi
