#!/bin/bash

set -ex
if [$JAVA_HOME];
then
	echo "1"
else
	echo "2"
fi
