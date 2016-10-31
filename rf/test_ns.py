#!/usr/bin/env python
# encoding: utf-8


import ns
import json
import traceback
import urllib2

# ns包删除
def do_package_delete(msb_url, package_id):
    try:
        package_url = str(msb_url) + "/api/v1/ns_o_p/nsPackages"
        flag = ns.ns_package_exist(package_url, package_id)
        if not flag:
            print("ns package [%s] cannot be deleted because it's not exist." % package_id)
            return
        print("delete ns package [%s]." % package_id)
        del_result = ns.delete_ns_package(package_url, package_id)
        return del_result
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()
    
# ns包注册
def do_ns_package_register(msb_url, package_id, filename, description):
    try:
        package_url = str(msb_url) + "/api/v1/ns_o_p/nsPackages"
        flag = ns.ns_package_exist(package_url, package_id)
        if flag:
            print("delete ns package [%s]." % package_id)
            del_result = ns.delete_ns_package(package_url, package_id)
            del_result = json.loads(del_result)
            if "delete success" not in del_result.get('msg'):
                print('Delete ns package [%s] fail.' % package_id)
                return
        create_url = package_url + "/create"
        register_result = ns.ns_package(create_url, package_id, filename, description)
        return register_result
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()

# ns删除
def do_ns_delete(msb_url, nsinstname):
    try:
        nss_url = str(msb_url) + "/api/v1/ns_o_p/nss"
        (flag, nsinstid) = ns.ns_exist_return_id(nss_url, nsinstname)
        if not flag:
            print("cannot delete ns inst [%s] because it's not exist." % nsinstname)
            return
        ns_delete_url = str(nss_url) + "/" + nsinstid + "/delete"
        print("ns delete url = [%s]" % ns_delete_url)
        delete_result = ns.send_delete_ns(ns_delete_url)
        jobid = json.loads(delete_result).get('jobid')
        progress_url = str(msb_url) + "/api/v1/ns_o_p/jobs/"
        while True:
            progress = ns.progress(progress_url, jobid)
            progress = json.loads(progress)
            if progress.get('status') == 'finished' and progress.get('progress') == 100:
                # TODO 查询服务是否已经成功创建 
                return progress
    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print traceback.format_exc()

# ns实例化    
def do_ns_instantiate(msb_url, ns_name, ns_package_id):
    try:
        nss_url = str(msb_url) + "/api/v1/ns_o_p/nss"
        (flag, nsinstid) = ns.ns_exist_return_id(nss_url, ns_name)
        if flag:
            print("ns inst [%s] is already exist, do delete.")
            delete_url = nss_url + "/" + str(nsinstid) + "/delete"
            delete_result = ns.send_delete_ns(delete_url)
            # 查询ns删除进度
            jobid = json.loads(delete_result).get('jobid')
            progress_url = str(msb_url) + "/api/v1/ns_o_p/jobs/" + str(jobid) + "/delete"
            while True:
                progress = ns.progress(progress_url, jobid)
                progress = josn.loads(progress)
                if progress.get('status') == 'finished' and progress.get('progress') == 100:
                    print("ns inst [%s] has been deleted successfully. begin to create." % ns_name)
                    break
                if progress.get('status') == 'error':
                    print("cannot create ns inst [%s],the exist inst delete fail.")
                    return
        # todo 创建ns实例


    except urllib2.HTTPError as e:
        print "*" * 50
        print e.code
        print e.read()
        print "*" * 50
    except Exception as e:
        print(traceback.format_exc())





