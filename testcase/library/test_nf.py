#!/usr/bin/env pytho
# encoding: utf-8

import nf
import json
import traceback
import urllib2
import time


class Test_Nf(object):
    def __init__(self):
        self.nf = nf.Nf()
        pass

    # nf包修改
    def package_change(self, from_package, msb_service_name, to_package):
        try:
            self.nf.change_nf_package(from_package, msb_service_name, to_package)
            return "success"
        except Exception as e:
            print(traceback.format_exc())
            return "fail"

    # nf包删除 √
    def do_package_delete(self, msb_url, package_id):
        try:
            package_url = str(msb_url) + "/api/v1/nf_o_p/package"
            flag = self.nf.nf_package_exist(package_url, package_id)
            if not flag:
                print("nf package [%s] cannot be deleted because it's not exist." % package_id)
                return
            print("delete nf package [%s]." % package_id)
            del_result = self.nf.delete_nf_package(package_url, package_id)
            return del_result
        except urllib2.HTTPError as e:
            print "*" * 50
            print e.code
            print e.read()
            print "*" * 50
        except Exception as e:
            print traceback.format_exc()

    # nf包注册 √
    def do_nf_package_register(self, msb_url, package_id, fileroot, description):
        try:
            package_url = str(msb_url) + "/api/v1/nf_o_p/package"
            flag = self.nf.nf_package_exist(package_url, package_id)
            if flag:
                print("nf package [%s] is already exist,delete first." % package_id)
                del_result = self.nf.delete_nf_package(package_url, package_id)
                del_result = json.loads(del_result)
                if "success" not in del_result.get('error_msg'):
                    print('Delete nf package [%s] fail.' % package_id)
                    return
            create_url = package_url + "/vnf/create"
            register_result = self.nf.nf_package(create_url, package_id, fileroot, description)
            return register_result  # {"error_msg":"success"}
        except urllib2.HTTPError as e:
            print "*" * 50
            print e.code
            print e.read()
            print "*" * 50
        except Exception as e:
            print traceback.format_exc()

    # nf实例化 √
    def do_nf_instantiate(self, msb_url, nf_name, nf_package_id):
        try:
            nfo_url = str(msb_url) + '/api/v1/nf_o_p'
            nso_url = str(msb_url) + '/api/v1/ns_o_p'
            nfs_url = str(nfo_url) + '/nfs'
            # package_url = str(nfo_url) + '/package'
            (flag, nfinstid) = self.nf.nf_exist_return_id(nfs_url, nf_name)
            if flag:
                print("nf [%s] instantiate fail,because it alreay exist." % nf_name)
                print("delete exist nf [%s]." % nf_name)
                # TODO delete nf.
                delete_result = self.do_nf_delete(msb_url, nf_name)
                if delete_result != "success":
                    print("delete fail.")
                    return

            data = self.nf.prepare_date_for_nf_instantiate(nfo_url, nf_name, nf_package_id)
            create_response = self.nf.send_create_nf(nfs_url, data)
            create_resp = json.loads(create_response)
            # vnfid = create_resp.get('vnfdinstanceid')
            jobid = create_resp.get('jobid')
            while True:
                job = self.nf.progress(nso_url, jobid)
                job = json.loads(job)
                status = job.get('status')
                progress = job.get('progress')
                if status == 'error':
                    print('job return error.')
                    return
                if status == 'finished' and progress == 100:
                    print('instantiate job finish.')
                    break
                time.sleep(10)
            print("nf [%s] instantiate success." % nf_name)
            return "success"
        except urllib2.HTTPError as e:
            print "*" * 50
            print e.code
            print e.read()
            print "*" * 50
        except Exception as e:
            print traceback.format_exc()

    # nf实例删除 √
    def do_nf_delete(self, msb_url, nfinstname):
        try:
            nfs_url = str(msb_url) + "/api/v1/nf_o_p/nfs"
            (flag, nfinstid) = self.nf.nf_exist_return_id(nfs_url, nfinstname)
            if not flag:
                print("cannot delete nf inst [%s] because it's not exist." % nfinstname)
                return "success"
            nf_delete_url = str(nfs_url) + "/" + nfinstid + "/delete"
            print("nf delete url = [%s]" % nf_delete_url)
            delete_result = self.nf.send_delete_nf(nf_delete_url)
            jobid = json.loads(delete_result).get('jobid')
            ns_o_url = str(msb_url) + "/api/v1/ns_o_p"
            while True:
                job = self.nf.progress(ns_o_url, jobid)
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
