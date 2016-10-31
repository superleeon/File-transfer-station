#!/usr/bin/env python
# coding: utf-8

import urllib2
import json
import time
import os

# 查询全部ns请求
def send_get_nss(nss_url):
    print("get all nss,url=[%s]" % nss_url)
    req = urllib2.Request(nss_url)
    req.add_header('Accept', 'application/json, text/plain, */*')
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("get all nss, resp = [%s]" % qrcont)
    return qrcont

# 发送删除请求
def send_delete_ns(delete_url):
    print("delete ns, url = [%s]" % delete_url)
    req = urllib2.Request(delete_url)
    req.get_method = lambda: 'DELETE'
    req.add_header('Accept', 'application/json, text/plain, */*')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("delete ns, resp = [%s]" % qrcont)
    return qrcont

# 发送实例化请求
def send_create_ns(create_url, data):
    data = json.dumps(data)
    req = urllib2.Request(create_url, data=data)
    req.add_header('Content-Type', 'application/json;charset=utf-8')
    print("send ns instantiation request to paas")
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("ns instantiation, resp = [%s]" % qrcont)
    return qrcont

# 查询工作流进度
def progress(url, jobid):
    job_url = url + "/" + str(jobid)
    print("get job progress, url = [%s]" % job_url)
    req = urllib2.Request(job_url)
    req.add_header('Accept', 'application/json, text/plain, */*')
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    return qrcont

# 注册ns包
def ns_package(package_url, package_id, filename, description): 
    print(package_url)
    # prepare data
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'packageId')
    data.append(str(package_id))
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'description')
    data.append(str(description))
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'packageLocation')
    data.append('1')
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'packagePath')
    data.append('')
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'deploymode')
    data.append('2')
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('file', str(filename)))
    data.append('Content-Type: %s\r\n' % 'application/zip')
    # fileresource = os.path.join(os.path.abspath('../resource'), str(filename))
    fileresource = os.path.abspath(os.path.join(os.path.dirname(__file__),"../resource","case6.csar"))
    print("ns package register, package resource = [%s]" % fileresource)
    fr = open(r'%s' % str(fileresource), 'rb')
    data.append(fr.read())
    fr.close()
    data.append('--%s--\r\n' % boundary)
    data = '\r\n'.join(data)
    package_url = str(package_url)
    
    req = urllib2.Request(package_url, data=data)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("register ns package [%s], resp = [%s]" % (package_id, qrcont))
    return qrcont

# 根据id查询ns包
def get_ns_package_by_package_id(package_url, package_id):
    package_url = str(package_url) + "/" + str(package_id)
    req = urllib2.Request(package_url)
    req.add_header('Accept', 'application/json, text/plain, */*')
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("get package, package_id=[%s], resp=[%s]" % (package_id, qrcont))
    return qrcont

# 查询全部的ns包
def get_ns_packages(package_url):
    package_url = str(package_url)
    req = urllib2.Request(package_url)
    req.add_header('Accept', 'application/json, text/plain, */*')
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("get ns packages, resp=[%s]" % qrcont)
    return qrcont

# 删除ns包
def delete_ns_package(package_url, package_id):
    package_url = str(package_url) + "/" + str(package_id) + "/delete"
    req = urllib2.Request(package_url)
    req.get_method = lambda: 'DELETE'
    req.add_header('Accept', 'application/json, text/plain, */*')
    resp = urllib2.urlopen(req, timeout=60)
    qrcont = resp.read()
    print("delete ns package [%s], resp = [%s]" % (package_id, qrcont))
    return qrcont

# 查询ns包是否存在
def ns_package_exist(package_url, package_id):
    ns_packages = get_ns_packages(package_url)
    ns_packages = json.loads(ns_packages).get('packages')
    for ns_package in ns_packages:
        if package_id == ns_package.get('packageId'):
            print("ns package [%s] already exist." % package_id)
            return True
    print("ns package [%s] not exist." % package_id)
    return False

# 查询ns是否存在
def ns_exist_return_id(nss_url,nsinstname):
    nss = send_get_nss(nss_url)
    nss = json.loads(nss).get('nsinsts')
    for ns in nss:
        if ns.get('nsinstname') == nsinstname:
            nsinstid = ns.get('nsinstid')
            print("ns inst [%s] is already exist." % nsinstname)
            print("ns inst [%s],nsinstid = [%s]." % (nsinstname, nsinstid))
            return (True, nsinstid)
    print("ns inst [%s] is not exist." % nsinstname)
    return (False, None)

# ns实例化参数准备
def prepare_date_for_ns_instantiate(nss_url, ns_name, ns_package_id):
    package_url = str(nss_url) + "/nsPackages"
    if not ns_package_exist(package_url, ns_package_id):
        print("cannot prepare data for ns instantiate, because the ns package [%s] is not exist." % ns_package_id)
        return
    package = get_ns_package_by_package_id(package_url, ns_package_id)
    data = {
        "nsdId": package.get('nsdId'),
        "nsdName": str(ns_name),
        "packageId": str(ns_package_id),
        "inputparameters": {},
        "vnfinputparameters": []
    }
    package = json.loads(package)
    inputparameters = package['inputParameters']['inputs']
    for param in inputparameters:
        value = inputparameters.get(param)
        data['inputparameters'][param] = value.get("default", "1")
    print(data['inputparameters'])
    vnfinputparameters = package['vnfInputParameters']
    for vnfInputParameter in vnfinputparameters:
        dict_tmp = {
            "vnfdId": vnfInputParameter.get('vnfdid'),
            "vnfdName": ,
            "vnfdVersion": vnfInputParameter.get('vnfdversion'),
            "inputs": ,
            "inputsDesc": ,
            "metadata": ,
            "isShared": ,
            "vnfInstanceId": ,
            "vnfInstanceName":"",
            "vnfNodeName": 
        }





