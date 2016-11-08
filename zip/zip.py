#!/usr/bin/env python
# encoding: utf-8
import zipfile
import os

import shutil

FILELIST = []


def unzip(filename, msb_service_name, dest_dir):
    (service_name, service_version) = msb_service_name.rsplit('_')
    fileroot = os.path.join(os.path.dirname(__file__), filename)
    zfile = zipfile.ZipFile(fileroot, 'r')
    for filename in zfile.namelist():
        if filename.endswith('/'):
            os.makedirs(filename)
        else:
            zfile.extract(filename, dest_dir)
        data = zfile.read(filename)
        if "vnfplugin_v1" in data:
            data = data.replace('vnfplugin_v1', msb_service_name)
        if "v1.16.20.03" in data:
            data = data.replace("v1.16.20.03", service_version)
        file = open(os.path.join(dest_dir, filename), 'w+b')
        FILELIST.append(dest_dir + filename)
        file.write(data)
        file.close()


def zip_dir(dirname, zipfilename):
    if os.path.exists(zipfilename):
        os.remove(zipfilename)
    # if os.path.exists(zipfilename):
    #     os.remove(os.path.join(os.path.dirname(__file__), zipfilename))
    zfile = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for file in FILELIST:
        zfile.write(file, "/".join(file.split("/")[1:]))
    zfile.close()
    if os.path.exists(dirname):
        shutil.rmtree(dirname)





if __name__ == "__main__":
    unzip("123.csar", "vnfplugin_v2012122222222", "tmp/")
    zip_dir("tmp/", "tosca.csar")
