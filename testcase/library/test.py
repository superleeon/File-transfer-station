def readfile(fileroot):
    fileroot = fileroot.replace("\\", "/")
    filename = fileroot.split("/")[-1]
    filedir = "/".join(fileroot.split("/")[0:-1])
    print(filename)
    print(filedir)
    file = open(fileroot, "r")
    a = file.read()
    file.close()
    print(a)


def areplace(data, **kwargs):
    tmpdict = {}
    for k in kwargs:
        v = kwargs.get(k)
        tmpdict[k] = v
        if k in data:
            data = data.replace(k, v)
    print(tmpdict)
    print(data)


if __name__ == "__main__":
    # readfile("E:\\RF\\testcase\\testcase\\NF.txt")
    # readfile("../testcase/NF.txt")
    data = "1122aabb1c1c2g2g2"
    areplace(data, **{"1122": "****", "c1c2": "||||"})