if __name__ == "__main__":
    prepare_date_for_ns_instantiate("http://10.62.100.149:10080/api/v1/ns_o_p", "case2", "case2")
    # delete_ns_package("http://10.62.100.149:10080/api/v1/ns_o_p/nsPackages","case6")
    # ns_package('http://10.62.100.149:10080/api/v1/ns_o_p/nsPackages/create', 'case6', 'case6.csar', 'case6')
    # get_ns_package_by_package_id("http://10.62.100.149:10080/api/v1/ns_o_p/nsPackages", "case1")\
    # get_ns_packages("http://10.62.100.149:10080/api/v1/ns_o_p/nsPackages")
    # data = {
    #     "nsdId": "",
    #     "nsdName": "case6",
    #     "packageId": "case6",
    #     "inputparameters": {
    #         "Latency": "10",
    #         "Mobility_level": "High",
    #         "Subscribers": "1000",
    #         "Scale_in_parameter": "action=scale_in,nf=zte_nf_am,step=1000",
    #         "Scale_out_threshold": "Subscribers>70",
    #         "plan_template_url": "ftp://root:root@10.62.57.171:21/ns-test",
    #         "Priority": "5",
    #         "Scale_out_parameter": "action=scale_out,nf=zte_nf_am,step=1000",
    #         "Scale_in_threshold": "Subscribers<40",
    #         "Granularity": "5",
    #         "Troughthput": "10",
    #         "Type": "eMBB"
    #     },
    #     "vnfinputparameters": [
    #         {
    #             "vnfdId": "zyl3",
    #             "vnfdName": "1",
    #             "vnfdVersion": "1",
    #             "inputs": {
    #                 "ipAddress": "3.3.3.3",
    #                 "dcId": "0",
    #                 "port": "3",
    #                 "resource_template_url": "ccc",
    #                 "nf_id": "3"
    #             },
    #             "inputsDesc": {
    #                 "ipAddress": "",
    #                 "dcId": "",
    #                 "port": "",
    #                 "resource_template_url": "",
    #                 "nf_id": ""
    #             },
    #             "metadata": {
    #                 "vnfInstances": [],
    #                 "vnfdid": "zyl3",
    #                 "vnfdversion": "1",
    #                 "vnfnodename": "VNFDC",
    #                 "vnfdname": "1",
    #                 "isShared": "False"
    #             },
    #             "isShared": "",
    #             "vnfInstanceId": "",
    #             "vnfInstanceName": ""
    #         },
    #         {
    #             "vnfdId": "zyl2",
    #             "vnfdName": "1",
    #             "vnfdVersion": "1",
    #             "inputs": {
    #                 "ipAddress": "2.2.2.2",
    #                 "dcId": "0",
    #                 "port": "2",
    #                 "nf_id": "2"
    #             },
    #             "inputsDesc": {
    #                 "ipAddress": "",
    #                 "dcId": "",
    #                 "port": "",
    #                 "nf_id": ""
    #             },
    #             "metadata": {
    #                 "vnfInstances": [],
    #                 "vnfdid": "zyl2",
    #                 "vnfdversion": "1",
    #                 "vnfnodename": "VNFDB",
    #                 "vnfdname": "1",
    #                 "isShared": "False"
    #             },
    #             "isShared": "",
    #             "vnfInstanceId": "",
    #             "vnfInstanceName": ""
    #         },
    #         {
    #             "vnfdId": "zyl1",
    #             "vnfdName": "1",
    #             "vnfdVersion": "1",
    #             "inputs": {
    #                 "ipAddress": "1.1.1.1",
    #                 "dcId": "0",
    #                 "port": "1",
    #                 "nf_id": "1"
    #             },
    #             "inputsDesc": {
    #                 "ipAddress": "",
    #                 "dcId": "",
    #                 "port": "",
    #                 "nf_id": ""
    #             },
    #             "metadata": {
    #                 "vnfInstances": [],
    #                 "vnfdid": "zyl1",
    #                 "vnfdversion": "1",
    #                 "vnfnodename": "VNFDA",
    #                 "vnfdname": "1",
    #                 "isShared": "False"
    #             },
    #             "isShared": "",
    #             "vnfInstanceId": "",
    #             "vnfInstanceName": ""
    #         },
    #         {
    #             "vnfdId": "zyl4",
    #             "vnfdName": "1",
    #             "vnfdVersion": "1",
    #             "inputs": {
    #                 "ipAddress": "4.4.4.4",
    #                 "dcId": "0",
    #                 "port": "4",
    #                 "resource_template_url": "ddd",
    #                 "nf_id": "4"
    #             },
    #             "inputsDesc": {
    #                 "ipAddress": "",
    #                 "dcId": "",
    #                 "port": "",
    #                 "resource_template_url": "",
    #                 "nf_id": ""
    #             },
    #             "metadata": {
    #                 "vnfInstances": [],
    #                 "vnfdid": "zyl4",
    #                 "vnfdversion": "1",
    #                 "vnfnodename": "VNFDD",
    #                 "vnfdname": "1",
    #                 "isShared": "False"
    #             },
    #             "isShared": "",
    #             "vnfInstanceId": "",
    #             "vnfInstanceName": ""
    #         }
    #     ]
    # }
    # send_create_ns("http://10.62.100.149:10080/api/v1/ns_o_p/nss",data)
    # progress("http://10.62.100.149:10080/api/v1/ns_o_p/jobs","cdb0822c967711e69c460242ac110006")
