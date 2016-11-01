#!/usr/bin/env pytho
# encoding: utf-8

import nf
import json
import traceback
import urllib2
import time

# nf包删除 √
def do_package_delete(msb_url, package_id):
    try:
        package_url = str(msb_url) + "/api/v1/nf_o_p/package"
        flag = nf.nf_package_exist(package_url, package_id)
        if not flag:
            print("nf package [%s] cannot be deleted because it's not exist." % package_id)
            return
        print("delete nf package [%s]." % package_id)
        del_result = nf.delete_nf_package(package_url, package_id)
        return del_result
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()

# nf包注册 √
def do_nf_package_register(msb_url, package_id, filename, description):
    try:
        package_url = str(msb_url) + "/api/v1/nf_o_p/package"
        flag = nf.nf_package_exist(package_url, package_id)
        if flag:
            print("nf package [%s] is already exist,delete first." % package_id)
            del_result = nf.delete_nf_package(package_url, package_id)
            del_result = json.loads(del_result)
            if "success" not in del_result.get('error_msg'):
                print('Delete nf package [%s] fail.' % package_id)
                return
        create_url = package_url + "/vnf/create"
        register_result = nf.nf_package(create_url, package_id, filename, description)
        return register_result # {"error_msg":"success"}
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()

# nf实例化 √
def do_nf_instantiate(msb_url, nf_name, nf_package_id):
    try:
        nfo_url = str(msb_url) + '/api/v1/nf_o_p'
        nso_url = str(msb_url) + '/api/v1/ns_o_p'
        nfs_url = str(nfo_url) + '/nfs'
        package_url = str(nfo_url) + '/package'
        (flag, nfinstid) = nf.nf_exist_return_id(nfs_url, nf_name)
        if flag:
            print("nf [%s] instantiate fail,because it alreay exist." % nf_name)
            return
        data = nf.prepare_date_for_nf_instantiate(nfo_url, nf_name, nf_package_id)
        create_response = nf.send_create_nf(nfs_url, data)
        create_resp = json.loads(create_response)
        vnfid = create_resp.get('vnfdinstanceid')
        jobid = create_resp.get('jobid')
        while True:
            job = nf.progress(nso_url, jobid)
            job = json.loads(job)
            status = job.get('status')
            progress = job.get('progress')
            if status == 'error':
                return 
            if status == 'finished' and progress == 100:
                break
            time.sleep(10)
        print("nf instantiate success.")
        return "success"
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()

# nf实例删除 √
def do_nf_delete(msb_url, nfinstname):
    try:
        nfs_url = str(msb_url) + "/api/v1/nf_o_p/nfs"
        (flag, nfinstid) = nf.nf_exist_return_id(nfs_url, nfinstname)
        if not flag:
            print("cannot delete nf inst [%s] because it's not exist." % nfinstname)
            return
        nf_delete_url = str(nfs_url) + "/" + nfinstid + "/delete"
        print("nf delete url = [%s]" % nf_delete_url)
        delete_result = nf.send_delete_nf(nf_delete_url)
        jobid = json.loads(delete_result).get('jobid')
        ns_o_url = str(msb_url) + "/api/v1/ns_o_p"
        while True:
            job = nf.progress(ns_o_url, jobid)
            job = json.loads(job)
            if job.get('status') == 'error':
                print('job return error.')
                return
            if job.get('status') == 'finished' and job.get('progress') == 100:
                print("delete job finished") 
                break
            time.sleep(10)
        print("delete nf [%s] success" % nfinstname)
        return "success"
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()

if __name__ == "__main__":
    do_nf_package_register('http://10.62.100.184:10080', 'VNFDA', 'VNFDA.csar', 'nf package VNFDA')
    do_nf_instantiate('http://10.62.100.184:10080', 'asdasdas', 'VNFDA')
    do_nf_delete('http://10.62.100.184:10080', 'asdasdas')
    do_package_delete('http://10.62.100.184:10080', 'VNFDA')