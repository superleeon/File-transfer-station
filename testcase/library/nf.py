#!/usr/bin/env python
# coding: utf-8

import urllib2
import json
import time
import zip


class Nf(object):
    def __init__(self):
        self.zip = zip.Zip()
        pass

    # 修改nf包
    # def change_nf_package(self, from_package, msb_service_name, to_package):
    #     files = self.zip.unzip(from_package, msb_service_name, "tmp/")
    #     self.zip.zip_dir("tmp/", to_package, files)

    # 注册nf包 √
    def nf_package(self, package_url, package_id, fileroot, description):
        print(package_url)
        fileroot = fileroot.replace("\\", "/")
        # prepare data
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'packageid')
        data.append(str(package_id))
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'desc')
        data.append(str(description))
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'packageloc')
        data.append('1')
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'packagepath')
        data.append('')
        data.append('--%s' % boundary)

        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'deploymode')
        data.append('2')
        data.append('--%s' % boundary)

        filename = fileroot.split("/")
        data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('file', str(filename)))
        data.append('Content-Type: %s\r\n' % 'application/zip')

        fr = open(r'%s' % str(fileroot), 'rb')
        data.append(fr.read())
        fr.close()
        data.append('--%s--\r\n' % boundary)
        data = '\r\n'.join(data)
        package_url = str(package_url)

        req = urllib2.Request(package_url, data=data)
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("register nf package [%s],resp=[%s]." % (package_id, qrcont))
        return qrcont

    # 查询所有的nf包 √
    def get_nf_packages(self, package_url):
        package_url = str(package_url)
        req = urllib2.Request(package_url)
        req.add_header('Accept', 'application/json, text/plain, */*')
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("get nf packages, resp=[%s]" % qrcont)
        return qrcont

    # 查询nf包是否存在 √
    def nf_package_exist(self, package_url, package_id):
        nf_packages = self.get_nf_packages(package_url)
        nf_packages = json.loads(nf_packages).get('packages')
        for nf_package in nf_packages:
            if package_id == nf_package.get('packageid'):
                print("nf package [%s] already exist." % package_id)
                return True
        print("nf package [%s] not exist." % package_id)
        return False

    # 根据id查询nf包信息 √
    def get_nf_package_by_package_id(self, package_url, package_id):
        package_url = str(package_url) + "/vnf/" + str(package_id) + "/detail"
        req = urllib2.Request(package_url)
        req.add_header('Accept', 'application/json, text/plain, */*')
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("get package, package_id=[%s], resp=[%s]" % (package_id, qrcont))
        return qrcont

    # 删除nf包 √
    def delete_nf_package(self, package_url, package_id):
        self.nf_package_disable(package_url, package_id)
        package_url = str(package_url) + "/vnf/" + str(package_id) + "/delete"
        req = urllib2.Request(package_url)
        req.get_method = lambda: 'DELETE'
        req.add_header('Accept', 'application/json, text/plain, */*')
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("delete nf package [%s], resp = [%s]" % (package_id, qrcont))
        return qrcont

    # disable package √
    def nf_package_disable(self, package_url, package_id):
        data = {"packageid": str(package_id)}
        disable_url = str(package_url) + '/vnf/status/disable'
        req = urllib2.Request(disable_url, data=json.dumps(data))
        req.add_header('Content-Type', 'application/json;charset=utf-8')
        print("nf package [%s] disable" % package_id)
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print qrcont
        return qrcont

    # 查询工作流进度 √
    def progress(self, nso_url, jobid):
        job_url = str(nso_url) + "/jobs/" + str(jobid)
        req = urllib2.Request(job_url)
        req.add_header('Accept', 'application/json, text/plain, */*')
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        return qrcont

    # 查询全部nf请求 √
    def send_get_nfs(self, nfs_url):
        print("get all nfs,url=[%s]" % nfs_url)
        req = urllib2.Request(nfs_url)
        req.add_header('Accept', 'application/json, text/plain, */*')
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("get all nfs, resp = [%s]" % qrcont)
        return qrcont

    # 查询nf是否存在 √
    def nf_exist_return_id(self, nfs_url, nfinstname):
        nfs = self.send_get_nfs(nfs_url)
        nfs = json.loads(nfs).get('vnfs')
        for nf in nfs:
            if nf.get('vnf_name') == nfinstname:
                nfinstid = nf.get('nf_inst_id')
                print("nf inst [%s] is already exist." % nfinstname)
                print("nf inst [%s],nfinstid = [%s]." % (nfinstname, nfinstid))
                return (True, nfinstid)
        print("nf inst [%s] is not exist." % nfinstname)
        return (False, None)

    # 发送删除请求 √
    def send_delete_nf(self, delete_url):
        req = urllib2.Request(delete_url)
        req.get_method = lambda: 'DELETE'
        req.add_header('Accept', 'application/json, text/plain, */*')
        req.add_header('Accept-Encoding', 'gzip, deflate')
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("delete nf, resp = [%s]" % qrcont)
        return qrcont

    # 发送实例化请求 √
    def send_create_nf(self, create_url, data):
        req = urllib2.Request(create_url, data=str(data))
        req.add_header('Content-Type', 'application/json;charset=utf-8')
        print("send nf instantiation request to paas")
        resp = urllib2.urlopen(req, timeout=60)
        qrcont = resp.read()
        print("nf instantiation, resp = [%s]" % qrcont)
        return qrcont

    # nf实例化参数准备 √
    def prepare_date_for_nf_instantiate(self, nfo_url, nf_name, nf_package_id):
        package_url = str(nfo_url) + "/package"
        package_detail_url = str(nfo_url) + "/package/" + str(nf_package_id) + "/detail"
        if not self.nf_package_exist(package_url, nf_package_id):
            print("cannot prepare data for nf instantiate, because the nf package [%s] is not exist." % nf_package_id)
            return
        package = self.get_nf_package_by_package_id(package_url, nf_package_id)
        package = json.loads(package)
        data = {
            "vnfdid": package.get('vnfdid'),
            "vnfname": str(nf_name),
            "inputparameters": {},
        }
        # params = json.loads(package.get('inputparameters'))
        params = package.get('inputparameters')
        for param in params:
            value = params.get(param)
            data['inputparameters'][param] = value.get("default", "1")
        data = json.dumps(data)
        return data
