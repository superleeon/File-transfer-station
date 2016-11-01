import json

if __name__ == "__main__":
    ns_name = "ns_name"
    ns_package_id = "ns_package_id"
    package = {
    "vendor": "1",
    "description": "case1",
    "vnfInputParameters": [
        {
            "inputs": {
                "displayName": {
                    "default": "itran1",
                    "type": "string",
                    "description": ""
                },
                "description": {
                    "default": "itran1",
                    "type": "string",
                    "description": ""
                },
                "nf_id": {
                    "default": "3",
                    "type": "string",
                    "description": ""
                },
                "dcId": {
                    "default": "0",
                    "type": "string",
                    "description": ""
                },
                "resource_template_url": {
                    "default": "ccc",
                    "type": "string",
                    "description": ""
                },
                "nf_name": {
                    "default": "itran1",
                    "type": "string",
                    "description": ""
                },
                "ipAddress": {
                    "default": "3.3.3.3",
                    "type": "string",
                    "description": ""
                },
                "port": {
                    "default": "3",
                    "type": "string",
                    "description": ""
                }
            },
            "metadata": {
                "vnfInstances": [
                    {
                        "vnfInstanceName": "zyl3",
                        "vnfInstanceId": "2cc551f7-51dc-4300-8548-137ad7b91e26"
                    }
                ],
                "vnfdid": "zyl3",
                "vnfdversion": "1",
                "vnfnodename": "VNFDC",
                "vnfdname": "1",
                "isShared": "False"
            }
        },
        {
            "inputs": {
                "displayName": {
                    "default": "itran2",
                    "type": "string",
                    "description": ""
                },
                "description": {
                    "default": "itran2",
                    "type": "string",
                    "description": ""
                },
                "nf_id": {
                    "default": "4",
                    "type": "string",
                    "description": ""
                },
                "dcId": {
                    "default": "0",
                    "type": "string",
                    "description": ""
                },
                "resource_template_url": {
                    "default": "ddd",
                    "type": "string",
                    "description": ""
                },
                "nf_name": {
                    "default": "itran2",
                    "type": "string",
                    "description": ""
                },
                "ipAddress": {
                    "default": "4.4.4.4",
                    "type": "string",
                    "description": ""
                },
                "port": {
                    "default": "4",
                    "type": "string",
                    "description": ""
                }
            },
            "metadata": {
                "vnfInstances": [
                    {
                        "vnfInstanceName": "zyl4",
                        "vnfInstanceId": "89dcc82b-6451-4eed-a1aa-0e3058b4fc2d"
                    }
                ],
                "vnfdid": "zyl4",
                "vnfdversion": "1",
                "vnfnodename": "VNFDD",
                "vnfdname": "1",
                "isShared": "False"
            }
        }
    ],
    "nsdId": "case2",
    "nsPackageUrl": "/NS/case1/case2.csar",
    "packageId": "case1",
    "registTime": "2016-11-01 09:00:5",
    "useStatus": 1,
    "lastupTime": "",
    "version": "1",
    "inputParameters": {
        "inputs": {
            "subnet_id": {
                "default": "2",
                "type": "string",
                "description": ""
            },
            "subnet_name": {
                "default": "case2",
                "type": "string",
                "description": ""
            },
            "slice_name": {
                "default": "case2",
                "type": "string",
                "description": ""
            },
            "slice_id": {
                "default": "2",
                "type": "string",
                "description": ""
            },
            "plan_template_url": {
                "default": "ftp://root:root@10.62.57.171:21/ns-test",
                "type": "string",
                "description": ""
            }
        }
    },
    "operationalState": 1
    }
    data = {
        "nsdId": package.get('nsdId'),
        "nsdName": str(ns_name),
        "packageId": str(ns_package_id),
        "inputparameters": {},
        "vnfinputparameters": []
    }
    inputparameters = package['inputParameters']['inputs']
    for param in inputparameters:
        value = inputparameters.get(param)
        data['inputparameters'][param] = value.get("default", "1")
    vnfinputparameters = package['vnfInputParameters']
    for vnfInputParameter in vnfinputparameters:
        dict_tmp = {
            "vnfdId": vnfInputParameter['metadata'].get('vnfdid'),
            "vnfdName": vnfInputParameter['metadata'].get('vnfdname'),
            "vnfdVersion": vnfInputParameter['metadata'].get('vnfdversion'),
            "inputs": {},
            "inputsDesc": {},
            "metadata": {},
            "isShared": "",
            "vnfInstanceId": "",
            "vnfInstanceName":"",
            "vnfNodeName": vnfInputParameter['metadata'].get('vnfnodename')
        }
        params = vnfInputParameter['inputs']
        for param in params:
            value = params.get(param)
            dict_tmp['inputs'][param] = value.get("default", "1")
            dict_tmp['inputsDesc'][param] = ""
        metadatas = vnfInputParameter['metadata']
        for meta in metadatas:
            dict_tmp['metadata'][meta] = metadatas.get(meta)
        dict_tmp['metadata']['vnfInstances'] = []
        data['vnfinputparameters'].append(dict_tmp)

    print("^"*100)
    print(data)
    print(type(data))