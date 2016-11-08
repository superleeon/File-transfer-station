#!/usr/bin/env python
# encoding: utf-8
import zipfile
import os


def unzip(filename):
    fileroot = os.path.join(os.path.dirname(__file__), filename)
    zfile = zipfile.ZipFile(fileroot, 'r')
    for filename in zfile.namelist():
        if filename.endswith('/'):
            os.makedirs(filename)
        else:
            zfile.extract(filename)
        data = zfile.read(filename)
        file = open(filename, 'w+b')
        file.write(data)
        file.close()


#
# def modify_content(change, change_to):
#

def zip():
    pass


if __name__ == "__main__":
    for p, ds, fs in os.walk('./Definitions'):
        for f in fs:
            fl = open(f, 'w+')
            fc = fl.read()
            fc.replace('vnfplugin_v1', 'vnfplugin-ms_v20161108172435')
            fc.replace('v1.16.20.03', 'v20161108172435')

            print(f)
