import zip


def modify_csar(msb_service_name, package_name, package_dest_name):
    zip.unzip(package_name, msb_service_name, "tmp/")
    zip.zip_dir("tmp/", package_dest_name)

if __name__ == "__main__":
    modify_csar("vnfplugin_v1111111", "123.csar", "package.csar")