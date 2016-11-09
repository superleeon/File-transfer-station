#!/usr/bin/env python
# encoding: utf-8
import zipfile
import os

import shutil


class Zip(object):
    def __init__(self):
        pass

    def unzip(self, fileroot, **kwargs):
        files = []
        if not os.path.exists(fileroot):
            print("package [%s] is not exist." % fileroot)
            return
        zfile = zipfile.ZipFile(fileroot, 'r')
        dest_dir = "/".join(fileroot.replace("\\", "/").split("/")[:-1]) + "/tmp"
        change_dict = {}
        for k in kwargs:
            v = kwargs.get(k)
            change_dict[k] = v
        for filename in zfile.namelist():
            if filename.endswith('/'):
                os.makedirs(filename)
            else:
                zfile.extract(filename, dest_dir)
            data = zfile.read(filename)
            for k in change_dict:
                if k in data:
                    data = data.replace(k, change_dict[k])
            file = open(os.path.join(dest_dir, filename), 'w+b')
            files.append(dest_dir + "/" + filename)
            file.write(data)
            file.close()
        return (files, dest_dir)

    def zip_dir(self, dest_zipfile, files, filename):
        print(dest_zipfile)
        if os.path.exists(dest_zipfile):
            shutil.rmtree(dest_zipfile)
        dir = "/".join(dest_zipfile.replace("\\", "/").split("/")[:-1])
        print(dir)
        zf = dir + "/" + filename
        print(zf)
        zfile = zipfile.ZipFile(zf, "w", zipfile.zlib.DEFLATED)
        for file in files:
            out_file = file.split("/tmp/")[1:]
            zfile.write(file, out_file)
        zfile.close()


if __name__ == "__main__":
    (files, dest_zipfile) = Zip().unzip("E:/RF/testcase/resource/VNFD-test.csar",
                                        **{"vnfplugin_v1": "vnfplugin-ms_v2016", "v1.16.20.03": "v2016"})
    dest_zipfile = dest_zipfile
    Zip().zip_dir(dest_zipfile, files, "2.csar")
